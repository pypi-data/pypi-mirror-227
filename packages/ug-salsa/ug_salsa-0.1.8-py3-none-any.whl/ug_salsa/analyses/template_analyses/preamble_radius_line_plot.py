from salsa.analyses.template_analyses import TemplateAnalysis
from typing import Dict
import numpy as np
#from plots import WaferPlot
#from salsa.helper_functions import exp_fit, template_exception_safeguard, log, log_runtime_class_decorator, merged_td
# from tool_noise import tool_noise
import salsa.plots.new_plots as new_plt
import numpy as np
import pandas as pd
import os
from tqdm import tqdm
#from matplotlib.ticker import MultipleLocator
import plotly.graph_objects as go
from salsa.data.templatedata import TemplateData


class PreambleRadiusLinePlot(TemplateAnalysis):

    def __init__(self, templates: Dict[str, TemplateData]) -> None:
        super().__init__(templates)
        
    def preprocess_data(self) -> None:
        self.radii = np.sort(np.unique(self.templates['TFSA1'].radii))
        self.flow_order = self.params['flow_order']
        
        
        
        self.sigmat = np.vstack([self.templates[template_name].sigmat[:,:4] for template_name in self.templates.keys()])
        self.tile = np.hstack([self.templates[template_name].XYT[:,2] for template_name in self.templates.keys()]).astype(int)
        self.tiles = self.templates['TFSA1  '].tiles

        self.signal_by_tile = np.zeros((self.tiles.shape[0],4))
        
        with tqdm(position = 0, total = self.tiles.shape[0], leave = True) as pbar:
            for i, tile_num in enumerate(self.tiles):
                tile_indices = np.where(self.tile == tile_num)[0]
                self.signal_by_tile[i,:] = np.mean(self.sigmat[tile_indices,:], axis = 0)
                pbar.update()
        return
    
    def report_data(self) -> None:
        return
    
    def plot_data(self) -> None:
        self.line_plot = new_plt.Figure()
        self.wafer_subplots = new_plt.SubPlot(rows = 2, cols = 2, vertical_spacing = 0.02)
        self.wafer_subplots.set_name(f"Template Preamble Mean Tile Signal - {self.runID}")
        self.wafer_subplots.update_layout(title_text=self.wafer_subplots.name,
                          coloraxis_colorbar=dict(title="Mean Signal per Tile"))
        self.positions = {'T': (1, 1),
                     'G': (1, 2),
                     'C': (2, 1),
                     'A': (2, 2),}
        
        for base_ind, base in enumerate(['T','G','C','A']):
            # TODO: update documentation
            # handle line plot
            signal = self.sigmat[:,base_ind]
            radius = self.radii[self.tile - 1]
            y = np.array([np.nanmean(signal[np.where(radius == r)[0]]) for r in self.radii])
            self.line_plot.add_trace(go.Scatter(
                x = self.radii.astype(int).astype(str),
                y = y,
                line = dict(color = self.base_color[self.flow_order[base_ind]]),
                name = base,
            ))
            
        self.line_plot.set_name(f"Template Preamble Signal by Radius - {self.runID}")
        self.line_plot.update_layout(title_text = self.line_plot.name,
                          hovermode = 'x unified')
        self.line_plot.update_xaxes(title_text = "Radius")
        self.line_plot.update_yaxes(title_text = "Signal")
        self.fig = self.line_plot
        return
