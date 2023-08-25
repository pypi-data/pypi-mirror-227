from salsa.data.ttecdata import TTECData
from salsa.analyses.ttec_analyses import TTECAnalysis
from typing import Dict
import numpy as np
import pandas as pd
import os
import salsa.plots.new_plots as new_plt
from salsa.data import *
import plotly.graph_objects as go

class FirstFlowStats(TTECAnalysis):
    def __init__(self, data: TTECData) -> None:
        super().__init__(data)

    def preprocess_data(self) -> None:
        self.flow_1_signals = self.data.sigmat[:, 0][::40]

        self.flow_metrics = dict()
        self.flow_metrics["ec_flow1_min"] = int(np.min(self.flow_1_signals))
        for quantile in [5, 25, 50, 75, 95]:
            self.flow_metrics[f"ec_flow1_quantile_{quantile}"] = int(
                np.quantile(self.flow_1_signals, quantile / 100)
            )
        self.flow_metrics["ec_flow1_max"] = int(np.max(self.flow_1_signals))
        self.flow_metrics["ec_flow1_signal_cv"] = np.std(self.flow_1_signals) / np.mean(
            self.flow_1_signals
        )

        return

    def report_data(self) -> None:
        for key, value in self.flow_metrics.items():
            self.metrics.add(key, value)
            self.flow_metrics["ec_flow1_signal_cv"] = "%.3f" % self.flow_metrics["ec_flow1_signal_cv"]

        self.table = pd.DataFrame(
            data=np.vstack([list(self.flow_metrics.keys()), list(self.flow_metrics.values())]).T,
            columns=["Metric", "Value"],
        )
        self.report_name = f"TTEC Flow 1 Signal Metrics - {self.runID}"
        pass

    def plot_data(self) -> None:
        self.hist = new_plt.Histogram(self.flow_1_signals)
        self.hist.set_name(f"TTEC Flow 1 Signal Histogram - {self.runID}")
        self.hist.update_layout(title_text=self.hist.name, showlegend=False)
        self.hist.update_xaxes(title_text="Signal Strength")
        self.hist.update_yaxes(
            title_text=f"Number of beads (Sample Size {int(self.flow_1_signals.shape[0]/1000)}k)"
        )
        self.hist.update_traces(xbins=dict(size=100))
        self.fig = self.hist
        return