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


class PassFilterCV(TemplateAnalysis):

    def __init__(self, templates: Dict[str, TemplateData]) -> None:
        super().__init__(templates)
        
    def preprocess_data(self) -> None:
        self.xyt_aggregated = np.hstack([self.templates[temp].XYT[:,2] for temp in self.templates.keys()])
        self.tiles = np.unique(self.xyt_aggregated).astype(int)
        self.num_template_beads_per_tile = np.array([len(np.where(self.xyt_aggregated == tile_num)[0]) for tile_num in self.tiles])
        self.total_beads_per_tile = self.templates['TFSA1'].FullBeadsPerTile[self.tiles - 1]
        self.keep_inds = np.where(self.total_beads_per_tile/self.templates['TFSA1'].tile_size > self.params['min_bead_density'])[0]
        
        total_found = np.sum([self.templates[temp].total_found for temp in self.templates.keys()])
        total_sampled = np.sum(self.num_template_beads_per_tile[self.keep_inds])
        scaling_factor = total_found/total_sampled
        
        self.pass_filter = scaling_factor*self.num_template_beads_per_tile/self.total_beads_per_tile
        self.pass_filter = self.pass_filter[self.keep_inds]
        self.cv = np.std(self.pass_filter)/np.mean(self.pass_filter)
        
        self.metrics.add("tf_pass_filter_average_pct", 100*np.mean(self.pass_filter))
        self.metrics.add("tf_pass_filter_cv", self.cv)
        
        self.radii = self.radii[self.tiles - 1]
        self.theta = self.theta[self.tiles - 1]*180/np.pi
        self.data = np.vstack([self.radii[self.keep_inds],
                          self.theta[self.keep_inds],
                          self.tiles[self.keep_inds],
                          100*self.pass_filter]).transpose()
        return

    def report_data(self) -> None:
        self.df = pd.DataFrame(self.data, columns = ['radius', 'theta', 'tileID', 'Pass Filter'])
        self.table = pd.DataFrame(data=np.vstack([['Pass Filter Average (%)','Pass Filter CV'],
                                 ['%.3f' % (100*np.mean(self.pass_filter)), '%.3f' % self.cv]]).T,
                             columns=["Metric", "Value"])
        self.report_title = f"Template Pass Filter Metrics - {self.runID}"
        return
    
    def plot_data(self) -> None:
        fig = new_plt.WaferPlot(self.df, r='radius', theta='theta', color='Pass Filter',
                                hover_name = np.array([f'Tile {int(tile)}' for tile in self.df['tileID'].to_numpy()]),
                                hover_data = {"Pass Filter": True},
                                color_continuous_scale = ['red','yellow','green'],
                                opacity=0.5)
        fig.set_name(f'Template Pass Filter Values - {self.runID}')
        fig.update_layout(title_text = fig.name,
                          coloraxis_colorbar=dict(title = "% template beads"))
        self.fig = fig

        pass