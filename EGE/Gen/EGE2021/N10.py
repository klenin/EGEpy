from EGE.GenBase import DirectInput
from collections import Counter, defaultdict
from random import choices
import re


class FindSubstringInText(DirectInput):
    model = None
    
    def generate(self):

        sentences_n = self.rnd.in_range(1000, 2000)
        full_file_text = self._generate_text(sentences_n)

        filename = 'N10_text.txt'

        with open(filename, 'w') as fout:
            fout.write(full_file_text)

        words = re.findall(r"[а-яА-Я]+", full_file_text)
        unique_words = Counter(words)
        rand_n = self.rnd.in_range(1, 100)
        substring, cnt = unique_words.most_common(rand_n)[rand_n - 1]
        
        text = f"""\
                    В файле <a href="{filename}" download="{filename}">{filename}</a> приведен текст, сгенерированный на основе произведений Льва Толстого.
                    Необходимо найти количество вхождений слова "{substring}".
                    """
        self.text = '\n'.join([line.strip() for line in text.split('\n') if line.strip() != ''])
        self.correct = cnt
        self.accept_number()
        
        return self
    
    def _generate_text(self, sentences_n):
        if self.model == None:
            self.model = TrigramModel().train('EGE/Gen/EGE2021/data/tolstoy.txt')

        result = self.model.generate_text(sentences_n)

        return result
    
class TrigramModel():

    model = {}
    allowed_template = re.compile(u'[а-яА-Я-]+|[.,:;?!]+')
    stop_symbol = '$'
    sentence_end = '.!?'
    punctuation = '.!?,;:'

    def train(self, corpus_file_path):
        trigrams = self.get_trigrams(corpus_file_path)

        bi, tri = defaultdict(lambda: 0.0), defaultdict(lambda: 0.0)

        for t0, t1, t2 in trigrams:
            bi[t0, t1] += 1
            tri[t0, t1, t2] += 1

        for (t0, t1, t2), freq in tri.items():
            if (t0, t1) in self.model:
                self.model[t0, t1].append((t2, freq / bi[t0, t1]))
            else:
                self.model[t0, t1] = [(t2, freq / bi[t0, t1])]

        return self
    
    def get_trigrams(self, corpus_file_path):
        lines = self.extract_lines(corpus_file_path)
        tokens = self.extract_tokens(lines)
        return self.extract_trigrams(tokens)
    
    def extract_lines(self, corpus_file_path):
        data = open(corpus_file_path)
        return [line.lower() for line in data]

    def extract_tokens(self, lines):
        return [token for line in lines for token in self.allowed_template.findall(line)]

    def extract_trigrams(self, tokens):
        t0, t1 = self.stop_symbol, self.stop_symbol
        trigrams = []

        for t2 in tokens:
            trigrams.append([t0, t1, t2])
            if t2 in self.sentence_end:
                trigrams.append([t1, t2, self.stop_symbol])
                trigrams.append([t2, self.stop_symbol, self.stop_symbol])
                t0, t1 = self.stop_symbol, self.stop_symbol
            else:
                t0, t1 = t1, t2
        
        return trigrams
    
    def generate_sentence(self):
        sentence = ''
        t0, t1 = self.stop_symbol, self.stop_symbol

        while 1:
            t0, t1 = t1, self.random_choice(self.model[t0, t1])

            if t1 == self.stop_symbol: break

            if t1 in (self.punctuation) or t0 == self.stop_symbol:
                sentence += t1
            else:
                sentence += ' ' + t1

        return sentence.capitalize()
    
    def random_choice(self, tokens_and_freqs):
        tokens, freqs = list(zip(*tokens_and_freqs))
        return choices(tokens, weights=freqs, k=1)[0]
    
    def generate_text(self, sentences_n):
        return '\n'.join([self.generate_sentence() for i in range(sentences_n)])


