from spider.bloom_filter import BloomFilter
from spider.article import Article


class FocusSpider:

    # TODO make bf shared by multiple processes
    bf = BloomFilter(500000, 10)

    def __init__(self):
        pass

    def parse(self, url):
        article = Article(url)
        article.download()
        article.parse()
        if __debug__:
            print("Crawling {}".format(article.url))
        links = []
        for link in article.links:
            if FocusSpider.bf.set(link):
                links.append(link)
        return links


if __name__ == '__main__':
    spider = FocusSpider()
    spider.parse('https://en.wikipedia.org/wiki/Main_Page')







