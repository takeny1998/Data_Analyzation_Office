import json
import pandas as pd
import urllib.request

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By as by

from konlpy.tag import Mecab
from collections import Counter


class CultureCrawler:
    
    def __init__(self, web_driv_path):
        # set chrome options to be web browser unvisible
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')

        # set web driver
        self.web_driv = webdriver.Chrome(web_driv_path, options = self.chrome_options)

        
        #메인
        urls = self.selenium()
        self.get_news(urls[0])
        news_df = pd.DataFrame(columns=("Title","Article"))
        for url in urls:
            df = self.get_news(url)
            news_df = pd.concat([news_df, df])

            
        str_article = ""
        for article in news_df['Article']:
            str_article += article
        #형태소분석기 konlp Mecab
        mecab = Mecab()
        nouns = mecab.nouns(str_article)
        clean_words = self.nouns_of_article(nouns)

        top_10 = self.top_nouns(clean_words,10)
        top_200 = self.top_nouns(clean_words,200)
        top_30 = self.top_nouns(clean_words,30)

        top_10 = json.dumps(top_10)
        top_30 = json.dumps(top_30)
        top_200 = json.dumps(top_200)

        # db = DBHandler()
        # db.insert_crawling_data('C', top_10, top_30, top_200)


    #정치 뉴스 들어가기 및 헤드라인 더보기 클릭을 위한 selenium
    def selenium(self):
        theview_url = []

        #문화 뉴스 url
        url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=103'
        self.web_driv.get(url)

        #find 'article find more' button
        cluster_more = self.web_driv.find_element(by.CLASS_NAME, 'cluster_more')

        # click it if it's exist
        if cluster_more is not None:
            cluster_more.click()

        self.web_driv.implicitly_wait(10)

        #뉴스더보기 url_list만들기
        theview_list = self.web_driv.find_elements(by.CLASS_NAME, 'cluster_head_topic > a')

        for theview in theview_list: 
            theview_url.append(theview.get_attribute('href'))            

        print(theview_url)
        self.web_driv.close()
        return theview_url


    #beautifulSoup을 사용해 세부 뉴스 데이터 크롤링
    def get_news(self, url):
        #데이터 프레임 만들기
        news_df = pd.DataFrame(columns=("Title","Article"))
        idx = 0
        
        #해당 뉴스를 들어가 정보 얻기
        search_url = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(search_url,'html.parser')
        links = soup.find_all('dt', {'class':'photo'})
        
        for link in links:
            news_url = link.find('a').get('href')
            news_link = urllib.request.urlopen(news_url).read()
            news_html = BeautifulSoup(news_link, 'html.parser')

            title = news_html.find('h3',{'id':'articleTitle'}).get_text()
            # datetime = news_html.find('span',{'class':'t11'}).get_text()
            article = news_html.find('div',{'id':'articleBodyContents'}).get_text()
            article = article.replace("// flash 오류를 우회하기 위한 함수 추가","")
            article = article.replace("function _flash_removeCallback()","")
            article = article.replace("{}","")
            
            article = article.replace("","")
            article = article.replace("\n","")
            article = article.replace("\t","")
            news_df.loc[idx] = [title, article]
            idx += 1
            
            print("#", end="") 
        return news_df

    #형태소 분석 함수: 명사만 추출
    def tokenize(self, df):
        mecab = Mecab()
        return mecab.nouns(df)
        
    #불용어 제거 함수
    def nouns_of_article(self, result):
        # 한글 불용어 리스트 불러오기 시작
        stopwords = []
        clean_words = []

        with open('/mnt/crawling/한글불용어.txt', 'r', encoding='utf8') as f:
            stopwords = f.read().split('\n')
        
        for word in result: 
            if word not in stopwords: #불용어 제거
                clean_words.append(word)
        
        return clean_words

    #top--10명사를 추출 
    def top_nouns(self, clean_words, top_num):
        count = Counter(clean_words)
        top_nouns = count.most_common(top_num)

        return top_nouns



c = CultureCrawler('/mnt/crawling/chromedriver')