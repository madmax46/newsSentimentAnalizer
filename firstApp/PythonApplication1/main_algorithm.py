import mysql.connector
from TssTerm import TssTerm
import re
import time
import pymorphy2
from datetime import datetime
from threading import Thread, current_thread
#from Thread import start_new_thread
from razdel import tokenize

morph = pymorphy2.MorphAnalyzer()



mydb = mysql.connector.connect(user='root', password='****',
                              host='localhost',
                              database='stockthesaurus')

mydbNewsParsers = mysql.connector.connect(user='root', password='****',
                              host='localhost',
                              database='newsparsers')

limitByLoadNews = int(100)

def parseTerms(myresult):
    """метод парсит термы из представления базы в свой класс TssTerm"""
    listOfTerms = []
    for x in myresult:
        temp = TssTerm()
        temp.id = int(x[0])
        temp.name = str(x[1])
        tokens = list(tokenize(temp.name))
        normalForms = list(map(lambda oneToken: morph.parse(oneToken.text)[0].normal_form,tokens))
        temp.normalForm = normalForms
        listOfTerms.append(temp)
    return listOfTerms

def executeQuery(db, query):
    """метод выполняет запрос к базе и возвращает все данные"""
    mycursor = db.cursor()
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    return myresult

def executeNonQuery(db, query):
    """метод выполняет запрос к базе и возвращает все данные"""
    cursor = db.cursor()
    result = cursor.execute(query)
    db.commit()
    

def executeQueryByCursorFirstRow(db, query):
    """метод выполняет запрос к базе и возвращает только первую строку"""
    mycursor = db.cursor()
    mycursor.execute(query)
    myresult = mycursor.fetchone()
    return myresult

def clearTermsFunc(listTerms:TssTerm):
    """функция очистки термов, для того чтобы они корректно воспринимались регулярными выражениями"""
    for x in listTerms:
        x.name = x.name.replace('.','\.')
    return listTerms


def parseWithStr(parsedNews, listTerms):
    """(устаревшее) метод парсинга термов и поиска их вхождений в переданном тексте новости с помощью стандартного метода для строк find"""
    allNews = list()
    for x in parsedNews:
       findedcount = 0
       tempList = list()
       for oneTerm in listTerms:
           if x[1].lower().find(oneTerm.name.lower()) != -1:
               findedcount+=1
               tempList.append(oneTerm.name)
           allNews.append(x)
    print('end')


def parseWithRegEx(parsedNews, listTerms:TssTerm):
    """(устаревшее) метод парсинга термов и поиска их вхождений в переданном тексте новости с помощью регулярок"""
    allNews = dict()
    for x in parsedNews:
       termsCounter = dict()
       for oneTerm in listTerms:            
           matchf = re.findall(oneTerm.name,x[1],re.IGNORECASE)
           if matchf != []:
               termsCounter[oneTerm] = len(matchf)
       allNews[x] = termsCounter
       print('{}'.format(x[1]))
    print('end')
    return allNews



def get_last_checked_id():
    idNewsStr = executeQueryByCursorFirstRow(mydb,"SELECT MAX(idNews) FROM stockthesaurus.tss_checked_filter_news")[0]
    lastCheckedId = int(0)
    if(idNewsStr != None):
      lastCheckedId = int(idNewsStr)
    return lastCheckedId


#idNewsStr = executeQueryByCursorFirstRow(mydb,"SELECT MAX(idNews) FROM
#stockthesaurus.tss_checked_filter_news")[0]
#lastCheckedId = int(0)
#if(idNewsStr != None):
#  lastCheckedId = int(idNewsStr)
maxNewsId = int(executeQueryByCursorFirstRow(mydbNewsParsers,"SELECT max(id) FROM newsparsers.tass_news")[0])

listOfNews = list()
def get_batch_news():
    global listOfNews
    if len(listOfNews) == 0:
        lastCheckedId = get_last_checked_id()
        listOfNews = list(executeQuery(mydbNewsParsers,'SELECT id, mainText FROM newsparsers.tass_parsed_news where id > {} order by id limit {}'.format(lastCheckedId,limitByLoadNews)))
        lastCheckedId = int(max(listOfNews,key=lambda item:int(item[0]))[0])
    if len(listOfNews) == 0:
        return None
    return listOfNews.pop(0)
        



