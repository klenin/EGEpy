
from functools import partial

def _remove_trailing_underline(s):
    return s[:-1] if s[-1] == '_' else s

def attrs_str(**kwargs):
    return ''.join(
        f" {_remove_trailing_underline(k)}=\"{v}\"" for k, v in sorted(kwargs.items()))

def open_tag(tag, attrs = {}, rest = '>'):
    return '<' + tag + attrs_str(**attrs) + rest

def tag(tag, body = None, **attrs):
    if hasattr(body, '__iter__'):
        body = ''.join(body)
    return open_tag(tag, attrs, f">{body}</{tag}>" if body else '/>')

def close_tag(tag):
    return f"</{tag}>"

def _build():
    for fn in ['div', 'li', 'ol']:
        globals()[fn] = partial(tag, fn)
_build()

def global_head():
    return """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
   "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="ru" xml:lang="ru">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <title>EGE</title>
  <style type="text/css">
    li.correct { color: #F02020; }
    div.q { border-bottom: 1px solid black; }
    div.code { margin: 3px 0 2px 15px; }
    div.code code { display: inline-block; padding: 4px; border: 1px dotted #6060F0; }
    tt { background-color: #F0FFF0; padding: 1px; }
  </style>
</head>
"""

def make_question_html(q):
    result = ''.join(
        (li(v, class_='correct') if q.correct == i else li(v)) + "\n" for i, v in enumerate(q.variants))
    return div(f"{q.text}\n" + ol("\n" + result) + "\n", class_='q') + "\n"

def make_html(questions):
    return global_head() + tag('body', map(make_question_html, questions))
