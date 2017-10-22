import newspaper, re, io
from lxml import etree


class Article(newspaper.Article):

    def __init__(self, url):
        super().__init__(url)
        self.links = []

        # build domain
        match = re.search('https?://[\w.]+', self.url)
        if not match:
            raise RuntimeError("Cannot parse domain of url {}".format(self.url))
        self.domain = match.group(0)

    def parse(self):
        super().parse()
        # build links
        parser = etree.HTMLParser()
        urls = etree.parse(io.StringIO(self.html), parser).xpath('//a/@href')
        for url in urls:
            if url.startswith('#') or url.startswith('?'):
                continue
            elif url.startswith('//'):
                # TODO do somthing
                continue
            match = re.search('[^#?]+', url)
            url = match.group(0) if match else None
            if url:
                self.links.append(self._compose_url(url))

    def _compose_url(self, url):
        if re.match('https?://+?', url):
            return url
        else:
            return self.domain+url if url.startswith('/') else self.domain+"/"+url


if __name__ == '__main__':
    article = Article('https://en.wikipedia.org/wiki/Main_Page')
    article.download()
    article.parse()
    print(article.links)

