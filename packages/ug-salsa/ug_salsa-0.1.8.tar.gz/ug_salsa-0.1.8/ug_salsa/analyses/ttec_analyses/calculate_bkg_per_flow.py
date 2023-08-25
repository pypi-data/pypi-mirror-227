from salsa.data.ttecdata import TTECData
from salsa.analyses.ttec_analyses import TTECAnalysis
from typing import Dict
import numpy as np
import pandas as pd
import os
import salsa.plots.new_plots as new_plt
from salsa.data import *
import plotly.graph_objects as go

data: TTECData

class CalculateBkgPerFlow(TTECAnalysis):
    def __init__(self, data: TTECData) -> None:
        super().__init__(data)
        self.sm: np.ndarray = np.ndarray(0,)

    def preprocess_data(self) -> None:
        self.sm = self.data.sigmat[:, self.data.preamble_length :].astype("float32")
        self.bkg = np.nan * np.zeros((np.shape(self.data.truekey)[1],))
        
    
    def analyze_data(self) -> None:
        for flow in range(8, np.shape(self.data.truekey)[1] - 8):
            tmp = np.array(
                [
                    self.data.truekey[:, flow - 8],
                    self.data.truekey[:, flow - 4],
                    self.data.truekey[:, flow],
                    self.data.truekey[:, flow + 4],
                    self.data.truekey[:, flow + 8],
                ]
            )
            desert_inds = np.where(np.sum(tmp, 0) == 0)[0]
            if len(desert_inds) > 10:
                self.bkg[flow] = np.median(self.sm[desert_inds, flow + self.data.preamble_length])

        self.bkg_ext = np.nan * np.zeros_like(self.bkg)
        for b in range(4):
            x = np.arange(b, np.shape(self.data.truekey)[1] - 8, 4)
            x1 = x[np.where(x >= self.data.preamble_length + 7 + b - 1)]
            p = np.polyfit(x1, self.bkg[x1], 1)
            self.bkg_ext[b : np.shape(self.data.truekey)[1] : 4] = np.polyval(
                p, np.arange(b, np.shape(self.data.truekey)[1], 4)
            )
    
    def plot_data(self) -> None:
        fig = new_plt.Figure()
        colors = ["red", "black", "blue", "lime"]
        flows = np.arange(self.data.preamble_length, self.data.preamble_length + self.bkg_ext.shape[0])
        for i, base in enumerate(self.params['flow_order']):
            fig.add_trace(
                go.Scatter(
                    x=flows[i::4],
                    y=self.bkg[i::4],
                    name=f"{base} floor",
                    mode="lines",
                    line=dict(color=colors[i]),
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=flows[i::4],
                    y=self.bkg_ext[i::4],
                    name=f"{base} floor ext",
                    mode="lines",
                    line=dict(color=colors[i], dash="dash"),
                )
            )
        fig.set_name(f"TTEC Floor Signals - {self.runID}")
        fig.update_layout(title_text=fig.name)
        fig.update_xaxes(title_text="Flow #")
        fig.update_yaxes(title_text="Floor signals")
        self.fig = fig
        return
    
    def get_bkg_ext(self):
        return self.bkg_ext
        
    def has_all_attributes(runid: str, self):
        attrs = vars(self).keys()
        for attr in attrs:
            if attr[attr] is None or (type(attrs[attr]) == np.ndarray and attrs[attr].shape[0] == 0) or runid != self.data.runID:
                return False
        return True