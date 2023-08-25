from salsa.analyses.template_analyses import TemplateAnalysis
from typing import Dict
import numpy as np
#from plots import WaferPlot
#from salsa.helper_functions import exp_fit, template_exception_safeguard, log, log_runtime_class_decorator, merged_td
from salsa.helper_functions import log
# from tool_noise import tool_noise
import salsa.plots.new_plots as new_plt
import numpy as np
import pandas as pd
import os
#from matplotlib.ticker import MultipleLocator
import plotly.graph_objects as go
import salsa.helper_functions as helper
from salsa.data import TemplateData

class Base1MerSignalFit(TemplateAnalysis):
    def __init__(self, templates: Dict[str, TemplateData], inds = None) -> None:
        super().__init__(templates)    
        self.inds = inds
        self.intercepts = []
        self.decay_rates = []
        self.early_fit_intercepts = []
        self.early_fit_decay_rates = []
        self.fit: Dict[str, np.ndarray] = {}
        self.early_fit = {}
        self.template:TemplateData = list(templates.values())[0]

        
    def preprocess_data(self) -> None:
        self.keys = self.template.template_tk.flatten()
        if self.inds is None or not self.inds.any():
            self.median_signal = np.nanmedian(self.template.sigmat, axis = 0)
        else:
            self.median_signal = np.nanmedian(self.template.sigmat[self.inds,:], axis = 0)
        
        self.fig = new_plt.SubPlot(rows = 2, cols = 2, horizontal_spacing=0.15)
        self.plot_loc = {
            'T': {"row": 1, "col":1},
            'G': {"row": 1, "col":2},
            'C': {"row": 2, "col":1},
            'A': {"row": 2, "col":2},
        }
        return
    def analyze_data(self) -> None:
        for base_num, base in enumerate(['T','G','C','A']):
            relevant_inds = np.array([ind for (ind, key_val) in list(enumerate(self.keys))[base_num::4] if key_val == 1], dtype = int)
            #if len(relevant_inds) < 2: # HOW SHOULD THIS BE HANDLED?
                #intercepts.append(np.nan)
                #decay_rates.append(np.nan)
                #continue
            flows = relevant_inds + 1
            signal = self.median_signal[relevant_inds] # subtract floor values
            self.generate_fits(flows, signal)
            self.generate_early_fits(flows, signal)
            self.plot_fits(flows, signal, base_num, base)
        return

    def generate_fits(self, flows, signal):
        try:
                self.fit = helper.exp_fit(flows, signal)
                self.intercepts.append(self.fit['fit_params']['A'])
                self.decay_rates.append(self.fit['fit_params']['b'])
        except Exception as e:
            log('exception', f"1mer fit failure: {e}")
            self.fit = {}
        return
    
    def generate_early_fits(self, flows, signal):
        try:
                self.inds = np.intersect1d(np.where(flows >= 9)[0], np.where(flows <= 200)[0])
                self.early_fit = helper.exp_fit(flows[self.inds], signal[self.inds])
                self.early_fit_intercepts.append(self.early_fit['fit_params']['A'])
                self.early_fit_decay_rates.append(self.early_fit['fit_params']['b'])
        except Exception as e:
            log('exception', f"1mer fit failure: {e}")
            self.early_fit = {}
        return

    def plot_fits(self, flows, signal, base_num: int, base: str) -> None: 
        self.fig.add_trace(go.Scatter(
                x = flows,
                y = signal,
                mode = 'markers',
                marker = dict(color = self.base_color[base_num]),
                name = f"{base} 1mers"
            ), **self.plot_loc[base])
        
        # plot full run fit
        try:
            self.fig.add_trace(go.Scatter(
                x = flows,
                y = self.fit['predicted'],
                    line=dict(color = self.base_color[base_num], dash = 'dash'),
                name = f"{base} 1mer fit"
            ), **self.plot_loc[base])
        except:
            pass
            
        # Plot early flow fit
        try:
            self.fig.add_trace(go.Scatter(
                x = flows,
                y = self.early_fit['fit_params']['A']*(np.exp(self.early_fit['fit_params']['b']*flows)),
                    line=dict(color = self.base_color[base_num], dash = 'dot'),
                name = f"{base} 1mer early fit"
            ), **self.plot_loc[base])
        except:
            pass                
        
        self.fig.update_xaxes(title_text = 'Flow #', **self.plot_loc[base])
        self.fig.update_yaxes(title_text = 'Signal', **self.plot_loc[base])
        return
    def plot_data(self) -> None:
        self.fig.set_name(f"{self.template} 1mer Fit by Base - {self.runID}")
        self.fig.update_layout(title_text = self.fig.name,
                            hovermode = "x unified")
    def report_data(self):
        return
        
    def get_fit_data(self):
        return self.early_fit_intercepts, self.early_fit_decay_rates, self.intercepts, self.decay_rates