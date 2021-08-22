import requests
import time
from bs4 import BeautifulSoup
import json

#爬取视频评论   https://www.bilibili.com/video/av17784172

# 爬虫模拟访问信息
def get_html(url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }

    r = requests.get(url, timeout=30,headers=headers)
    r.raise_for_status()
    r.endcodding = 'utf-8'
    return r.text

#分析网页文件，整理信息，保存在列表变量中
def get_content(url):
    comments = []
    html = get_html(url)
    try:
        s=json.loads(html)
        num=len(s['data']['replies']) 
        # 获取每页评论栏的数量
        i=0
        while i<num:
            comment=s['data']['replies'][i]
            # 获取每栏评论

            InfoDict={}
             # 存储每组信息字典

            InfoDict['Content']=comment['content']['message'] # 评论内容       
            comments.append(InfoDict)
            i=i+1
        return comments
    except:
        print("jsonload error")
    


#将爬取到的文件写入到本地
def Out2File(dict):
    with open('BiliBili评论.txt', 'a+',encoding='utf-8') as f:
        i=0
        for comment in dict:
            i=i+1
            try:
                f.write('{}'.format(comment['Content']))
            except:
                print("out2File error")
        print('当前页面保存完成')

if __name__ == '__main__':
    e=0
    page=1
    while e == 0 :
        url = "https://api.bilibili.com/x/v2/reply?pn="+ str(page)+"&type=1&oid=17784172&sort=2" 	
        try:
            print()
            content=get_content(url)
            print("page:",page)
            Out2File(content)
            page=page+1
            # 为了降低被封ip的风险，每爬20页便歇5秒。
            if page%10 == 0:
                time.sleep(5)
        except:
            e=1


#根据爬取的评论生成的txt文件生成词云
from wordcloud import WordCloud
import matplotlib.pyplot as plt  
import  jieba     
from PIL import Image               

path_txt='BiliBili评论.txt'
f = open(path_txt,'r',encoding='UTF-8').read()

# 结巴分词，生成字符串，wordcloud是英文库，无法直接生成正确的中文词云
cut_text = " ".join(jieba.cut(f))

wordcloud = WordCloud(
   font_path="C:/Windows/Fonts/simfang.ttf",
   #设置字体
   background_color="white",
   #背景颜色
   width=1000,height=800).generate(cut_text)
   #设置图片宽和高

plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
wordcloud.to_file("哔哩哔哩词云.png") 