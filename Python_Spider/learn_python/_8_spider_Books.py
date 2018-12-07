import requests
from lxml import etree
import json
from _4_mysql_connection import connect_mysql
import traceback
from _3_spider_of_IP import IpPool
import time
# class douban():
# """https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?type=S ---> get all books' api"""
#     def book_url(self,category,type = 's'):
#         pass
# for i in
def get_books():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4620.400 QQBrowser/9.7.13014.400'
    }
    for i in range(225,250,25):
        sql_con = connect_mysql('douban_books')
        url = 'https://book.douban.com/top250?start='+str(i)
        ip = IpPool()
        response = requests.get(url,headers=headers,verify=False)
        response_etree = etree.HTML(response.text)
        for j in range(1,25):
            try:
                id_xpath = '//*[@id="content"]/div/div[1]/div/table['+str(j)+']/tr/td[2]/div[1]/a/@href'
                str_xpath = '//*[@id="content"]/div/div[1]/div/table['+str(j)+']/tr/td[2]/p[2]/span/text()'
                id = response_etree.xpath(id_xpath)[0].split('/')[-2]
                str_ = response_etree.xpath(str_xpath)[0]
                # print(requests.get(url='https://api.douban.com/v2/book/'+id,verify=False).text)
                time.sleep(1)
                rows = ip.get_ip()
                ip_url = "http://" + rows[0] + ":" + rows[1]
                url = 'https://api.douban.com/v2/book/' + id
                info_json = json.loads(requests.get(url,headers=headers,verify=False,proxies={rows[4]:ip_url}).text)
                rating = info_json.get('rating')
                numRaters = str(rating.get('numRaters')) # 评分人数
                average = str(rating.get('average')) # 平均分
                subtitle = str(info_json.get('subtitle'))
                author = str(info_json.get('author')) # 原作者
                pubdate = str(info_json.get('pubdate')) # 出版日期
                tags = str(info_json.get('tags')) # 标签 列表
                origin_title = str(info_json.get('origin_title')) # 原名
                image = str(info_json.get('image')) # 图片url
                binding = str(info_json.get('binding')) # 图书包装样式
                translator = str(info_json.get('translator')) # 译者  列表11
                catalog = str(info_json.get('catalog')) # 目录
                pages = str(info_json.get('pages')) # 页数
                images = info_json.get('images')
                images_small = str(images.get('small')) # 小图
                images_large = str(images.get('large')) # 大图
                images_medium = str(images.get('medium')) # 中图
                publisher = str(info_json.get('publisher')) # 出版社
                isbn10 = str(info_json.get('isbn10'))
                isbn13 = str(info_json.get('isbn13'))
                title = str(info_json.get('title'))
                url = str(info_json.get('url')) # 豆瓣原图书url
                alt_title = str(info_json.get('alt_title')) # 别名
                author_intro = str(info_json.get('author_intro')) # 作者简介
                summary = str(info_json.get('summary')) # 内容简介
                price = str(info_json.get('price')) # 书籍定价
                sql_str = 'insert into douban_books.books_info(numRaters,average,subtitle,author,pubdate,tags,origin_title,image,binding,translator,catalog,pages,images_small,images_large,images_medium,\
                          id,publisher,isbn10,isbn13,title,url,alt_title,author_intro,summary,price,str) values (\''+numRaters+'\',\''+average+'\',\''+subtitle+'\',\"'+author+'\",\''+pubdate+'\',\"'+tags+'\",\''+origin_title+'\',\''+image+'\',\''+\
                          binding+'\',\"'+translator+'\",\''+catalog+'\',\''+pages+'\',\''+images_small+'\',\''+images_large+'\',\''+images_medium+'\',\''+id+'\',\''+publisher+'\',\''+isbn10+'\',\''+isbn13+'\',\''+title+'\',\''+url+'\',\''+alt_title+'\',\''+author_intro+'\',\''+\
                          summary+'\',\''+price+'\',\''+str_+'\')'
                # print(sql_str)
                sql_con.execute(sql_str=sql_str)
                print('ok')
            except:
                print(traceback.format_exc())
                print('出错url     :     '+url)
    sql_con.close()
print(requests.get(url = 'https://api.douban.com/v2/book/1770782',verify=False).text)
# for i in range(1,3600):
#     time.sleep(1)
#     print(str(3600-i)+'秒后开始尝试爬取')
get_books()