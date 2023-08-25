from salsa.data import RefBeadData
from salsa.analyses.refbead_analyses.refbead_analysis import RefBeadAnalysis

import numpy as np
import salsa.plots.new_plots as new_plt
import pandas as pd

class PlotBeadDensity(RefBeadAnalysis):
    
    def __init__(self, data: RefBeadData) -> None:
        super().__init__(data)
        return
    
    def report_data(self) -> None:
        return
    
    def plot_data(self) -> None:
        data = np.vstack([self.data.tiles,
                            self.data.radii,
                            self.data.theta*180/np.pi,
                            self.data.FullBeadsPerTile/(self.data.tile_size)]).transpose()
        df = pd.DataFrame(data, columns = ["tileID",'radius','theta','Bead Density'])
        df['Bead Density'] = df['Bead Density'].astype(np.int64)
        
        hist = new_plt.Histogram(df, x='Bead Density', height = 300)
        hist.set_name(f"Bead Density Histogram - {self.runID}")
        hist.update_layout(title_text=hist.name)
        hist.update_xaxes(title_text='Bead Density (beads/mm<sup>2</sup>)')
        hist.update_yaxes(title_text='Number of Tiles')
        hist.update_traces(xbins=dict(size=10**4/2))
        self.hist = hist

        fig = new_plt.WaferPlot(df, r="radius", theta="theta", color="Bead Density",
                hover_name = np.array([f'Tile {int(tile)}' for tile in df['tileID'].to_numpy()]),
                hover_data = {"Bead Density": True},
                range_color=[int(df['Bead Density'].quantile(0.01)), int(df['Bead Density'].quantile(0.99))],
                #range_color = [0, 55*10**4],
                opacity=0.5)
        fig.set_name(f"Bead Density - {self.runID}")
        fig.update_layout(title_text=fig.name,
                coloraxis_colorbar=dict(title="Beads/mm<sup>2</sup>"))
        self.fig = fig
        return
    
    def add_plot_to_html(self):
        self.hist.send_json(self.runID)
        self.hist.append_to_html(interactive = False)
        self.fig.send_json(self.runID)
        self.fig.append_to_html()

