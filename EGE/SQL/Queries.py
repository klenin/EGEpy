from abc import ABC, abstractmethod

import EGE.Html as html
from EGE.GenBase import EGEError
from EGE.SQL.Table import Table, Field
from EGE.Prog import SynElement, Block

class Query(ABC):
    def __init__(self, table, *,
                 where: SynElement = None,
                 having: SynElement = None,
                 group_by: list[SynElement] = None):
        """table: Union[Table, str]"""
        if table is None:
            raise EGEError('Table is none!')

        self.table = table if isinstance(table, Table) else None
        self.table_name = table.name if isinstance(table, Table) else table

        self.where: SynElement = where
        self.having: SynElement = having
        self.group_by: list[SynElement] = group_by

    @abstractmethod
    def text(self, opts: dict):
        """opts: dict[str, Any]"""
        pass

    @abstractmethod
    def run(self):
        pass

    def text_html(self):
        return self.text({ 'html': 1 })

    def text_html_tt(self):
        return html.tag('tt', self.text({ 'html': 1 }))

    def _field_list_sql(self, fields: list, opts: dict):
        """
        fields: list[SynElement | str]
        opts: dict[str, Any]
        """
        return ', '.join([ f.to_lang_named('SQL', opts)
                           if issubclass(type(f), SynElement) else f
                           for f in fields ])

    def where_sql(self, opts: dict):
        return f"WHERE {self.where.to_lang_named('SQL', opts)}" if self.where else ''

    def having_sql(self, opts: dict):
        return f"HAVING {self.having.to_lang_named('SQL', opts)}" if self.having else ''

    def group_by_sql(self, opts: dict):
        return f"GROUP BY {self._field_list_sql(self.group_by, opts)}" if self.group_by else ''

    def _maybe_run(self):
        with getattr(self, 'run', None) as run:
            if callable(run):
                return run()
        return self

class Update(Query):
    def __init__(self, table, assigns: Block, *, where: SynElement = None):
        if assigns is None:
            raise EGEError('Assigns is none!')
        super(Update, self).__init__(table, where=where)
        self.assigns: Block = assigns
    
    def run(self):
        self.table.update(self.assigns, self.where)
        # TODO check if need return table

    def text(self, opts: dict):
        """opts: dict[str, Any]"""
        assigns = self.assigns.to_lang_named('SQL')
        where_sql = self.where_sql(opts)
        if where_sql:
            return f"UPDATE {self.table_name} SET {assigns} {where_sql}"
        else:
            return f"UPDATE {self.table_name} SET {assigns}"
