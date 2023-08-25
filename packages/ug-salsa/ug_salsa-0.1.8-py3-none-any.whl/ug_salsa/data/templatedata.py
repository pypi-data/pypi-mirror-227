#%% Load imports
import numpy as np
from salsa.data.sequence_substrate_data import SequenceSubstrateData
from salsa.data.metadataloader import MetadataLoader

class TemplateData(SequenceSubstrateData):
    '''
    A class for storing Template run data
    '''
    def __init__(self,runID: str) -> None:
        super().__init__(runID)
        self.flow_order: np.ndarray = np.empty(0,)
        self.flow_type: np.ndarray = np.empty(0,)
        self.total_found: np.ndarray = np.empty(0,)
        self.template_sq: np.ndarray = np.empty(0,)
        self.template_tk: np.ndarray = np.empty(0,)
        self.name: str = ''
        return
    
    def __str__(self) -> str:
        return f"TemplateData:\n\
            run ID: {self.runID}\n\
            template name: {self.name}\n\
            file name: {self.mat_filename}\n\
            sigmat: {self.sigmat.shape}\n\
            XYT: {self.XYT.shape}\n"

    def __repr__(self) -> str:
        return f"TemplateData( run ID: {self.runID}, template name: {self.name}, file name: {self.mat_filename}, sigmat: {self.sigmat.shape}, XYT: {self.XYT.shape})\n"
    
    def populate_sigmat(self) -> None:
        self.name = self.file_data.pop('temp_name').flatten()[0]
        self.sigmat = self.file_data.pop('SigMat')
        return
    
    def populate_xyt(self) -> None:
        self.XYT = self.file_data.pop('XYT')
        return
    
    def populate_all_attributes(self) -> None:
        self.populate_sigmat()
        self.populate_keys()
        self.populate_xyt()
        self.populate_flow_data()
        self.populate_metadata(MetadataLoader())
        return
    
    def populate_flow_data(self) -> None:
        self.flow_order = self.file_data.pop('flow_order')[0]
        self.flow_type = self.file_data.pop('flow_type')[0]
        return
    
    def populate_keys(self) -> None:
        self.template_tk = self.file_data.pop('template_tk').flatten()
        self.template_sq  = self.file_data.pop('template_sq')[0]
        return
