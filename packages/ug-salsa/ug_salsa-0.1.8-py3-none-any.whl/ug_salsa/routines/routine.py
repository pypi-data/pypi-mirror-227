from salsa.routines.init__ import Runnable
from salsa.report import Report
from salsa.plots.figure import Figure
from salsa.routines.output_handler import OutputHandler
from typing import Tuple, Any, List
import pandas as pd

class Routine(Runnable, OutputHandler):
    
    def __init__(self):
        self.routines: list[Runnable] = []
        self.reports: list[Report] = []
        self.parent_routine: OutputHandler = None
        return
    
    def __str__(self) -> str:
        result = "="*10 + "\n"
        result += "This routine's report list:\n\n"
        for report in self.reports:
            result += report.__str__() + "\n"
        if self.routines:
            result += "This routine's subroutines/analyses:\n"
            for routine in self.routines:
                result += routine.__str__() + "\n"
        result += "="*10 + "\n"
        return result

    def run(self) -> None:
        for runnable in self.routines:
            runnable.run()

        #Once a routine has finished all its subroutines and analyses, end html
        for report in self.reports:
            report.end_document()
        return
    
    def append(self, runnable_obj) -> None:
        if isinstance(runnable_obj, Runnable):
            self.routines.append(runnable_obj)
            runnable_obj.set_parent(self)
        else:
            raise ValueError("The object must implement the Runnable interface")
        return
    
    def pop(self, index: int = -1) -> Runnable:
        '''
            Remove and return runnable at position index of routines list, default -1
        '''
        return self.routines.pop(index)
    

    def add_report(self, report: Report):
        self.reports.append(report)
        report.start_document()
        report.add_sam_header()

    def add_table(self,  table: pd.DataFrame, title: str, **kwargs) -> None:
        for report in self.reports:
            report.add_table(table, title, **kwargs)
        return

    def add_interactive_plot(self, fig: Figure) -> None:
      # method changed to take routine as input
      # if routine is not None | EmptyRoutine:
      #    for report_manager in routine.reports:
      #        report_manager.add_to_html(self)
        for report in self.reports:
            report.add_to_html(fig)
        if self.parent_routine:
             self.parent_routine.add_interactive_plot(fig)   
        return
    
    def add_noninteractive_plot(self, fig: Figure, size: Tuple[Any, Any] = (None,None), newline: bool = True) -> None:
        for report in self.reports:
            report.save_png(fig, size, newline)
        if self.parent_routine:
            self.parent_routine.add_noninteractive_plot(fig)   
        return       

    def set_tab_sections(self, names: List[str]):
        for report in self.reports:
            report.set_tab_sections(names)
        if self.parent_routine:
            self.parent_routine.set_tab_sections(names)

    def new_section(self, name: str):
        for report in self.reports:
            report.start_tab(name)
