from salsa.routines.init__ import Runnable
import salsa.plots.new_plots as new_plt
class NewSection(Runnable):
    
    def __init__(self, section_name: str = ""):
        self.section_name = section_name
        return
    
    def run(self):
        self.parent_routine.new_section(self.section_name)
        return