def find_term_entries_count(tokenizedOneNews, oneTermNormStr:str):
    """функция поиска вхождения одного терма в новости"""
    counter = int(0)
    for oneToken in tokenizedOneNews:
        if oneToken == oneTermNormStr:
            counter +=1
    return counter

def find_multyform_term_entry_count(tokenizedOneNews, oneTerm:TssTerm):
    """функция поиска вхождения одного терма состоящего из нескольких слов в новости"""
    counter = int(0)
    termWords = len(oneTerm.normalForm)
    for iter in range(0,len(tokenizedOneNews) - termWords):
        isAllFinded = True
        for iterTermWords in range(0,termWords):
            if tokenizedOneNews[iter + iterTermWords] != oneTerm.normalForm[iterTermWords]:
                isAllFinded = False
                break
        if isAllFinded == True:
            counter +=1
    return counter     


def find_term_entries_in_one_news(normWord, listTerms:list):
    """функция поиска вхождения одного нормализованного слова из новости в списке одиночных термов"""
    for oneTerm in listTerms:
        if len(oneTerm.normalForm) > 1:
            continue
        if oneTerm.normalForm[0] == normWord:
            return oneTerm
    return None

def find_terms_in_one_parsed_news(normOneNews, listTerms:list):
    """(старая версия) ищет совпадения термов в одной новости"""
    termsCounterDic = dict()
    for oneTerm in listTerms:
        entryCount = 0
        if len(oneTerm.normalForm) > 1:
          entryCount = 0
          hzChtoDelat = True
        else:
            entryCount = find_term_entries_count(normOneNews,oneTerm.normalForm[0])
        if entryCount > 0:
            termsCounterDic[oneTerm] = entryCount

    return termsCounterDic


def find_terms_in_one_parsed_news_other_version(normOneNews, listTerms:list):
    """ищет совпадения термов в одной новости по другому алгоритму"""
    termsCounterDict = dict()
    for oneToken in normOneNews:       #Тут мы проходим по каждому токену из новости, чтобы было меньше
                                       #итераций
        termEntry = find_term_entries_in_one_news(oneToken,listTerms)
        if termEntry == None:
            continue
        else:
             #print('{}'.format(termEntry.name)) #если хочешь вывести все
             #найденные одинарне термы то раскомментируй
             if termsCounterDict.get(termEntry) == None:
                 termsCounterDict[termEntry] = 1
             else: 
                 termsCounterDict[termEntry] += 1
    for oneTerm in listTerms: #Тут мы проходим по каждому терму из базы для
    #поиска термов состоящих
         entryCount = 0 #из нескольких слов
         if len(oneTerm.normalForm) > 1:
             entryCount = find_multyform_term_entry_count(normOneNews,oneTerm)
         else:
             continue
         if entryCount > 0:
             if termsCounterDict.get(oneTerm) == None:
                 termsCounterDict[oneTerm] = entryCount
             else:
                 termsCounterDict[oneTerm] += entryCount
    #for onefinded in termsCounterDict:
    #    print('{} | {}'.format(onefinded.name, termsCounterDict[onefinded]))
    return termsCounterDict



def find_terms_in_batch_parsed_news(parsedNews, listTerms:list):
    """метод парсинга термов и поиска их вхождений в переданном тексте новости с помощью регулярок"""
    allNews = dict()
    for oneNews in parsedNews:
        tokenizedOneNews = list(tokenize(oneNews[1]))
        normolizedNews = list(map(lambda r: morph.normal_forms(r.text)[0],tokenizedOneNews))
        termsCounter = dict()
        #findedInOneNews =
        #find_terms_in_one_parsed_news(normolizedNews,listTerms)
        findedInOneNews = find_terms_in_one_parsed_news_other_version(normolizedNews,listTerms)
        allNews[oneNews] = findedInOneNews
        print('{} succes'.format(oneNews[0]))
    print('end')
    return allNews


