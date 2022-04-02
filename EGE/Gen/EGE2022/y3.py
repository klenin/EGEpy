from ...RussianModules.Products import products
from ...RussianModules.Addresses import addresses
from ...RussianModules.Districts import districts, districts_genetive
from ...GenBase import DirectInput
from ..EGE2022.image import img_src
import pandas as pd


# add to Requirements pandas and xlsxwriter

def measure_genetive(name):
    if name == 'кг':
        return 'килограмм'
    if name == 'шт':
        return 'штук'
    if name == 'литр':
        return 'литров'


class Task:
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
                 movement_type1_3,
                 movement_type4):
        self.rnd = rnd
        self.name = name
        self.price = price
        self.provider = provider
        self.measurement = measurement
        self.prod_id = prod_id
        self.amount = amount
        self.district = district
        self.dates_info = dates_info
        self.movement_type1_3 = movement_type1_3
        self.movement_type4 = movement_type4
        self.text = ""
        self.correct = -1


class TaskType1(Task):
    def __init__(self, rnd, name, price, provider, measurement, prod_id, amount, district, dates_info, movement_type1_3,
                 movement_type4):
        super().__init__(rnd, name, price, provider, measurement, prod_id, amount, district, dates_info,
                         movement_type1_3, movement_type4)

    def gen(self):
        movement = self.movement_type1_3[self.movement_type1_3['Артикул'] == self.prod_id]
        accepted = movement[movement['Тип операции'] == 'Поступление']['Количество упаковок, шт.'].sum()
        soled = movement[movement['Тип операции'] == 'Продажа']['Количество упаковок, шт.'].sum()
        self.correct = accepted - soled
        self.text = (f"на сколько увеличилось количество упаковок товара \"{self.name}\" "
                     f"имеющихся в наличии в магазинах {self.district} за период c {self.dates_info[0]} по "
                     f"{self.dates_info[-1]} "
                     "В ответе запишите только число.</p>")

        return self.text, self.correct


class TaskType2(Task):
    def __init__(self, rnd, name, price, provider, measurement, prod_id, amount, district, dates_info, movement_type1_3,
                 movement_type4):
        super().__init__(rnd, name, price, provider, measurement, prod_id, amount, district, dates_info,
                         movement_type1_3, movement_type4)

    def gen(self):
        fork = self.fork()
        #var = 0
        self.text = (f"сколько {measure_genetive(self.measurement)} "
                     f"товара \"{self.name}\" {fork} в "
                     f"магазинах {districts_genetive(self.district)} района за период с "
                     f"{self.dates_info[0]} до {self.dates_info[-1]}\n"
                     "В ответе запишите только число. Ответ округлите до десятых.</p>")
        if fork == 'было продано':
            var = self.movement_type1_3[self.movement_type1_3['Тип операции'] == 'Продажа'][
                'Количество упаковок, шт.'].sum()
        else:
            var = self.movement_type1_3[self.movement_type1_3['Тип операции'] == 'Поступление'][
                'Количество упаковок, шт.'].sum()

        self.correct = var * self.amount
        return self.text, self.correct

    def fork(self):
        return self.rnd.pick(['было продано', 'поступило'])


class TaskType3(Task):
    def __init__(self, rnd, name, price, provider, measurement, prod_id, amount, district, dates_info, movement_type1_3,
                 movement_type4):
        super().__init__(rnd, name, price, provider, measurement, prod_id, amount, district, dates_info,
                         movement_type1_3, movement_type4)

    def gen(self):
        fork = self.fork()
        #var = 0
        self.text = (f"сколько рублей {fork[0]} "
                     f"{districts_genetive(self.district)} района {fork[1]} "
                     f"товара \"{self.name}\" за период с "
                     f"{self.dates_info[0]} до {self.dates_info[-1]}\n"
                     "В ответе запишите только число.</p>")
        if fork[0] == 'выручили магазины':
            var = self.movement_type1_3[self.movement_type1_3['Тип операции'] == 'Продажа'][
                'Количество упаковок, шт.'].sum()
        else:
            var = self.movement_type1_3[self.movement_type1_3['Тип операции'] == 'Поступление'][
                'Количество упаковок, шт.'].sum()

        self.correct = var * self.price
        return self.text, self.correct

    def fork(self):
        return self.rnd.pick([['потребовалось магазинам', 'для закупки'], ['выручили магазины', 'от продажи']])


