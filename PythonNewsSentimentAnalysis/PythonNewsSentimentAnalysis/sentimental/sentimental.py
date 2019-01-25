import re
import os
import csv
import sys
from collections import defaultdict

from razdel import tokenize

class Sentimental(object):
    def __init__(self, word_list=None, negation=None):
        if word_list is None and negation is None:
            base_dir = os.path.dirname(__file__)
            #word_list = [os.path.join(base_dir, p) for p in
            #['./word_list/afinn.csv', './word_list/russian.csv']]
            ##emo_dict_ANSI.csv
            word_list = [os.path.join(base_dir, p) for p in ['./word_list/afinn.csv', './word_list/emo_dict_ANSI.csv']]
            negation = os.path.join(base_dir, './word_list/negations.csv')

        self.word_list = {}
        self.negations = set()

        for wl_filename in self.__to_arg_list(word_list):
            self.load_word_list(wl_filename)
        for negations_filename in self.__to_arg_list(negation):
            self.load_neagations(negations_filename)

        self.__negation_skip = {'a', 'an', 'so', 'too'}

    @staticmethod
    def __to_arg_list(obj):
        if obj is not None:
            if not isinstance(obj, list):
                obj = [obj]
        else:
            obj = []
        return obj

    def __is_prefixed_by_negation(self, token_idx, tokens):
        #   True if i != 0 and tokens[i - 1] in self.negations else False
        prev_idx = token_idx - 1
        if tokens[prev_idx] in self.__negation_skip:
            prev_idx -= 1

        is_prefixed = False
        if token_idx > 0 and prev_idx >= 0 and tokens[prev_idx] in self.negations:
            is_prefixed = True

        return is_prefixed

    def load_neagations(self, filename):
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            negations = set([row['token'] for row in reader])
        self.negations |= negations

    def load_word_list(self, filename):
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            word_list = {row['word']: float(row['score']) for row in reader}
        self.word_list.update(word_list)

    def analyze(self, sentence):
        #sentence_clean = re.sub(r'[^\w ]', ' ', sentence.lower())
        #tokens = sentence_clean.split()
        list_tokens = list(tokenize(sentence))
        tokens = list(map(lambda x: x.text, list_tokens))
    
        #scores = defaultdict(float)

        scores = defaultdict(list)
        words = defaultdict(list)
        comparative = 0

        for i, token in enumerate(tokens):
            is_prefixed_by_negation = self.__is_prefixed_by_negation(i, tokens)
            if token in self.word_list and not is_prefixed_by_negation:
                score = self.word_list[token]

                if score >= 1:
                    score_type = 'positive'
                else:
                    if score <= -1:
                        score_type = 'negative'
                    else:
                        score_type = 'neutral'   #if score > -1 and score < 1:
            
                    

                #score_type = 'negative' if score <= 1 else 'positive'
                scores[score_type].append(score) 
                words[score_type].append(token)
         
        neu = 0
        pos = 0
        neg = 0

        if len(scores['neutral']) > 0:
            neu = average(scores['neutral'])

        if len(scores['positive']) > 0:
            pos = average(scores['positive'])
        
        if len(scores['negative']) > 0:
            neg = average(scores['negative'])

        allScores = dict()
        allScores['positive'] = pos
        allScores['negative'] = neg
        allScores['neutral'] = neu

        result = {
            'positive': pos,
            'negative': neg,
            'neutral':  neu,
            'allScores' : allScores
        }

        #if len(tokens) > 0:
        #    comparative = (scores['positive'] + scores['negative']) /
        #    len(tokens)
        #    scores['neutral'] = comparative
        #minScore = sys.float_info.max
        #maxScore = sys.float_info.min
        #for oneScore in scores:
        #    if scores[oneScore] < minScore:
        #        minScore = scores[oneScore]
        #    if scores[oneScore] > maxScore:
        #        maxScore = scores[oneScore]

        #for oneScore in scores:
        #    scores[oneScore] = minmax_norm(scores[oneScore],minScore,maxScore)

        #result = {
        #    #'score': scores['positive'] + scores['negative'],
        #    'positive': scores['positive'],
        #    'negative': scores['negative'],
        #    'neutral': scores['neutral'],
        #    'allScores' : scores
        #}




        return result


def minmax_norm(input, min, max):
    norm = (input - min) / (max - min)
    return norm

def average(lst): 
    return sum(lst) / len(lst) 



def main():
    sent = Sentimental(word_list=['./word_list/afinn.csv', './word_list/russian.csv'],
                       negation='./word_list/negations.csv')

    sentences = ['Today is a very good day!',
        'Today is not a bad day!',
        'Today is a bad day!',
        'Сегодня хороший день!',
        'Сегодня не плохой день!',
        'Сегодня плохой день!',
        'во весь западный демократический страна в тот число в сша запрещать реклама табачный и водочный изделие',]

    for s in sentences:
        result = sent.analyze(s)
        print(s, result)


if __name__ == '__main__':
    main()
