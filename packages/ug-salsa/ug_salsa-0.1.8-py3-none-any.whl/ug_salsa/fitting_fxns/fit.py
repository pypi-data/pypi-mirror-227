import numpy as np
from abc import ABC, abstractmethod


class Fit(ABC):

    def __init__(self) -> None:
        return

    @abstractmethod
    def fitting_fxn(self) -> None:
        return

    @abstractmethod
    def fit(self) -> None:
        return
    
    @abstractmethod
    def goodness_of_fit(self):
        return