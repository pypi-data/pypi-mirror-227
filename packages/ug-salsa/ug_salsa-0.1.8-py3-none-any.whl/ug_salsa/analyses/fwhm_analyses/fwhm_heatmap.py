
from salsa.analyses.analysis import Analysis
from salsa.data.fwhmdata import FWHMData
import numpy as np
from typing import Tuple
import pandas as pd
import salsa.plots.new_plots as new_plt

class FWHMHeatMap(Analysis):

    def __init__(self, data: FWHMData) -> None:
        super().__init__(data)

    def plot_data(self) -> None:
        fwhm_map_data: np.ndarray = np.nanmean(self.data.fwhmMap, axis = 1)
        
        xedges = np.arange(1,fwhm_map_data.shape[0]+1)
        yedges = np.arange(1,fwhm_map_data.shape[1]+1)
        
        fig = new_plt.HeatMap(z = fwhm_map_data.transpose(), x = xedges, y = yedges,
                              colorbar=dict(title='FWHM (um)'))
        fig.set_name(f"FWHM by FOV HeatMap - {self.runID}")
        fig.update_layout(title_text = fig.name, height = 600)
        fig.update_xaxes(title_text = "Flow Num")
        fig.update_yaxes(title_text = "X Bin")
        self.fig = fig
        return 
    
    def add_plot_to_html(self):
        self.fig.send_json(self.runID)
        self.parent_routine.add_noninteractive_plot(self.fig)