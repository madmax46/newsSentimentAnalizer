
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



def mainProccesFilteringNews():
    """главный метод поиска термов в новостях"""
    lastCheckedId = get_last_checked_id()
    myresult = executeQuery(mydb,"SELECT * FROM tss_terms order by id")
    parsedTerms = parseTerms(myresult)
    clearTerms = clearTermsFunc(parsedTerms)

    maxNewsId = int(executeQueryByCursorFirstRow(mydbNewsParsers,"SELECT max(id) FROM newsparsers.tass_news")[0])
    while lastCheckedId < maxNewsId:
        print('{} Берем пачку начиная с id {}'.format(datetime.now(),lastCheckedId))
        newsBatch = get_batch_news()
        if newsBatch == None:
            return
      
        newsBatchlist = list()
        newsBatchlist.append(newsBatch)
        newsAndTerms = find_terms_in_batch_parsed_news(newsBatchlist,clearTerms)
        saveNewsAndTermsRelation(newsAndTerms)
        lastCheckedId = int(max(newsBatchlist,key=lambda item:int(item[0]))[0])
        print('{} обработали и сохранили пачку максимальный id {}'.format(datetime.now(),lastCheckedId))
