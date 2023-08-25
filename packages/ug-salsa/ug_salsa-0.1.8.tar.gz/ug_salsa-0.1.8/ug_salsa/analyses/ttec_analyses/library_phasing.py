from salsa.data.ttecdata import TTECData
from salsa.analyses.ttec_analyses import TTECAnalysis
from typing import Dict
import numpy as np
import pandas as pd
import os
import salsa.plots.new_plots as new_plt
from salsa.data import *
import plotly.graph_objects as go

class LibraryPhasing(TTECAnalysis):
    def __init__(self, data: TTECData) -> None:
        super().__init__(data)

    def preprocess_data(self) -> None:
        return

    def analyze_data(self) -> None:
        return

    def report_data(self) -> None:
        pass

    def plot_data(self) -> None:
        return