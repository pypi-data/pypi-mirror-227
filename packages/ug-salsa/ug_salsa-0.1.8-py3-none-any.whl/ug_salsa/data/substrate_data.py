from abc import abstractmethod

import numpy as np

from salsa.data import DataContainer


class SubstrateData(DataContainer):
    '''
    A base class for storing data of a type of substrate in a sequencing run (RefBeads, TTEC, Templates, etc)
    '''
    def __init__(self,runID: str) -> None:
        super().__init__(runID)
        self.sigmat: np.ndarray = np.empty(0,)
        self.XYT: np.ndarray = np.empty(0,)
        return
    
    @abstractmethod
    def populate_sigmat(self) -> None:
        '''
        Populates the signal strength attributes of the data
        '''
        pass

    @abstractmethod
    def populate_xyt(self) -> None:
        '''
        Populates the XYT position attributes of the data
        '''
        pass
