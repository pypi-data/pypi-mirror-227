from salsa.analyses.analysis import Analysis
from salsa.data.fwhmdata import FWHMData
import numpy as np
import plotly.graph_objects as go
from salsa.plots.figure import Figure

class MeanFWHMPerFlowByBase(Analysis):
    def __init__(self, data: FWHMData) -> None:
        super().__init__(data)

    def preprocess_data(self) -> None:
        self.mean_fwhm_per_flow: np.ndarray = np.nanmean(self.data.fwhmMap, axis = (1,2))
        self.flows = np.arange(1, self.mean_fwhm_per_flow.shape[0] + 1)

    def plot_data(self) -> None:
        line_plot = Figure()
        
        for base_ind, base in enumerate(['T','G','C','A']):
            base_fwhm = self.mean_fwhm_per_flow[base_ind::4]
            base_flows = self.flows[base_ind::4]
            line_plot.add_trace(go.Scatter(
                x = base_flows,
                y = base_fwhm,
                line = dict(color = self.base_color[base_ind]),
                name = base,
            ))
            
        line_plot.set_name(f"Mean FWHM per flow by Base - {self.runID}")
        line_plot.update_layout(title_text = line_plot.name,
                          hovermode = 'x unified')
        line_plot.update_xaxes(title_text = "Flow Num")
        line_plot.update_yaxes(title_text = "FWHM (um)")
        self.fig = line_plot

    def add_plot_to_html(self):
        self.fig.send_json(self.runID)
        self.parent_routine.add_noninteractive_plot(self.fig)


        

                
        
