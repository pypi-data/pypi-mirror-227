from abc import ABC, abstractmethod

class OutputHandler(ABC):

    @abstractmethod
    def add_table(self, table, title, **kwargs):
        pass

    @abstractmethod
    def add_interactive_plot(self, fig):
        pass

    @abstractmethod
    def add_noninteractive_plot(self, fig, size, newline):
        pass

    @abstractmethod
    def set_tab_sections(self, names):
        pass

    @abstractmethod
    def new_section(self, name):
        pass