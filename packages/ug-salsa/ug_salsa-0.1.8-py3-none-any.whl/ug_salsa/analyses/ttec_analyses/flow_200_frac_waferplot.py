from salsa.data.ttecdata import TTECData
from salsa.analyses.ttec_analyses import TTECAnalysis
from typing import Dict
import numpy as np
import pandas as pd
import os
import salsa.plots.new_plots as new_plt
from salsa.data import *
from salsa.analyses.ttec_analyses.calculate_bkg_per_flow import CalculateBkgPerFlow
import tqdm

class Flow200fracWaferPlot(TTECAnalysis):
    def __init__(self, bkg: CalculateBkgPerFlow = None, data: TTECData = None) -> None:
        super().__init__(data)

        if not bkg.has_all_attributes(self.data.runID):
            calcbkg = CalculateBkgPerFlow(self.data, plot=True)
            calcbkg.run_without_output()
            self.bkg = calcbkg.get_bkg_ext()
            self.subanalysis_figs.append(calcbkg.fig)
        else:
            self.bkg = bkg.bkg_ext

    def preprocess_data(self) -> None:
        
        floors = self.bkg
        self.cyc1_floors = floors[0:4]
        self.cyc50_floors = floors[196 - self.data.preamble_length : 200 - self.data.preamble_length]

        self.ec_tiles = np.unique(self.data.XYT[:, 2])
        # tile_frac = {}
        self.tile_frac = np.nan * np.zeros(self.ec_tiles.shape[0])

        return

    def analyze_data(self) -> None:
        with tqdm(total=self.ec_tiles.shape[0], position=0, leave=True) as pbar:
            for i, tile in enumerate(self.ec_tiles):
                inds = np.where(self.XYT[:, 2] == tile)[0]
                ntile_beads = inds.shape[0]

                tcyc1_keys = np.sum(self.data.truekey[inds, 0:4], axis=0)
                tcyc1_keys_tiled = np.tile(
                    tcyc1_keys[
                        None,
                    ].transpose(),
                    ntile_beads,
                ).transpose()
                tcyc50_keys = np.sum(
                    self.data.truekey[
                        inds,
                        (196 - self.data.preamble_length) : (200 - self.data.preamble_length),
                    ],
                    axis=0,
                )
                tcyc50_keys_tiled = np.tile(
                    tcyc50_keys[
                        None,
                    ].transpose(),
                    ntile_beads,
                ).transpose()

                cyc1_floors_tile = np.tile(
                    self.cyc1_floors[
                        None,
                    ].transpose(),
                    ntile_beads,
                ).transpose()
                cyc50_floors_tile = np.tile(
                    self.cyc50_floors[
                        None,
                    ].transpose(),
                    ntile_beads,
                ).transpose()

                tcyc1_normed = np.sum(
                    (self.data.sigmat[inds, 8:12] - cyc1_floors_tile) / tcyc1_keys_tiled,
                    axis=0,
                )
                tcyc50_normed = np.sum(
                    (self.data.sigmat[inds, 196:200] - cyc50_floors_tile)
                    / tcyc50_keys_tiled,
                    axis=0,
                )

                finite_inds = np.where(np.isfinite(tcyc50_normed)*np.isfinite(tcyc1_normed))[0]
                if finite_inds.shape[0] == 0:
                    self.tile_frac[i] = np.nan
                    pbar.update()
                    continue
                self.tile_frac[i] = np.mean((tcyc50_normed / tcyc1_normed)[finite_inds])
                pbar.update()
        self.df = pd.DataFrame(
            index=self.ec_tiles, columns=["Tile", "Radius", "Theta", "Flow200 Frac"]
        )
        self.df["Tile"] = self.ec_tiles
        self.df["Radius"] = self.radii[self.ec_tiles.astype(int) - 1]
        self.df["Theta"] = self.theta[self.ec_tiles.astype(int) - 1] * 180 / np.pi
        self.df["Flow200 Frac"] = self.tile_frac
        return

    def report_data(self) -> None:
        pass

    def plot_data(self) -> None:
        
        fig = new_plt.WaferPlot(
            self.df,
            r="Radius",
            theta="Theta",
            color="Flow200 Frac",
            hover_name=np.array(
                [f"Tile {int(tile)}" for tile in self.df["Tile"].to_numpy()]
            ),
            color_continuous_scale="turbo_r",
            range_color=[0.35, 0.75],
            title=f"RunID{self.runID} TTEC Flow200 Fraction",
        )
        fig.set_name(f"TTEC Flow200 Fraction - {self.runID}")
        self.fig = fig
        return