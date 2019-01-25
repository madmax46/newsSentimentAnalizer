# -*- coding: utf-8 -*-
#import sys; sys.setdefaultencoding('utf-16-be')
# sys.setdefaultencoding() does not exist, here!
#sys.setdefaultencoding('UTF8')
import mysql.connector
import sentimental
#from TssTerm import TssTerm
import re
import time
import pymorphy2
from datetime import datetime
from threading import Thread, current_thread
#from Thread import start_new_thread
from razdel import tokenize
from sentimental import Sentimental

morph = pymorphy2.MorphAnalyzer()

sent = Sentimental()

limitNews = 100
minCountEntries = 10

tss_db = mysql.connector.connect(user='root', password='28Q{f6NA!r',
                              host='localhost',
                              database='stockthesaurus')

mydbNewsParsers = mysql.connector.connect(user='root', password='28Q{f6NA!r',
                              host='localhost',
                              database='newsparsers')


def executeQuery(db, query):
    """метод выполняет запрос к базе и возвращает все данные"""
    mycursor = db.cursor()
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    return myresult

def executeNonQuery(db, query):
    """метод выполняет запрос к базе и возвращает все данные"""
    db.connect()
    mycursor = db.cursor()
    result = mycursor.execute(query)
    db.commit()


def oneIterSentimentAnalysis():
    """загрузка пачки новостей и их анализ"""
    global tss_db
    lastId = 0
    maxVal = executeQuery(tss_db,"SELECT Max(idNews) FROM stockthesaurus.senty_results")[0][0]
    if maxVal is not None:
        lastId = int(maxVal)

    newsIds = list() #из базы вытягивеам идентификаторы подходящих новостей
    fetchedNewsIds = executeQuery(tss_db, "call GetNewsForSentimentAnalyse({},{},{})".format(lastId,limitNews,minCountEntries))
    if len(fetchedNewsIds) > 0:
        newsIds = list(map(lambda x: int(x[0]), fetchedNewsIds))
    else:
        return None
    
    txtIds = (','.join(list(map(lambda x: str(x), newsIds))))
    newsBatch = executeQuery(mydbNewsParsers,'SELECT id, mainText FROM newsparsers.tass_parsed_news where id in ({})'.format(txtIds))

    if len(newsBatch) == 0:
        return None

    dictResAnalysisNews = dict()
    for oneNews in newsBatch:
        sentence = oneNews[1]
        result = sent.analyze(sentence)
        #print(result)
        dictResAnalysisNews[oneNews[0]] = result
    query = create_sql_query_insert_analysis_res(dictResAnalysisNews)
    executeNonQuery(tss_db,query)
    print(query)
    print(query)
    return True


def sentimentAnalysisMain():
    """основной метод анализа новостей"""
    resultAnalysis = True
    while resultAnalysis == True:
        resultAnalysis = oneIterSentimentAnalysis()


def create_sql_query_insert_analysis_res(dictResAnalysisNews:dict):
    """метод генерирует из результатов анализа sql запрос на сохранение"""
    listInsertedValues = list()
    for oneKey in dictResAnalysisNews:
        res = dictResAnalysisNews[oneKey]['allScores']
        listInsertedValues.append('({},{},{},{})'.format(oneKey,res['positive'],res['negative'],res['neutral']))

    insertedValues = (','.join(listInsertedValues))
    query = 'INSERT INTO senty_results (idNews, positiveValue, negativeValue, neutralValue) VALUES {} ON DUPLICATE KEY UPDATE positiveValue = VALUES(positiveValue), negativeValue = VALUES(negativeValue), neutralValue = VALUES(neutralValue);'.format(insertedValues)
    return query



sentimentAnalysisMain()


result = sent.analyze(sentence)
    
input()
