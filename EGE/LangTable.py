from Prog import SynElement, lang_names
from Html import row_n, cdata, table

def lang_row(prog: SynElement, row: list):
    wrap_in_pre_tag = lambda lang_name: '<pre>' + cdata(prog.to_lang_named(lang_name)) + '</pre>'
    return row_n('th', list(map(lang_names, row))) + row_n('td', list(map(wrap_in_pre_tag, row)))

def unpre(string: str):
    return f']]></pre>{string}<pre><![CDATA['

def table(prog: SynElement, rows: list):
    raw = ''.join(list(map(lambda row: lang_row(prog, row), rows)))
    return table(f'\n{raw}', { 'border': 1}) + "\n"
