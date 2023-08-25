# Load imports
import numpy as np
from salsa.data.data_container import DataContainer
from salsa.data.metadataloader import MetadataLoader

class FWHMData(DataContainer):
    def __init__(self, runID: str) -> None:
        super().__init__(runID)
        self.fwhmMap: np.ndarray = np.empty(0,)
        self.mat_filename: str = ''
        return
    
    def __str__(self) -> str:
        return f"FWHM Data:\n\
            run ID: {self.runID}\n\
            file name: {self.mat_filename}\n"
    
    def __repr__(self) -> str:
        return f"FWHMData(run ID: {self.runID}, file name: {self.mat_filename}, fwhmMap: {self.fwhmMap})\n"
    
    def populate_all_attributes(self) -> None:
        self.populate_metadata(MetadataLoader())
        self.populate_fwhmMap()
        return
    def populate_fwhmMap(self) -> None:
        self.fwhmMap = self.file_data["fwhmMap"] # shape is (flow, tile, FOV)
        return