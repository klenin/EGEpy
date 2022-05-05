from ...GenBase import DirectInput
from EGE.LangTable import table
from EGE.Prog import make_block
from ...Utils import Box
from math import ceil

class SumOfTwoLinearFunctions(DirectInput):
    def generate(self):
        p1, p2 = self.rnd.shuffle([ 's', 'n' ])
        loop_op = self.rnd.pick([ '<', '<=' ])
        loop_p = self.rnd.in_range(100, 400)

        p1_init, p1_op, p1_arg, p2_init, p2_op, p2_arg = self.rnd.pick([
            [ self.rnd.in_range(0, 10), '+', self.rnd.in_range(10, 40),
              self.rnd.in_range(30, 200), '-', self.rnd.in_range(5, 20) ],
            [ self.rnd.in_range(80, 150), '-', self.rnd.in_range(5, 20),
              self.rnd.in_range(0, 10), '+', self.rnd.in_range(20, 40) ]
        ])

        code_block = make_block([
            '=', p1, p1_init,
            '=', p2, p2_init,
            'while', [ loop_op, [ '+', p1, p2 ], loop_p ],
            [ '=', p1, [ p1_op, p1, p1_arg ], '=', p2, [ p2_op, p2, p2_arg ], ],
            'expr', ['print', 'num', p1]
        ])
        lt = table(code_block, [['Basic', 'Alg'], ['Pascal', 'C']])

        vars = { p1: Box(0), p2: Box(0) }
        code_block.run(vars)
        self.correct = vars[p1]

        self.accept = r"^\-?\d+"
        self.text = f"""
Запишите число, которое будет напечатано в результате выполнения следующей программы. 
Для Вашего удобства программа представлена на разных языках программирования. {lt}"""
        return self

class ArithmeticProgression(DirectInput):
    def generate(self):
        p_sum, p_counter = self.rnd.shuffle([ 's', 'k' ])
        p_loop, p_return = self.rnd.shuffle([p_sum, p_counter])
        counter_arg = self.rnd.in_range(1, 5)
        counter_op = self.rnd.pick(['-', '+'])
        sum_init = self.rnd.in_range(0, 10)
        counter_init = self.rnd.in_range(6, 15) if counter_op == '-' else self.rnd.in_range(0, 3)
        loop_var = self.rnd.in_range(10, 100) if counter_op != '-' else 0
        op1, op2 = self.rnd.pick_n(2, [
            [ '=', p_sum, [ '+', p_sum, p_counter ] ],
            [ '=', p_counter, [ counter_op, p_counter, counter_arg ] ],
        ])

        code_block = make_block([
            '=', p_sum, sum_init,
            '=', p_counter, counter_init,
            'while', [ '>' if counter_op == '-' else '<', p_loop, loop_var ],
           op1 + op2,
            'expr', ['print', 'num', p_return]
        ])
        lt = table(code_block, [['Basic', 'Alg'], ['Pascal', 'C']])

        vars = { p_return: Box(0) }
        code_block.run(vars)
        self.correct = vars[p_return]

        self.accept = r"^\-?\d+"
        self.text = f"""
Определите, что будет напечатано в результате выполнения программы (записанной ниже на разных языках программирования): {lt}"""
        return self

class TwoLinearFunctions(DirectInput):
    def generate(self):
        p1, p2 = self.rnd.shuffle(['s', 'n'])
        is_p1_loop = self.rnd.coin()
        p_loop, p_return = (p1, p2) if is_p1_loop else (p2, p1)
        p1_op, p1_init, p1_arg = self.rnd.pick([
            [ '+', self.rnd.in_range(0, 30),   self.rnd.in_range(10, 30) ],
            [ '-', self.rnd.in_range(70, 100), self.rnd.in_range(5, 20) ],
            [ '*', 1,                          self.rnd.in_range(2, 4) ],
        ])
        p2_op, p2_init, p2_arg = self.rnd.pick([
            [ '+', self.rnd.in_range(0, 10), self.rnd.in_range(1, 10) ],
            # [ '*', 1,                        self.rnd.in_range(2, 5) ],
        ])

        loop_op, loop_arg = self.rnd.pick([ '<', '<=' ]), self.rnd.in_range(30, 100)
        if is_p1_loop and p1_op == '-':
            loop_op, loop_arg = self.rnd.pick([ '>', '>=']), 0
        if self.rnd.in_range(0, 100) < 20:
            loop_block = [ loop_op, [ '*', self.rnd.in_range(2, 3), p_loop ], loop_arg ]
        else:
            loop_block = [ loop_op, p_loop, loop_arg ]

        code_block = make_block([
            '=', p1, p1_init,
            '=', p2, p2_init,
            'while', loop_block,
            [ '=', p1, [ p1_op, p1, p1_arg ], '=', p2, [ p2_op, p2, p2_arg ], ],
            'expr', [ 'print', 'num', p_return ]
        ])
        lt = table(code_block, [['Basic', 'Alg'], ['Pascal', 'C']])

        vars = { p1: Box(0), p2: Box(0) }
        code_block.run(vars)
        self.correct = vars[p_return]

        self.accept = r"^\-?\d+"
        self.text = f"""
Запишите число, которое будет напечатано в результате выполнения следующей программы. 
Для Вашего удобства программа представлена на разных языках программирования. {lt}"""
        return self

class InputTwoLinearFunctions(DirectInput):
    def generate(self):
        num_iteration = self.rnd.in_range(4, 10)
        task_type = self.rnd.in_range(0, 2)

        if task_type == 0:
            loop_op, s_op, n_op = '<', '+', '*'
            s_arg = self.rnd.in_range(2, 20)
            n_arg = self.rnd.in_range(2, 5)
            n_init = self.rnd.in_range(1, 10)
            loop_arg = num_iteration * s_arg + self.rnd.in_range(1, 100)
            num = n_init * (n_arg ** num_iteration)
            ans = loop_arg - (num_iteration - 1) * s_arg - 1
        elif task_type == 1:
            loop_op, s_op, n_op = '<', '*', '+'
            s_arg = self.rnd.in_range(2, 5)
            n_arg = self.rnd.in_range(1, 20)
            n_init = self.rnd.in_range(20, 100)
            loop_arg = (s_arg ** num_iteration) + self.rnd.in_range(1, 200)
            num = n_init + num_iteration * n_arg
            tmp = s_arg ** (num_iteration - 1)
            ans = loop_arg // tmp - (1 if loop_arg % tmp == 0 else 0)
        else:
            loop_op, s_op, n_op = '>', '-', '//'
            n_arg = self.rnd.in_range(2, 4)
            s_arg = self.rnd.in_range(5, 20)
            n_init = n_arg ** num_iteration + self.rnd.in_range(10, 100)
            loop_arg = self.rnd.in_range(0, 10)
            num = n_init // (n_arg ** num_iteration)
            ans = loop_arg + num_iteration * s_arg

        code_block = make_block([
            'expr', [ 'input', 's' ],
            '=', 'n', n_init,
            'while', [ loop_op, 's', loop_arg ],
            [ '=', 's', [ s_op, 's', s_arg], '=', 'n', [ n_op, 'n', n_arg], ],
            'expr', [ 'print', 'num', 'n' ]
        ])
        lt = table(code_block, [['Basic', 'Alg'], ['Pascal', 'C']])
        self.correct = ans
        self.accept = r"^\-?\d+"
        self.text = f"""
Определите, при каком наибольшем введённом значении переменной s программа выведет число {num}.  
Для Вашего удобства программа представлена на разных языках программирования. {lt}"""
        return self
