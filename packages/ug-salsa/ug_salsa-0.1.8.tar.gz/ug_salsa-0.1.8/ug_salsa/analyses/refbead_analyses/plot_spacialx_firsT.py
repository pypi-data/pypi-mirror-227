from salsa.data import RefBeadData
from salsa.analyses.refbead_analyses.refbead_analysis import RefBeadAnalysis

import numpy as np
import salsa.plots.new_plots as new_plt
import pandas as pd
from salsa.analyses.refbead_analyses import BeadLoss
from salsa.data.fwhmdata import FWHMData
from scipy.stats import binned_statistic
import plotly.graph_objects as go
from salsa.helper_functions import log

class PlotSpacialXFirsT(RefBeadAnalysis):
    
    def __init__(self, fwhmdata: FWHMData, data: RefBeadData, bead_loss: BeadLoss) -> None:
        super().__init__(data)
        self.bead_loss = bead_loss
        self.fwhmdata = fwhmdata
        return
    def preprocess_data(self) -> None:
        data = [self.bead_loss.get_steady_refbeads()[:,0],
                        self.bead_loss.get_steady_XYT()[:,0],
                        int(np.max(self.bead_loss.get_steady_XYT()[:,0]))] 
        
        bin_size = int(np.ceil(data[2]/10))
        
        all_xlocs_count, self.pixel_bins = np.histogram(data[1], bins=bin_size)
        # this isn't quite right
        self.firstT, _, _ = binned_statistic(data[1], data[0], statistic='mean', bins = self.pixel_bins)
        self.spacial_X_first_T_cv = np.round(np.std(self.firstT)/np.mean(self.firstT),3)
    def report_data(self) -> None:
        self.table = pd.DataFrame(data=np.vstack([['Flow 1 FOV CV'],
                                                [self.spacial_X_first_T_cv]]).T,
                                columns = ['Metric', 'Value'])
        self.report_title =  f"Flow 1 Metrics - {self.runID}"
        self.metrics.add('rb_fov_cv', self.spacial_X_first_T_cv)
        return
    
    def plot_data(self) -> None:
        fig = new_plt.SubPlot(specs=[[{'secondary_y': True}]])
        
        # fig.add_trace(go.Scatter(
        #       x = pixel_bins[1:],
        #       y = all_xlocs_count,
        #       name = "RefBeads Total"
        # ), secondary_y = False)
        
        fig.add_trace(go.Scatter(
                x = self.pixel_bins[1:],
                y = self.firstT,
                name = "Refbead First T Signal"
        ), secondary_y = False)
        
        if self.fwhmdata:
                try:
                    fwhm_first_flow = np.nanmean(self.fwhmdata.fwhmMap, axis = 1)[0,:]
                    base_edges = np.arange(17)*(self.data.tile_width/16)
                    fwhm_bins = (base_edges[1:] + base_edges[:-1])/2
                    fig.add_trace(go.Scatter(
                            x = fwhm_bins,
                            y = fwhm_first_flow,
                            name = "FWHM Profile"
                    ), secondary_y = True)
                except FileNotFoundError:
                    log("warning", f"rb_spacialX: No FWHM file found")
                except Exception as e:
                    log("exception", f"Exception plotting FWHM for RB spacial plot: {e}")
        
        fig.set_name(f"Spatial First T Distribution: X-Positions - {self.runID}")
        fig.update_layout(hovermode = 'x unified')
        
        fig.update_xaxes(title_text = "X-Position (Pixels)")
        fig.update_yaxes(title_text = "Refbeads First T Signal", secondary_y = False)
        fig.update_yaxes(title_text = "FWHM Value (um)", secondary_y = True)
        self.fig = fig
        return


 


