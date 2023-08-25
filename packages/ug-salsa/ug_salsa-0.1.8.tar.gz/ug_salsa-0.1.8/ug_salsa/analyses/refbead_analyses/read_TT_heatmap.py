from salsa.data import RefBeadData
from salsa.analyses.refbead_analyses.refbead_analysis import RefBeadAnalysis

from salsa.helper_functions import log
import salsa.plots.new_plots as new_plt
import shutil

class ReadTTHeatmap(RefBeadAnalysis):
    
    def __init__(self, data: RefBeadData) -> None:
        super().__init__(data)
        return
    
    def report_data(self) -> None:
        return
    
    def plot_data(self) -> None:
        log("info", "Including TT Heatmap")
        try:
                self.read_TT_heatmap()
        except Exception as e:
                log("warning", f"Error reading TT heatmap: {e}")
        return
    
    def read_TT_heatmap(self):
            heatmap_path = f"{self.params['base_out']}{self.runID}_TTheatmap.png"
            dest = f"{self.params['save_loc']}json/RunID{self.runID}_TT_HeatMap.png"
            new_plt.PlotHandler.add_png(heatmap_path)
            shutil.copy(heatmap_path, dest)
            with open(f"{self.params['save_loc']}RunID{self.params['runid']}_uploads_list.txt", 'a+') as file:
                  file.write(f"json/RunID{self.runID}_TT_HeatMap.png\n")
            return
