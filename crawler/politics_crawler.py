import requests
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote
from datetime import date, datetime
from selenium import webdriver
from konlpy.tag import Mecab
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import font_manager, rc
from PIL import Image
import numpy as np


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

#정치 뉴스 들어가기 및 헤드라인 더보기 클릭을 위한 selenium
def selenium():
    wd = webdriver.Chrome('/mnt/crawling/chromedriver',options=chrome_options)
    #정치 뉴스 url
    url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100'
    wd.get(url)

    #헤드라인뉴스 더보기 클릭
    date = wd.find_element_by_class_name('lnb_date').text
    date = '2021' + date
    date = date.replace(".","")
    date = date[:8]
    
    wd.find_element_by_class_name('cluster_more').click()
    wd.implicitly_wait(10)


    #뉴스더보기 url_list만들기
    theview_url = []
    theview_list = wd.find_elements_by_class_name('cluster_foot_inner > a')
    for theview in theview_list: 
        theview_url.append(theview.get_attribute('href'))                                                                                        

    wd.close()
    return theview_url,date


#beautifulSoup을 사용해 세부 뉴스 데이터 크롤링
def get_news(url):
    #데이터 프레임 만들기
    news_df = pd.DataFrame(columns=("Title","Article"))
    idx = 0
    
    #관련뉴스 더보기를 들어간 후 세부뉴스 url 열기
    search_url = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(search_url,'html.parser')
    links = soup.find_all('dt', {'class':'photo'})
    
    for link in links:
        news_url = link.find('a').get('href')
        
        news_link = urllib.request.urlopen(news_url).read()
        news_html = BeautifulSoup(news_link, 'html.parser')

        title = news_html.find('h3',{'id':'articleTitle'}).get_text()
        datetime = news_html.find('span',{'class':'t11'}).get_text()
        datetime = datetime.replace(".","")
        date = datetime[:8]
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
def tokenize(df):
    mecab = Mecab()
    return mecab.nouns(df)
    
#불용어 제거 함수
def nouns_of_article(result):
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
def top_nouns(clean_words, top_num):
    count = Counter(clean_words)
    top_nouns = count.most_common(top_num)

    return top_nouns

#wordcloud만드는 함수
def wordcloud(date,top_keyword):
    icon = Image.open('/mnt/crawling/images/politics.png')
    mask = Image.new("RGB", icon.size, (255,255,255))
    mask.paste(icon,icon)
    mask = np.array(mask)
    wc = WordCloud(font_path="/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf",\
                                background_color="white", \
                                width=800, \
                                height=600,\
                                max_words=100,\
                                max_font_size=300,\
                                mask = mask)   
                                 
    wc.generate_from_frequencies(dict(top_keyword))
    wc.to_file('/mnt/result/Politics/{}-W.png'.format(date))


#matplot으로 그래프 그리는 함수 
def showGraph(date,top_keyword):
    nouns_dict = dict(top_keyword)
    print(nouns_dict)
    
    font_path = "/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf"
    font_name = font_manager.FontProperties(fname=font_path).get_name()

    matplotlib.rc('font',family=font_name)
    plt.xlabel('주요 단어')
    plt.ylabel('빈도수')

    Sorted_Dict_Values = sorted(nouns_dict.values(), reverse=True)
    Sorted_Dict_Keys = sorted(nouns_dict, reverse=True)

    plt.bar(range(len(nouns_dict)), Sorted_Dict_Values, align='center')
    plt.xticks(range(len(nouns_dict)), list(Sorted_Dict_Keys), rotation='70')

    plt.savefig('/mnt/result/Politics/{}-G.png'.format(date))


#메인
urls , date = selenium()

date = date.strip()
news_df = pd.DataFrame(columns=("Title","Article"))
for url in urls:
    df = get_news(url)
    news_df = pd.concat([news_df, df])

str_article = ""
for article in news_df['Article']:
    str_article += article

#형태소분석기 konlp Mecab
mecab = Mecab()
nouns = mecab.nouns(str_article)
clean_words = nouns_of_article(nouns)

top = 60 #상위 몇개의 명사를 추출할지 정하는 변수
top_10 = top_nouns(clean_words,10)
top_200 = top_nouns(clean_words,200)
top_30 = top_nouns(clean_words,30)


 #키워드 링크 보여줌
top_10 = pd.DataFrame.from_dict(top_10)
top_10.to_csv('/mnt/result/Politics/{}-C.csv'.format(date),index=False,header=False, encoding='utf-8-sig')
wordcloud(date,top_200) #워드클라우드
showGraph(date,top_30) # 그래프

