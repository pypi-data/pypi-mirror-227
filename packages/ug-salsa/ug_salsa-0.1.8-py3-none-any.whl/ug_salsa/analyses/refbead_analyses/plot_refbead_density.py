from salsa.data import RefBeadData
from salsa.analyses.refbead_analyses.refbead_analysis import RefBeadAnalysis

import numpy as np
import salsa.plots.new_plots as new_plt
import pandas as pd
from salsa.analyses.refbead_analyses.loading_density_metrics import LoadingDensityMetrics

class PlotRefBeadDensity(RefBeadAnalysis):
    
    def __init__(self, data: RefBeadData, loading_density_metrics: LoadingDensityMetrics) -> None:
        super().__init__(data)
        self.loading_density_metrics = loading_density_metrics
        return
    
    def report_data(self) -> None:
        return
    
    def plot_data(self) -> None:
        data = np.vstack([self.data.tiles,
                            self.data.radii,
                            self.data.theta*180/np.pi,
                            self.loading_density_metrics.refbeads_pertile/self.data.tile_size]).transpose()
        df = pd.DataFrame(data, columns = ["tileID",'radius','theta','RefBead Density'])
        df['RefBead Density'] = df['RefBead Density'].astype(np.int64)

        fig = new_plt.WaferPlot(df, r="radius", theta="theta", color="RefBead Density",
                hover_name = np.array([f'Tile {int(tile)}' for tile in df['tileID'].to_numpy()]),
                hover_data = {"RefBead Density": True},
                color_continuous_scale=["red", "yellow", "green"],
                range_color=[int(df['RefBead Density'].quantile(0.01)), int(df['RefBead Density'].quantile(0.99))],
                opacity=0.5)
        fig.set_name(f"RefBead Density - {self.runID}")
        fig.update_layout(title_text=fig.name,
                coloraxis_colorbar=dict(title="RefBeads/mm<sup>2</sup>"))
        self.fig = fig
        return

