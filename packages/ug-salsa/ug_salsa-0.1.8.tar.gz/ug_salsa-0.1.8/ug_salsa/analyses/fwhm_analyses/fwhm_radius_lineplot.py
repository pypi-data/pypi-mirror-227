from salsa.analyses.analysis import Analysis
from salsa.data.fwhmdata import FWHMData
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from salsa.plots.figure import Figure

from typing import List

class FWHMRadiusLinePlot(Analysis):
    def __init__(self, data: FWHMData) -> None:
        super().__init__(data)
        self.plots: List[Figure] = []

    def plot_data(self) -> None:
        data = np.nanmean(self.data.fwhmMap, axis = 0)
        data_df = pd.DataFrame(data, columns = [f"FOV_{i+1}" for i in range(16)])
        data_df.insert(0, "Radius", self.data.radii.astype(int))
        fov_mean_by_radius = data_df.groupby("Radius").mean()
        
        line_plot =  Figure()
        norm_plot = Figure()
        base_edges = np.arange(17)*(self.data.tile_width/16)
        fwhm_bins = (base_edges[1:] + base_edges[:-1])/2
        
        for radius, row in fov_mean_by_radius.iterrows():
            line_plot.add_trace(go.Scatter(
                x = fwhm_bins,
                y = row.to_numpy(),
                name = f"{radius} mm",
            ))
            
            norm_plot.add_trace(go.Scatter(
                x = fwhm_bins,
                y = row.to_numpy()/np.min(row.to_numpy()),
                name = f"{radius} mm",
            ))
            
        line_plot.set_name(f"Flow-averaged FWHM by FOV position - {self.runID}")
        line_plot.update_layout(title_text = line_plot.name,
                          hovermode = 'x unified')
        line_plot.update_xaxes(title_text = "FOV X-position (Pixels)")
        line_plot.update_yaxes(title_text = "Avg FWHM (um)")
        self.plots.append(line_plot)
        
        norm_plot.set_name(f"Min-normalized Flow-averaged FWHM by FOV position - {self.runID}")
        norm_plot.update_layout(title_text = norm_plot.name,
                          hovermode = 'x unified')
        norm_plot.update_xaxes(title_text = "FOV X-position (Pixels)")
        norm_plot.update_yaxes(title_text = "Normalized Avg FWHM (um)")
        self.plots.append(norm_plot)

    def add_plot_to_html(self):
        for plot in self.plots:
            #plot.send_json(self.runID)
            self.parent_routine.add_interactive_plot(plot)



