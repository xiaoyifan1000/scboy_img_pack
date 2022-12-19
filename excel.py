import openpyxl
import os
import main

EXCEL_Version = "1.2v"


@main.log_record
class EXCEL:

    def __init__(self):
        self.save_ = f"{main.SAVE_FILE}/img/scboy_href.xlsx"
        self.excel = openpyxl.Workbook()
        self.temp_sheet = self.excel.active

    def write_in(self):
        sql = main.SQlScboy()
        out_list = sql.select_all()
        out_list.reverse()
        for a in out_list:
            self.temp_sheet.append(list(a))
        self.excel.save(self.save_)


if __name__ == '__main__':
    main.SAVE_FILE = '.'
    ex = EXCEL()
    ex.write_in()




