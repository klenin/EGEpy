from ..GenBase import EGEError
from ..Prog import CallFuncAggregate
from ..Utils import aggregate_function

class Field:
    name: str
    name_alias: str

    def __init__(self, attr):
        if isinstance(attr, dict):
            self.name = attr['name']
            self.name = attr['name_alias']
        else:
            self.name = attr

    def to_lang(self):
        return self.name_alias + '.' + self.name if self.name_alias else self.name

class Table:
    name: list
    fields: list
    data: list = []
    field_index: dict = {}

    def __int__(self, fields: list, ):
        if not fields:
            raise EGEError('No fields')

        self.fields = [ self._make_field(i) for i in fields ]
        self._update_field_index()
        for i in self.fields:
            i.table = self

    def _make_field(self, field):
        return field if isinstance(field, Field) else Field(field)

    def _update_field_index(self):
        for i, key in enumerate(self.fields):
            self.field_index[i] = i

    def fields(self):
        return self.fields

    def insert_row(self, fields):
        if len(fields) != len(self.fields):
            EGEError(f'Wrong column count {len(fields)} != {len(self.fields)}')
        self.data.append(fields)
        return self

    def _hash(self):
        env = {}
        env['&columns'] =  +{ map { $_ => $self->column_array($_) } @{$self->{fields}} };
        env['&'] = +{ map { $_ => 'EGE::SQL::Table::Aggregate::' . $_ } aggregate_function };
        env['&count'] = self.count()
        return env

    def select(self, fields, where, p):
        ref, aggr, group, having = 0, 0, 0, 0
        if isinstance(ref, dict):
            ref = p[ref]
            group = p[group]
            having = p[having]

        aggr = list(filter(lambda x: isinstance(x, CallFuncAggregate), fields))
        k = 0

        result = Table([ map { not isinstance(i, Field) and ref $_ ? 'expr_' . ++$k : $_ } @$fields ]);

        values = map { ref $_ ? $_ : make_expr($_) } @$fields
        calc_row = lambda x: [ i.run(x) for i in values ]

        tab_where = self.where(where, ref)
        if group:
            result[data] = tab_where.group_by(calc_row, group, having)
        else:
            ans = []
            env = tab_where._hash()
            for i in tab_where[data]:
                ans.append([ calc_row(tab_where._row_hash(i, env)) ])
            result[data] = [ ans[0] ] if aggr else [ ans ]

        return result
