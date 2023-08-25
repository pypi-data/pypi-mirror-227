   
#%% Load imports
import numpy as np
import pandas as pd
from typing import List, Dict, Union, Tuple
import os
from scipy.io import loadmat
# #from matplotlib.ticker import MultipleLocator
# import plotly.graph_objects as go
import traceback
import pickle
import functools
import types
import inspect

#from plots import WaferPlot
#from salsa.helper_functions import exp_fit, template_exception_safeguard, log, log_runtime_class_decorator, merged_td
from salsa.helper_functions import log
from salsa.parameters import Parameters
# from tool_noise import tool_noise
# import new_plots as new_plt
from salsa.data.sequence_substrate_data import SequenceSubstrateData
from salsa.run_metrics import RunMetrics
from salsa.data.metadataloader import MetadataLoader

class TTECData(SequenceSubstrateData):
    '''
    A class for storing TTEC run data
    '''
    def __init__(self, runID: str) -> None:
        super().__init__(runID)
        self.sigmat_filepath: str = ''
        self.truekey_filepath: str = ''
        self.metadata_filepath: str = ''
        self.num_flows: Union[int, None] = None
        self.truekey: np.ndarray = np.empty(0,)
        self.seq_key_front: np.ndarray = np.empty(0,)
        self.seq_key_back: np.ndarray = np.empty(0,)
        return
    
    def __str__(self) -> str:
        return f"TTECData:\n\
            run ID: {self.runID}\n\
            sigmat filepath: {self.sigmat_filepath}\n\
            truekey filepath: {self.truekey_filepath}\n\
            metadata filepath: {self.metadata_filepath}\n\
            sigmat: {self.sigmat.shape}\n\
            XYT: {self.XYT.shape}\n\
            Keys: {self.truekey.shape}\n"
    
    def __repr__(self) -> str:
        return f"TTECData( run ID: {self.runID}, sigmat filepath: {self.sigmat_filepath}, truekey filepath: {self.truekey_filepath}, metadata filepath: \
            {self.metadata_filepath}, sigmat: {self.sigmat.shape}, XYT: {self.XYT.shape}, Keys: {self.truekey.shape})\n"


    def populate_keys(self) -> None:
        stop_index = self.get_min_index_from_sigmat_and_truekeys()
        self.truekey = self.file_data['truekey'][:, :stop_index - 8]
        self.seq_key_front = self.file_data.pop("genomSeqKey_f")[0]
        self.seq_key_back = self.file_data.pop("genomSeqKey_b")[0]
        return
    
    def populate_sigmat(self) -> None:
        stop_index = self.get_min_index_from_sigmat_and_truekeys()
        self.sigmat = self.file_data['sigmat'][:, :stop_index]
        return
    
    def get_min_index_from_sigmat_and_truekeys(self) -> int:
        nflow_sigmat = self.file_data['sigmat'].shape[1]
        nflow_truekey = self.file_data['truekey'].shape[1]
        nflow_target = (np.min([nflow_sigmat, nflow_truekey + 8]) // 4) * 4 # +8 for truekey because of preamble
        return nflow_target
    
    def populate_xyt(self) -> None:
        self.XYT = self.file_data.pop("XYT")
        return
    
    def load(self,
        sigmat_path: str,
        truekey_path: str,
        metadata_path: str,
        num_flows_in: Union[int, None] = None,) -> None:

        #set num_flows attribute
        self.set_template_parameters(num_flows_in)

        #load in appropriate data based on the num_flows field
        try:
            self.file_data = loadmat(metadata_path)
        except FileNotFoundError as e:
            log('exception', str(e))
            raise FileNotFoundError
        except Exception as e:
            #log
            traceback.print_exc()

        self.load_appropriate_sigmat_truekey_columns(sigmat_path, truekey_path)
        self.populate_all_attributes()
        return
    
    def load_appropriate_sigmat_truekey_columns(self,
        sigmat_path: str,
        truekey_path: str,) -> None:

        #get the appropriate columns to load
        sigmat_cols_to_read, truekey_cols_to_read = self.get_cols_to_read_based_on_nflows()

        # load them in
        try:
            sigmat = pd.read_parquet(
                sigmat_path, columns=sigmat_cols_to_read
            ).to_numpy(dtype="float32")
            # num beads x num flows
            truekey = pd.read_parquet(
                truekey_path, columns=truekey_cols_to_read
            ).to_numpy(dtype="int8")

            #save in file_data
            self.file_data['sigmat'] = sigmat
            self.file_data['truekey'] = truekey
            
        except FileNotFoundError as e:
            log("exception", str(e))
        return
    
    def set_template_parameters(self, num_flows_in: Union[int, None] = None,) -> None:
        #load in template parameters
        self.preamble_length = 8
        self.num_flows = num_flows_in
        return
    
    def get_cols_to_read_based_on_nflows(self) -> tuple:
        sigmat_cols_to_read = (
            [f'flow{str(n).rjust(3, "0")}' for n in range(1, self.num_flows)]
            if self.num_flows is not None
            else None
        )

        truekey_cols_to_read = (
            sigmat_cols_to_read[self.preamble_length :]
            if self.num_flows is not None and sigmat_cols_to_read is not None
            else None
        )
        return sigmat_cols_to_read, truekey_cols_to_read

    def populate_all_attributes(self) -> None:
         self.populate_sigmat()
         self.populate_xyt()
         self.populate_metadata(MetadataLoader())
         self.populate_keys()
         pass