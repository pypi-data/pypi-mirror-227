from abc import ABC, abstractmethod
from typing import Dict

import numpy as np


class MetadataLoadingInterface(ABC):
    
    file_data: Dict[str, np.ndarray] = {}
    
    @abstractmethod
    def load_metadata_from(self, source: Dict[str, np.ndarray]):
        return
    
    @abstractmethod
    def load_metadata_into(self, destination: "DataContainer"):
        return