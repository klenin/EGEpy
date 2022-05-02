import re

districts = [ 'Октябрьский',
              'Первомайский',
              'Заречный'
              ]


def districts_genetive(district):
    if re.search('ий$', district):
        district = re.sub('ий$', 'ого', district)
    elif re.search('ый$', district):
        district = re.sub('ый$', 'ого', district)
    return district
