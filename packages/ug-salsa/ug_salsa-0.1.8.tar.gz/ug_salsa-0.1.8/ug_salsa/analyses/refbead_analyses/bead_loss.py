from salsa.data import RefBeadData
from salsa.analyses.refbead_analyses.refbead_analysis import RefBeadAnalysis
import numpy as np
import pandas as pd

class BeadLoss(RefBeadAnalysis):
    
    def __init__(self, data: RefBeadData) -> None:
        super().__init__(data)
        return
    
    def analyze_data(self) -> None:

        loss_threshold = self.params['bead_loss_threshold']
        min_gradient = self.params['beadLoss_min_gradient']
        count_threshold = self.params['flicker_count_threshold']
        refbeads =self.data.sigmat # self.lost_sigmat.copy()
        xyt = self.data.XYT
    
        self.remove_flickering_beads(refbeads, min_gradient, count_threshold)
    
        self.determine_lost_flow_idx(loss_threshold, min_gradient)
    
        self.get_lost_per_cycle()

        self.get_loss_norm_per_tile(refbeads, xyt)
        return

    def remove_flickering_beads(self, refbeads, min_gradient, count_threshold):
        # Remove flickering beads from reference bead sample
        flicker_boolean = np.abs(np.diff(refbeads))>min_gradient
        steady_flicker = (np.unique(np.where(flicker_boolean)[0], return_counts=True)[1])>count_threshold
        flicker_idx = np.unique(np.where(flicker_boolean==True)[0])[np.where(steady_flicker==True)]
        refbeads[flicker_idx] = np.nan
        steady_index = (np.unique(np.where(~np.isnan(refbeads))[0]))
        self.steady_refbeads = refbeads[steady_index]
        self.nrefbeads = self.steady_refbeads.shape[0]

    def determine_lost_flow_idx(self, loss_threshold, min_gradient):
         # Determine index of lost beads and flow on which they were lost. Omit last 5 flows from this analysis.
        detections = self.steady_refbeads>loss_threshold
        self.lostCyc = (np.size(detections,1) - np.sum(np.cumprod(np.fliplr(detections) == 0, 1), 1)).astype('double')
        self.lostCyc[(np.size(detections,1)  - self.lostCyc)<5] = np.nan
        self.islost=np.where(~(np.isnan(self.lostCyc)))[0]
        signal_drop_before_low = self.steady_refbeads[self.islost,self.lostCyc[self.islost].astype(int) - 1] - self.steady_refbeads[self.islost,self.lostCyc[self.islost].astype(int)]
        self.islost = self.islost[np.where(signal_drop_before_low > 500)[0]]            
        self.high_gradients = np.where(np.abs(np.diff(self.steady_refbeads[self.islost]))>min_gradient)
        self.lost_beads = self.high_gradients[0][np.unique(self.high_gradients[0],return_index=True)[1]]

    def get_lost_per_cycle(self):
        lostFlows = [int(np.max(self.high_gradients[1][np.where(self.high_gradients[0]==self.lost_beads[i])])) for i in range(self.lost_beads.size)]
        for i in range(len(np.transpose(self.islost))):
                if(np.all(self.lost_beads != i)):
                    lostFlows.append(int(self.lostCyc[np.transpose(self.islost)[i]]))
                    self.lost_beads = np.append(self.lost_beads, i)
    
        self.lostFlows = lostFlows = [int(i) for i in lostFlows]
        fraction_lost = (np.array(np.unique(lostFlows, return_counts = True)[1])/self.nrefbeads)*100      
        self.lost_percycle = np.zeros(self.steady_refbeads[1].size)
        self.lost_percycle[list(np.unique(lostFlows))] = [fraction_lost[i] for i in range(np.unique(lostFlows).size)]
        self.islost_200 = self.islost[np.where(np.array(lostFlows) <= 200)[0]]

    def get_loss_norm_per_tile(self, refbeads, xyt):
        self.steady_XYT = steady_XYT = xyt[(np.unique(np.where(~np.isnan(refbeads))[0]))]
        tile_IDs = np.arange(1,self.data.ntiles+1)
        counts_perTile, rb_perTile, self.lossNorm_perTile = np.zeros(tile_IDs.shape[0]), np.zeros(tile_IDs.shape[0]), np.zeros(tile_IDs.shape[0])
        lost_tileIDs, lost_tile_idx, lost_perTile = np.unique(steady_XYT[:,2][self.islost], return_index = True, return_counts = True)

        if(len(lost_tile_idx)>0):
                counts_perTile[lost_tileIDs.astype('int')-1] = lost_perTile
        steady_tileIDs, steady_rb_idx, steady_rb_perTile = np.unique(steady_XYT[:,2], return_index = True, return_counts = True)
        if(len(steady_rb_idx)>0):
                rb_perTile[steady_tileIDs.astype('int')-1] = steady_rb_perTile

        norm_mask = np.logical_and(rb_perTile > 0, counts_perTile > 0) # tiles with refbeads and lost beads 
        self.lossNorm_perTile[norm_mask] = counts_perTile[norm_mask]/rb_perTile[norm_mask]

    def report_data(self) -> None:
        bead_loss_data = {
            'bead_loss_pct':(self.islost_200.shape[0]/self.nrefbeads)*100, # fraction lost
            'bead_loss_pct_maxflow':(self.islost.shape[0]/self.nrefbeads)*100,
            'max_bl_flow': int(np.argmax(self.lost_percycle) + 1), # flow #
            'max_bl_pct':np.max(self.lost_percycle), # frac_lost
            'median_bl_perflow_pct':np.median(self.lost_percycle),
        }
        metrics_dict = {
                'Bead Loss %':np.round((self.islost_200.shape[0]/self.nrefbeads)*100,2), # fraction lost 
                'Bead Loss % @ Max Flows':np.round((self.islost.shape[0]/self.nrefbeads)*100,2),
                'Max Bead Loss Flow': np.argmax(self.lost_percycle) + 1, # flow #
                'Max Bead Loss %':np.round(np.max(self.lost_percycle),3), # frac_lost
                'Median % lost per flow':np.round(np.median(self.lost_percycle),3),
        }
        
        metrics = [key for key in metrics_dict]
        values = [metrics_dict[key] for key in metrics]
            
        self.table = pd.DataFrame(data=np.vstack([metrics,values]).T, columns = ['Metric', 'Value'])
        self.report_title = f"Bead Loss Metrics - {self.runID}"

        for key, value in bead_loss_data.items():
            self.metrics.add(key, value)
        return
    
    def get_islost(self):
         return self.islost
    
    def get_islost200(self):
         return self.islost_200
    
    def get_lost_percycle(self):
        return self.lost_percycle
    
    def get_percLost_perTile(self):
         return self.lossNorm_perTile*100
    
    def get_steady_XYT(self):
         return self.steady_XYT
    
    def get_lost_flows(self):
         return self.lostFlows
    
    def get_steady_refbeads(self):
         return self.steady_refbeads
    