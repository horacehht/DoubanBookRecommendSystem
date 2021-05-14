import requests
import re
from lxml import etree
from bs4 import BeautifulSoup


class CrawlBook:
    def __init__(self, res):
        try:
            self.soup = BeautifulSoup(res.text, 'lxml')
            self.html = etree.HTML(res.text)
            self.data = dict()
            self.get_book_name()
            self.get_author()
            self.data.setdefault('author', '')
            self.get_many()
            self.data.setdefault('出版社:', '')
            self.data.setdefault('出版年:', '')
            self.data.setdefault('页数:', '0')
            self.data.setdefault('定价:', '')
            self.data.setdefault('ISBN:', '')
            self.get_score()
            self.data.setdefault('score', 0.0)
            self.get_rating_num()
            self.data.setdefault('rating_num', 0)
            self.get_content()
            self.data.setdefault('content_introduction', '')
            self.get_image()
            self.get_readers()
            self.data.setdefault('readers', '[]')
        except Exception as e:
            print(e)

    def get_book_name(self):
        book_name = self.soup.find(name='span', attrs={'property': 'v:itemreviewed'}).string
        self.data.setdefault('book_name', book_name)

    def get_author(self):
        author = self.soup.find(name='span', text=re.compile('.*?作者.*?')).next_sibling.next_sibling\
            .string.replace('\n', '').replace(' ', '')
        self.data.setdefault('author', author)

    def get_many(self):
        want_to_spider = ['出版社:', '出版年:', '页数:', '定价:', 'ISBN:']
        for i in self.soup.find_all(name='span', attrs={'class': 'pl'}):
            if i.string in want_to_spider:
                self.data.setdefault(i.string, i.next_sibling.replace(' ', ''))

    def get_score(self):
        score = float(self.soup.find(name='strong', attrs={'property': 'v:average'}).string)
        self.data.setdefault('score', score)

    def get_rating_num(self):
        rating_num = int(self.soup.find(name='span', attrs={'property': 'v:votes'}).string)
        self.data.setdefault('rating_num', rating_num)

    def get_content(self):
        l = ''
        try:
            for i in self.soup.find(name='div', attrs={'class': 'intro'}).contents:
                l += str(i)
            self.data.setdefault('content_introduction', l.strip())
        except Exception as e:
            print(e)
            self.data.setdefault('content_introduction', '')

    def get_image(self):
        image_url = self.soup.find(name='img', attrs={'rel': 'v:photo'})['src']
        self.data.setdefault('cover_url', image_url)

    def get_readers(self):
        readers = str(self.html.xpath('//*[@id="collector"]//div/div[2]/a/@href'))
        self.data.setdefault('readers', readers)