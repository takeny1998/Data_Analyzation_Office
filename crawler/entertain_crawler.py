
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote
from konlpy.tag import Mecab
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import font_manager, rc
from PIL import Image
import numpy as np


def get_news():
    url = 'https://entertain.naver.com/ranking'
    news_df = pd.DataFrame(columns=("Title","Article"))
    idx = 0

    search_url = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(search_url,'html.parser')
    content = soup.find('div',{'class':'rank_lst'})
    ul = content.find('ul')
    links = ul.find_all('li')

    for link in links:
        news_url = "https://entertain.naver.com/" + link.find('a').get('href')
        news_link = urllib.request.urlopen(news_url).read()
        news_html = BeautifulSoup(news_link, 'html.parser')

        date = news_html.find('span',{'class','author'}).get_text()
        date = date.replace(".","")
        date = date[4:12]

        title = news_html.find('h2',{'class':'end_tit'}).get_text()
        article = news_html.find('div',{'id':'articeBody'}).get_text()
        article = article.replace("// flash 오류를 우회하기 위한 함수 추가","")
        article = article.replace("function _flash_removeCallback()","")
        article = article.replace("{}","")
            
        article = article.replace("","")
        article = article.replace("\n","")
        article = article.replace("\t","")
        news_df.loc[idx] = [title, article]
        idx += 1

        print("#", end="") 
 
    return news_df, date

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
    icon = Image.open('/mnt/crawling/images/entertain.png')
    mask = Image.new("RGB", icon.size, (255,255,255))
    mask.paste(icon,icon)
    mask = np.array(mask)

    wc = WordCloud(font_path="/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf",\
                                background_color="white", \
                                width=2000, \
                                height=1000,\
                                max_words=100,\
                                max_font_size=300,\
                                mask = mask)   
                                 
    wc.generate_from_frequencies(dict(top_keyword))
    wc.to_file('/mnt/result/Entertain/{}-W.png'.format(date))


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

    
    plt.savefig('/mnt/result/Entertain/{}-G.png'.format(date))

news_df,date = get_news()

date = date.strip()
#모든 본문기사 합치기
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

top_10 = pd.DataFrame.from_dict(top_10)
top_10.to_csv('/mnt/result/Entertain/{}-C.csv'.format(date),index=False,header=False, encoding='utf-8-sig')
wordcloud(date,top_200) #워드클라우드
showGraph(date,top_30) # 그래프
