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
import plotly.graph_objects as go
from salsa.data.templatedata import TemplateData
from salsa.analyses.template_analyses.floor_sig_per_base import FloorSignalPerBase
from salsa.run_metrics import RunMetrics

class TrackFloorSignalDrift(TemplateAnalysis):

    def __init__(self, templates: Dict[str,TemplateData]) -> None:
        super().__init__(templates)
        self.data: Dict = {}    
        self.desert_template = templates['desert_template']
        self.floor_template = templates['floor_template']
        self.cutoffs: np.ndarray = np.ndarray(0,)
        
    def preprocess_data(self) -> None:
        self.signals = self.desert_template.sigmat
        self.keys = self.desert_template.template_tk.flatten()
        self.med: np.ndarray = np.median(self.signals, axis = 0)
        self.num_flows = self.med.shape[0]
        self.flows = np.arange(1,self.num_flows + 1)
        self.cutoffs = np.append(np.arange(self.num_flows)[::200], self.num_flows)
        
        #all_data = {}
        #fig = plt.figure()
        #plt.title(f"floor signal drift - {self.runID}")
        #plt.xlabel("Flows")
        ##plt.xticks(ticks = np.arange(len(data['signal'])), labels = [f'{x}-{y}' for x, y in zip(cutoffs[:-1], cutoffs[1:])])
        #plt.xlim([1, num_flows + 1])
        #plt.ylabel("min 0mer signal")
        return

    def analyze_data(i: int, base: str, fig: new_plt.Figure, self) -> None:
        self.data = {}
        self.data["signal"] = []
        self.data["flow"] = []
        self.data['num_0mers'] = []
        for start, end in zip(self.cutoffs[:-1], self.cutoffs[1:]):
            inds = np.where(self.eys[start:end][i::4] == 0)[0]
            subflows = self.flows[start:end][i::4][inds]
            num_0mers = inds.shape[0]
            self.data['num_0mers'].append(num_0mers)
            
            if num_0mers == 0:
                self.data['signal'].append(np.nan)
                self.data['flow'].append(np.nan)
            else:
                min_0mer_signal = np.min(self.med[start:end][i::4][inds])
                min_0mer_ind = subflows[np.argmin(self.med[start:end][i::4][inds])]
                self.data['signal'].append(min_0mer_signal)
                self.data['flow'].append(min_0mer_ind)
    

        no_nan_signal = np.array(self.data['signal'])[~np.isnan(self.data['signal'])]
        no_nan_flow = np.array(self.data['flow'])[~np.isnan(self.data['flow'])]
        if no_nan_signal.shape[0] < 2 or no_nan_flow.shape[0] < 2:
            self.metrics.add(f'tf_floor_drift_slope_{self.base}', np.nan)
            self.metrics.add(f'tf_floor_drift_1{self.base}', np.nan)
        else:
            m, b = np.polyfit(np.array(no_nan_flow), np.array(no_nan_signal), 1)
            self.m_list.append('%.3f' % m)
            self.b_list.append(int(b))
            self.metrics.add(f'tf_floor_drift_slope_{base}', m)
            self.metrics.add(f'tf_floor_drift_1{base}', int(b))
            
            fig.add_trace(go.Scatter(
            x = self.data['flow'],
            y = m*np.array(self.data["flow"]) + b,
            name = f"{base} floor fit",
            mode = 'lines',
            line=dict(color = self.base_color[i], dash = 'dash'),
            ))

        return

    def report_data(self) -> None:
        fsperbase = FloorSignalPerBase({self.floor_template.name: self.floor_template})
        fsperbase.run_without_output()
        floors = fsperbase.get_floors()
        
        self.table = pd.DataFrame(data=np.vstack([['T','G','C','A'],
                                 np.array(floors).astype(int),
                                 self.m_list,
                                 self.b_list]).T,
                            columns=['Base', 'Absolute Floor', 'Drift Slope', 'Drift Intercept'])
        self.report_title = f'Template Floor Signal Metrics - {self.runID}'

        return
    def plot_data(self) -> None:
        fig = new_plt.Figure()
        fig.set_name(f"Template Floor Signal Drift - {self.runID}")
        fig.update_layout(title_text = fig.name)
        fig.update_xaxes(title_text = "Flow #")
        fig.update_yaxes(title_text = "Min 0mer signal")
        
        self.m_list = []
        self.b_list = []
        for i, base in enumerate(["T","G","C","A"]):
            self.analyze_data(i, base, fig)
            #plt.plot(subflows, med[start:end][i::4][inds], f'{self.base_color[i]}+', label = '_no_legend_')
            #plt.plot(min_0mer_ind, min_0mer_signal, f'{self.base_color[i]}o', label = '_no_legend_')
            fig.add_trace(go.Scatter(
                x = self.data['flow'],
                y = self.data['signal'],
                mode = 'markers',
                name = f'{base} floor',
                marker = dict(color = self.base_color[i]),
            ))

        #plt.legend()
        #fig.savefig(f"{self.params['save_loc']}plots/floor_drift.png")
        #plt.close(fig)
        self.report_data()
        
        return
    
    def run_without_output(self):
        self.preprocess_data()
        self.plot_data()