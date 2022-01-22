from ...GenBase import DirectInput
from ...RussianModules.Sports import sports
from ... import Html as html

class SearchQuery(DirectInput):

    def generate(self):
        item1, item2 = self.rnd.pick_n(2, sports)
        item1_cnt, item2_cnt = [ 10 * self.rnd.in_range(200, 999) for _ in range(2) ]
        both_cnt = 10 * self.rnd.in_range(100, min(item1_cnt, item2_cnt) / 20)

        variants = [
            [ f'{item1} | {item2}', item1_cnt + item2_cnt - both_cnt ],
            [ item1, item1_cnt ],
            [ item2, item2_cnt ],
            [ f'{item1} &amp; {item2}', both_cnt ]
        ]

        correct = variants.pop(self.rnd.in_range(0, 3))
        self.correct = correct[1]

        table = html.table([
            html.row('th', [ '<b>Запрос</b>', '<b>Найдено страниц (в тысячах)</b>' ]),
            *[ html.row('td', i) for i in variants ]
        ], attrs={ 'border': 1, **html.style(text_align='center') })
        self.text = f'''В языке запросов поискового сервера для обозначения логической операции «ИЛИ» 
используется символ «|», а для логической операции «И» – символ «&amp;». В таблице приведены запросы и количество 
найденных по ним страниц некоторого сегмента сети Интернет. {table} Какое количество страниц (в тысячах) будет найдено 
по запросу<br/><i><b>{correct[0]}?</b></i><br/> Считается, что все запросы выполнялись практически одновременно, так 
что набор страниц, содержащих все искомые слова, не изменялся за время выполнения запросов.'''

        return self