class TaskType4(TaskType3):
    def __init__(self, rnd, name, price, provider, measurement, prod_id, amount, district, dates_info, movement_type1_3,
                 movement_type4):
        super().__init__(rnd, name, price, provider, measurement, prod_id, amount, district, dates_info,
                         movement_type1_3, movement_type4)

    def gen(self):
        fork = self.fork()
        #var = 0
        self.text = (f"сколько рублей {fork[0]} "
                     f"{districts_genetive(self.district)} района {fork[1]} "
                     f"товаров поставщика \"{self.provider}\" за период с "
                     f"{self.dates_info[0]} до {self.dates_info[-1]}\n"
                     "В ответе запишите только число.</p>")
        if fork[0] == 'потребовалось магазинам':
            var = self.movement_type4[self.movement_type4['Тип операции'] == 'Продажа'][
                'Количество упаковок, шт.'].sum()
        else:
            var = self.movement_type4[self.movement_type4['Тип операции'] == 'Поступление'][
                'Количество упаковок, шт.'].sum()

        self.correct = var * self.price
        return self.text, self.correct


class GenDatabase(DirectInput):
    def __init__(self, rnd, num):
        self.text = (
            "<p>В файле приведён фрагмент базы данных «Продукты», содержащей"
            "информацию о поставках товаров и их продаже.База данных состоит из трёх таблиц.</p>"
            "<center><a href=\"EGE/Gen/EGE2022/multiple.xlsx\">База данных</a></center>"
            "<p>Таблица «Движение товаров» содержит записи о поставках товаров в магазины города "
            "в первой декаде июня 2021г. и о продаже товаров в этот же период.Таблица «Товар» содержит"
            " данные о товарах.Таблица «Магазин» содержит адреса магазинов."
            "На рисунке приведена схема базы данных, содержащая все поля каждой таблицы и связи между ними.</p>"
            f"<img src=\"{img_src}\" "
            "style = \"display: block; margin-left: auto;margin-right: auto;\"/>\n"
            "<p>Используя информацию из приведённой базы данных, определите, "
        )
        self.rnd = rnd
        self.num = num
        self.dates = ['0' + str(i + 1) + '.06.2021' for i in range(rnd.in_range(3, 6))]  # rnd.pick([4, 6, 8])
        self.number_of_shops = rnd.in_range(10, 18)
        self.number_of_rows = self.number_of_shops * 142

        self.number_of_products = rnd.in_range(20, 65)

        if self.number_of_shops % 2 != 0:
            self.number_of_shops += 1
        self.addresses = [addresses[rnd.in_range(0, 15)] + ", " + str(rnd.in_range(1, 30)) for _ in
                          range(self.number_of_shops)]
        self.districts = [rnd.pick(districts) for _ in range(self.number_of_shops)]

    def gen_shops(self):
        shops = pd.DataFrame()
        shops_ids = ["M" + str(i) for i in range(self.number_of_shops)]
        shops['ID Магазина'] = shops_ids
        shops['Район'] = self.districts
        shops['Адрес'] = self.addresses
        return shops, shops_ids

    def gen_products(self):
        # it could me more random if choose random product name and delete it from list of products
        # for the first time its good as it is
        # but if you'll do it,then you should somehow give list of products to gen_text()
        product = []
        price_list = []
        for i in range(self.number_of_products):
            price_list.append(self.rnd.in_range(100, 200))
            supplier = ''
            if products[i].type == 'milk':
                supplier = 'Молокозавод'
            if products[i].type == 'eggs':
                supplier = 'Птицеферма'
            if products[i].type == 'eco':
                supplier = 'Экопродукты'
            if products[i].type == 'grain':
                supplier = 'Продбаза'
            if products[i].type == 'pasta':
                supplier = 'Макаронная фабрика'
            if products[i].type == 'tea-coffe':
                supplier = 'Чай-Кофе-Сахар'
            if products[i].type == 'meat':
                supplier = 'Мясокомбинат'

            if products[i].measurement == 'шт':
                amount = self.rnd.in_range(1, 10)
            else:
                amount = self.rnd.in_range(1, 10) / 10
            product.append({'Артикул': i,
                            'Отдел': products[i].department,
                            'Наименование товара': products[i].name,
                            'Ед. изм': products[i].measurement,
                            'Количество в упаковке': amount,
                            'Поставщик': supplier
                            })
        return product, price_list

    def lines_per_day(self, num_rows, num_days):
        res = []
        while num_rows > 0:
            if num_days <= 1:
                res.append(num_rows)
                break
            r = self.rnd.in_range(100, num_rows / 2)
            if r % 2 != 0:
                r += 1
            res.append(r)
            num_rows -= r
            num_days -= 1
        return res

    def gen_movement(self, price_list, shops_ids):
        movement = []
        lines_per_shop = self.number_of_rows / self.number_of_shops
        lines_per_day = self.lines_per_day(self.number_of_rows, len(self.dates))
        shops_lst = shops_ids.copy()

        counter_shops = 0
        counter_days = 0
        j = 0
        for i in range(0, int(self.number_of_rows / 2), 2):
            day = ''
            shop = ''
            articul = self.rnd.in_range(0, len(price_list) - 1)
            if i == counter_shops:
                counter_shops += lines_per_shop
                shop = self.rnd.pick(shops_lst)
                shops_lst.remove(shop)

            if (i == counter_days) & (i != self.number_of_rows):
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
            movement.append({'ID операции': i + 2,
                             'Дата': day,
                             'ID Магазина': shop,
                             'Артикул': articul,
                             'Количество упаковок, шт.': selled,
                             'Тип операции': 'Продажа',
                             'Цена руб./шт.': price_list[articul]
                             })
        return movement

    def gen_text(self, product, shops, movement, price_list, num=0):
        product_id = self.rnd.in_range(1, self.number_of_products)
        shops_list = movement['ID Магазина'].unique()
        district_list = shops[shops['ID Магазина'].isin(shops_list)]['Район'].unique()
        district = self.rnd.pick(district_list)
        movement_type1_3 = movement[movement['Артикул'] == product_id].copy()

        provider = self.rnd.pick(product['Поставщик'].unique())
        product_list = product[product['Поставщик'] == provider]['Артикул'].to_list()
        movement_type4 = movement[movement['Артикул'].isin(product_list)].copy()
        # task_type = self.rnd.pick([TaskType1, TaskType2, TaskType3, TaskType4])
        task_type = [TaskType1, TaskType2, TaskType3, TaskType4]
        task = task_type[num](rnd=self.rnd,
                              name=products[product_id].name,
                              price=price_list[product_id],
                              provider=provider,
                              measurement=product[product['Артикул'] == product_id][['Ед. изм']].values[0],
                              prod_id=product_id,
                              amount=product[product['Артикул'] == product_id][['Количество в упаковке']].values[0],
                              district=district,
                              dates_info=self.dates,
                              movement_type1_3=movement_type1_3,
                              movement_type4=movement_type4)
        task, ans = task.gen()
        self.text += task
        self.correct = ans
        # if 0 <= num <= 4:
        #     movement = movement[movement['Артикул'] == product_id]
        #     measurement, amount = \
        #         product[product['Артикул'] == product_id][['Ед. изм', 'Количество в упаковке']].values[0]
        # elif 5 <= num <= 7:
        #     provider = self.rnd.pick(product['Поставщик'].unique())
        #     product_list = product[product['Поставщик'] == provider]['Артикул'].to_list()
        #     movement = movement[movement['Артикул'].isin(product_list)]
        #
        # shops_list = movement['ID Магазина'].unique()
        #
        # shops_list = shops[shops['Район'] == district]['ID Магазина'].to_list()
        # movement = movement[movement['ID Магазина'].isin(shops_list)]
        #
        # price = price_list[product_id]
        # if num == 0:
        #     # делать крч тут по классам а не ифами
        #     self.text += (f"<p>Используя информацию из приведённой базы данных, определите, на сколько увеличилось "
        #                   f"количество упаковок товара \"{products[product_id]['name']}\", имеющихся в наличии в "
        #                   f"магазинах {districts_genetive(district)} района за период с "
        #                   f"{self.dates[0]} до {self.dates[-1]}\n"
        #                   f"В ответе запишите только число.</p>")
        #     accepted = movement[movement['Тип операции'] == 'Поступление']['Количество упаковок, шт.'].sum()
        #     selled = movement[movement['Тип операции'] == 'Продажа']['Количество упаковок, шт.'].sum()
        #     self.correct = accepted - selled
        # elif num == 1:
        #     self.text += (f"<p>Используя информацию из приведённой базы данных, определите, "
        #                   f"сколько {measure_genetive(measurement)} "
        #                   f"товара \"{products[product_id]['name']}\" было продано в "
        #                   f"магазинах {districts_genetive(district)} района за период с "
        #                   f"{self.dates[0]} до {self.dates[-1]}\n"
        #                   f"В ответе запишите только число. Ответ округлите до десятых.</p>")
        #     selled = movement[movement['Тип операции'] == 'Продажа']['Количество упаковок, шт.'].sum()
        #     self.correct = selled * amount
        # elif num == 2:
        #     self.text += (f"<p>Используя информацию из приведённой базы данных, определите, "
        #                   f"сколько {measure_genetive(measurement)} "
        #                   f"товара \"{products[product_id]['name']}\" поступило в "
        #                   f"магазины {districts_genetive(district)} района за период с "
        #                   f"{self.dates[0]} до {self.dates[-1]}\n"
        #                   f"В ответе запишите только число. Ответ округлите до десятых.</p>")
        #     accepted = movement[movement['Тип операции'] == 'Поступление']['Количество упаковок, шт.'].sum()
        #     self.correct = accepted * amount
        # elif num == 3:  # 1,2 done
        #     self.text += (f"<p>Используя информацию из приведённой базы данных, определите, "
        #                   f"сколько рублей потребовалось магазинам "
        #                   f"{districts_genetive(district)} района для закупки "
        #                   f"товара \"{products[product_id]['name']}\" за период с "
        #                   f"{self.dates[0]} до {self.dates[-1]}\n"
        #                   f"В ответе запишите только число.</p>")
        #     accepted = movement[movement['Тип операции'] == 'Поступление']['Количество упаковок, шт.'].sum()
        #     self.correct = accepted * price
        # elif num == 4:
        #     self.text += (f"<p>Используя информацию из приведённой базы данных, определите, "
        #                   f"сколько рублей выручили магазины "
        #                   f"{districts_genetive(district)} района от продажи "
        #                   f"товара \"{products[product_id]['name']}\" за период с "
        #                   f"{self.dates[0]} до {self.dates[-1]}\n"
        #                   f"В ответе запишите только число.</p>")
        #     selled = movement[movement['Тип операции'] == 'Продажа']['Количество упаковок, шт.'].sum()
        #     self.correct = selled * price
        #
        # elif num == 5:
        #     self.text += (f"<p>Используя информацию из приведённой базы данных, определите, "
        #                   f"сколько рублей выручили магазины "
        #                   f"{districts_genetive(district)} района от продажи "
        #                   f"товаров поставщика \"{provider}\" за период с "
        #                   f"{self.dates[0]} до {self.dates[-1]}\n"
        #                   f"В ответе запишите только число.</p>")
        #     selled = movement[movement['Тип операции'] == 'Продажа']['Количество упаковок, шт.'].sum()
        #     self.correct = selled * price
        # elif num == 6:
        #     self.text += (f"<p>Используя информацию из приведённой базы данных, определите "
        #                   f"общую стоимость продуктов "
        #                   f"поставленных за период с {self.dates[0]} до {self.dates[-1]}\n"
        #                   f"от поставщика \"{provider}\" в магазины "
        #                   f"{districts_genetive(district)} района "
        #                   f"В ответе запишите только число.</p>")
        #     accepted = movement[movement['Тип операции'] == 'Поступление']['Количество упаковок, шт.'].sum()
        #     self.correct = accepted * price

    def generate(self):
        # нужен ли пандас? или использовать имеющийся код для бд
        product, price_list = self.gen_products()
        shops, shops_ids = self.gen_shops()
        product, shops = pd.DataFrame(product), pd.DataFrame(shops)
        movement = pd.DataFrame(self.gen_movement(price_list, shops_ids))
        self.gen_text(product, shops, movement, price_list, self.num)

        write = pd.ExcelWriter(r'EGE/Gen/EGE2022/multiple.xlsx', engine='xlsxwriter')
        movement.to_excel(write, sheet_name='Движение товаров', index=False)
        product.to_excel(write, sheet_name='Товар', index=False)
        shops.to_excel(write, sheet_name='Магазин', index=False)
        write.save()

        return self
