from typing import Dict, Any
from run_metrics import RunMetrics
from collections import UserDict

class MetricManager(UserDict):
    
    _run_metrics: Dict[str, RunMetrics] = {}
    
    def __init__(self) -> None:
        self.data = self._run_metrics
        return
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance: MetricManager = super(RunMetrics, cls).__new__(cls)
        return cls.instance
    
    def create_run_if_not_exists(self, runID: str) -> RunMetrics:
        if runID in self._run_metrics:
            return self._run_metrics[runID]
        run_metric = RunMetrics(runID)
        self._run_metrics[runID] = run_metric
        return run_metric
    
    def add(self, runID: str, key: Any, value: Any):
        run_metric = self.create_run_if_not_exists(runID)
        run_metric.add(key, value)
        return
    
    def update_report(self, runID: str, key: Any, value: Any):
        run_metric = self.create_run_if_not_exists(runID)
        run_metric.update_report(key, value)
        
    def to_csv(self, runID: str, file_path: str, *args, **kwargs):
        run_metric = self.create_run_if_not_exists(runID)
        run_metric.to_csv(file_path, *args, **kwargs)