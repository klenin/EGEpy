from ...RussianModules.Measurements import measure_genetive
from ...RussianModules.Products import products
from ...RussianModules.Addresses import addresses
from ...RussianModules.Districts import districts, districts_genetive
from ...GenBase import DirectInput
from ..EGE2022.image import img_src
import pandas as pd


class Problem:
    def __init__(self,
                 rnd,
                 name: str,
                 price: int,
                 provider: str,
                 measurement: str,
                 prod_id: int,
                 amount: int,
                 district: str,
                 dates_info: list[str],
                 shop_to_filter,
                 product_list,
                 movement,
                 mutations):
        self.rnd = rnd
        self.name = name
        self.price = price
        self.provider = provider
        self.measurement = measurement
        self.prod_id = prod_id
        self.amount = amount
        self.district = district
        self.dates_info = dates_info
        self.shop_to_filter = shop_to_filter
        self.product_list = product_list
        self.movement = movement
        self.text = ""
        self.correct = -1
        self.mutations = mutations

    def mutation(self):
        return self.mutations[self.rnd.pick(list(self.mutations.keys()))]


class FirstProblemType(Problem):
    def __init__(self, rnd, name, price, provider, measurement, prod_id, amount, district, dates_info, shop_to_filter,
                 product_list, movement):
        super().__init__(rnd, name, price, provider, measurement, prod_id, amount, district, dates_info, shop_to_filter,
                         product_list, movement, {})

    def gen(self):
        movement = self.movement[self.movement['ID Магазина'].isin(self.shop_to_filter)].copy()
        movement = movement[movement['Артикул'] == self.prod_id]
        accepted = movement[movement['Тип операции'] == 'Поступление']['Количество упаковок, шт.'].sum()
        soled = movement[movement['Тип операции'] == 'Продажа']['Количество упаковок, шт.'].sum()
        self.correct = accepted - soled
        self.text = (f"""на сколько увеличилось количество упаковок товара \"{self.name}\", 
                     имеющихся в наличии в магазинах {districts_genetive(self.district)} района за период c {self.dates_info[0]} по 
                     {self.dates_info[-1]}.
                     В ответе запишите только число.</p>""")

        return self.text, self.correct


class SecondProblemType(Problem):
    def __init__(self, rnd, name, price, provider, measurement, prod_id, amount, district, dates_info, shop_to_filter,
                 product_list, movement):
        super().__init__(rnd, name, price, provider, measurement, prod_id, amount, district, dates_info, shop_to_filter,
                         product_list, movement, { 1: 'было продано', 2: 'появилось' })

    def gen(self):
        temp_calc = -1
        mutation = self.mutation()
        movement = self.movement[self.movement['ID Магазина'].isin(self.shop_to_filter)].copy()
        movement = movement[movement['Артикул'] == self.prod_id]
        self.text = (f"""сколько {measure_genetive(self.measurement)} 
                     товара \"{self.name}\" {mutation} в 
                     магазинах {districts_genetive(self.district)} района за период с 
                     {self.dates_info[0]} до {self.dates_info[-1]}.\n
                     В ответе запишите только число. Ответ округлите до десятых.</p>""")
        if mutation == 'было продано':
            temp_calc = movement[movement['Тип операции'] == 'Продажа'][
                'Количество упаковок, шт.'].sum()
        elif mutation == 'появилось':
            temp_calc = movement[movement['Тип операции'] == 'Поступление'][
                'Количество упаковок, шт.'].sum()

        self.correct = temp_calc * self.amount
        return self.text, self.correct


class ThirdProblemType(Problem):
    def __init__(self, rnd, name, price, provider, measurement, prod_id, amount, district, dates_info, shop_to_filter,
                 product_list, movement):
        super().__init__(rnd, name, price, provider, measurement, prod_id, amount, district, dates_info, shop_to_filter,
                         product_list, movement,
                         { 1: [ 'потребовалось магазинам', 'для закупки' ], 2: [ 'выручили магазины', 'от продажи' ] })

    def gen(self):
        mutation = self.mutation()
        temp_calc = -1
        movement = self.movement[self.movement['ID Магазина'].isin(self.shop_to_filter)].copy()
        movement = movement[movement['Артикул'] == self.prod_id]
        self.text = (f"""сколько рублей {mutation[0]} 
                     {districts_genetive(self.district)} района {mutation[1]} 
                     товара \"{self.name}\" за период с 
                     {self.dates_info[0]} до {self.dates_info[-1]}.\n
                     В ответе запишите только число.</p>""")
        if mutation[0] == 'выручили магазины':
            temp_calc = movement[movement['Тип операции'] == 'Продажа'][
                'Количество упаковок, шт.'].sum()
        elif mutation[0] == 'потребовалось магазинам':
            temp_calc = movement[movement['Тип операции'] == 'Поступление'][
                'Количество упаковок, шт.'].sum()

        self.correct = temp_calc * self.price
        return self.text, self.correct


