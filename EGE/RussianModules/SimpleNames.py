import re

simple_names = ['Александр',
                'Алексей',
                'Анатолий',
                'Андрей',
                'Антон',
                'Аркадий',
                'Артём',
                'Борис',
                'Вадим',
                'Василий',
                'Виктор',
                'Виталий',
                'Владимир',
                'Вячеслав',
                'Геннадий',
                'Георгий',
                'Глеб',
                'Григорий',
                'Денис',
                'Дмитрий',
                'Евгений',
                'Егор',
                'Иван',
                'Кирилл',
                'Константин',
                'Леонид',
                'Михаил',
                'Николай',
                'Олег',
                'Петр',
                'Роман',
                'Семён',
                'Сергей',
                'Степан',
                'Тимофей',
                'Федор',
                'Эдуард',
                'Юрий',
                'Яков',
                ]

def genitive(name):
    if re.search('й$', name):
        name = re.sub('й$', 'я', name)
    else:
        name = name + 'а'
    return name
