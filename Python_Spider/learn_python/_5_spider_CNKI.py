# coding: utf-8
import requests
import time
from lxml import etree
import _3_spider_of_IP
import traceback
import random


class SpiderCNKI():
    def __init__(self):
        self.thesis = dict()

    def spider_of_searchcnki(self, keyword, rankid=0, searchid=1, thesisNum=16):  # 知识搜索,默认为相关度，主题,爬取的文章数
        rank = ['relevant', 'citeNumber', 'download', 'date']
        search = ['qw:', 'theme:', 'title:', 'author:', 'abstract:']
        '''
        query_data参数说明：
        q:关键词
        rank：排序方式（relevant-相关度；citeNumber-引用次数；download-下载次数；date-时间）
        search:搜索方式（qw: 全文，theme: 主题,title: 篇名，author： 作者，abstract: 摘要）
        p:搜索结果以15个为一页
        '''
        q = search[1] + str(keyword)
        query_data = {'q': q,
                      'rank': rank[rankid],
                      'cluster': 'all',
                      'val': '',
                      'p': '0'}
        url = 'http://search.cnki.net/search.aspx'
        # ip = _3_spider_of_IP.IpPool().get_ip()
        # response = requests.get(url=url, params=query_data, proxies={ip[4]: ip[0] + ':' + ip[1]})
        self.response = requests.get(url=url, params=query_data)
        thesis_conut = 0
        error_conut = 0
        while (thesis_conut < thesisNum):
            try:
                page_etree = etree.HTML(self.response.text)
                thesis_ts = page_etree.xpath('//div[@class="wz_content"]/h3/a[1]')
                thesis_urls = page_etree.xpath('//div[@class="wz_content"]/h3/a[2]/@href')
                count = 0
                for thesis_t in thesis_ts:
                    self.thesis[thesis_t.xpath('string(.)')] = thesis_urls[count]
                    thesis_conut += 1
                    # print('论文题目为：%s,\n论文下载链接为:%s'%(thesis_t.xpath('string(.)'),thesis_urls[count]))
                    count += 1
                    if (thesis_conut == thesisNum):
                        break
                next_url = 'http://search.cnki.net/' + page_etree.xpath('//p[@id="page"]/a[@class="n"]/@href')[-1]
                self.response = requests.get(url=next_url)
            except:
                error_conut += 1
                if (error_conut > 5):
                    break
                print('文章不存在，或搜索结果少无法满足爬取数量条件')
                print(traceback.format_exc())
                # return self.thesis

    def download(self, title, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4620.400 QQBrowser/9.7.13014.400',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Charset': 'GB2312,utf-8;q=0.9',
            'Cookie': '',
        }
        headers['Accept-Language'] = 'zh-CN,zh;q=0.8'
        # 先访问网页上的下载链接(search....)，带着headers访问，然后得到第一次重定向的url
        page = requests.get(url=url, headers=headers, allow_redirects=False)
        # 转换为字典
        # page_headers = eval()
        # 获取cookie
        red_headers = self.get_Cookie(page, headers)
        # 获取重定向的URL
        html_page = etree.HTML(page.text)
        red_url = html_page.xpath('//a/@href')[0]
        # 访问  caj.d.cnki.net   来获取  login.cnki.net
        red = requests.get(url=red_url, headers=headers, allow_redirects=False)
        # 获取Cookie 这是下载页面的headers
        caj_headers = self.get_Cookie(red, headers)
        # print(caj_headers)
        # 获取登陆URL
        red_page = etree.HTML(red.text)
        login_url = red_page.xpath('//a/@href')[0]
        # 获取登陆信息 访问  login.cnki.net
        login1 = requests.get(url=login_url, headers=headers, allow_redirects=False)
        # 获取Cookie
        login1_headers = self.get_Cookie(login1, headers)
        # 获取表单内容
        body = self.get_body(login1.text)
        # 使用post进行IP登陆,获得完整的download_headers
        download_headers, succe_page = self.login_ip(url=login_url, login_headers=login1_headers, body=body,
                                                     caj_headers=caj_headers)
        # 剥离网页url
        download_url = etree.HTML(succe_page.text).xpath('//a/@href')[0]
        download_response = requests.get(download_url, headers=download_headers, allow_redirects=False)
        download_url2 = download_response.headers.get('Location')

        # download_headers['Accept - Encoding']='gzip, deflate, sdch'
        # print(download_headers)
        print('downloading...')
        p = requests.get(url=download_url2, headers=download_headers, stream=True)  # 使用stream模式下载大文件

        lenth = p.headers.get('Content-Length')
        # import chardet
        # print(chardet.detect(str.encode(file_name))) str.encode(file_name).decode('utf-8')

        print('文件名为:%s,\n文件大小为：%s' % (title + '.caj', str(lenth)))
        with open('C:\\Users\yangergou\Desktop\\CNIK_test\\' + str(title) + '.caj', 'wb') as f:
            for i in p.iter_content(chunk_size=512):
                f.write(i)

    def get_Cookie(self, page, h):  # 获取cookie
        headers = h.copy()
        Set_Cookie = page.headers.get('Set-Cookie')
        Set_Cookie = Set_Cookie.replace(',', ';').split(';')
        Cookie = ''
        for i in range(len(Set_Cookie)):
            if Set_Cookie[i] == ' path=/' or Set_Cookie[i] == ' HttpOnly':
                continue
            else:
                Cookie += Set_Cookie[i] + ';'
        headers['Cookie'] = headers.get('Cookie') + Cookie if headers.get('Cookie') == '' else headers.get(
            'Cookie') + ';' + Cookie
        return headers

    def get_body(self, page):  # 获取表单
        body = {}
        inp = etree.HTML(page).xpath('//div[@class="aspNetHidden"]/input')
        for i in inp:
            name = i.xpath('@name')
            value = i.xpath('@value')
            body[name[0]] = value[0]
        body['__EVENTTARGET'] = 'Button2'
        body['TextBoxUserName'] = ''
        body['TextBoxPwd'] = ''
        return body

    def login_ip(self, url, login_headers, body, caj_headers):
        # print(url)
        # print(login_headers)
        # print(body)
        # print(caj_headers)
        page = requests.post(url=url, headers=login_headers, data=body, allow_redirects=False)
        return self.get_Cookie(page, caj_headers), page

    def login_pw(self, url, login_headers, body, caj_headers):
        pass


i = SpiderCNKI()
# 参数设定 关键词，排序方式，搜索方式，爬取数量
keyword = ['决策支持系统综述']
rankid = 0
searchid = 1
thesisNum = 6
for kw in keyword:
    i.spider_of_searchcnki(keyword, rankid, searchid, thesisNum + 1)
error_con = 0
for key, value in i.thesis.items():
    try:
        print('进行下载：' + key + '\n下载url:' + value)
        i.download(title=key, url=value)
        print('完成下载')
        time.sleep(random.randint(5, 10))
        # input('暂停。。。')
    except:
        error_con += 1
        if (error_con > 3):
            break
        print(traceback.format_exc())
    else:
        print('进行下载：' + key + '\n下载url:' + value)
        i.download(title=key, url=value)
        print('完成下载')
        time.sleep(random.randint(5, 10))
