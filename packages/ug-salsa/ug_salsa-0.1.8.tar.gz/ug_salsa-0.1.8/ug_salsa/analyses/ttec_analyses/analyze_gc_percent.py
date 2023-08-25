from salsa.data.ttecdata import TTECData
from salsa.analyses.ttec_analyses import TTECAnalysis
from typing import Dict
import numpy as np
import pandas as pd
import os
import salsa.plots.new_plots as new_plt
from salsa.data import *
import plotly.graph_objects as go

class AnalyzeGCContent(TTECAnalysis):
    def __init__(self, data: TTECData) -> None:
        super().__init__(data)
        self.plot_list: list[new_plt.Figure] = []

    def preprocess_data(self) -> None:
        num_flows = self.data.truekey.shape[1]

        ref_gc_percent = []
        ref_windows = range(0, len(self.data.seq_key_front) - num_flows, 4)
        for x in ref_windows:
            window = self.data.seq_key_front[x : x + num_flows]
            ref_gc_percent.append(
                (np.sum(window[1::4]) + np.sum(window[2::4])) / np.sum(window)
            )

        nwindows = len(ref_windows)
        bins = np.linspace(0, 1, 101)
        ref_bin_nums = np.digitize(ref_gc_percent, bins)
        ref_unique_bins = np.unique(ref_bin_nums)

        G_keys = self.data.truekey[:, 1::4]
        C_keys = self.data.truekey[:, 2::4]

        gc_incorps = np.sum(G_keys, axis=1) + np.sum(C_keys, axis=1)
        all_incorps = np.sum(self.data.truekey, axis=1)
        gc_percent = gc_incorps / all_incorps
        nbeads = gc_percent.shape[0]
        bins = np.linspace(0, 1, 101)
        bin_nums = np.digitize(gc_percent, bins)
        unique_bins = np.unique(bin_nums)
        self.ind_dict = {
            b: np.where(bin_nums == b)[0]
            for b in np.intersect1d(ref_unique_bins, unique_bins)
        }
        ref_ind_dict = {
            b: np.where(ref_bin_nums == b)[0]
            for b in np.intersect1d(ref_unique_bins, unique_bins)
        }

        self.x_ref = np.array(list(ref_ind_dict.keys()))
        self.y_ref = np.array([ref_ind_dict[k].shape[0] for k in self.x_ref]) / nwindows * 100
        self.x = np.array(list(self.ind_dict.keys()), dtype=np.int64)
        self.y = np.array([self.ind_dict[k].shape[0] for k in x]) / nbeads * 100
        self.gc_bias = self.y / self.y_ref

        lgc = 0.3
        l_ind = [i for i, elem in enumerate(x) if bins[elem] <= lgc]
        l_y = np.array([self.y[i] for i in l_ind])
        l_gc_bias = np.array([self.gc_bias[i] for i in l_ind])
        self.low_gc = np.sum(l_gc_bias * (l_y / np.sum(l_y)))

        hgc = 0.6
        h_ind = [i for i, elem in enumerate(x) if bins[elem] > hgc]
        h_y = np.array([self.y[i] for i in h_ind])
        h_gc_bias = np.array([self.gc_bias[i] for i in h_ind])
        self.high_gc = np.sum(h_gc_bias * (h_y / np.sum(h_y)))

        self.first_T_signal = self.data.sigmat[:, 0]
        return

    def report_data(self) -> None:
        # metric table
        self.metrics.add("ec_low_GC_bias", self.low_gc)
        self.metrics.add("ec_high_GC_bias", self.high_gc)

        self.table = pd.DataFrame(
            data=np.vstack(
                [
                    ["EC Low GC Bias", "EC High GC Bias"],
                    ["%.3f" % self.low_gc, "%.3f" % self.high_gc],
                ]
            ).T,
            columns=["Metric", "Value"],
        )
        self.report_title = f"TTEC GC Bias Metrics - {self.runID}"
        return

    def plot_data(self) -> None:
         # GC Bias Plot
        gc_bias_fig = new_plt.SubPlot(specs=[[{"secondary_y": True}]])
        gc_bias_fig.set_name(f"GC Bias Plot - {self.runID}")
        gc_bias_fig.update_layout(
            title_text=gc_bias_fig.name,
            height=500,
            width=900,
        )
        gc_bias_fig.update_xaxes(title_text="GC %", range=[0, 100])
        gc_bias_fig.update_yaxes(title_text="% of all Reads", secondary_y=False)
        gc_bias_fig.update_yaxes(title_text="log<sub>2</sub> Bias", secondary_y=True)

        gc_bias_fig.add_trace(
            go.Scatter(
                x=self.x, y=self.y, name="Sample of aligned reads", line=dict(color="#1f77b4")
            ),
            secondary_y=False,
        )
        gc_bias_fig.add_trace(
            go.Scatter(
                x=self.x_ref,
                y=self.y_ref,
                name="Unbiased reference genome",
                line=dict(color="#ff7f0e"),
            ),
            secondary_y=False,
        )

        gc_bias_fig.add_trace(
            go.Scatter(
                x=self.x_ref,
                y=np.log2(self.gc_bias, where=(self.gc_bias != 0)),
                name="GC Ratio",
                line=dict(color="#1f77b4", dash="dash"),
            ),
            secondary_y=True,
        )
        gc_bias_fig.add_trace(
            go.Scatter(
                x=self.x_ref,
                y=np.log2(np.ones(len(self.gc_bias))),
                name="Unbiased GC Ratio",
                line=dict(color="#ff7f0e", dash="dash"),
            ),
            secondary_y=True,
        )
        self.plot_list.append(gc_bias_fig)

        # GC First T Plot
        self.y = np.array([np.mean(self.first_T_signal[self.ind_dict[k]]) for k in self.x], dtype=np.int64)
        df_gc_pct = pd.DataFrame(
            data=np.vstack([self.x, self.y]).transpose(), columns=["GC %", "First T Signal"]
        )

        gc_first_T_fig = new_plt.LinePlot(df_gc_pct, x="GC %", y="First T Signal")
        gc_first_T_fig.set_name(f"TTEC First T Signal binned by GC % - {self.runID}")
        gc_first_T_fig.update_layout(
            title_text=gc_first_T_fig.name,
            height=500,
            width=725,
            hovermode="x",
        )
        gc_first_T_fig.update_xaxes(range=[0, 100])
        self.plot_list.append(gc_first_T_fig)
        return

    def add_plot_to_html(self):
        for fig in self.plot_list:
            fig.send_json(self.runID)
            fig.append_to_html()