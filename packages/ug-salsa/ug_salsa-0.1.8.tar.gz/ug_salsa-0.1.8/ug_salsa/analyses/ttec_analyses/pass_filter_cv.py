from salsa.data.ttecdata import TTECData
from salsa.analyses.ttec_analyses import TTECAnalysis
import numpy as np
import pandas as pd
import salsa.plots.new_plots as new_plt
from salsa.data import TTECData

class TTECPassFilterCV(TTECAnalysis):
    def __init__(self, data: TTECData) -> None:
        super().__init__(data)

    def preprocess_data(self) -> None:
        tiles = np.unique(self.data.XYT[:, 2]).astype(int)
        num_ttec_beads_per_tile = np.array(
            [len(np.where(self.data.XYT[:, 2] == tile_num)[0]) for tile_num in tiles]
        )
        total_beads_per_tile = self.FullBeadsPerTile[tiles - 1]

        keep_inds = np.where(
            total_beads_per_tile / self.tile_size > self.params["min_bead_density"]
        )[0]
        total_found = self.data.total_found
        total_sampled = np.sum(num_ttec_beads_per_tile[keep_inds])
        scaling_factor = total_found / total_sampled

        self.pass_filter = scaling_factor * num_ttec_beads_per_tile / total_beads_per_tile
        self.pass_filter = self.pass_filter[keep_inds]
        self.active_tiles = tiles[keep_inds]
        
        self.df = pd.DataFrame(100*self.pass_filter, columns = ["Pass Filter"])
        self.df["tile"] = self.active_tiles
        self.df["radius"] = self.radii[self.active_tiles - 1]
        self.df["theta"] = self.theta[self.active_tiles - 1]*180/np.pi
        self.cv = np.std(self.pass_filter) / np.mean(self.pass_filter)
        return

    def report_data(self) -> None:
        self.metrics.add("ec_pass_filter_average_pct", 100 * np.mean(self.pass_filter))
        self.metrics.add("ec_pass_filter_cv", self.cv)

        self.table = pd.DataFrame(
            data=np.vstack(
                [
                    ["Average Pass Filter %", "Pass Filter CV"],
                    ["%.3f" % (100 * np.mean(self.pass_filter)), "%.3f" % self.cv],
                ]
            ).T,
            columns=["Metric", "Value"],
        )
        self.report_title = f"TTEC Pass Filter Metrics - {self.runID}"
        return

    def plot_data(self) -> None:

        fig = new_plt.WaferPlot(self.df, r='radius', theta='theta', color='Pass Filter',
                                hover_name = np.array([f'Tile {int(tile)}' for tile in self.df['tile'].to_numpy()]),
                                hover_data = {"Pass Filter": True},
                                color_continuous_scale = ['red','yellow','green'],
                                opacity=0.5)
        fig.set_name(f'TTEC Pass Filter Values - {self.runID}')
        fig.update_layout(title_text = fig.name,
                          coloraxis_colorbar=dict(title = "% TTEC beads"))
        self.fig = fig
        return
    
    def run_without_output(self) -> None:
        if self.meets_conditions_for_analysis(1_000_000):
            self.preprocess_data()
            self.plot_data()
            self.report_data()