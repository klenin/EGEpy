from . import Html as html

def start(viewBox: list):
    return html.open_tag('svg', {
        'xmlns': 'http://www.w3.org/2000/svg',
        'version': '1.1',
        'viewBox': ' '.join(viewBox),
        'preserveAspectRatio': 'none meet'
    }) + '\n'

def end():
    return '</svg>\n'

def figure(tag: str, **kwargs):
    return html.tag(tag, None, **kwargs) + '\n'

def text_tag(tag: str, text, **kwargs):
    if isinstance(text, list):
        text = ''.join(text)
    return html.tag(tag, text, **kwargs) + '\n'

def line(**kwargs):
    return figure('line', **kwargs)

def circle(**kwargs):
    return figure('circle', **kwargs)

def rect(**kwargs):
    return figure('rect', **kwargs)

def path(**kwargs):
    return figure('path', **kwargs)

def text(text, **kwargs):
    return text_tag('text', text, **kwargs)

def tspan(text, **kwargs):
    return text_tag('tspan', text, **kwargs)

def g(text, **kwargs):
    return text_tag('g', text, **kwargs)

def pattern(text, **kwargs):
    return text_tag('pattern', text, **kwargs)

def marker(text, **kwargs):
    return text_tag('marker', text, **kwargs)

def defs(text, **kwargs):
    return text_tag('defs', text, **kwargs)

