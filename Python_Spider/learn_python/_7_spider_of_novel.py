import requests
from lxml import etree
class  Novel():
    def __init__(self):
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4620.400 QQBrowser/9.7.13014.400'
       }
    def getCategory(self):
        return etree.HTML(requests.get('http://www.51shucheng.net/fenlei',self.headers).text).xpath('//ul/li/a/@href')
    def getNovel(self):
        urls = self.getCategory()
        novel_urls=[]
        for url in urls:
            novel_urls += etree.HTML(requests.get(url,self.headers).text).xpath('//*[@id="page"]/div[2]/div[2]/div[4]/ul/li/@href')
        return novel_urls
    def downloadNovel(self,url):
        page = etree.HTML(requests.get(url,self.headers).text)
        title = page.xpath('//*[@id="page"]/div[2]/div[2]/h1/text()')
        zj_urls  = page.xpath('//*[@id="page"]/div[2]/div[2]/div[@class="mulu-list"]/ul/li/a/@href')
        count = 0
        with open('C:\\Users\yangergou\Desktop\三体.txt', 'a') as f:
            for zj_url in zj_urls:
                content = ''
                a = etree.HTML(requests.get(zj_url, self.headers).text)
                title = a.xpath('//*[@id="page"]/div[2]/div/h1/text()')
                print(title)
                b = a.xpath('//*[@id="page"]/div[2]/div/div[4]')[0]
                content += title[0]+b.xpath('string(.)')
                count += len(content)
                f.write(content)
            print('全文长'+str(count))

s = Novel()
s.downloadNovel('http://www.51shucheng.net/kehuan/santi')
