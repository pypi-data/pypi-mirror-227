from salsa.analyses.analysis import Analysis
from salsa.data.fwhmdata import FWHMData
import numpy as np
from typing import Tuple
import pandas as pd

class FWHMMetricsTable(Analysis):
    def __init__(self, data: FWHMData) -> None:
        super().__init__(data)
    
    def analyze_data(self):
        self.fwhm_std = self.calculate_fwhm_std()
        self.q1, self.q50, self.q99, self.flow_range = self.calculate_fwhm_quantile_metrics()
        self.fov_range = self.calculate_fwhm_range()
        return
    
    def calculate_fwhm_range(self) -> np.float64:
        fov_per_flow = np.nanmean(self.data.fwhmMap, axis = (0,1))
        fwhm_range = np.nanmax(fov_per_flow) - np.nanmin(fov_per_flow)
        self.metrics.add("opt_fwhm_fov_range_um", fwhm_range)
        return fwhm_range
    
    def calculate_fwhm_quantile_metrics(self) -> Tuple[np.float64, np.float64, np.float64, np.float64]:
        fwhm_per_flow = np.nanmean(self.data.fwhmMap, axis = (1,2))
        quantile_1 = np.nanquantile(fwhm_per_flow, 0.01)
        quantile_50 = np.nanquantile(fwhm_per_flow, 0.5)
        quantile_99 = np.nanquantile(fwhm_per_flow, 0.99)
        flow_range = quantile_99 - quantile_1
        self.metrics.add("opt_fwhm_1_quantile_um", quantile_1)
        self.metrics.add("opt_fwhm_50_quantile_um", quantile_50)
        self.metrics.add("opt_fwhm_99_quantile_um", quantile_99)
        self.metrics.add("opt_fwhm_flow_range_um", flow_range)
        return quantile_1, quantile_50, quantile_99, flow_range
    
    def calculate_fwhm_std(self) -> np.float64:
        fwhm_per_flow = np.nanmean(self.data.fwhmMap, axis = (1,2))
        fwhm_std = np.nanstd(fwhm_per_flow)
        self.metrics.add("opt_fwhm_std_um", fwhm_std)
        return fwhm_std
    
    def report_data(self) -> None:
        names_col = ["FWHM StDev (over flows)",
                "1st Quantile (over flows)",
                "50th Quantile (over flows)",
                "99th Quantile (over flows)",
                "FWHM Range (over flows)",
                "FWHM Range (over FOV)",
                ]
        value_col = ['%.3f' % self.fwhm_std,
                        '%.3f' % self.q1,
                        '%.3f' % self.q50,
                        '%.3f' % self.q99,
                        '%.3f' % self.flow_range,
                        '%.3f' % self.fov_range,]
        metrics_df = pd.DataFrame()
        metrics_df["Metric Name"] = names_col
        metrics_df["Value (um)"] = value_col
        self.table = metrics_df
        self.report_title = f"FWHM Metrics - {self.runID}"
        return 
