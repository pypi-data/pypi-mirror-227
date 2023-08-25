from typing import Dict

from salsa.helper_functions import log
from typing import List, Dict, Union
from salsa.plots.figure import Figure
from salsa.analyses import Analysis
from salsa.run_metrics import RunMetrics
from salsa.parameters import Parameters
from salsa.data.templatedata import TemplateData
from salsa.routines.output_handler import OutputHandler
import pandas as pd
import copy
#------------------------------------------------------------------------------------------------------------------------------------------------------------
import functools
import types
import numpy as np

def _check_TFSA1_TFSA2():
    '''
    Decorator to check that arg dict has 'TFSA1' and 'TFSA2' as keys, keys to be passed as parameter when decorator is called. Checks that data objects are for the same run.
    '''
    def inner(func: types.FunctionType):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            # Check if all required keys are present in the argument dictionary
            for key in ['TFSA1', 'TFSA2']:
                if key not in kwargs:
                    raise ValueError(f"Missing required '{key}' in list of templates.")

            # Check that data objects are for the same run
            run_id = None
            for data_obj in kwargs.values():
                if run_id is None:
                    run_id = data_obj.run_id
                elif run_id != data_obj.run_id:
                    raise ValueError("Data objects are not for the same run.")
            # Call the original function with the given arguments
            return func(self, *args, **kwargs)

        return wrapper

    return inner

