from dataclasses import dataclass


@dataclass
class Prods:
    type: str
    department: str
    name: str
    measurement: str


products = [
    Prods(type="milk", department="Молоко", name="Молоко ультрапастеризованное", measurement="литр"),
    Prods(type="eco", department="Молоко", name="Молоко безлактозное", measurement="литр"),
    Prods(type="milk", department="Молоко", name="Молоко детское с 8 месяцев", measurement="литр"),
    Prods(type="milk", department="Молоко", name="Кефир 3,2%", measurement="литр"),
    Prods(type="milk", department="Молоко", name="Кефир обезжиренный", measurement="литр"),
    Prods(type="milk", department="Молоко", name="Ряженка термостатная", measurement="литр"),
    Prods(type="milk", department="Молоко", name="Сливки 10%", measurement="литр"),
    Prods(type="milk", department="Молоко", name="Сливки 35% для взбивания", measurement="литр"),
    Prods(type="milk", department="Молоко", name="Сметана 15%", measurement="литр"),
    Prods(type="milk", department="Молоко", name="Сметана 25%", measurement="литр"),
    Prods(type="eco", department="Молоко", name="Молоко кокосовое", measurement="литр"),
    Prods(type="eco", department="Молоко", name="Молоко овсяное", measurement="литр"),
    Prods(type="milk", department="Молоко", name="Творог 9% жирности", measurement="кг"),
    Prods(type="milk", department="Молоко", name="Творожок детский сладкий", measurement="кг"),
    Prods(type="eggs", department="Молоко", name="Яйцо диетическое", measurement="шт"),
    Prods(type="milk", department="Молоко", name="Масло сливочное крестьянское", measurement="кг"),
    Prods(type="grain", department="Бакалея", name="Крупа гречневая ядрица", measurement="кг"),
    Prods(type="grain", department="Бакалея", name="Крупа манная", measurement="кг"),
    Prods(type="grain", department="Бакалея", name="Крупа пшено", measurement="кг"),
    Prods(type="grain", department="Бакалея", name="Крупа перловая", measurement="кг"),
    Prods(type="grain", department="Бакалея", name="Рис круглозерный", measurement="кг"),
    Prods(type="grain", department="Бакалея", name="Рис длиннозерный", measurement="кг"),
    Prods(type="grain", department="Бакалея", name="Бурый рис", measurement="кг"),
    Prods(type="pasta", department="Бакалея", name="Макароны спагетти ", measurement="кг"),
    Prods(type="pasta", department="Бакалея", name="Макароны вермишель", measurement="кг"),
    Prods(type="pasta", department="Бакалея", name="Макароны рожки", measurement="кг"),
    Prods(type="pasta", department="Бакалея", name="Макароны перья", measurement="кг"),
    Prods(type="tea-coffe", department="Бакалея", name="Сахар песок белый", measurement="кг"),
    Prods(type="tea-coffe", department="Бакалея", name="Сахар демерара коричневый", measurement="кг"),
    Prods(type="tea-coffe", department="Бакалея", name="Сахар рафинад быстрорастворимый", measurement="кг"),
    Prods(type="eco", department="Бакалея", name="Лапша гречневая", measurement="кг"),
    Prods(type="eco", department="Бакалея", name="Фунчоза", measurement="кг"),
    Prods(type="grain", department="Бакалея", name="Мука хлебопекарная в\с", measurement="кг"),
    Prods(type="grain", department="Бакалея", name="Мука блинная", measurement="кг"),
    Prods(type="grain", department="Бакалея", name="Горох желтый колотый", measurement="кг"),
    Prods(type="grain", department="Бакалея", name="Чечевица красная", measurement="кг"),
    Prods(type="grain", department="Бакалея", name="Хлопья овсяные Геркулес", measurement="кг"),
    Prods(type="grain", department="Бакалея", name="Хлопья 4 злака", measurement="кг"),
    Prods(type="grain", department="Бакалея", name="Кукурузные хлопья с сахаром", measurement="кг"),
    Prods(type="grain", department="Бакалея", name="Соль каменная помол №1", measurement="кг"),
    Prods(type="grain", department="Бакалея", name="Соль поваренная Экстра", measurement="кг"),
    Prods(type="grain", department="Бакалея", name="Крахмал картофельный", measurement="кг"),
    Prods(type="grain", department="Бакалея", name="Сода пищевая", measurement="кг"),
    Prods(type="tea-coffe", department="Бакалея", name="Чай черный индийский", measurement="кг"),
    Prods(type="tea-coffe", department="Бакалея", name="Чай зеленый ", measurement="кг"),
    Prods(type="tea-coffe", department="Бакалея", name="Кофе растворимый", measurement="кг"),
    Prods(type="tea-coffe", department="Бакалея", name="Кофе в зернах ", measurement="кг"),
    Prods(type="tea-coffe", department="Бакалея", name="Кофе молотый", measurement="кг"),
    Prods(type="meat", department="Мясная гастрономия", name="Колбаса вареная докторская", measurement="кг"),
    Prods(type="meat", department="Мясная гастрономия", name="Колбаса вареная любительская", measurement="кг"),
    Prods(type="meat", department="Мясная гастрономия", name="Сервелат варенокопченый", measurement="кг"),
    Prods(type="meat", department="Мясная гастрономия", name="Колбаса краковская", measurement="кг"),
    Prods(type="meat", department="Мясная гастрономия", name="Сосиски молочные", measurement="кг"),
    Prods(type="meat", department="Мясная гастрономия", name="Сосиски венские", measurement="кг"),
    Prods(type="meat", department="Мясная гастрономия", name="Сосиски куриные", measurement="кг"),
    Prods(type="meat", department="Мясная гастрономия", name="Сардельки", measurement="кг"),
    Prods(type="meat", department="Мясная гастрономия", name="Колбаса сырокопченая салями", measurement="кг"),
    Prods(type="meat", department="Мясная гастрономия", name="Бекон варенокопченый", measurement="кг"),
    Prods(type="meat", department="Мясная гастрономия", name="Бекон сырокопченый", measurement="кг"),
    Prods(type="meat", department="Мясная гастрономия", name="Грудинка копченая", measurement="кг"),
    Prods(type="meat", department="Мясная гастрономия", name="Ветчина в оболочке", measurement="кг"),
    Prods(type="meat", department="Мясная гастрономия", name="Паштет фермерский с грибами", measurement="кг"),
    Prods(type="meat", department="Мясная гастрономия", name="Паштет из куриной печени", measurement="кг"),
    Prods(type="meat", department="Мясная гастрономия", name="Колбаса ливерная", measurement="кг")
]
