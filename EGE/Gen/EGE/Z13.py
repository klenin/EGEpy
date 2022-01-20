from EGE.GenBase import DirectInput
from ...RussianModules.NumText import num_text

class Tumblers(DirectInput):
    def generate(self):
        tumblers_count = self.rnd.in_range(2, 5)
        tumbler_state = self.rnd.in_range(4, 8)
        off_state_message = 'При этом устройство имеет специальную кнопку включения/выключения.'
        self.correct = tumbler_state ** tumblers_count
        if self.rnd.coin():
            self.correct -= 1
            off_state_message = '''
При этом крайнее нижнее одновременное положение 
всех ручек соответствует отключению устройства.'''

        self.text = f'''
Выбор режима работы в некотором устройстве осуществляется установкой ручек {tumblers_count} тумблеров, 
каждая из которых может находиться в одном из {tumbler_state} положений. {off_state_message} 
Сколько различных режимов работы может иметь устройство? Выключенное состояние режимом работы не считать.'''
        return self

class TumblersMin(DirectInput):
    def generate(self):
        tumbler_state = self.rnd.pick([ 2, 3, 4, 5, 8 ])
        tumbler_count = self.rnd.in_range(3, 5)
        n = self.rnd.in_range(tumbler_state ** (tumbler_count - 1), tumbler_state ** tumbler_count)
        self.correct = tumbler_count
        self.text = f'''
Выбор режима работы в некотором устройстве осуществляется установкой ручек тумблеров, 
каждая из которых может находиться в одном из {tumbler_state} положений. 
Каково минимальное количество необходимых тумблеров для обеспечения работы устройства на {n} режимах.'''
        return self

class YoungSpy(DirectInput):
    def generate(self):
        n = self.rnd.in_range(2, 8)
        time = self.rnd.in_range(2, 9)
        n_flags = self.rnd.in_range(2, 5)
        time_text, all_time_text = [ num_text(t, [ 'минуту', 'минуты', 'минут' ]) for t in [ time, n * time ] ]
        changes_text = num_text(n - 1, [ 'перемену', 'перемены', 'перемен' ])
        self.correct = n_flags ** n
        self.text = f'''
В детскую игрушку «Набор юного шпиона» входят два одинаковых комплекта из {n_flags} флажков различных цветов. 
Сколько различных тайных сообщений можно передать этими флажками, 
условившись менять выставленный флажок каждые {time_text} и наблюдая за процессом {all_time_text}? 
Наблюдатель видит вынос первого флажка и {changes_text} флажка. 
При этом возможна смена флажка на флажок того же цвета.'''
        return self
