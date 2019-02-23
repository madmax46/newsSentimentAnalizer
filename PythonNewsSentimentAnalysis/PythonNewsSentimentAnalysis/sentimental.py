import re
import os
import csv
import sys
from collections import defaultdict
import pymorphy2
from razdel import tokenize

morph = pymorphy2.MorphAnalyzer()


class Sentimental(object):
    def __init__(self, dataRow, negation):
       
        self.single_word_list = {}
        self.multi_word_list = list()

        self.negations = set()
      

        res = self.convert_to_word_list(dataRow)
        self.single_word_list = res[0]
        self.multi_word_list = res[1]



        self.__negation_skip = {}
     
        
    def convert_to_word_list(self, dataRow):
        """Преобразует таблицу в словарь в памяти программы"""
        singlLemmaWords = dict()
        multiLemmaWords = list()

        for oneRow in dataRow:
            lemmatizied = oneRow[3]
            tokenizedValues = lemmatizied.split(sep=' ')
            if len(tokenizedValues) == 1:
                singlLemmaWords[tokenizedValues[0]] = {'score':float(oneRow[2]), 'id':int(oneRow[0]), 'row': oneRow}
            else:
                multiLemmaWords.append({'lemmas': tokenizedValues,'score':float(oneRow[2]), 'id':int(oneRow[0]), 'row':  oneRow})
        return (singlLemmaWords,multiLemmaWords)

    def find_multyform_term(self,tokenizedOneNews, oneTerm):
        """функция поиска вхождения одного терма состоящего из нескольких слов в новости"""
        counter = int(0)
        listTokens = list()
        termWords = len(oneTerm['lemmas'])
        onlyTextList = list(map(lambda x: x.text,tokenizedOneNews))
        if oneTerm['lemmas'][0] not in onlyTextList: 
            return (0,listTokens)
        for iter in range(0,len(tokenizedOneNews) - termWords + 1):
            isAllFinded = True
            for iterTermWords in range(0,termWords):
                if tokenizedOneNews[iter + iterTermWords].text != oneTerm['lemmas'][iterTermWords]:
                    isAllFinded = False
                    break
            if isAllFinded == True:
                listTokens.append({'id':oneTerm['id'] , 'word':' '.join(oneTerm['lemmas']),  'start':tokenizedOneNews[iter].start, 'stop': tokenizedOneNews[iter + termWords - 1].stop})

                #for jiter in range(0,termWords):
                    #listTokens.append({'id':oneTerm['id'] ,
                    #'word':tokenizedOneNews[iter + jiter].text,
                    #'start':tokenizedOneNews[iter + jiter].start, 'stop':
                    #tokenizedOneNews[iter + jiter].stop})
                    #listTokens.append(tokenizedOneNews[iter + jiter])
                counter +=1

        return (counter,listTokens)    
    
    def determine_range_name(self,score):
        score_type = 'neutral'
        if score >= 1:
           score_type = 'positive'
        else:
            if score <= -1:
                score_type = 'negative'
            else:
                score_type = 'neutral'
        return score_type

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
        if tokens[prev_idx].text in self.__negation_skip:
            prev_idx -= 1

        is_prefixed = False
        if token_idx > 0 and prev_idx >= 0 and tokens[prev_idx].text in self.negations:
            is_prefixed = True

        return is_prefixed

    def load_neagations(self, filename):
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            negations = set([row['token'] for row in reader])
        self.negations |= negations

        
        


    def analyze(self, sentence):
        list_tokens = list(tokenize(sentence))
        #tokens = list(map(lambda x: morph.normal_forms(x.text)[0],
        #list_tokens))
        for oneToken in list_tokens:
            oneToken.text = morph.normal_forms(oneToken.text)[0]
    
        scores = defaultdict(list)
        words = list()
        for i, token in enumerate(list_tokens):
            is_prefixed_by_negation = self.__is_prefixed_by_negation(i, list_tokens)
            #if token in self.word_list and not is_prefixed_by_negation:
            if token.text in self.single_word_list:
                findedRow = self.single_word_list[token.text]
                score = findedRow['score'] 
                score_type = self.determine_range_name(score)
                               
                scores[score_type].append(score) 
                scores['all'].append(score) 
                words.append({'id':findedRow['id'] , 'word':token.text,  'start':token.start, 'stop': token.stop})
        
        for i, term in enumerate(self.multi_word_list):
            entries = self.find_multyform_term(list_tokens,term)
            if entries[0] > 0:
                score = term['score']
                score_type = self.determine_range_name(score)
                scores[score_type].append(score) 
                scores['all'].append(score)
                for oneEntry in entries[1]:
                    words.append(oneEntry)


        neu = 0
        pos = 0
        neg = 0
        resEval = 0

        if len(scores['neutral']) > 0:
            neu = average(scores['neutral'])

        if len(scores['positive']) > 0:
            pos = average(scores['positive'])
        
        if len(scores['negative']) > 0:
            neg = average(scores['negative'])

        if len(scores['all']) > 0:
            resEval = average(scores['all'])

        allScores = dict()
        allScores['positive'] = pos
        allScores['negative'] = neg
        allScores['neutral'] = neu
        allScores['resEval'] = resEval

        result = {
            'positive': pos,
            'negative': neg,
            'neutral':  neu,
            'resEval':  resEval,
            'allScores' : allScores,
            'allWords' : words
        }
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
