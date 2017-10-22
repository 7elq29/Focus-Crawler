from keywords.extractor import KeywordExtractor


class Score:

    @staticmethod
    def get_score(preference, text):
        file_keywords = KeywordExtractor.extract(text)
        if len(file_keywords) == 0:
            return 0
        return sum([(preference.get_score(x[0]) ** 0.5)*x[1] for x in file_keywords if preference.has_word(x[0])]) \
                / (len(file_keywords) ** 2)


