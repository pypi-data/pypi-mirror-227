from salsa.analyses.template_analyses import TemplateAnalysis
from typing import Dict
import numpy as np
import pandas as pd
#from plots import WaferPlot
#from salsa.helper_functions import exp_fit, template_exception_safeguard, log, log_runtime_class_decorator, merged_td
# from tool_noise import tool_noise
import salsa.plots.new_plots as new_plt
import numpy as np
import pandas as pd
import os
#from matplotlib.ticker import MultipleLocator
from salsa.data.templatedata import TemplateData


class PreambleBaseCVByTile(TemplateAnalysis):

    def __init__(self, templates: Dict[str, TemplateData]) -> None:
        super().__init__(templates)
        self.plot_list: list[list[new_plt.Figure, bool]] = []
        
    def preprocess_data(self) -> None:
        self.total_sigmat = np.vstack([self.templates[template_name].sigmat[:,:4] for template_name in self.templates.keys()])
        self.total_xyt = np.vstack([self.templates[template_name].XYT for template_name in self.templates.keys()])
        self.data = pd.DataFrame(np.hstack([self.total_sigmat, self.total_xyt[:,2][None,].T]), columns = ["T Signal","G Signal","C Signal","A Signal","Tile"])
        self.mean_signal_per_tile_per_flow = self.data.groupby("Tile").filter(lambda group: group.size >= 10).groupby("Tile").mean()
        self.tiles = self.mean_signal_per_tile_per_flow.index.astype(int).to_numpy()
        self.mean_signal_per_tile_per_flow["radius"] = self.templates['TFSA1'].radii[self.tiles-1]
        self.mean_signal_per_tile_per_flow["theta"] = self.templates['TFSA1'].theta[self.tiles-1]*180/np.pi #ask jerry
        self.base_means = self.mean_signal_per_tile_per_flow.mean()
        self.base_stds = self.mean_signal_per_tile_per_flow.std() 
        return
    
    def plot_data(self) -> None:
        new_plt.PlotHandler.add_title(f"Template Preamble Waferplots - {self.runID}")
        for flow, base in enumerate(['T','G','C','A']):
            fig = new_plt.WaferPlot(self.mean_signal_per_tile_per_flow,
                                    r="radius", theta="theta", color=f"{base} Signal",
                                    hover_name = np.array([f'Tile {int(tile)}' for tile in
                                                           self.mean_signal_per_tile_per_flow.index.to_numpy()]),
                                    hover_data = {f"{base} Signal": True},
                                    range_color=[int(self.mean_signal_per_tile_per_flow[f'{base} Signal'].quantile(0.01)),
                                                 int(self.mean_signal_per_tile_per_flow[f'{base} Signal'].quantile(0.99))],
                                    opacity=0.5)
            fig.set_name(f"Template Preamble {base} Signal - {self.runID}")
            fig.update_layout(title_text=fig.name)
            self.plot_list.append(fig, (base in ["G","A"]))
            
            total_mean = self.base_means[f'{base} Signal']
            total_std = self.base_stds[f'{base} Signal']
            self.metrics.add(f'tf_preamble_tile_cv_{self.params["flow_order"][flow]}', total_std/total_mean)
        pass

    def add_plot_to_html(self):
        for fig, nline in self.plot_list:
            fig.send_json(self.runID)
            fig.append_to_html(size = (270,360), newline = nline) 