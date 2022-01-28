from EGE.GenBase import EGEError
from EGE.Prog import CallFuncAggregate, make_expr, Op, SynElement, Block
from EGE.Random import Random
from EGE.Utils import aggregate_function

class Field:
    def __init__(self, attr):
        self.name: str = ''
        self.name_alias: str = ''
        if isinstance(attr, dict):
            self.name = attr['name']
            self.name_alias = attr['name_alias']
        else:
            self.name = attr

    def to_lang(self):
        return self.name_alias + '.' + self.name if self.name_alias else self.name

    def __str__(self):
        return self.name

    def __repr__(self):
        if self.name_alias:
            return f"Field({{'name': '{self.name}', 'name_alias': '{self.name_alias}'}})"
        return f"Field('{self.name}')"

    def __eq__(self, other):
        if isinstance(other, str):
            return other == self.name or other == self.name_alias
        elif isinstance(other, Field):
            return other.name == self.name and other.name_alias == self.name_alias
        raise EGEError("Imvalid type to compare with Field!")



class Table:
    def __init__(self, fields: list, **kwargs):
        if fields is None:
            raise EGEError('No fields')

        self.fields: list[Field] = [ self._make_field(i) for i in fields ]
        self.name: str = kwargs['name'] if 'name' in kwargs.keys() else ''
        self.field_index: dict = {}
        self._update_field_index()
        for i in self.fields:
            i.table = self
        self.data: list = []

    def _make_field(self, field):
        return field if isinstance(field, Field) else Field(field)

    def _update_field_index(self):
        for i, key in enumerate(self.fields):
            self.field_index[key.name] = i

    def assign_field_alias(self, alias: str):
       raise NotImplemented()

    def insert_row(self, *fields):
        if len(fields) != len(self.fields):
            EGEError(f'Wrong column count {len(fields)} != {len(self.fields)}')
        self.data.append(list(fields))
        return self

    def insert_rows(self, *rows):
        for fields in rows:
            self.insert_row(*fields)
        return self

    def insert_column(self):
        raise NotImplemented()

    def print_row(self, row):
        raise NotImplemented()

    def print(self):
        raise NotImplemented()

    def count(self):
        return len(self.data)

    def _row_hash(self, row, env=None):
        if env is None:
            env = {}
        for f in self.fields:
            env[f.name] = row[self.field_index[f.name]]
        return env

    def _hash(self):
        env = { '&columns': { str(f): self.column_array(str(f)) for f in self.fields },
                '&': aggregate_function(),
                '&count': self.count() }
        return env

    def select(self, fields, where=None, p=None):
        if not isinstance(fields, list):
            fields = [ fields ]
        for f in fields:
            if not isinstance(f, CallFuncAggregate) and f not in self.fields:
                raise EGEError(f"Table '{self.name}' does not contain field '{f}'!")
        ref, aggr, group, having = 0, 0, 0, 0
        if isinstance(ref, dict):
            ref = p[ref]
            group = p[group]
            having = p[having]

        aggr = list(filter(lambda x: isinstance(x, CallFuncAggregate), fields))
        k = 0
        args = []
        exprs = [ f'expr_{i}' for i in range(1, 4) ]
        for f in fields:
            # TODO this seems to be wrong. Check later
            if not isinstance(f, Field) and hasattr(f, '__call__') and f.__name__ in exprs:
                k += 1
                args.append(f'expr_{k}')
            else:
                args.append(f)
        result = Table(args)
        values = [ f if hasattr(f, '__call__') else make_expr(f) for f in fields ]
        calc_row = lambda x: [ i.run(x) for i in values ]

        tab_where = self.where(where, ref)
        if group:
            raise NotImplemented()
        else:
            ans = []
            env = tab_where._hash()
            for data in tab_where.data:
                ans.append(calc_row(tab_where._row_hash(data, env)))
            result.data = [ ans[0] ] if aggr else ans #TODO check correctness in case if aggr == True

        return result

    def group_by(self):
        raise NotImplemented()

    def where(self, where: Op = None, ref: bool = None):
        """where: Union[callable, None], ref: Union[bool, None]"""
        if where is None:
            return self
        table = Table(self.fields)
        table.data = [ data if ref else data[:] for data in self.data if where.run(self._row_hash(data)) ]
        return table

    def count_where(self, where: Op = None):
        if where is None:
            return self.count()
        res = list(filter(lambda x: where.run(self._row_hash(x)), self.data))
        return len(res)

    def update(self, assigns: Block, where: Op = None):
        data = self.data if where is None else self.where(where, True)
        for row in data:
            row_hash = self._row_hash(row)
            assigns.run(row_hash)
            for f in self.fields:
                row[self._field_index(f.name)] = row_hash[f.name]
        return self

    def delete(self):
        raise NotImplemented()

    def natural_join(self):
        raise NotImplemented()

    def inner_join(self):
        raise NotImplemented()

    def inner_join_expr(self):
        raise NotImplemented()

    def table_html(self):
        raise NotImplemented()

    def fetch_val(self):
        raise NotImplemented()

    #TODO how best to implement getting the random number generator in table methods
    def random_row(self, rnd: Random):
        return rnd.pick(self.data)

    def _field_index(self, field: str):
        """field: Union[int, str]"""
        if isinstance(field, int):
            if 1 <= field <= len(self.fields):
                return field - 1
            else:
                raise EGEError(f"Unknown field {field}")
        if field not in self.field_index.keys():
            raise EGEError(f"Unknown field {field}")
        return self.field_index[field]

    def column_array(self, field):
        """field: Union[int, str]"""
        column_idx = self._field_index(field)
        return [ data[column_idx] for data in self.data ]

    def column_hash(self, field):
        """field: Union[int, str]"""
        column_idx = self._field_index(field)
        r = {}
        for row in self.data:
            if row[column_idx] not in r.keys():
                r[row[column_idx]] = 0
            r[row[column_idx]] += 1
        return r
