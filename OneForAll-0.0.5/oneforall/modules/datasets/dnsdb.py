import time
import random
import cloudscraper
from bs4 import BeautifulSoup
from common.query import Query
from config import logger


class DNSdb(Query):
    def __init__(self, domain):
        Query.__init__(self)
        self.domain = self.register(domain)
        self.module = 'Dataset'
        self.source = 'DNSdbQuery'
        self.addr = 'http://www.dnsdb.org/'
        self.url = f'{self.addr}{self.domain}/'

    def get_tokens(self):
        """
        绕过cloudFlare验证并获取taken

        :return: 绕过失败返回None 成功返回tokens
        """
        scraper = cloudscraper.create_scraper()
        scraper.interpreter = 'js2py'
        scraper.proxies = self.get_proxy(self.source)
        scraper.timeout = 10
        try:
            tokens = scraper.get_tokens(self.url)
        except Exception as e:
            logger.log('ERROR', e.args)
            return None
        if len(tokens) != 2:
            return None
        return tokens

    def query(self):
        """
        向接口查询子域并做子域匹配
        """
        tokens = self.get_tokens()
        if not tokens:
            logger.log('ALERT', f'{self.source}模块绕过cloudFlare检查失败')
            return False
        self.cookie = tokens[0]
        self.header = {'User-Agent': tokens[1]}
        self.timeout = 10
        resp = self.get(self.url)
        if not resp:
            return
        if 'index' in resp.text:
            soup = BeautifulSoup(resp.text, features='lxml')
            base = self.addr+self.domain
            urls = list(map(lambda a: base + '/' + a.get('href'),
                            soup.find_all('a')))
            urls = urls[:-1]  # idn域名暂时不考虑
            for url in urls:
                resp = self.get(url)
                if not resp:
                    return
                subdomains = self.match(self.domain, resp.text)
                # 合并搜索子域名搜索结果
                self.subdomains = self.subdomains.union(subdomains)
        else:
            subdomains = self.match(self.domain, resp.text)
            # 合并搜索子域名搜索结果
            self.subdomains = self.subdomains.union(subdomains)

    def run(self):
        """
        类执行入口
        """
        self.begin()
        self.query()
        self.finish()
        self.save_json()
        self.gen_result()
        self.save_db()


def do(domain):  # 统一入口名字 方便多线程调用
    """
    类统一调用入口

    :param str domain: 域名
    """
    query = DNSdb(domain)
    query.run()


if __name__ == '__main__':
    do('example.com')
