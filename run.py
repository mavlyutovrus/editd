from search_engine import TSearchEngine
import sys

if __name__ == '__main__':
    search_engine = TSearchEngine("search_dataset.csv")
    for line in sys.stdin:
        query = line.decode("utf8")
        snippets = search_engine.Search(query)
        print len(snippets)
        for snippet in search_engine.Search(query):
            print snippet.encode("utf8")         
      