class TemplateAnalysis(Analysis):
    
    # @_check_TFSA1_TFSA2
    def __init__(self, templates: Dict[str, TemplateData]) -> None:
        super().__init__()
        self.templates = templates
        self.runID = list(self.templates.values())[0].runID
        self.base_color: Dict = {"T":'red', "G":'black', "C":'blue', "A":'lime',
                        "t":'red', "g":'black', "c":'blue', "a":'lime',
                        0: 'red',  1: 'black',  2: 'blue',  3: 'lime'}


    def meets_conditions_for_analysis(self, bead_count: int = 0) -> bool:
        # if bead_count == 0:
        #     # bead_count = 5000
        for template in self.templates.values():
            if  template.total_found < bead_count:
                log('warning', f"Insufficient Template Beads ({template.total_found}). Skipping analysis")
                return False
        return True
    
    def sample_beads(self, template_in: TemplateData, target_num: int):
        out = copy.deepcopy(template_in) #ask jerry
        total_beads = out.sigmat.shape[0]
        num_samples = int(target_num)
        if total_beads <= num_samples:
            return out
        
        seed = int(''.join([char for char in self.runID if char.isnumeric()])) % (2**32 - 1)
        order = np.random.RandomState(seed = seed).permutation(total_beads)[:np.min([num_samples, total_beads])]
        out.sigmat = out.sigmat[order]
        out.XYT = out.XYT[order]
        return out
    
    def best_threshold( signal_vec1, signal_vec2 ):
        # compute best threshold for 2-population separation
        s_tot = np.concatenate( [signal_vec1, signal_vec2], axis=0 )
        c_tot = np.concatenate( [signal_vec1*0, signal_vec2*0+1], axis=0 )
        
        ix = np.argsort( s_tot )
        err_vec = np.cumsum( c_tot[ix] ) + np.flip(  np.cumsum( np.flip(1-c_tot[ix]) )  )
        threshold = s_tot[ix[np.argmin(err_vec)]]
        return threshold
    
    def templErr(self, x, flows, seq, signal):
                simtrace, ph_eff = self.phase_keys(x, flows, seq)
                sigvec = np.squeeze(np.reshape(signal, ( np.size(signal),1)))
                rss = np.sqrt(sum( (sigvec-simtrace)**2 ))
                return rss
    
    def phase_keys(self, x, flows, seq ):
        # legacy code, refactor when time permits
        p_lag = x[0]
        p_lead = x[1]
        p_droop = x[2]
        p_match = 1-p_lag

        h = np.diff(np.where(np.append(np.append(True, np.diff(seq)!=0),True)))
        hmer = np.append(1,h)

        seq1mer = seq[np.cumsum(h)-1]

        flows = np.append(np.nan, flows)
        posvflow = np.zeros_like(flows).astype(int)   
        nextbase = seq1mer[0]
        
        fgmat = np.zeros((len(flows),len(seq1mer)+1))
        fgmat[0,0]=1
        simtrace = np.zeros(len(flows))
        
        #ph_eff = np.nan

        for f in range(1,len(flows)):

            
            flow = flows[f].astype(int)
            
            if flow==nextbase:
                posvflow[f]=posvflow[f-1]+1
                nextbase = seq1mer[posvflow[f]]
            else:
                posvflow[f]=posvflow[f-1]
        
            

            lastflow = np.copy(fgmat[f-1,:])
            thisflow = np.copy(fgmat[f,:])

            # droop
            lastflow = (1-p_droop)*lastflow

            # lead 1
            iicatchup = np.where(seq1mer != flow)[0]
            iistay = np.where(seq1mer == flow)[0]

            thisflow[iicatchup+1] = thisflow[iicatchup+1] + p_lead*lastflow[iicatchup]*hmer[iicatchup+1]/hmer[iicatchup]
            thisflow[iicatchup] = thisflow[iicatchup] + (1-p_lead)*lastflow[iicatchup]
            thisflow[iistay] = thisflow[iistay] + lastflow[iistay]

            # lag phasing
            iimatch = np.where(seq1mer == flow)[0]
            iimismatch = np.where(seq1mer != flow)[0]

            fgmat[f,iimatch+1] = fgmat[f,iimatch+1] + p_match*thisflow[iimatch]*hmer[iimatch+1]/hmer[iimatch]
            fgmat[f,iimatch] =  fgmat[f,iimatch]+ p_lag*thisflow[iimatch]
            fgmat[f,iimismatch] = fgmat[f,iimismatch] + thisflow[iimismatch]

            #signal added this flow from incorporations
            simtrace[f] = simtrace[f]+ np.sum( p_match*thisflow[iimatch]*hmer[iimatch+1]/hmer[iimatch])

            # lead phasing
            iilp = np.intersect1d( (iimatch+1), np.where(seq1mer != flow)[0] )
            lead = p_lead*fgmat[f,iilp]/hmer[iilp]
            fgmat[f,iilp] = fgmat[f,iilp] - lead*hmer[iilp]
            fgmat[f,iilp+1] = fgmat[f,iilp+1] + lead*hmer[iilp+1]
            
        nmat = fgmat/hmer #hmer normalize phasing matrix
        nmat = (nmat.T/np.sum(nmat,axis=1)).T #de-droop phasing matrix
        
        #accumulated phasing vs flow number
        lagfrac = np.zeros(len(posvflow)-1)
        inphase = np.zeros_like(lagfrac)
        leadfrac = np.zeros_like(lagfrac)
        for p in range(1,len(posvflow)):
            lagfrac[p-1] =np.sum(nmat[p,:posvflow[p]])
            inphase[p-1] = nmat[p,posvflow[p]]
            leadfrac[p-1] = np.sum(nmat[p,posvflow[p]+1:])
            
        #effective lag rate 
        lagrate_hats = 100*np.diff(lagfrac[:-1])/inphase[:-2]
        mu = np.median(lagrate_hats)
        stdev = np.std(lagrate_hats)
        ul = mu +4*stdev
        ll = mu -4*stdev
        outlier_removed_ind = np.where((lagrate_hats>ll) & (lagrate_hats<ul))[0] 
        laghat = np.mean(lagrate_hats[outlier_removed_ind])
        
        #effective lead rate
        leadrate_hats = 100*np.diff(leadfrac[:-1])/inphase[:-2]
        mu = np.median(leadrate_hats)
        stdev = np.std(leadrate_hats)
        ul = mu +4*stdev
        ll = mu -4*stdev
        outlier_removed_ind = np.where((leadrate_hats>ll) & (leadrate_hats<ul))[0] 
        leadhat = np.mean(leadrate_hats[outlier_removed_ind])    
        
        ph_eff = np.array([laghat, leadhat])
        
        #return simtrace[1:]
        return simtrace[1:], ph_eff   