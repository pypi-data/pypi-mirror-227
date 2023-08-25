from salsa.data.ttecdata import TTECData
from salsa.analyses.ttec_analyses import TTECAnalysis
from typing import Dict
import numpy as np
import pandas as pd
import os
import salsa.plots.new_plots as new_plt
from salsa.data import *
from salsa.analyses.ttec_analyses.calculate_bkg_per_flow import CalculateBkgPerFlow
import plotly.graph_objects as go
import salsa.helper_functions as helper
from salsa.helper_functions import log

class NormedSignal(TTECAnalysis):
    def __init__(self, bkg: CalculateBkgPerFlow = None, data: TTECData = None) -> None:
        super().__init__(data)
        if not bkg.has_all_attributes(self.data.runID):
            calcbkg = CalculateBkgPerFlow(self.data)
            calcbkg.run_without_output()
            self.bkg = calcbkg.get_bkg_ext()
            self.subanalysis_figs.append(calcbkg.fig)
        else:
            self.bkg = bkg.bkg_ext
  
        self.base_list = []
        self.mape_list = []
        self.droop_list = []
        self.base_1mer_list = []
        self.normalized_signal= np.ndarray(0,)
        self.flows = np.ndarray(0,)

    def preprocess_data(self) -> None:
        self.initialize_fig()
        return
    
    def initialize_fig(self):
        self.fig = new_plt.Figure()
        self.fig.set_name(f"TTEC Average Incorporation Signal per Flow - {self.runID}")
        self.fig.update_layout(
            title_text=self.fig.name,
            height=500,
            width=750,
            hovermode="x unified",
        )
        self.fig.update_xaxes(title_text="Flow")
        self.fig.update_yaxes(title_text="Signal")

    def analyze_data(self) -> None:
        for i, base in enumerate(self.params['flow_order']):
            base_keys = self.data.truekey[:, i::4]
            base_signals = self.data.sigmat[:, self.data.preamble_length + i :: 4]

            base_bkg = self.bkg[i::4]
            total_keys = np.sum(base_keys, axis=0)
            total_keys_tiled = np.tile(
                total_keys[:, None], base_signals.shape[0]
            ).transpose()
            base_bkg_tiled = np.tile(
                base_bkg[:, None], base_signals.shape[0]
            ).transpose()

            self.normalized_signal = np.sum(
                (base_signals - base_bkg_tiled) / total_keys_tiled, axis=0
            )

            self.flows = (
                4
                * ((self.data.preamble_length // 4) + np.arange(self.normalized_signal.shape[0]))
                + i
            )

            try:
                self.fit_results = helper.exp_fit(self.flows, self.normalized_signal)
                # print(f"base {base} fit results: {fit_results}")
                self.base_list.append(base)

                mape = helper.MAPE(self.normalized_signal, self.fit_results["predicted"])
                mape_okay = (mape <= 20)
                self.metrics.add(f"ec_instability_{base}", mape)

                self.mape_list.append("%.1f" % mape)

                droop = helper.format_decays(self.fit_results["fit_params"]["b"])
                if not mape_okay:
                    droop = np.nan
                self.metrics.add(f"ec_droop_{base}", droop)
                self.droop_list.append("%.3f" % droop)

                intercept = int(self.fit_results["predicted"][0])
                if not mape_okay:
                    intercept = np.nan
                self.metrics.add(f"ec_1mer_1{base}", intercept)
                self.base_1mer_list.append(intercept)

            except Exception as e:
                log("exception", f"TTEC normalized fit failure: {e}")
                self.fit_results = None
                self.base_list.append(base)
                self.metrics.add(f"ec_instability_{base}", np.nan)
                self.mape_list.append(np.nan)
                self.metrics.add(f"ec_droop_{base}", np.nan)
                self.droop_list.append(np.nan)
                self.metrics.add(f"ec_1mer_1{base}", np.nan)
                self.base_1mer_list.append(np.nan)

            self.plot_data(self.normalized_signal, base)
        return
    
    def report_data(self) -> None:
        self.metrics.add(
            "ec_droop",
            np.nanmean(
                [
                    self.metrics.get(f"ec_droop_{base}", np.nan)
                    for base in ["T", "G", "C", "A"]
                ]
            ),
        )
        if not np.isnan(self.metrics.get("ec_droop", np.nan)):
            self.metrics.update_report("Droop", self.metrics["ec_droop"])
        self.metrics.add(
            "ec_instability",
            np.nanmean(
                [
                    self.metrics.get(f"ec_instability_{base}", np.nan)
                    for base in ["T", "G", "C", "A"]
                ]
            ),
        )
        ec_norm_1mer_int = np.nanmean(
            [
                self.metrics.get(f"ec_1mer_1{base}", np.nan)
                for base in ["T", "G", "C", "A"]
            ]
        )
        if not np.isnan(ec_norm_1mer_int):
            ec_norm_1mer_int = int(ec_norm_1mer_int)
        self.metrics.add(
            "ec_1mer_int",
            ec_norm_1mer_int,
        )
        self.base_list.append("Overall (Averaged)")
        self.mape_list.append("%.1f" % self.metrics.get("ec_instability"))
        self.droop_list.append("%.3f" % self.metrics.get("ec_droop"))
        self.base_1mer_list.append(self.metrics.get("ec_1mer_int"))

        self.metrics.add(
            "ec_droop",
            np.nanmean(
                [
                    self.metrics.get(f"ec_droop_{base}", np.nan)
                    for base in ["T", "G", "C", "A"]
                ]
            ),
        )
        self.metrics.add(
            "ec_instability",
            np.nanmean(
                [
                    self.metrics.get(f"ec_instability_{base}", np.nan)
                    for base in ["T", "G", "C", "A"]
                ]
            ),
        )

        self.table = pd.DataFrame(
            data=np.vstack([self.base_list, self.mape_list, self.droop_list, self.base_1mer_list]).T,
            columns=["Base", "Instability", "Droop", "1mer Fit"],
        )

        self.title = f"TTEC Signal Metrics - {self.runID}"
        return
    
    def plot_data(self, base: str) -> None:
        self.fig.add_trace(
                go.Scatter(
                    x=(self.flows + 1),
                    y=self.normalized_signal,
                    line=dict(color=self.plotly_color[base]),
                    name=f"{base} Signal",
                    hovertemplate="Flow %{x}<br>" + f"{base} Signal: " + "%{y:d}",
                )
            )
        if self.fit_results is not None:
            self.fig.add_trace(
                go.Scatter(
                    x=(self.flows + 1),
                    y=self.fit_results["predicted"],
                    line=dict(color=self.plotly_color[base], dash="dash"),
                    name=f"{base} Fit",
                    showlegend=False,
                    hovertemplate="Flow %{x}<br>" + f"{base} Fit: " + "%{y:d}",
                )
            )
        return

    def run_without_output(self) -> None:
        self.preprocess_data()
        self.analyze_data()
        self.report_data()