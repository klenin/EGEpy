from ...GenBase import DirectInput

import xlsxwriter

import datetime
from calendar import monthrange


class WorkingWithTable(DirectInput):
    class WeatherByHours:
        def __init__(self, problem) -> None:
            self.problem = problem
            self.tempautre_calendar = {
                1:  { 'min': -40.0, 'max':  0.0 },
                2:  { 'min': -35.0, 'max':  5.0 },
                3:  { 'min': -30.0, 'max': 10.0 },
                4:  { 'min': -15.0, 'max': 15.0 },
                5:  { 'min': -10.0, 'max': 30.0 },
                6:  { 'min':   0.0, 'max': 40.0 },
                7:  { 'min':   0.0, 'max': 40.0 },
                8:  { 'min':  -5.0, 'max': 30.0 },
                9:  { 'min': -15.0, 'max': 25.0 },
                10: { 'min': -25.0, 'max': 15.0 },
                11: { 'min': -35.0, 'max':  5.0 },
                12: { 'min': -40.0, 'max':  0.0 },
            }

        def generate(self):
            self.problem.text = self.__get_random_introduction()
            workbook = self.__generate_table()    

        def __get_random_introduction(self) -> str:
            if self.problem.rnd.coin():
                return"""
Откройте файл электронной таблицы, содержащей вещественные числа - результаты ежечасного измерения температуры воздуха на протяжении трёх месяцев.
"""
            else:
                return"""
Электронная таблица содержит результаты ежечасного измерения температуры воздуха на протяжении трёх месяцев.
"""

        def __generate_table(self):
            workbook = xlsxwriter.Workbook('table.xlsx')
            worksheet = workbook.add_worksheet()

            worksheet.set_column('A:A', 15)

            self.__write_time(workbook, worksheet)

            self.start_year = self.problem.rnd.pick([ 2019, 2020, 2021, ])
            self.start_month = self.problem.rnd.in_range(1, 12)
            self.month_count = 3

            self.__write_dates(workbook, worksheet)
            self.__fill_table(workbook, worksheet)

            workbook.close()
            return workbook

        def __write_time(self, workbook, worksheet):
            time_format = workbook.add_format()
            time_format.set_bg_color('yellow')

            for hour in range(24):
                worksheet.write(f"{chr(ord('B') + hour)}1", f"{hour:0>2}:00", time_format)

        def __write_dates(self, workbook, worksheet):
            date_format = workbook.add_format({ 'num_format': 'dd/mm/yyyy' })
            date_format.set_bg_color('yellow')

            date_time = datetime.datetime.strptime(f'{self.start_year}-{self.start_month}-01', '%Y-%m-%d')
            row_number = 2
            for _ in range(self.month_count):
                for _ in range(1, monthrange(date_time.year, date_time.month)[1] + 1):
                    worksheet.write_datetime(f'A{row_number}', date_time, date_format)
                    row_number += 1
                    date_time += datetime.timedelta(days=1)

        def __fill_table(self, workbook, worksheet):
            date_time = datetime.datetime.strptime(f'{self.start_year}-{self.start_month}-01', '%Y-%m-%d')
            row_number = 2
            for _ in range(self.month_count):
                for _ in range(1, monthrange(date_time.year, date_time.month)[1] + 1):
                    

                    row_number += 1
                    date_time += datetime.timedelta(days=1)


    class Geometry:
        pass

    class WeatherByParameters:
        pass

    def generate(self):
        weather_by_hours = self.WeatherByHours(self)
        weather_by_hours.generate()
        return self
