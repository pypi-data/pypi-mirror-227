from salsa.data import RefBeadData
from salsa.analyses.refbead_analyses.bead_loss import BeadLoss
from salsa.analyses.refbead_analyses.refbead_analysis import RefBeadAnalysis

import numpy as np
import salsa.plots.new_plots as new_plt
import pandas as pd

class PlotBeadLossHist2D(RefBeadAnalysis):
                
    def __init__(self, data: RefBeadData, bead_loss: BeadLoss, step: int = 100) -> None:
        super().__init__(data)
        self.bead_loss = bead_loss
        self.step = step
        return
    def report_data(self) -> None:
        return
    def plot_data(self):           
        x = self.bead_loss.get_lost_flows()
        y = self.bead_loss.get_steady_XYT()[:,0][self.bead_loss.get_islost()]
        y_upper = self.step*((np.max(y) // self.step) + 1)
        z, xedges, yedges = np.histogram2d(x, y,
                                            bins = [np.arange(1,self.data.sigmat.shape[1] + 1),
                                                    np.arange(0,y_upper,self.step)])
        
        fig = new_plt.HeatMap(z = z.transpose(), x = xedges[1:], y = yedges[1:])
        fig.set_name(f"Bead Loss HeatMap - {self.runID}")
        fig.update_layout(title_text = fig.name, height = 720)
        fig.update_xaxes(title_text = "Flow")
        fig.update_yaxes(title_text = "X Position")
        self.fig = fig

    def add_plot_to_html(self):
        self.fig.send_json(self.runID)
        self.fig.append_to_html(interactive = False)

    