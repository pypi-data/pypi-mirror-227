from salsa.data.ttecdata import TTECData
from salsa.analyses.ttec_analyses import TTECAnalysis
from typing import Dict
import numpy as np
import pandas as pd
import os
import salsa.plots.new_plots as new_plt
from salsa.data import *
import plotly.graph_objects as go
from scipy.stats import linregress
from salsa.helper_functions import log, MAPE


class HmerLinearity(TTECAnalysis):
    def __init__(self, data: TTECData) -> None:
        super().__init__(data)
        self.base_list = []
        self.slope_list = []
        self.norm_slope_list = []
        self.mape_list = []


    def preprocess_data(self) -> None:
        # TO DO: generate plot of hmer median signals
        # TO DO: filter by count per hmer

        self.hmer_flows = {"C": 51, "A": 52, "T": 53, "G": 54}

        self.fig = new_plt.LinePlot()
        self.fig.update_layout(height=500, width=725)
        return

    def analyze_data(self) -> None:
        for base in self.hmer_flows.keys():

            self.flow_num = self.hmer_flows[base]
            self.base_signal = self.data.sigmat[:, self.flow_num - 1]
            self.base_keys = self.data.truekey[:, self.flow_num - self.data.preamble_length - 1]
            self.base_1mer_mean = np.mean(self.base_signal[np.where(self.base_keys == 1)[0]])
            self.base_0mer_mean = np.mean(self.base_signal[np.where(self.base_keys == 0)[0]])
            #%% calculate 1mer signal and scale slope, save both signal unit and ratio unit slope

            self.hmers = np.array(range(self.params["linearity_max_hmer"] + 1))
            self.median_signal_per_hmer = np.array(
                [
                    np.median(self.base_signal[np.where(self.base_keys == hmer)[0]])
                    for hmer in self.hmers
                ]
            )
            self.count = np.array(
                [np.where(self.base_keys == hmer)[0].shape[0] for hmer in self.hmers]
            )
            
            self.fit_hmers = self.hmers[np.where(self.count > 0)[0]]
            self.fit_medians = self.median_signal_per_hmer[np.where(self.count > 0)[0]]

            if not np.all(self.count[0:3] > 200):
                log("info", "Not enough records to proceed. Skipping.")
                self.metrics.add(f"ec_lin_{base}_slope", np.nan)
                self.metrics.add(f"ec_lin_{base}_norm_slope", np.nan)
                self.metrics.add(f"ec_lin_{base}_mape", np.nan)
                continue

            self.slope, self.intercept, self.corr, _, _ = linregress(self.fit_hmers, self.fit_medians)
            self.over200_inds = np.where(self.count[self.count > 0] > 200)[0]
            predicted = np.array([self.intercept + self.slope * hmer for hmer in self.hmers])
            
            self.plot_data(base)

            mape = MAPE(self.median_signal_per_hmer, predicted)

            self.base_list.append(base)
            self.metrics.add(f"ec_lin_slope_{base}", int(self.slope))
            self.slope_list.append(int(self.slope))
            self.metrics.add(
                f"ec_linearity_{base}", self.slope / (self.base_1mer_mean - self.base_0mer_mean)
            )
            self.norm_slope_list.append("%.3f" % (self.slope / (self.base_1mer_mean - self.base_0mer_mean)))
            self.metrics.add(f"ec_lin_fit_error_{base}", mape)
            self.mape_list.append("%.1f" % mape)
        self.close_plot()
        return

    def report_data(self) -> None:
        self.table = pd.DataFrame(
            data=np.vstack([self.base_list, self.slope_list, self.norm_slope_list, self.mape_list]).T,
            columns=["Base", "Slope", "Slope/1mer", "Fit Error"],
        )
        self.report_title = f"TTEC Hmer Linearity Metrics - {self.runID}"
        pass

    def plot_data(base: str, self) -> None:
        self.fig.add_trace(
            go.Scatter(
                x=self.fit_hmers,
                y=self.fit_medians,
                customdata=np.array(self.count),
                line=dict(color=self.plotly_color[base]),
                name=f"Flow {self.hmer_flows[base]}, Base {base}",
                hovertemplate="%{x}mer signal: %{y:d} su<br>%{customdata} samples",
                showlegend=False,
            )
        )

        self.fig.add_trace(
            go.Scatter(
                x=self.fit_hmers[self.over200_inds],
                y=self.fit_medians[self.over200_inds],
                customdata=np.array(self.count[self.over200_inds]),
                line=dict(color=self.plotly_color[base], width=4),
                name=f"Flow {self.hmer_flows[base]}, Base {base}",
                hovertemplate="%{x}mer signal: %{y:d} su<br>%{customdata} samples",
            )
        )

        self.fig.add_trace(
            go.Scatter(
                x=self.hmers,
                y=self.predicted,
                marker=dict(opacity=0),
                line=dict(color=self.plotly_color[base], dash="dash"),
                name=f"Flow {self.hmer_flows[base]}, Base {base} Fit",
                hovertemplate="%{x}mer fit: %{y:d} su",
                showlegend=False,
            )
        )
        return
    
    def close_plot(self):
        self.fig.set_name(f"TTEC Hmer linearity - {self.runID}")
        self.fig.update_xaxes(title_text="hmer length (> 200 samples)")
        self.fig.update_yaxes(title_text="Median Signal")
        self.fig.update_layout(title_text=self.fig.name)

    def run_without_output(self) -> None:
        self.preprocess_data()
        self.analyze_data()
        self.report_data()