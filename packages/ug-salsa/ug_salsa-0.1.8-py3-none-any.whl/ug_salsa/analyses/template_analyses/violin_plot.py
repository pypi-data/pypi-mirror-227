from salsa.analyses.template_analyses import TemplateAnalysis
from typing import Dict
#from plots import WaferPlot
#from salsa.helper_functions import exp_fit, template_exception_safeguard, log, log_runtime_class_decorator, merged_td
# from tool_noise import tool_noise
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
#from matplotlib.ticker import MultipleLocator
from salsa.data.templatedata import TemplateData
import salsa.plots.new_plots as new_plt
from salsa.analyses.template_analyses.normalize_signals_std_normal import NormalizeSignalsStandardNormal
from salsa.plots.figure import Figure
import plotly.figure_factory as ff

class ViolinPlot(TemplateAnalysis):

    def __init__(self, templates: Dict[str, TemplateData], norm_func: TemplateAnalysis = None, max_cycles = None) -> None:
        super().__init__(templates)
        self.norm_func = norm_func
        self.max_cycles = max_cycles
        self.template = list(templates.values())[0] #consider replacing with next(iter(templates.values()))
        
    def preprocess_data(self) -> None:
        if self.norm_func is None:
            self.norm_func = NormalizeSignalsStandardNormal
        
        self.norm_func({self.template.name: self.template}).run_without_output()
        self.SigMat = self.norm_func.get_sigmat()
        self.keys = self.template.template_tk
        
        self.num_beads, self.num_flows = self.SigMat.shape
        self.sample = np.arange(self.num_beads)[::self.num_beads//50]
    
        self.max_cycles_full = False
        if self.max_cycles is None:
            self.max_cycles_full = True
            self.max_cycles = (self.num_flows // 4)
        self.flows = np.arange(1, 1 + self.num_flows//4)[:self.max_cycles]
        return
    
    def report_data(self) -> None:
        return

    def quantile_range(self, arr, lower = 0.05, upper = 0.95 ):
        ql = np.quantile(arr, lower)
        qu = np.quantile(arr, upper)
        
        above_lower = np.where(arr > ql)[0]
        below_upper = np.where(arr < qu)[0]
        between = np.intersect1d(above_lower, below_upper)
        return arr[between]

    def plot_data(self) -> None:
        fig, axes = plt.subplots(4,1)
        fig.set_figwidth(9)
        fig.set_figheight(11)
        fig.tight_layout(h_pad=2.5)
        fig.subplots_adjust(top=0.9, left = 0.1, bottom = 0.05)

        for i, base in enumerate(["T","G","C","A"]):
            # Subplot settings
            ax = axes[i]
            ax.grid(zorder = 0)
            ax.set_ylabel("Signal Strength")
            ax.set_title(f"{base} Signal")

            # Base data
            target_sample_size = 1000
            sampling_factor = self.SigMat.shape[0]//target_sample_size
            
            base_sig_full = self.SigMat[:,i::4][:,:self.max_cycles]
            base_sig = base_sig_full[self.sample, :]
            base_keys = self.keys[i::4][:self.max_cycles]
            base_key_factor = base_keys + (base_keys == 0)
            
            plot_colors = {'gray': np.where(base_keys == 0)[0],
                           self.base_color[base]: np.where(base_keys == 1)[0],
                           'cyan': np.where(base_keys > 1)[0]}

            # Plot background lines
            for sample_num in range(self.sample.shape[0]):
                ax.plot(self.flows, (base_sig[sample_num,:]/base_key_factor),
                        color = 'gray', linewidth = 1, alpha = 0.2, label = "_no_legend_", zorder = 1)

            # Plot violins
            for color, inds in plot_colors.items():
                if inds.shape[0] < 1:
                    continue
                
                signals = [self.quantile_range(base_sig_full[::sampling_factor,cycle]/base_key_factor[cycle], 0.025, 0.975) for cycle in inds]
                vp = ax.violinplot(signals, inds + 1,
                                   widths = 1, showextrema = False)
                
                for body in vp['bodies']:
                    body.set_alpha(0.9)
                    body.set_facecolor(color)
                    body.set_zorder(2)
            
            #label hmers > 1
            ylim_min = int(ax.get_ylim()[0])
            spacing = 0.7
            for hmer_flow in plot_colors['cyan']:
                hmer = int(base_keys[hmer_flow])
                ax.text(hmer_flow + ((spacing + 0.4) - 0.4*(self.max_cycles/50)), np.max([0, ylim_min]), f"{hmer}", color = 'm')
        
        axes[3].set_xlabel("Cycle")
        if self.template.name == "TFSA2":
            spacing = 0.45
            axes[0].text( 4 - (spacing/2 + spacing/2 * self.max_cycles/50), 0, "M", color = 'r')
            axes[1].text( 8 - (spacing/2 + spacing/2 * self.max_cycles/50), 0, "M", color = 'r')
            axes[2].text(25 - (spacing/2 + spacing/2 * self.max_cycles/50), 0, "M", color = 'r')
            axes[3].text(33 - (spacing/2 + spacing/2 * self.max_cycles/50), 0, "M", color = 'r')
        
        fig.suptitle(f"{self.template.name} Violin Plots ({self.max_cycles} cycles) - {self.runID}")
        self.fig = fig
        plt.close(fig)

        # os.makedirs(f"{self.params['save_loc']}/json", exist_ok=True)
        # num_cycles = self.max_cycles_full*'full' + (not self.max_cycles_full)*str(self.max_cycles)
        # filename_base = f"{self.params['save_loc']}json/RunID{self.runID}_{self.template}_violin_{num_cycles}_cycles"
        # fig.savefig(f"{filename_base}.png")
        # fig.savefig(f"{filename_base}.jpeg")
        # new_plt.PlotHandler.add_png(f"{filename_base}.png")
        # with open(f"{self.params['save_loc']}json/figure_list.txt", 'a+') as json_log:
        #     json_log.write(f"RunID{self.runID}_{self.template}_violin_{num_cycles}_cycles.png\n")
        #     json_log.write(f"RunID{self.runID}_{self.template}_violin_{num_cycles}_cycles.jpeg\n")
        # with open(f"{self.params['save_loc']}RunID{self.params['runid']}_uploads_list.txt", 'a+') as file:
        #     file.write(f"json/RunID{self.runID}_{self.template}_violin_{num_cycles}_cycles.png\n")
        #     file.write(f"json/RunID{self.runID}_{self.template}_violin_{num_cycles}_cycles.jpeg\n")
        return
    
    def add_plot_to_html(self):
        #self.fig.send_json(self.runID)
        self.parent_routine.add_noninteractive_plot(self.fig, size=(1100, 900))