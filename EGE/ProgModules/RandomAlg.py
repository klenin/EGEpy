from ..Prog import make_expr

def big_o(arg_code_block):
    return '<i>O</i>(' + to_logic(arg_code_block) + ')'

def pow(number, power):
    return number if str(power) == '1' else [ '**', number, power, ] 

def monomial(factor: str, coef: str, power: str) -> list:
    """Return code block of ax^y statement"""
    if str(power) == '0':
        return coef
    pow_block = pow(factor, power)
    return pow_block if str(coef) == '1' else [ '*', coef, pow_block, ]

def to_logic(code_block):
    return make_expr(code_block).to_lang_named('Logic', { 'html': True })
