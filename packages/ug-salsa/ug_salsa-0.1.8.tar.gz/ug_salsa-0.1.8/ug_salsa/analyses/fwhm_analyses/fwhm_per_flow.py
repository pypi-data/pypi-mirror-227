from salsa.analyses.analysis import Analysis
from salsa.data.fwhmdata import FWHMData
import numpy as np
import plotly.graph_objects as go
from salsa.plots.figure import Figure

class FWHMPerFlow(Analysis):
    def __init__(self, data: FWHMData) -> None:
        super().__init__(data)

    def preprocess_data(self) -> None:
        self.mean_tile_fwhm_per_flow: np.ndarray = np.nanmean(self.data.fwhmMap, axis = 2)
        self.flows = np.arange(1, self.mean_tile_fwhm_per_flow.shape[0] + 1)

    def plot_data(self) -> None:
        line_plot = Figure()
        
        for q, q_name in zip([0.01, 0.5, 0.99], ["1st","50th","99th"]):
            quantile_fwhm = np.nanquantile(self.mean_tile_fwhm_per_flow, q, axis = 1)
            line_plot.add_trace(go.Scatter(
                x = self.flows,
                y = quantile_fwhm,
                name = f"{q_name} quantile",
            ))
            
        line_plot.set_name(f"FWHM Range per Flow - {self.runID}")
        line_plot.update_layout(title_text = line_plot.name,
                          hovermode = 'x unified')
        line_plot.update_xaxes(title_text = "Flow Num")
        line_plot.update_yaxes(title_text = "FWHM (um)")
        self.fig = line_plot

    def add_plot_to_html(self):
        self.fig.send_json(self.runID)
        self.parent_routine.add_noninteractive_plot(self.fig)
