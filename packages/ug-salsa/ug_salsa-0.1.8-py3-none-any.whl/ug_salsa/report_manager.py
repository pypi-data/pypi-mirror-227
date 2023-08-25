from salsa.report import Report

class ReportManager:
    def __new__(cls): #singleton functionality
        if not hasattr(cls, 'instance'):
            cls.instance = super(ReportManager, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.report_dict: dict[str, Report] = {}

    def _add_report(self, file_path: str = '') -> None:
        self.report_dict[file_path] = Report(file_path)

    def get_report(self, file_path: str) -> Report:
        if file_path in self.report_dict.keys():
            return self.report_dict[file_path]
        else:
            self._add_report(file_path)
            return self.report_dict[file_path]

        