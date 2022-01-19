from ...GenBase import DirectInput
from ...RussianModules.NumText import num_text
from ...RussianModules.Names import female, male, ablative, genitive, dative

class TransRate(DirectInput):

    def generate(self):
        K = 1024
        time1, time2 = 0, 0
        # Отсекаем неоднозначный ответ (А0, Б0) и ответ Б23 из примера.
        while time1 == time2 or time2 - time1 == 23:
            size = 10 * self.rnd.in_range(1, 5)
            compress_rate = self.rnd.pick([ 10, 20, 50 ])
            speed = self.rnd.in_range(23, 27)
            pack = self.rnd.in_range(5, 15)
            unpack = self.rnd.in_range(25, 35)

            Kspeed = 2**(speed - 18)
            time1 = size * K / Kspeed
            time2 = size * (100 - compress_rate) / 100 * K / Kspeed + pack + unpack

        self.text = f'''Документ объемом {size} Мбайт можно передать с одного компьютера на другой двумя способами: 
<br/>\n А) Сжать архиватором, передать архив по каналу связи, распаковать <br/>\n Б) Передать по каналу связи без 
использования архиватора. <br/>\n Какой способ быстрее и насколько, если\n <ul><li>средняя скорость передачи данных по 
каналу связи составляет 2<sup>{speed}</sup> бит в секунду,</li><li>объем сжатого архиватором документа равен 
{compress_rate}% от исходного,</li><li>время, требуемое на сжатие документа — {pack} сек., на распаковку — 
{unpack} сек.?</li></ul> В ответе напишите букву А, если способ А быстрее или Б, если быстрее способ Б. Сразу после 
буквы напишите количество секунд, насколько один способ быстрее другого. Так, например, если способ Б быстрее способа 
А на 23 секунды, в ответе нужно написать Б23. Слов «секунд», «сек.», «с.» к ответу добавлять <b>не нужно</b>.'''

        self.correct = ('А' if time1 > time2 else 'Б') + str(abs(time2 - time1))
        self.accept = r'^[АБ]\d+$'

        return self

class TransTime(DirectInput):

    def _trans_init_common(self):
        size = self.rnd.in_range(10, 50)
        speed1 = self.rnd.in_range(18, 23)
        speed2 = self.rnd.in_range(18, 23, speed1)
        self.time_sec = (2 ** (23 - speed1) + 2 ** (23 - speed2)) * size
        self.text = f'''Данные объемом {size} Мбайт передаются из пункта А в пункт Б по каналу связи, обеспечивающему 
скорость передачи данных 2<sup>{speed1}</sup> бит в секунду, а затем из пункта Б в пункт В по каналу связи, 
обеспечивающему скорость передачи данных 2<sup>{speed2}</sup> бит в секунду. '''
        self.accept_number()

    def generate(self):
        self._trans_init_common()
        latency = self.rnd.in_range(13, 35)

        self.text += f'''Задержка в пункте Б (время между окончанием приема данных из пункта А 
и началом передачи в пункт В) составляет {num_text(latency, ['секунду', 'секунды', 'секунд'])}. Сколько 
времени (в секундах) прошло с момента начала передачи данных из пункта А до их полного получения в пункте В? В ответе 
укажите только число, слово «секунд» или букву «с» добавлять <b>не нужно</b>.'''

        self.correct = self.time_sec + latency

        return self

class TransLatency(TransTime):

    def generate(self):
        self._trans_init_common()
        minutes = int(self.time_sec / 60) + self.rnd.in_range(1, 3)
        latency = minutes * 60 - self.time_sec

        self.text = f'''От начала передачи данных из пункта А до их полного получения в пункте В прошло 
{num_text(minutes, [ 'минута', 'минуты', 'минут' ])}. Сколько времени в секундах составила задержка в пункте Б, т.е. 
время между окончанием приема данных из пункта А и началом передачи данных в пункт В? В ответе укажите только число, 
слово «секунд» или букву «с» добавлять <b>не нужно</b>.'''
        self.correct = latency

        return self

class MinPeriodOfTime(DirectInput):

    def generate(self):
        high_speed = self.rnd.in_range(17, 23)
        slow_speed = self.rnd.in_range(12, 15)
        required_data = self.rnd.in_range(6, 12)
        full_data = 2 ** self.rnd.in_range(high_speed - 13, 10)

        male_or_female  = self.rnd.coin()
        female_name = self.rnd.pick(female)
        male_name = self.rnd.pick(male)
        name_first = female_name if male_or_female else male_name
        name_second = male_name if male_or_female else female_name
        argeed = 'договорился' if male_or_female else 'договорилась'
        she_he = 'она' if male_or_female else 'он'

        genitive_first  = genitive(name_first)
        ablative_first  = ablative(name_first)
        genitive_second = genitive(name_second)
        ablative_second = ablative(name_second)
        dative_second   = dative(name_second)

        self.text = f'''<p>У {genitive_first} есть доступ к сети Интернет по высокоскоростному одностороннему 
радиоканалу, обеспечивающему скорость получения информации 2<sup>{high_speed}</sup> бит в секунду. У {genitive_second} 
нет скоростного доступа в Интернет, но есть возможность получать информацию от {genitive_first} по телефонному каналу 
со средней скоростью 2<sup>{slow_speed}</sup> бит в секунду. {name_second} {argeed} с {ablative_first}, что {she_he} 
скачает для него данные объемом {required_data} Мбайт по высокоскоростному каналу и ретранслирует их {dative_second} по 
низкоскоростному каналу.</p> <p>Компьютер {genitive_first} может начать ретрансляцию данных не раньше, чем им будут 
получены первые {full_data} Кбайт этих данных. Каков минимально возможный промежуток времени (в секундах) с момента 
начала скачивания {ablative_first} данных до полного их получения {ablative_second}?</p> <p>В ответе укажите только 
число, слово «секунд» или букву «с» добавлять не нужно.</p>'''

        self.correct = 2 ** (23 - slow_speed) * required_data + full_data * 2 ** (13 - high_speed)
        self.accept_number()

        return self

class TransText(DirectInput):

    def generate(self):
        speed = (2 ** self.rnd.in_range(3, 9)) * (10 ** self.rnd.in_range(2, 3))
        seconds = self.rnd.in_range(10, 40)
        typecon = 'модемное ' if speed < 52000 else 'ADSL-'
        self.text = f'''Скорость передачи данных через {typecon}соединение равна {speed} бит/с. Передача текстового 
файла через это соединение заняла {num_text(seconds, [ "секунду", "секунды", "секунд" ])}. Определите, сколько символов 
содержал переданный текст, если известно, что он был представлен в 16-битной кодировке Unicode.'''
        self.correct = speed * seconds / 16
        self.accept_number()

        return self

class TransTimeSize(DirectInput):

    def generate(self):
        Kspeed = 2 ** self.rnd.in_range(9, 10)
        time1 = self.rnd.in_range(1, 7) * 2
        time2 = self.rnd.in_range(1, 7) * 2
        time = time1 + time2
        self.text = f'''По каналу связи непрерывно в течение {time} часов передаются данные. Скорость передачи данных в 
течение первых {time1} часов составляет {Kspeed} Кбит в секунду, а в остальное время — в два раза меньше. Сколько Мбайт 
данных было передано за время работы канала?'''
        self.correct = (time1 + time2 / 2) * 3600 * Kspeed / 8192
        self.accept_number()

        return self
