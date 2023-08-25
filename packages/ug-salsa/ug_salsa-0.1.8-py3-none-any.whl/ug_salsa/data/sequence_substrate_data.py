from abc import abstractmethod
from salsa.data.substrate_data import SubstrateData

class SequenceSubstrateData(SubstrateData):

    def __init__(self, runID: str) -> None:
        super().__init__(runID)

    @abstractmethod
    def populate_keys(self) -> None:
        '''
        Populates the sequencing keys attributes of the data
        '''
        pass