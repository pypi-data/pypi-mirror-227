from salsa.data.ttecdata import TTECData
from salsa.analyses.ttec_analyses import TTECAnalysis
from typing import Dict
import numpy as np
import pandas as pd
import os
import salsa.plots.new_plots as new_plt
from salsa.data import *
import plotly.graph_objects as go
from salsa.analyses.ttec_analyses.normed_signal import NormedSignal
import warnings


class Cycle_Frac(TTECAnalysis):
    
    def __init__(self, data: TTECData, normed_sig: NormedSignal = None) -> None:
        super().__init__(data)
        if(normed_sig is None):
            self.normed_sig_analysis = NormedSignal(self.data)
        else:
            self.normed_sig_analysis = normed_sig
            # check that runID matches, check if data is saved and accessible
        self.normalized_signal = self.normed_sig_analysis.normalized_signal
        self.flows = normed_sig.flows
        self.cyc50_frac = []
        self.cyc75_frac = []
        self.cyc100_frac = []
        self.cycEnd_frac = []

    def preprocess_data(self) -> None:
        for i, _ in enumerate(self.params['flow_order']):
            try:
                    self.cyc50_frac.append(
                        self.normalized_signal[np.where( self.flows == (4 * 49 + i))[0]][0]
                        /  self.normalized_signal[0]
                    )
                    self.cyc75_frac.append(
                        self.normalized_signal[np.where( self.flows == (4 * 74 + i))[0]][0]
                        /  self.normalized_signal[0]
                    )
                    self.cyc100_frac.append(
                        self.normalized_signal[np.where( self.flows == (4 * 99 + i))[0]][0]
                        /  self.normalized_signal[0]
                    )
            except IndexError:
                pass
            self.cycEnd_frac.append(
                self.normalized_signal[np.where( self.flows == np.max( self.flows))[0]][0]
                /  self.normalized_signal[0]
            )
    
    def report_data(self):
        if not np.isnan(self.metrics.get("ec_instability", np.nan)):
            self.metrics.add("ec_flow200_frac", np.nanmean( self.cyc50_frac))
            self.metrics.update_report("CYC50_FRAC", np.nanmean( self.cyc50_frac))
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=RuntimeWarning)
                self.metrics.add(
                    "ec_flow300_frac", (bool( self.cyc75_frac) * np.mean( self.cyc75_frac))
                )
                self.metrics.add(
                    "ec_flow400_frac", (bool( self.cyc100_frac) * np.mean( self.cyc100_frac))
                )
                self.metrics.update_report(
                    "CYC100_FRAC", (bool( self.cyc100_frac) * np.mean( self.cyc100_frac))
                )  # faulting for some reason
        else:
            self.metrics.add("ec_flow200_frac", np.nan)
            self.metrics.add("ec_flow300_frac", np.nan)
            self.metrics.add("ec_flow400_frac", np.nan)
        self.metrics.add(f"num_cycles", int(self.data.sigmat.shape[1] // 4))
        self.metrics.add(f"ec_flow_end_frac", np.mean( self.cycEnd_frac))

        self.table = pd.DataFrame(
            data=np.vstack(
                [
                    [
                        "Flow 200 Fraction",
                        "Flow 300 Fraction",
                        "Flow 400 Fraction",
                        f"Flow {int(self.data.sigmat.shape[1])} (End) Fraction",
                    ],
                    [
                        "%.3f" % self.metrics.get("ec_flow200_frac"),
                        "%.3f" % self.metrics.get("ec_flow300_frac"),
                        "%.3f" % self.metrics.get("ec_flow400_frac"),
                        "%.3f" % self.metrics.get("ec_flow_end_frac"),
                    ],
                ]
            ).T,
            columns=["Metric", "Value"],
        )
        self.report_title = f"TTEC Cycle Frac Metrics - {self.runID}"




      
        
            




