from salsa.data import RefBeadData
from salsa.analyses.refbead_analyses.refbead_analysis import RefBeadAnalysis

import numpy as np
import salsa.plots.new_plots as new_plt
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import median_abs_deviation
import tqdm

class SignalNoise(RefBeadAnalysis):
                
    def __init__(self, data: RefBeadData) -> None:
        super().__init__(data)
        return
    def preprocess_data(self) -> None:
        self.min_flow = 198
        self.max_flow = 202
        self.img_buffer = 100
        self.num_xbins = 5
        self.num_sigbins = 9
    
        self.tile_size = [2**round(np.log2(np.max(self.data.XYT[:,1]))),2**round(np.log2(np.max(self.XYT[:,0])))]
        sub_sigmat = self.data.sigmat[:,self.min_flow-1:self.max_flow]
        self.min_sig = int(np.quantile(sub_sigmat.flatten(), 0.05))
        self.max_sig = int(np.quantile(sub_sigmat.flatten(), 0.95))
        self.num_beads, self.num_flows = sub_sigmat.shape
        self.tiles = np.unique(self.data.XYT[:,2]).astype(int)
        #num_tiles = tiles.shape[0]
        return
    
    def analyze_data(self) -> None:
        self.mean_tile_sigmat = np.zeros((np.max(self.tiles), self.num_flows))
        self.tile_inds = {d:np.where(self.XYT[:,2] == d)[0] for d in self.tiles}
        self.rb_per_tile = np.array([self.tile_inds.get(tile + 1, np.array([])).shape[0]
                                for tile in range(int(np.max(self.XYT[:,2])))])
        with tqdm(total = len(self.tile_inds), position=0, leave= True) as pbar:
                for tile, inds in self.tile_inds.items():
                    tile_data = self.sub_sigmat[inds,:]
                    tile_data.sort(axis = 0)
                    n_exclude = round(tile_data.shape[0]*(.125)-0.0000001)
                    if n_exclude == 0:
                            val = np.mean(tile_data, axis = 0)
                    else:
                            val = np.mean(tile_data[n_exclude:-n_exclude, :], axis = 0)
                    self.mean_tile_sigmat[tile-1,:] = val
                    pbar.update()
        mean_flow_sigmat = np.mean(self.mean_tile_sigmat, axis = 1)
        # above calculations have nan vals, which matlab defaults to 0
    
        norm_sigmat = self.sub_sigmat \
            - self.ean_tile_sigmat[self.XYT[:,2].astype(int)-1,:] \
                + np.tile(mean_flow_sigmat[self.XYT[:,2].astype(int)-1][None,].transpose(),self.sub_sigmat.shape[1])

        enough_refbeads_inds = np.where(rb_per_tile[self.XYT[:,2].astype(int) - 1] >= 16)[0]
        goodNormSig = norm_sigmat[enough_refbeads_inds]
        goodMeanSig = np.mean(goodNormSig, axis = 1)
        goodSigCV = median_abs_deviation(goodNormSig, axis = 1, scale = 'normal')/goodMeanSig
        goodSigCV[np.where(np.abs(goodSigCV) > 1000)[0]] = np.nan
        goodXYT = self.XYT[enough_refbeads_inds]
    
        x_valid = np.intersect1d(np.where(goodXYT[:,0] > self.img_buffer)[0], np.where(goodXYT[:,0] < (self.tile_size[1] - self.img_buffer))[0])
        y_valid = np.intersect1d(np.where(goodXYT[:,1] > self.img_buffer)[0], np.where(goodXYT[:,1] < (self.tile_size[0] - self.img_buffer))[0])
        away_from_edge_inds = np.intersect1d(x_valid, y_valid)
        signal_in_range_inds = np.intersect1d(np.where(goodMeanSig > self.min_sig), np.where(goodMeanSig < self.max_sig))
    
        valid_inds = np.intersect1d(away_from_edge_inds, signal_in_range_inds)
        # pass_filter_ratio = valid_inds.shape[0]/goodXYT.shape[0]
    
        x_bins = np.arange(0, self.tile_size[1] + 1, self.tile_size[1]/self.num_xbins)
        self.x_bin_centers = np.array([np.mean([x_bins[i], x_bins[i + 1]]) for i in range(x_bins.shape[0] - 1)])
        x_binned = np.digitize(goodXYT[:,0], x_bins)
    
        sig_bins = np.arange(self.min_sig, self.max_sig + 1, (self.max_sig - self.min_sig)/self.num_sigbins)
        #sig_bin_centers = np.array([np.mean([sig_bins[i], sig_bins[i + 1]]) for i in range(sig_bins.shape[0] - 1)])/6.6 # Gray level
        self.sig_bin_centers = np.array([np.mean([sig_bins[i], sig_bins[i + 1]]) for i in range(sig_bins.shape[0] - 1)])
    
        sigMean = np.nan*np.zeros((self.num_sigbins, self.num_xbins))
        self.sigCV = np.nan*np.zeros((self.num_sigbins, self.num_xbins))
        self.binSize = np.nan*np.zeros((self.num_sigbins, self.num_xbins))
    
        for i in range(self.num_xbins):
                bin_inds = np.intersect1d(np.where(x_binned == (i + 1))[0], valid_inds)
                self.binSize[:,i], _ = np.histogram(goodNormSig[bin_inds,:], sig_bins)
    
                goodMeanSig_digitized = np.digitize(goodMeanSig, sig_bins)
                for j in range(self.num_sigbins):
                    sig_inds = np.intersect1d(np.where(goodMeanSig_digitized == (j + 1))[0], bin_inds)
                    if sig_inds.shape[0] > 50:
                            sigMean[j,i] = np.mean(goodMeanSig[sig_inds])
                            self.sigCV[j,i] = np.nanmedian(goodSigCV[sig_inds])
        self.binSize = self.binSize.astype(int)
        self.metrics.add("opt_sigcv", np.mean(self.sigCV))
        return
    
    def report_data(self) -> None:
        return
    
    def plot_data(self):
        # Plotting
        fig = new_plt.SubPlot(rows = 2, cols = 1, vertical_spacing = 0.15)
        xbin_key = {0: 'Left',
                    2: 'Center',
                    4: 'Right',}
        for xbin in [0,2,4]:
                fig.add_trace(go.Scatter(
                    x = self.sig_bin_centers,
                    y = self.sigCV[:,xbin],
                    name = f"{xbin_key[xbin]} X bin",
                    hovertemplate = f'{xbin_key[xbin]} X bin' +
                    '<br>%{text}',
                    text = [f"{p}<br>{b} beads" for p, b in zip(
                            [f"{round(i/10 - 0.05,2)}-{round(i/10 + 0.05,2)} quantile" for i in range(1,10)],
                            self.binSize[:, xbin])],
                ), row = 1, col = 1)
                
        fig.add_trace(go.Scatter(
                x = self.x_bin_centers,
                y = self.sigCV[4,:],
                name = f"SigCV of Median Signal Reads",
        ), row = 2, col = 1)
        
        fig.set_name(f'SigCV around Flow 200 - {self.runID}')
        fig.update_layout(title_text = fig.name, height = 720)
        fig.update_xaxes(title_text = 'Signal Level', row = 1, col = 1)
        fig.update_yaxes(title_text = 'SigCV', row = 1, col = 1)
        fig.update_xaxes(title_text = 'X bin', row = 2, col = 1)
        fig.update_yaxes(title_text = 'SigCV', row = 2, col = 1)
        self.fig = fig

    def add_plot_to_html(self):
        self.fig.append_to_html(interactive = False)             
