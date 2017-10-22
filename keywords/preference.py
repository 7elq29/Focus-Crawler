from keywords.ccnetwork import CCNetwork


class Preference:

    def __init__(self, network):
        self.keywords = []
        self.co_occurrence = {}
        self.ccnetwork = network

    def prefer(self, keyword):
        keyword = keyword.lower()
        if keyword in self.keywords:
            return
        self.keywords.append(keyword)
        for word, score in self.ccnetwork.get_coocurrence(keyword):
            if word == '_':
                self.co_occurrence[keyword] = self.co_occurrence.get(keyword, 0) + score
            else:
                self.co_occurrence[word] = self.co_occurrence.get(word, 0) + score

    def get_score(self, keyword):
        return self.co_occurrence[keyword]

    def has_word(self, keyword):
        return keyword in self.co_occurrence

    def top(self, limit=20):
        keys = [key for key in self.co_occurrence]
        sorted(keys, key=lambda x: self.co_occurrence[x], reverse=True)
        return keys[:limit]



