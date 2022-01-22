from ...GenBase import DirectInput
from ...Prog import make_block, add_statement
from ...LangTable import table

class RecursiveAlg(DirectInput):
    def _gen_branches_sum(self, n, branches):
        cur_oper = branches[n]
        if n == 0:
            return cur_oper
        return [ '+', self._gen_branches_sum(n - 1, branches), cur_oper ]

    def _gen_text_block(self, args):
        return make_block([
            'func', [ 'F', args['param'] ], [
                '=', 'F', args['value'],
                'if', [ args['sign'], args['param'], args['threshold'] ], [
                    '=', 'F', args['branches_sum']
                ]
            ]
        ])

    def _gen_eval_block(self, args):
        code_block = self._gen_text_block(args)
        return add_statement(code_block, [ '=', 'M', [ '()', 'F', args['start'] ] ])

    def _gen_text_print_block(self, args):
        return make_block([
            'func', [ 'F', args['param'] ], [
                'expr', [ 'print', args['print_type'], args['value'] ],
                'if', [ args['sign'], args['param'], args['threshold'] ],
                    args['branches_call']
            ]
        ])

    def _gen_eval_print_block(self, args):
        return make_block([
            'func', [ 'F', args['param'] ], [
                '=', 'F', 0,
                'if', [ args['sign'], args['param'], args['threshold'] ], [
                    '=', 'F', args['branches_sum']
                ],
                '=', 'F', [ '+', 'F', args['ret'] ]
            ],
            '=', 'M', [ '()', 'F', args['start'] ]
        ])

    def generate(self):
        param = self.rnd.index_var()[0]
        alg = self.rnd.pick([
            { 'sign': '>', 'op': '-', 'threshold': self.rnd.in_range(1, 3), 'start': self.rnd.in_range(4, 7) },
            { 'sign': '<', 'op': '+', 'threshold': 7 - self.rnd.in_range(1, 3), 'start': 7 - self.rnd.in_range(3, 6) }
        ])

        task = self.rnd.pick([
            {
                'val': param, 'ret': param,
                'text': 'Че­му бу­дет рав­на сум­ма всех чи­сел, на­пе­ча­тан­ных на экра­не при вы­пол­не­нии вы­зо­ва',
                'gen_text_block':  self._gen_text_print_block, 'gen_eval_block':  self._gen_eval_print_block, 'print_type': 'num'},
            {
                'val': '*', 'ret': 1,
                'text': 'Сколь­ко сим­во­лов «звёздоч­ка» будет на­пе­ча­та­но на экра­не при вы­пол­не­нии вы­зо­ва',
                'gen_text_block':  self._gen_text_print_block, 'gen_eval_block':  self._gen_eval_print_block, 'print_type': 'str'},
            {
                'val': self.rnd.in_range(2, 5),
                'text': 'Че­му бу­дет рав­но зна­че­ние, вы­чис­лен­ное ал­го­рит­мом при вы­пол­не­нии вы­зо­ва',
                'gen_text_block': self._gen_text_block, 'gen_eval_block': self._gen_eval_block
            }
        ])

        steps = [ self.rnd.in_range(1, 3) for _ in range(1, self.rnd.in_range(3, 4)) ]
        branches = [ [ '()', 'F', [ alg['op'], param, i ] ] for i in steps ]
        branches_call = []
        for branch in branches:
            branches_call.append('expr')
            branches_call.append(branch)
        branches_sum = self._gen_branches_sum(len(branches) - 1, branches)
        args = {
            'param': param, 'value': task['val'], 'sign': alg['sign'],
            'threshold': alg['threshold'], 'branches_call':  branches_call,
            'branches_sum': branches_sum, 'ret': task.get('ret'), 'start': alg['start'],
            'print_type': task.get('print_type')
        }
        self.text = f'''Ниже на че­ты­рех язы­ках про­грам­ми­ро­ва­ния за­пи­сан ре­кур­сив­ный ал­го­ритм F 
{table(task['gen_text_block'](args), [ [ 'Basic', 'Alg' ], [ 'Pascal', 'C' ] ])} 
{task['text']}  F({alg['start']})"'''

        code_block = task['gen_eval_block'](args)
        self.correct = code_block.run_val('M')
        self.accept = r"^-?\d+$"
        return self
