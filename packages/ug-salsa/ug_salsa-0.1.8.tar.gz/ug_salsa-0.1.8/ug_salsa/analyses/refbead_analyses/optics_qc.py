from salsa.data import RefBeadData
from salsa.analyses.refbead_analyses.refbead_analysis import RefBeadAnalysis

import numpy as np
import salsa.plots.new_plots as new_plt
import pandas as pd
import plotly.graph_objects as go
from scipy.optimize import curve_fit
import plotly.express as px
from salsa.helper_functions import log
from scipy.stats import binned_statistic

class OpticsQC(RefBeadAnalysis):

    def __init__(self, data: RefBeadData) -> None:
        super().__init__(data)
        self.num_pixels = self.data.tile_width
        self.buffer_size = 16
        self.window_size = 20
        self.num_bins = 1024

        self.Xbins = np.linspace(self.buffer_size - 1, self.num_pixels - self.buffer_size, self.num_bins + 1)

        self.sigmat = self.data.sigmat[:,0]
        self.tileX = self.data.XYT[:,0]
        self.bead_radii = self.data.radii[self.data.XYT[:,2].astype(int) - 1]
        self.target_radii_inds = [1,3,5,7,9,11]
        self.radii = np.unique(self.data.radii)
        return
    
    def linear(self, x, m, b):
            return m*x + b

    def quadratic(self, x, a, offset):
        return a*(x - self.num_pixels/2.)**2 + offset

    def scatter_plot(self):
        self.overall_fig = new_plt.Figure()
        self.radius_figs = []
        self.metric_df = pd.DataFrame(index = self.radii[self.target_radii_inds],
                                    columns = ['Peak to Valley','Edge to Edge'])
        self.max_y = []
        self.ptv_values = []
        self.e2e_values = []
        for ind in self.target_radii_inds:
            radius = self.radii[ind]
            ring_radius = int(self.radii[ind])
            radius_inds = np.where(self.bead_radii == radius)[0]
            radius_sigmat = self.sigmat[radius_inds]
            radius_tileX = self.tileX[radius_inds]
            
            bin_mean_sig, _, _ = binned_statistic(radius_tileX, radius_sigmat, 'mean', self.Xbins)
            Xbins_adj = self.Xbins[np.where(np.isfinite(bin_mean_sig))[0]]
            SigX = bin_mean_sig[np.where(np.isfinite(bin_mean_sig))[0]]
            
            SigXconv = np.convolve(SigX, np.ones(self.window_size) / self.window_size, mode='valid')
            
            self.overall_fig.add_trace(
                go.Scatter(x = Xbins_adj[10:-9],
                            y = SigXconv,
                            name=f"Radius {ring_radius}mm profile",
                )
            )            
            
            plin, _ = curve_fit(self.linear, self.Xbins[:SigXconv.shape[0]], SigXconv)
            
            pq, _ = curve_fit(self.quadratic, Xbins_adj, SigX - self.linear(Xbins_adj, *plin))
            
            self.max_y.extend([np.max(self.linear(Xbins_adj, *plin)), np.max(SigXconv), np.max(SigX)])
            
            this_radius_fig = new_plt.SubPlot(rows = 1, cols = 2,
                                            subplot_titles = [
                                                    f"Radius {int(radius)}mm Profile",
                                                    f"{int(radius)}mm Residual Profile"
                                            ])
            this_radius_fig.add_trace(
                go.Scatter(
                        x = Xbins_adj,
                        y = SigX,
                        name = f'Raw Signal',
                        mode = 'lines',
                        line = dict(color = px.colors.qualitative.Plotly[0])
                ),
                row = 1, col = 1
            )
            this_radius_fig.add_trace(
                go.Scatter(
                        x = Xbins_adj[10:-9],
                        y = SigXconv,
                        name = f'Smoothed Signal',
                        mode = 'lines',
                        line = dict(color = px.colors.qualitative.Plotly[2])
                ),
                row = 1, col = 1
            )
            this_radius_fig.add_trace(
                go.Scatter(
                        x = Xbins_adj,
                        y = self.linear(Xbins_adj, *plin),
                        name = f'Linear Fit',
                        mode = 'lines',
                        line = dict(color = px.colors.qualitative.Plotly[1], dash = 'dash')
                ),
                row = 1, col = 1
            )
            this_radius_fig.update_yaxes(title="Signal", row = 1, col = 1)
            this_radius_fig.update_xaxes(title="FOV X Position (pixels)", row = 1, col = 1)
            this_radius_fig.add_trace(
                go.Scatter(
                        x = Xbins_adj,
                        y = SigX - self.linear(Xbins_adj, *plin),
                        name = f'Raw Residuals',
                        mode = 'lines',
                        line = dict(color = px.colors.qualitative.Plotly[0])
                ),
                row = 1, col = 2
            )
            this_radius_fig.add_trace(
                go.Scatter(
                        x = Xbins_adj,
                        y = self.quadratic(Xbins_adj, *pq),
                        name = f'Quadratic Fit',
                        mode = 'lines',
                        line = dict(color = px.colors.qualitative.Plotly[1], dash = 'dash')
                ),
                row = 1, col = 2
            )
            
            this_radius_fig.update_xaxes(title="FOV X Position (pixels)", row = 1, col = 2)
            this_radius_fig.update_layout(height = 400, width = 800)
            
            self.radius_figs.append(this_radius_fig)
            
            PTV = 100*(1. - min(SigXconv) / max(SigXconv))
            self.ptv_values.append(PTV)
            self.metric_df.loc[(radius, "Peak to Valley")] = "%.1f" % PTV
            self.metrics.add(f"opt_ring{ind}_PTV", PTV)
            
            EdgeDiff = 100*(self.linear(Xbins_adj[-1], *plin) - self.linear(Xbins_adj[0], *plin)) / np.mean(SigXconv)
            self.e2e_values.append(EdgeDiff)
            self.metric_df.loc[(radius, "Edge to Edge")] = "%.1f" % EdgeDiff
            self.metrics.add(f"opt_ring{ind}_EdgeDiff", EdgeDiff)

    def report_data(self) -> None:
        self.metrics.add("opt_avg_PTV", np.nanmean(self.ptv_values))
        self.metrics.add("opt_avg_E2E", np.nanmean(self.e2e_values))
        self.metrics.add("opt_max_PTV", np.nanmax(self.ptv_values))
        self.metrics.add("opt_max_E2E", self.e2e_values[np.nanargmax(np.abs(self.e2e_values))])
        self.max_y = np.max(self.max_y)*1.05
        self.overall_fig.set_name(f"Uniformity for select Radii - {self.runID}")
        self.overall_fig.update_layout(title=self.overall_fig.name)
        self.overall_fig.update_xaxes(title="FOV X Position (pixels)")
        self.overall_fig.update_yaxes(title="Signal", range = [0, self.max_y])
        
        self.metric_df.insert(0, "Radius (mm)", self.metric_df.index.astype(int))
        self.table = self.metric_df
        self.report_title = f"Optics Uniformity Metrics - {self.runID}"

        return
    
    def run_without_output(self) -> None:
        if not (self.runID.endswith("_1") or self.runID.endswith("_2")):
            log("exception", "Cannot determine run cam. Skipping optics QC.")
            return
        self.scatter_plot()
        self.report_data()
        return

    def add_plot_to_html(self):
        self.overall_fig.append_to_html()
        #self.overall_fig.send_json(self.runID)
        for fig in self.radius_figs:
                fig.update_yaxes(range = [0, self.max_y], col = 1, row = 1)
                fig.append_to_html(interactive = False)