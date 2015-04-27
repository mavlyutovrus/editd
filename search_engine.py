from simple_trie import TSimpleTrie
import sys

def tokenize(string):
    import re
    words = re.findall("http://[a-zA-Z.\/0-9_\-&?=]+|[a-zA-Z0-9&_\-]+", string)
    words = [word.lower() for word in words]
    return words

class TSearchEngine():
    def __init__(self, csv):
        self.TokenIndex = TSimpleTrie()
        self.WordFreq = {}
        self.Id2Data = {}
        self.Upload__(csv)

    def Search(self, query):
        ids = self.SearchMatchingIds__(query)
        ids_by_score = self.Rank__(ids, query)
        ids_by_score.sort(reverse=True)
        ids_by_score = ids_by_score[:10]
        snippets = []
        for score, id in ids_by_score:
            title, brand = self.Id2Data[id]
            snippets.append("%f,%d,%s,%s" % (score, id, title, brand))
        return snippets

    def Rank__(self, ids, query):
        query_words = tokenize(query)
        ids_by_score = []
        for id in ids:
            title, brand = self.Id2Data[id]
            title_words = tokenize(title)
            brand_words = tokenize(brand)
            
            #length score
            total_length = len(title_words) + len(brand_words)
            score_length = len(query_words) / float(total_length)
            
            if len(query_words) == 1 or total_length <= 2:
                ids_by_score += [(score_length, id)]
                continue
            
            #order score
            matched_bigrams = 0
            for q_start in xrange(len(query_words) - 1):
                for t_start in xrange(len(title_words) - 1):
                    if title_words[t_start].startswith(query_words[q_start]) and \
                            title_words[t_start + 1].startswith(query_words[q_start + 1]):
                        matched_bigrams += 1
                for b_start in xrange(len(brand_words) - 1):
                    if brand_words[b_start].startswith(query_words[q_start]) and \
                            brand_words[b_start + 1].startswith(query_words[q_start + 1]):
                        matched_bigrams += 1
            max_matched_bigrams = len(title_words) + len(query_words) - 2
            
            score_order = matched_bigrams / float(max_matched_bigrams)
            score = (score_length + score_order) / 2
            ids_by_score += [(score, id)]
        return ids_by_score
    
    def SearchMatchingIds__(self, query): 
        words = tokenize(query)   
        if not words:
            return []
        for word in words:
            if not word in self.WordFreq:
                print word
                return 0
        if "least frequent first":
            words = [(self.WordFreq[word], word) for word in words]
            words.sort()
            words = [word for _, word in words]
        #search
        matching_ids = set(self.TokenIndex.GetAllValuesInSubtree(words[0]))   
        for word in words[1:]:
            if not matching_ids:
                break
            word_ids = set(self.TokenIndex.GetAllValuesInSubtree(word))
            matching_ids &= word_ids
        return matching_ids        
    

        
    def Add2Index__(self, id, brand, title):
        words = set(tokenize(brand) + tokenize(title))
        for word in words:
            for length in xrange(1, len(word) + 1):
                self.WordFreq.setdefault(word[:length], 0)
                self.WordFreq[word[:length]] += 1 
            self.TokenIndex.Insert(word, id)
            
    def Upload__(self, csv):
        for line in open(csv):
            try:
                chunks = line.decode("utf8")[:-1].split(",")
                id = int(chunks[0])
                brand = chunks[-1]
                title = ",".join(chunks[1:-1])                
            except:
                raise ValueError('wrong csv line format', line)
            self.Id2Data[id] = (title, brand)
            self.Add2Index__(id, brand, title)





