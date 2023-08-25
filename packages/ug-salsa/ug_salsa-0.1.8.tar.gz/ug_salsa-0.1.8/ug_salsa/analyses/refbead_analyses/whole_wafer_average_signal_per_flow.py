from salsa.data import RefBeadData
from salsa.analyses.refbead_analyses.refbead_analysis import RefBeadAnalysis

from salsa.helper_functions import log
import numpy as np
import salsa.plots.new_plots as new_plt
import plotly.graph_objects as go


class WholeWaferAverageSignalPerFlow(RefBeadAnalysis):

    def __init__(self, data: RefBeadData) -> None:
        super().__init__(data)
        return
    
    def analyze_data(self) -> None:
        if self.data.mean_sig_per_flow is None:
            log('warning', f"No mean sig per flow data found for runID {self.runID}")
            return
        
        self.processed_data = self.data.mean_sig_per_flow[:4*(self.data.mean_sig_per_flow.shape[0]//4)]
        self.cycles = np.arange(self.processed_data.shape[0]//4) + 1
        return

    def report_data(self) -> None:
        return
    def plot_data(self) -> None:
        colors = ['red','black','blue','green']
        
        fig = new_plt.Figure()
        
        for i, base in enumerate(['T','G','C','A']):
                base_data = self.processed_data[i::4]
                fig.add_trace(go.Scatter(x=self.cycles, y=base_data, name=base,
                    line=dict(color=colors[i])))
        fig.set_name(f"Whole Wafer Average Signal per Flow - {self.runID}")
        fig.update_layout(title_text=fig.name,
                            hovermode='x unified')
        fig.update_xaxes(title_text="Cycle #")
        fig.update_yaxes(title_text="Signal")
        self.fig = fig
        return