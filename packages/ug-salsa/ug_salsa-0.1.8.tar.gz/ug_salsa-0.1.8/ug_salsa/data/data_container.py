import traceback
from abc import ABC, abstractmethod
from typing import Dict

import numpy as np
from scipy.io import loadmat

from salsa.helper_functions import log
from salsa.parameters import Parameters
from salsa.data import MetadataLoadingInterface

class DataContainer(ABC):
    def __init__(self, runID: str) -> None:
        self.params: Parameters = Parameters()
        self.runID: str = runID
        self.file_data: Dict[str, np.ndarray] = {}
        self.mat_filename: str = ''
        return
        
    def empty(self) -> bool:
        return self.file_data == {}

    def load(self, filename: str = '') -> None:
        try:
            self.mat_filename = filename
            self.file_data = loadmat(filename)
        except FileNotFoundError as e:
            log('exception', str(e))
            raise FileNotFoundError
        except Exception as e:
            #log
            traceback.print_exc()
        
        self.populate_all_attributes()
        return
    
    @abstractmethod
    def populate_all_attributes(self) -> None:
        '''
        Populates all the attributes for a given data class
        '''
        pass
    
    def populate_metadata(self, metadata_loader: MetadataLoadingInterface) -> None:
        metadata_loader.load_metadata_from(self.file_data)
        metadata_loader.load_metadata_into(self)
        return
