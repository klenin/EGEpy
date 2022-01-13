from re import search

def base_to_dec(base: int, number: str):
    ans = 0
    for c in number:
        if search(r'[0-9]', c):
            t = ord('0')
        elif search(r'[a-z]', c):
            t = ord('a') - 10
        elif search(r'[A-Z]', c):
            t = ord('A') - 10
        else:
            raise ValueError()
        digit = ord(c) - t
        if digit >= base:
            raise ValueError()
        ans = ans * base + digit
    return ans

def dec_to_base(base: int, number: int):
    if not number:
        return '0'
    n = number
    ans = ''
    while n:
        digit = n % base
        if digit > 9:
            digit = chr(ord('A') + digit - 10)
        ans = str(digit) + ans
        n = n // base
    return ans

