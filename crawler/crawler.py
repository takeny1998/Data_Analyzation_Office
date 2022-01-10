import json
import pandas as pd
import urllib.request


from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By as by
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from konlpy.tag import Mecab
from collections import Counter

from database.db_handler import DBHandler
import time

class Crawler:
    BASE_URL = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1='
    keywords = {
        'POLITICAL': '100',
        'ECONOMY': '101',
        'SOCIAL': '102',
        'LIFE/CULTURE': '103',
        'WORLD': '104',
        'IT/SCIENCE': '105'
    }

    def __init__(self, keyword):
        # set chrome options to be web browser unvisible
        self.__chrome_options = webdriver.ChromeOptions()
        self.__chrome_options.add_argument('--headless')
        self.__chrome_options.add_argument('--no-sandbox')
        self.__chrome_options.add_argument('--disable-dev-shm-usage')


        service = Service(ChromeDriverManager().install())
        # set web driver
        web_driv = webdriver.Chrome(service=service, options = self.__chrome_options)
        
        # pre-precessing(ex. click 'find more button')
        # and get url list from headline news page
        urls = self.__pre_processing(web_driv, str.upper(keyword))
        
        web_driv.close()

        articles_str = self.__process(urls)
        self.__clean_words = self.__analyze_morpheme(articles_str)

    #Pre-processing news pages using selenium
    def __pre_processing(self, web_driv, keyword):
        headline_urls = []
        
        url = f'{self.BASE_URL}{self.keywords[keyword]}'

        #문화 뉴스 url
        web_driv.get(url)

        #find 'article find more' button
        cluster_more = web_driv.find_elements(by.CLASS_NAME, 'cluster_more')

        # click it if it's exist
        if len(cluster_more) > 0:
            cluster_more[0].click()

        web_driv.implicitly_wait(10)

        headline_links = web_driv.find_elements(by.CLASS_NAME, '_persist a')

        for headline_link in headline_links: 
            headline_url = headline_link.get_attribute('href')
            headline_urls.append(headline_url)

        return headline_urls


    def __process(self, urls):
        news_df = pd.DataFrame(columns=("Title","Article"))
        
        for url in urls:
            df = self.__get_news(url)
            news_df = pd.concat([news_df, df])
            
        articles_str = ""
        for article_str in news_df['Article']:
            articles_str += article_str
        
        return articles_str


    #beautifulSoup을 사용해 세부 뉴스 데이터 크롤링
    def __get_news(self, url):
        #데이터 프레임 만들기
        news_df = pd.DataFrame(columns=("Title","Article"))
        
        #해당 뉴스를 들어가 정보 얻기
        search_url = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(search_url,'html.parser')
        links = soup.find_all('dt', {'class':'photo'})
        
        for link in links:
            news_url = link.find('a').get('href')
            news_link = urllib.request.urlopen(news_url).read()
            news_html = BeautifulSoup(news_link, 'html.parser')

            title = news_html.find('h3',{'id':'articleTitle'}).get_text()
            article = news_html.find('div',{'id':'articleBodyContents'}).get_text()
            article = article.replace("// flash 오류를 우회하기 위한 함수 추가","")
            article = article.replace("function _flash_removeCallback()","")
            article = article.replace("{}","")
            
            article = article.replace("","")
            article = article.replace("\n","")
            article = article.replace("\t","")

            row = {'Title': title, 'Article': article}
            news_df = news_df.append(row, ignore_index=True)
            
        return news_df

    def __analyze_morpheme(self, articles):
        mecab = Mecab()
        nouns = mecab.nouns(articles)
        clean_words = self.__nouns_of_article(nouns)
        return clean_words

    #불용어 제거 함수
    def __nouns_of_article(self, result):
        # 한글 불용어 리스트 불러오기 시작
        stopwords = []
        clean_words = []

        with open('/mnt/crawling/한글불용어.txt', 'r', encoding='utf8') as f:
            stopwords = f.read().split('\n')
        
        for word in result: 
            if word not in stopwords: #불용어 제거
                clean_words.append(word)
        return clean_words

    def nouns(self):
        top_nouns = Counter(self.__clean_words)

        return json.dumps(top_nouns, ensure_ascii=False)
        
    def top_nouns(self, top_num):
        count = Counter(self.__clean_words)
        top_nouns = count.most_common(top_num)

        return json.dumps(top_nouns, ensure_ascii=False)

if __name__ == '__main__':
        
    start = time.time()  # 시작 시간 저장
    political = Crawler('POLITICAL')
    economy = Crawler('ECONOMY')
    social = Crawler('SOCIAL')
    life_cluture = Crawler('LIFE/CULTURE')
    world = Crawler('WORLD')
    it_science = Crawler('IT/SCIENCE')

    p_json = political.nouns()
    e_json = economy.nouns()
    s_json = social.nouns()
    c_json = life_cluture.nouns()
    w_json = world.nouns()
    i_json = it_science.nouns()

    db_handler = DBHandler()
    db_handler.insert_crawling_data('P', p_json)
    db_handler.insert_crawling_data('E', e_json)
    db_handler.insert_crawling_data('S', s_json)
    db_handler.insert_crawling_data('C', c_json)
    db_handler.insert_crawling_data('W', w_json)
    db_handler.insert_crawling_data('I', i_json)
    db_handler.close()
    print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간