def saveNewsAndTermsRelation(newsAndTermsReletions:dict):
    """сохранение в базу связи текста новости с найденными термами"""
    for oneKey in newsAndTermsReletions:
        findedTerms = newsAndTermsReletions[oneKey]
        insert_new_last_checked_id(oneKey[0])
        if(len(findedTerms) == 0):
            continue
        queryInsert = createSqlQuerySaveOneNews(oneKey[0],findedTerms)
        queryDelete = 'delete from tss_news_terms where idNews = {}'.format(oneKey[0])
        executeNonQuery(mydb, queryDelete)
        executeNonQuery(mydb, queryInsert)


def createSqlQuerySaveOneNews(newsId, termsAndCount):
    """создает запрос на вставку связи найденных термов в новости"""
    insertedValues = (','.join(map(lambda x: '({}, {}, {})'.format(newsId,str(x.id),str(termsAndCount[x])),termsAndCount)))
    query = 'insert into tss_news_terms (idNews, idTerm, countEntries) values {};'.format(insertedValues) 
    return query

def insert_new_last_checked_id(lastCheckedId):
    query = 'INSERT INTO tss_checked_filter_news ( idNews) VALUES ({});'.format(lastCheckedId)
    executeNonQuery(mydb, query)




def mainProccesFilteringNews():
    """главный метод поиска термов в новостях"""
    myresult = executeQuery(mydb,"SELECT * FROM tss_terms order by id")
    parsedTerms = parseTerms(myresult)
    clearTerms = clearTermsFunc(parsedTerms)

    idNewsStr = executeQueryByCursorFirstRow(mydb,"SELECT MAX(idNews) FROM stockthesaurus.tss_checked_filter_news")[0]
    lastCheckedId = 0
    if(idNewsStr != None):
        lastCheckedId = int(idNewsStr)

    maxNewsId = int(executeQueryByCursorFirstRow(mydbNewsParsers,"SELECT max(id) FROM newsparsers.tass_news")[0])
    while lastCheckedId < maxNewsId:
        print('{} Берем пачку начиная с id {}'.format(datetime.now(),lastCheckedId))
        newsBatch = executeQuery(mydbNewsParsers,'SELECT id, mainText FROM newsparsers.tass_parsed_news where id > {} order by id limit {}'.format(lastCheckedId,limitByLoadNews))
        newsAndTerms = find_terms_in_batch_parsed_news(newsBatch,clearTerms)
        saveNewsAndTermsRelation(newsAndTerms)
        lastCheckedId = int(max(newsBatch,key=lambda item:int(item[0]))[0])
        print('{} обработали и сохранили пачку максимальный id {}'.format(datetime.now(),lastCheckedId))






#myresult = executeQuery(mydb,"SELECT * FROM tss_terms order by id")
#clearTerms = parseTerms(myresult)
#listTerms2 = clearTermsFunc(clearTerms)
#parsedNews = executeQuery(mydbNewsParsers,"SELECT id, mainText FROM
#newsparsers.tass_parsed_news WHERE id = 757311 order by id limit 10")

#find_terms_in_batch_parsed_news(parsedNews,listTerms2)

#tokens112 = list(tokenize(parsedNews[0][1]))


#for oneToken in tokens112:
#    morphParsed1 = morph.parse(oneToken.text)
#    print('{} | {}'.format(oneToken.text, morphParsed1[0].normal_form))


#morphParsed = morph.parse(parsedNews[0][1])
#print(morphParsed[0].normal_form)
#res1 = executeQueryByCursorFirstRow(mydbNewsParsers,"SELECT max(id)FROM
#newsparsers.tass_news")[0]
#lastCheckedId = int(max(parsedNews,key=lambda item:int(item[0]))[0])


timeStart = time.time()
mainProccesFilteringNews()
timeEnd = time.time()
print('все выполнение заняло {}'.format(timeEnd - timeStart))


tempDot = int(1)
print('Завершение основного процесса проекта, для заверешния нажмите Enter')
input()
