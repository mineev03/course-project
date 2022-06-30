from openpyxl import Workbook

from utils.styles_excel import Styles


class Excel(Styles):
    def __init__(self):
        self.workbook = None
        self.sheet = None

    def create_workbook(self):
        self.workbook = Workbook()
        self.sheet = self.workbook.active

    def set_sheet_title(self, title):
        self.sheet.title = title

    def append_to_sheet(self, data):
        self.sheet.append(data)