class ForthProblemType(ThirdProblemType):
    def __init__(self, rnd, name, price, provider, measurement, prod_id, amount, district, dates_info, shop_to_filter,
                 product_list, movement):
        super().__init__(rnd, name, price, provider, measurement, prod_id, amount, district, dates_info, shop_to_filter,
                         product_list, movement)

    def gen(self):
        mutation = self.mutation()
        temp_calc = -1
        movement = self.movement[self.movement['Артикул'].isin(self.product_list)].copy()
        movement = movement[movement['ID Магазина'].isin(self.shop_to_filter)]
        self.text = (f"""сколько рублей {mutation[0]} 
                     {districts_genetive(self.district)} района {mutation[1]} 
                     товаров поставщика \"{self.provider}\" за период с 
                     {self.dates_info[0]} до {self.dates_info[-1]}.\n
                     В ответе запишите только число.</p>""")
        if mutation[0] == 'потребовалось магазинам':
            temp_calc = movement[movement['Тип операции'] == 'Поступление'][
                'Количество упаковок, шт.']
            temp_calc = temp_calc * movement[movement['Тип операции'] == 'Поступление'][
                'Цена руб./шт.']
            temp_calc = temp_calc.sum()
        elif mutation[0] == 'выручили магазины':
            temp_calc = movement[movement['Тип операции'] == 'Продажа'][
                'Количество упаковок, шт.']
            temp_calc = temp_calc * movement[movement['Тип операции'] == 'Продажа'][
                'Цена руб./шт.']
            temp_calc = temp_calc.sum()

        self.correct = temp_calc
        return self.text, self.correct


