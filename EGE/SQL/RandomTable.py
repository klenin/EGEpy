from EGE.Random import Random

class BaseTable:
    columns: list
    def __init__(self, rnd: Random, col_count, row_count, name):
        self.rnd = rnd
        self.columns = self.get_columns()
        self.fields = [
            self.columns[0],
            rnd.pick_n(
                col_count - 1,
                self.columns[1:len(self.columns)]
            )
        ]
        row_sources = [ row for row in self.get_rows_array()
                        if len(row) >= row_count ]
        self.rows = rnd.pick_n(row_count, row_sources)


    def get_columns(self) -> list:
        return []

    def get_rows_array(self):
        pass

class Products(BaseTable):
    pass

class Jobs(BaseTable):
    pass

class SalesMonth(BaseTable):
    pass

class Cities(BaseTable):
    pass

class People(BaseTable):
    pass

class Subjects(BaseTable):
    pass

class Marks(BaseTable):
    pass

class ParticipantsMonth(BaseTable):
    pass

def ok_table(table: BaseTable, rows, cols):
    t_cols = table.get_columns()
    t_rows = table.get_rows_array()
    return t_cols >= cols and any([len(t_rows) > rows])

def pick(rnd: Random, *args):
    return rnd.pick([
        lambda *args2: Products(args2),
        lambda *args2: Jobs(args2),
        lambda *args2: SalesMonth(args2),
        lambda *args2: Cities(args2),
        lambda *args2: People(args2),
        lambda *args2: Subjects(args2),
        lambda *args2: Marks(args2),
        lambda *args2: ParticipantsMonth(args2),
    ])(args)

def create_table(rnd: Random, rows: int, columns: int):
    table = pick(rnd, rows, columns)
    return table
