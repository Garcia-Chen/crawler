import csv
import json
import re

from lxml import etree
import requests
from bs4 import BeautifulSoup

def get_html(url):
    try:
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        res=requests.get(url,headers=headers)
        if res.status_code==200:#状态码为200表示请求成功
            res.encoding='utf-8'
            return res.text
    except TimeoutError:
        print('请求失败!')
        return None

def parse_html(html):
    soup=BeautifulSoup(html,'html.parser')
    title= soup.select('h1.main-title')[0].text
    time=soup.select('.date-source')[0].contents[1].text
    source=soup.select('.date-source')[0].contents[3].text
    article=[]
    for p in soup.select('.article p')[:-1]:
        article.append(p.text.strip())
    article=' '.join(article)
    comments = requests.get('http://comment.sina.com.cn/page/info?version=1&format=json&channel=cj&newsid=comos-imxyqwa0683806&group=undefined&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=3&t_size=3&h_size=3&thread=1&uid=unlogin_user&callback=jsonp_1584293874129&_=1584293874129')
    comments.encoding='utf-8'
    jd=json.loads(re.match(".*?({.*}).*", comments.text, re.S).group(1))
    comment_num = jd['result']['count']['show']
    return title,time,source,article,comment_num


if __name__=='__main__':
    url = 'https://finance.sina.com.cn/consume/2020-03-15/doc-iimxyqwa0683806.shtml'
    html=get_html(url)
    title,time,source,article,comment_num=parse_html(html)
    f=open('news.csv','w',newline='',encoding='utf-8')
    writer = csv.writer(f)
    writer.writerow(['url','title','time','source','article','comment_num'])
    writer.writerow([url,title,time,source,article,comment_num])
