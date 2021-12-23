import Html

from Prog import SynElement, lang_names
from Html import row_n, cdata

def lang_row(prog: SynElement, row: list):
    wrap_in_pre_tag = lambda lang_name: '<pre>' + cdata(prog.to_lang_named(lang_name)) + '</pre>'
    return row_n('th', [ lang_names(x) for x in row ]) + row_n('td', [ wrap_in_pre_tag(x) for x in row ])

def unpre(string: str):
    return f']]></pre>{string}<pre><![CDATA['

def table(prog: SynElement, rows: list):
    raw = ''.join([ lang_row(prog, row) for row in rows ])
    return Html.table(body=f'\n{raw}', border=1) + "\n"
