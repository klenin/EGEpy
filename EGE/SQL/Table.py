from ..GenBase import EGEError

class Field:
    name: str
    name_alias: str

    def __int__(self, attr):
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
        return Field(field)





