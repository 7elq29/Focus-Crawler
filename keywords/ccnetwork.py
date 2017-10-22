"""
Co-occurrence network
"""
from keywords.extractor import KeywordExtractor
from pathlib import Path
from collections import deque


class CCNetwork:

    _instance = None
    network = {}

    """
    TODO: make text_queue thread safe
    """
    @staticmethod
    def build(text_queue: deque):
        while len(text_queue) > 0:
            text = text_queue.popleft()
            keywords = KeywordExtractor.extract(text)
            for keyword, score in keywords:
                if keyword not in CCNetwork.network:
                    CCNetwork.network.setdefault(keyword, {"_": score})
                else:
                    CCNetwork.network[keyword]["_"] += score
                for coocur, coscore in keywords:
                    CCNetwork.network[keyword][coocur] = (CCNetwork.network[keyword].setdefault(coocur, 0)+coscore) \
                        if coocur != keyword else 0

    def get_coocurrence(self, keyword, limit=None):
        if keyword not in CCNetwork.network:
            return []
        else:
            buffer = [(k, v) for k, v in CCNetwork.network[keyword].items() if k != "_"]
            buffer.sort(key=lambda x: x[1], reverse=True)
            print(len(buffer))
            return buffer[:limit] if limit else buffer

    def exist(self, keyword):
        return keyword in CCNetwork.network


