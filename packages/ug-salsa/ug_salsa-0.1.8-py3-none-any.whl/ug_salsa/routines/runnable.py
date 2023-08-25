from abc import ABC, abstractmethod
from salsa.routines.output_handler import OutputHandler
class Runnable(ABC):

    @abstractmethod
    def run(self):
        pass

    # @abstractmethod
    # def add_table(self):
    #     pass

    # @abstractmethod
    # def add_interactive_plot(self):
    #     pass

    # @abstractmethod
    # def add_noninteractive_plot(self):
    #     pass

    def set_parent(self, routine: OutputHandler):
        self.parent_routine = routine