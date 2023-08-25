from salsa.data import RefBeadData
from salsa.analyses.refbead_analyses.bead_loss import BeadLoss
from salsa.analyses.refbead_analyses.refbead_analysis import RefBeadAnalysis

import numpy as np
import salsa.plots.new_plots as new_plt
import pandas as pd
import plotly.graph_objects as go

class PlotBeadLossPerFlow(RefBeadAnalysis):
                
    def __init__(self, data: RefBeadData, bead_loss: BeadLoss) -> None:
        super().__init__(data)
        self.bead_loss = bead_loss
        return
    
    def report_data(self) -> None:
        return
    
    def plot_data(self):                       
        x = np.arange(8, self.data.sigmat.shape[1]+1)
            
        fig = new_plt.SubPlot(specs=[[{'secondary_y': True}]])
        
        fig.add_trace(go.Scatter(
                x = x,
                y = self.bead_loss.get_lost_percycle()[7:-5],
                name = "% lost per flow"
        ), secondary_y = False)
        
        fig.add_trace(go.Scatter(
                x = x,
                y = np.nancumsum(self.bead_loss.get_lost_percycle())[7:-5],
                name = "Cumulative % lost"
        ), secondary_y = True)

        fig.set_name(f"Bead Loss per Flow - {self.runID}")
        fig.update_layout(title_text=fig.name,
                            hovermode = 'x unified')
        fig.update_xaxes(title_text = "Flow Number")
        fig.update_yaxes(title_text = "Beads Lost (%)", secondary_y = False)
        fig.update_yaxes(title_text = "Cumulative Lost (%)", secondary_y = True)            
        self.fig = fig