class GenDatabase(DirectInput):
    def __init__(self, rnd):
        self.text = (
            f"""<p>В файле приведён фрагмент базы данных «Продукты», содержащей
            информацию о поставках товаров и их продаже.База данных состоит из трёх таблиц.</p>
            <center><a href=\"EGE/Gen/EGE2022/multiple.xlsx\">База данных</a></center>
            <p> Таблица «Движение товаров» содержит записи о поставках товаров в магазины города 
            в первой декаде июня 2021г. и о продаже товаров в этот же период. Таблица «Товар» содержит
             данные о товарах. Таблица «Магазин» содержит адреса магазинов.
            На рисунке приведена схема базы данных, содержащая все поля каждой таблицы и связи между ними.</p>
            <img src=\"{img_src}\" 
            style = \"display: block; margin-left: auto;margin-right: auto;\"/>\n
            <p>Используя информацию из приведённой базы данных, определите, """
        )
        self.CONST_ROWS_PER_SHOP = 142
        self.rnd = rnd
        self.dates = [ '0' + str(i + 1) + '.06.2021' for i in range(rnd.in_range(3, 6)) ]
        self.number_of_shops = rnd.in_range(10, 18)
        self.number_of_rows = self.number_of_shops * self.CONST_ROWS_PER_SHOP

        self.number_of_products = rnd.in_range(20, 64)

        if self.number_of_shops % 2 != 0:
            self.number_of_shops += 1
        self.addresses = [ addresses[rnd.in_range(0, 15)] + ", " + str(rnd.in_range(1, 30)) for _ in
                          range(self.number_of_shops) ]
        self.districts = [ rnd.pick(districts) for _ in range(self.number_of_shops) ]

    def gen_shop_ids(self):
        return [ "M" + str(i) for i in range(self.number_of_shops) ]

    def gen_shops(self, movement):
        shops = pd.DataFrame()
        lst = movement['ID Магазина'].unique()

        shops['ID Магазина'] = lst
        shops['Район'] = self.districts[:len(lst)]
        shops['Адрес'] = self.addresses[:len(lst)]
        return shops

    def gen_products(self):
        product = []
        price_list = []
        for i in range(self.number_of_products):
            price_list.append(self.rnd.in_range(100, 200))
            supplier = ''
            if products[i].type == 'milk':
                supplier = 'Молокозавод'
            elif products[i].type == 'eggs':
                supplier = 'Птицеферма'
            elif products[i].type == 'eco':
                supplier = 'Экопродукты'
            elif products[i].type == 'grain':
                supplier = 'Продбаза'
            elif products[i].type == 'pasta':
                supplier = 'Макаронная фабрика'
            elif products[i].type == 'tea-coffee':
                supplier = 'Чай-Кофе-Сахар'
            elif products[i].type == 'meat':
                supplier = 'Мясокомбинат'

            if products[i].measurement == 'шт':
                amount = self.rnd.in_range(1, 10)
            else:
                amount = self.rnd.in_range(1, 10) / 10
            product.append({ 'Артикул': i, 'Отдел': products[i].department, 'Наименование товара': products[i].name, 'Ед. изм': products[i].measurement,
                             'Количество в упаковке': amount, 'Поставщик': supplier })
        return product, price_list

    def lines_per_day(self, num_rows, num_days):
        res = []
        while num_rows > 0:
            if num_days <= 1:
                res.append(num_rows)
                break
            rows_per_day = self.rnd.in_range(100, num_rows / 2)
            if rows_per_day % 2 != 0:
                rows_per_day += 1
            res.append(rows_per_day)
            num_rows -= rows_per_day
            num_days -= 1
        return res

    def gen_movement(self, price_list, shops_ids):
        movement = []
        lines_per_shop = self.CONST_ROWS_PER_SHOP
        lines_per_day = self.lines_per_day(self.number_of_rows, len(self.dates))
        shops_lst = shops_ids.copy()

        counter_shops = 0
        counter_days = 0
        j = 0
        day = ''
        shop = ''
        for i in range(0, int(self.number_of_rows), 2):
            articul = self.rnd.in_range(0, len(price_list) - 1)
            if i == counter_shops:
                counter_shops += lines_per_shop
                shop = self.rnd.pick(shops_lst)
                shops_lst.remove(shop)

            if i == counter_days:
                shops_lst = shops_ids.copy()
                day = self.dates[j]
                counter_days += lines_per_day[j]
                j += 1

            accepted = self.rnd.in_range(20, 200)
            selled = self.rnd.in_range(10, accepted)
            movement.append({
                'ID операции': i + 1,
                'Дата': day,
                'ID Магазина': shop,
                'Артикул': articul,
                'Количество упаковок, шт.': accepted,
                'Тип операции': 'Поступление',
                'Цена руб./шт.': price_list[articul]
            })
            movement.append({
                'ID операции': i + 2,
                'Дата': day,
                'ID Магазина': shop,
                'Артикул': articul,
                'Количество упаковок, шт.': selled,
                'Тип операции': 'Продажа',
                'Цена руб./шт.': price_list[articul]
            })
        return movement

    def gen_text(self, product, shops, movement, price_list):
        product_id = self.rnd.in_range(1, self.number_of_products - 1)
        shops_list = movement['ID Магазина'].unique()
        district_list = shops[shops['ID Магазина'].isin(shops_list)]['Район'].unique()
        district = self.rnd.pick(district_list)
        shop_to_filter = shops[shops['Район'] == district]['ID Магазина']
        provider = self.rnd.pick(product['Поставщик'].unique())
        product_list = product[product['Поставщик'] == provider]['Артикул'].to_list()
        task_type = [ FirstProblemType, SecondProblemType, ThirdProblemType, ForthProblemType ]
        task = task_type[ self.rnd.pick([0, 1, 2, 3]) ](rnd=self.rnd,
                                                        name=products[product_id].name,
                                                        price=price_list[product_id],
                                                        provider=provider,
                                                        measurement=
                                                        product[product['Артикул'] == product_id][['Ед. изм']].values[0],
                                                        prod_id=product_id,
                                                        amount=product[product['Артикул'] == product_id][
                                                          ['Количество в упаковке']].values[0],
                                                        district=district,
                                                        dates_info=self.dates,
                                                        shop_to_filter=shop_to_filter,
                                                        product_list=product_list,
                                                        movement=movement)
        task, ans = task.gen()
        self.text += task
        self.correct = ans

    def generate(self):
        product, price_list = self.gen_products()
        shops_ids = self.gen_shop_ids()
        product = pd.DataFrame(product)
        movement = pd.DataFrame(self.gen_movement(price_list, shops_ids))
        shops = pd.DataFrame(self.gen_shops(movement))
        self.gen_text(product, shops, movement, price_list)

        write = pd.ExcelWriter(r'EGE/Gen/EGE2022/multiple.xlsx', engine='xlsxwriter')
        movement.to_excel(write, sheet_name='Движение товаров', index=False)
        product.to_excel(write, sheet_name='Товар', index=False)
        shops.to_excel(write, sheet_name='Магазин', index=False)
        for my_dataframe, sheet_name in zip([ movement, product, shops ], [ 'Движение товаров', 'Товар', 'Магазин' ]):
            worksheet = write.sheets[sheet_name]
            for i, col in enumerate(my_dataframe.columns):
                column_len = my_dataframe[col].astype(str).str.len().max()
                column_len = max(column_len, len(col)) + 2
                worksheet.set_column(i, i, column_len)
        write.save()
        return self
