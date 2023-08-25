import numpy as np

from salsa.data.metadataloader import MetadataLoader
from salsa.helper_functions import log
from salsa.data import SubstrateData

class RefBeadData(SubstrateData):
    '''
    A class for storing RefBead run data
    '''
    def __init__(self, runID: str) -> None:
        super().__init__(runID)
        self.lost_sigmat: np.ndarray = np.empty(0,)
        self.lost_XYT: np.ndarray = np.empty(0,)
        self.mean_sig_per_flow: np.ndarray = np.empty(0,)
        return
    
    def __str__(self) -> str:
        return f"RefBeadData:\n\
            run ID: {self.runID}\n\
            file name: {self.mat_filename}\n\
            sigmat: {self.sigmat.shape}\n\
            XYT: {self.XYT.shape}\n"
            
    def __repr__(self) -> str:
        return f"RefBeadData(run ID: {self.runID}, file name: {self.mat_filename}\n, sigmat: {self.sigmat.shape}, XYT: {self.XYT.shape})\n"
    
    def populate_sigmat(self) -> None:
        self.sigmat = self.file_data.pop('ref_SigMat')
        self.lost_sigmat = self.file_data.pop('ref_lost_SigMat')
        return
    
    def populate_xyt(self) -> None:
        self.XYT = self.file_data.pop('ref_XYT')
        self.lost_XYT = self.file_data.pop('ref_lost_XYT')
        return
    
    def populate_all_attributes(self) -> None:
        self.populate_sigmat()
        self.populate_xyt()
        self.populate_metadata(MetadataLoader())
        self.populate_mean_sig_per_flow()
        self.populate_std_sig_per_flow()
        return
    
    def populate_mean_sig_per_flow(self) -> None:
        '''
        Populates the mean signal per flow field of the RefBeadData class
        '''
        # new addition as of 1.2.0.0
        try:
              self.mean_sig_per_flow = self.file_data.pop('mean_sig_per_flow').flatten()
        except:
              log('warning', f'No mean signal per flow found for runID {self.runID}. This feature was added as of version 1.2.0.0')
              self.mean_sig_per_flow = np.empty(0,)
        return
    
    def populate_std_sig_per_flow(self) -> None:
        '''
        Populates the mean signal per flow field of the RefBeadData class
        '''
        # new addition as of 1.2.0.0
        try:
              self.std_sig_per_flow = self.file_data.pop('std_sig_per_flow').flatten()
        except:
              log('warning', f'No std signal per flow found for runID {self.runID}. This feature was added as of version 1.2.0.0')
              self.std_sig_per_flow = np.empty(0,)
        return

    
        