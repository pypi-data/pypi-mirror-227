import numpy as np
import pandas as pd
from typing import Dict

from salsa.data.metadata_loading import MetadataLoadingInterface
from salsa.data.data_container import DataContainer
from salsa.parameters import Parameters

class MetadataLoader(MetadataLoadingInterface):
    '''
    A base class for storing data that posesses metadata
    '''
    def __init__(self) -> None:
        self.params: Parameters = Parameters()
        self.TileID: np.ndarray = np.empty((0,))
        self.TileOffset: np.ndarray = np.empty((0,))
        self.FullBeadsPerTile: np.ndarray = np.empty((0,))
        self.Ring: np.ndarray = np.empty((0,))
        
        self.radii: np.ndarray = np.empty((0,))
        self.theta: np.ndarray = np.empty((0,))
        self.nbeads: int = 0
        self.ntiles:int = 0
        self.tiles: np.ndarray = np.empty((0,))
        
        self.tile_width: int = 0
        self.tile_height: int = 0
        self.tile_size: float = 0.
        
        self.total_found: int = 0
        self.low_loading_inds: np.ndarray = np.empty((0,))
        return

    def empty(self) -> bool:
        return self.file_data == {}
    
    def load_metadata_from(self, source: Dict[str, np.ndarray]):
        self.file_data = source
        return
    
    def load_metadata_into(self, destination: DataContainer) -> None:
        '''
        Populates the SubstrateData's metadata like tile size, tile number, radii, etc
        '''
        metadata_df = self.read_metadata_csv()
        self.set_metadata_attributes(metadata_df)
        destination.__dict__.update(self.__dict__)
        return

    def read_metadata_csv(self) -> pd.DataFrame:
        columns = self.get_metadata_column_labels()
        tilesDescription = pd.DataFrame(data = self.file_data.pop('tilesDescription'), columns = [col.strip() for col in columns])
        return tilesDescription
    
    def get_metadata_column_labels(self) -> np.ndarray:
        if self.file_data['tilesDescription_columns'].shape[0] == 1:
            columns = np.hstack(self.file_data.pop("tilesDescription_columns").tolist()).flatten()
        else:
            columns = self.file_data.pop("tilesDescription_columns")
        return columns
    
    def set_metadata_attributes(self, tilesDescription: pd.DataFrame) -> None:
        self.TileID = tilesDescription['TileID'].astype(int).to_numpy()
        self.TileOffset = tilesDescription['TileOffset'].astype(int).to_numpy()
        self.FullBeadsPerTile = tilesDescription['FullBeadsPerTile'].astype(int).to_numpy()
        self.Ring = tilesDescription['Ring'].astype(int).to_numpy()
        
        self.radii = tilesDescription['Radius'].to_numpy()
        self.theta = np.modf(tilesDescription['Theta'].to_numpy())[0]*2*np.pi # in radians
        self.nbeads = np.sum(self.FullBeadsPerTile)
        self.ntiles = tilesDescription.shape[0]
        self.tiles = tilesDescription["TileID"].to_numpy().astype(float).astype(int)

        self.populate_metadata_total_found()
        self.populate_metadata_photometry()
        self.filter_low_loading_tiles(tilesDescription)
        return
    
    def populate_metadata_total_found(self) -> None:
        self.total_found = self.file_data.pop('total_found').flatten()[0]
        return
    
    def populate_metadata_photometry(self) -> None:
        self.tile_width = int(self.file_data.pop('tile_width')[0].flatten()[0])
        self.tile_height = int(self.file_data.pop('tile_height')[0].flatten()[0])
        self.tile_size = float(self.file_data.pop('tile_size')[0].flatten()[0])
        return
    
    def filter_low_loading_tiles(self, tilesDescription: pd.DataFrame) -> None:
        fullDensity = (tilesDescription['FullBeadsPerTile'].to_numpy()/self.tile_size).flatten()
        self.low_loading_inds = np.where(fullDensity < self.params['min_bead_density'])[0]
        return
