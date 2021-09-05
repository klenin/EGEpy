
from collections import Counter

class EGEError(Exception):
    pass

class Question:

    def __init__(self, rnd, text: str = None, correct = None):
        self.rnd = rnd
        self.text = text
        self.correct = correct

    def post_process():
        pass

    def export_type():
        raise EGEError()


class SingleChoice(Question):

    def __init__(self, rnd, text: str = None, correct: int = 0):
        super().__init__(rnd, text, correct)
        self.variants = []

    def export_type(self):
        return 'sc'

    def set_variants(self, variants):
        self.variants = variants
        return self

    def set_formatted_variants(self, format: str, args):
        self.variants = [ format % a for a in args ]
        return self

    def check_distinct_variants(self):
        duplicates = [ v for v, cnt in Counter(self.variants).items() if cnt > 1 ]
        if duplicates:
            raise EGEError(f"Duplicate variants: {', '.join(duplicates)}")

    def shuffle_variants(self):
        if not self.variants:
            raise EGEError()
        permutation = self.rnd.shuffle(list(range(len(self.variants))))
        self.correct = permutation.index(self.correct)
        self.variants = [ self.variants[i] for i in permutation ]

    def post_process(self):
        self.check_distinct_variants()
        self.shuffle_variants()

