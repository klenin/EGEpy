alphabet = list('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')
consonants = list('БВГДЖЗЙКЛМНПРСТФХЦЧШЩ')
vowels = list('АЕЁИОУЫЭЮЯ')

def join_comma_and(arr: list):
    if len(arr) > 1:
        return ', '.join(arr[0: -2]) + ' и ' + arr[-1]
    else:
        return arr[0]

def different(rnd, items, count):
    cache = {}
    for i in items:
        if i in cache:
            cache[i[0]].append(i)
        else:
            cache[i[0]] = [i]
    return [rnd.pick(cache[i]) for i in rnd.pick_n(count, cache.keys())]
