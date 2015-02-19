import os
from nbiosearch import Handler, SearchEngine
# from nbiosearch.__main__ import main

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
indexsearch_database = os.path.join(CURRENT_DIR, 'IndexSearch.ISDB')
print(indexsearch_database)
indexsearch_database = os.path.join(CURRENT_DIR, 'FDP-FTU', 'multi_template_6_0.min')
print(indexsearch_database)

# def test_main():
#    assert main([]) == 0


def test_apiversion():
    handler = Handler()
    assert handler._api_version == (1, 8510)
    handler.close()


def test_load_db():

    handler = Handler()
    indexsearch = SearchEngine(handler)
    assert indexsearch.load(indexsearch_database) == True
    handler.close()
    del indexsearch

