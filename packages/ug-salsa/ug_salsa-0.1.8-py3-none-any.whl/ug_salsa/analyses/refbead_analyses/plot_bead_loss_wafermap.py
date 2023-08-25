from salsa.data import RefBeadData
from salsa.analyses.refbead_analyses.bead_loss import BeadLoss
from salsa.analyses.refbead_analyses.refbead_analysis import RefBeadAnalysis

import numpy as np
import salsa.plots.new_plots as new_plt
import pandas as pd
import plotly.graph_objects as go

class PlotBeadLossWaferMap(RefBeadAnalysis):
                
    def __init__(self, data: RefBeadData, bead_loss: BeadLoss) -> None:
        super().__init__(data)
        self.bead_loss = bead_loss
        return
    
    def preprocess_data(self) -> None:
        data = np.vstack([np.arange(1,self.data.ntiles+1), self.data.radii, self.data.theta*180/np.pi, self.bead_loss.get_percLost_perTile(),
        np.log10(self.bead_loss.get_percLost_perTile() + (self.bead_loss.get_percLost_perTile() < 1).astype(int))]).transpose()
        self.df = pd.DataFrame(data, columns = ["tileID",'radius','theta','% lost','log % lost'])
        return

    def report_data(self) -> None:
        return
    
    def plot_data(self):                       

        fig = new_plt.WaferPlot(self.df, r="radius", theta="theta", color="log % lost",
                hover_name = np.array([f'Tile {int(tile)}' for tile in self.df['tileID'].to_numpy()]),
                hover_data = {"% lost": True, "log % lost": False},
                color_continuous_scale=["green", "yellow", "red"],
                # range_color=[0, 20],
                opacity=0.5)
        fig.set_name(f"Bead Loss Wafer Plot - {self.runID}")
        fig.update_layout(title_text=fig.name,
                coloraxis_colorbar=dict(title="% Lost",
                                        tickvals=np.log10(np.array([1,2,5,10,20,50,100])),
                                        ticktext=np.array([1,2,5,10,20,50,100]),))
        fig.update_yaxes(range=[0,2])
        self.fig = fig

