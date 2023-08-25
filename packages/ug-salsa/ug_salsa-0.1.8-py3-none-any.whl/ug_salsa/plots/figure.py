import plotly.graph_objects as go
from plotly.graph_objs._figure import Figure
import plotly.io as pio
import json 
import os
import re 
#%% figure base class
class Figure(go.Figure):
    
    name: str = 'newplot'
    
    def __init__(self):
        super().__init__()
        self.apply_defaults()
        return

    def apply_defaults(self):
        # layout
        default_layout = {'height': 445,
                          'width': 720,}
        layout_updatable = {key: value for key, value in default_layout.items()
                            if self.layout[key] is None}
        self.update_layout(**layout_updatable, overwrite = False)

        return

    def set_name(self, name: str):
        self.name = name
        return
    
    # def append_to_html(self, interactive = True):
    #     if interactive:
    #         PlotHandler.add_to_html(self)
    #         return
    #     PlotHandler.save_png(self)
    #     return

    # def send_json(self, runID):
    #     name = re.sub("[ -]+", '_', self.name)
    #     os.makedirs(f"{cls.params['save_loc']}/json", exist_ok=True)
    #     filename_base = f"{cls.params['save_loc']}json/{name}"
        
    #     with open(f"{filename_base}.json", 'w+') as file:
    #         json.dump(pio.to_json(self), file)
        
    #     self.write_image(f"{filename_base}.jpeg")
        
    #     with open(f"{cls.params['save_loc']}json/figure_list.txt", 'a+') as json_log:
    #         json_log.write(f"{name}.json\n")
    #         json_log.write(f"{name}.jpeg\n")
            
    #     with open(f"{cls.params['save_loc']}RunID{cls.params['runid']}_uploads_list.txt", 'a+') as file:
    #         file.write(f"json/{name}.json\n")
    #         file.write(f"json/{name}.jpeg\n")        
    #     # requires nexus fix
    #     #plot_json = pio.to_json(self).replace('"', "\\'")
    #     #Nexus.update_metrics(runID, {name: plot_json}, purpose = 'rundmc\\_plots')
    #     return