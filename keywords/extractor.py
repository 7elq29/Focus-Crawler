from rake_nltk import Rake
from keywords.rake import rake
import operator

"""
TODO: limit keywords noun only.
"""


class KeywordExtractor:

    """
    Each word has at least 3 characters
    Each phrase has at most 3 words
    Each keyword appears in the text at least 2 times
    """
    r = rake.Rake("keywords/rake/SmartStoplist.txt", 3, 3, 2)

    @staticmethod
    def extract(text):
        return KeywordExtractor.r.run(text)

    @staticmethod
    def nltk_extract(text):
        rake = Rake()
        rake.extract_keywords_from_text(text)
        return rake.get_ranked_phrases_with_scores()

if __name__ == "__main__":
    print(KeywordExtractor.nltk_extract(open("../test.txt").read())[:20])

