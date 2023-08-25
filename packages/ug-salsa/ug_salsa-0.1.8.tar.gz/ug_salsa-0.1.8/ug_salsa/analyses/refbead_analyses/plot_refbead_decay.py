from salsa.data import RefBeadData
from salsa.analyses.refbead_analyses.refbead_analysis import RefBeadAnalysis

from salsa.fitting_fxns import RefBeadBiexpFit, RefBeadExpFit
from salsa.analyses.refbead_analyses import NSB
from salsa.helper_functions import log
import numpy as np
import pandas as pd
import salsa.plots.new_plots as new_plt
import traceback
import plotly.graph_objects as go
from salsa.helper_functions import log, format_decays

class PlotRefBeadDecay(RefBeadAnalysis):
    
    def __init__(self, data: RefBeadData, fit: RefBeadBiexpFit, alt_fit: RefBeadExpFit = None, nsb_data: NSB = None) -> None:
        super().__init__(data)
        self.outputs = {} # type hint later
        self.fit = fit
        self.alt_fit = alt_fit
        self.nsb_data = nsb_data
        self.plot_list: list[new_plt.Figure] = []
        return
    
    def preprocess_data(self) -> None:
         # holistic metrics
        self.ref_sig = {}
        if self.alt_fit is not None:
                for base, fit in zip(['T','G','C','A'], self.alt_fit.get_attr_order()):
                    if fit['fit_params'] is None:
                            self.ref_sig[f'rb_decay_rate_pct_{base}'] = np.nan
                            self.ref_sig[f'rb_amplitude_{base}'] = np.nan
                            self.ref_sig[f'rb_floor_{base}'] = np.nan
                            continue
                    self.ref_sig[f'rb_decay_rate_pct_{base}'] = format_decays(self.fit['fit_params']['r'])
                    self.ref_sig[f'rb_amplitude_{base}'] = fit['fit_params']['L']
                    self.ref_sig[f'rb_floor_{base}'] = fit['fit_params']['k']
        else:
                for base in ['T','G','C','A']:
                    self.ref_sig[f'rb_decay_rate_pct_{base}'] = np.nan
                    self.ref_sig[f'rb_amplitude_{base}'] = np.nan
                    self.ref_sig[f'rb_floor_{base}'] = np.nan   

        self.ref_stability = self.fit.get_ref_stability()
        self.intercepts = self.fit.get_intercepts()


        self.bases = ['T','G','C','A']
        self.instability = [np.round(self.ref_stability[f'{base}'],3) for base in self.bases]
        self.decay1 = ['%.3f' % self.ref_sig[f'rb_decay_rate_pct_{base}'] for base in self.bases]
        self.amp = ['%.3f' % self.ref_sig[f'rb_amplitude_{base}'] for base in self.bases]
        self.floor = ['%.3f' % self.ref_sig[f'rb_floor_{base}'] for base in self.bases]
        self.fit_int = [self.intercepts[f'rb_fit_int_{base}'] for base in self.bases]
        self.sig_nsb = [self.nsb_data.get_output()[base] for base in self.bases]
        return

    def report_decay(self):
        self.table1 = pd.DataFrame(data=np.vstack([
                                ["Refbead Overall Instability", "Refbead % Decay (predicted)"],
                                # TODO: make sure RefbeadFit has r2 attr, get_decay_percent_predicted() method
                                [np.round(self.fit.r2,3),
                                    np.round(100*self.fit.get_decay_percent_predicted(),1)]]).T,
                                columns = ['Metric', 'Value'],
                                )
        self.report_title1 = f'Reference Bead Decay General Metrics - {self.runID}'

    def report_data(self) -> None:
        self.table2 = pd.DataFrame(data = np.vstack([self.bases, self.instability, self.decay1, self.amp, self.floor, self.fit_int, self.sig_nsb]).T,
                                columns = ["Base", "Instability",
                                    "Decay Rate (%/flow)", "Amplitude", "Floor", "Fit Intercept",
                                    "Signal NSB"])
        self.report_title2 = f'Reference Bead Base Metrics - {self.runID}'
        
        for key, value in self.ref_sig.items():
            self.metrics.add(key,value)

        self.metrics.add('rb_instability', self.ref_stability['overall'])
        for base in self.params['flow_order']:
             self.metrics.add(f'rb_instability_{base}', self.ref_stability[f'{base}'])
        self.metrics.add(f'rb_pct_decay', self.ref_stability['% decay (predicted)'])
        

        for key, value in self.intercepts.items():
            self.metrics.add(key,value)


        return

    def plot_data(self, in_fit: RefBeadBiexpFit) -> None:
        colors = ['red','black','blue','green']
        fig = new_plt.Figure()
        for i, base in enumerate(in_fit.attr_order):
            fig.add_trace(go.Scatter(x=base['x'], y=base['y'], name=in_fit.order[i],
                        line=dict(color=colors[i])))
            try:
                    fig.add_trace(go.Scatter(x=base['x'], y=base['predicted'], name=f"{in_fit.order[i]} fit",
                                            line=dict(color=colors[i], dash='dot')))
            except:
                    continue
            
        fig.set_name(f"Reference Bead Signal - {self.runID}")
        fig.update_layout(title_text=fig.name,
                        hovermode='x unified')
        fig.update_xaxes(title_text="Flow #")
        fig.update_yaxes(title_text="Signal")
        self.plot_list.append(fig)
    
    def run_without_output(self) -> None:
        self.preprocess_data()
        self.report_decay()
        # Base line plot
        if self.fit.fit_success:
            self.plot_data(self.fit)

        elif self.alt_fit.fit_success:
            self.plot_data(self.alt_fit)
        else:
                log('warning','Both double and single exponential fit failed. Nothing to plot.')
        self.report_data()
    
    def add_plot_to_html(self):
        for fig in self.plot_list:
            fig.send_json(self.runID)            
            fig.append_to_html()    

    def add_report_to_html(self):
         new_plt.PlotHandler.add_table_to_report(self.table1, self.report_title1)
         new_plt.PlotHandler.add_table_to_report(self.table2, self.report_title2)