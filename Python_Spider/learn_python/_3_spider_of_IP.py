import requests
import traceback
import xlsxwriter
from lxml import etree
import time
class IpPool():
    def __init__(self):
        self.headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4620.400 QQBrowser/9.7.13014.400'
        }
    def update(self):
        all_count = 1
        ipAddress,ipPort,serverAddress,isAnonymous,protocol,survivalTime,testTime=[],[],[],[],[],[],[]
        while(all_count<21):
            try:
                etree_re = etree.HTML(requests.get('http://www.xicidaili.com/nn/'+str(all_count),headers = self.headers).text)
                ipAddress += etree_re.xpath('//table[@id="ip_list"]/tr/td[2]/text()')
                ipPort += etree_re.xpath('//table[@id="ip_list"]/tr/td[3]/text()')
                serverAddress += etree_re.xpath('//table[@id="ip_list"]/tr/td[4]/a/text()')
                isAnonymous += etree_re.xpath('//table[@id="ip_list"]/tr/td[5]/text()')
                protocol += etree_re.xpath('//table[@id="ip_list"]/tr/td[6]/text()')
                survivalTime += etree_re.xpath('//table[@id="ip_list"]/tr/td[9]/text()')
                testTime += etree_re.xpath('//table[@id="ip_list"]/tr/td[10]/text()')
                print("get"+str(all_count)+"#### there are "+str(len(etree_re.xpath('//table[@id="ip_list"]/tr')))+" pages")
                all_count += 1
            except :
                print(traceback.format_exc())
        save_path = 'C:\\Users\yangergou\Desktop\code\data\\ip_pool_'+str(time.strftime('%Y-%m-%d',time.localtime(time.time())))+'.xlsx'
        wk = xlsxwriter.Workbook(save_path)
        sheet = wk.add_worksheet('ip_pool')
        sheet_title = ['ipAddress', 'ipPort', 'serverAddress', 'isAnonymous',
                       'protocol', 'survivalTime', 'testTime']
        sheet.write_row('A1', sheet_title)
        sheet.write_column(1, 0, ipAddress)
        sheet.write_column(1, 1, ipPort)
        sheet.write_column(1, 2, serverAddress)
        sheet.write_column(1, 3, isAnonymous)
        sheet.write_column(1, 4, protocol)
        sheet.write_column(1, 5, survivalTime)
        sheet.write_column(1, 6, testTime)
    def get_ip(self):
        import xlrd
        import random
        try:
            #读取ip表
            data = xlrd.open_workbook('C:\\Users\yangergou\Desktop\code\data\\ip_pool_'+str(time.strftime('%Y-%m-%d',time.localtime(time.time())))+'.xlsx')
        except:
            self.update()
        else:
            table = data.sheet_by_index(0)
            nrows = table.nrows
            count = 0
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4620.400 QQBrowser/9.7.13014.400'}
            while(True):
                #100次都抽不到可用ip,就更新ip表
                if(count>100):
                    self.update()
                    count = 0
                count += 1
                rows = table.row_values(random.randint(1, nrows))
                url = "http://"+rows[0]+":"+rows[1]
                print(url)
                try:
                    requests.get(url = 'http://wenshu.court.gov.cn/',headers = headers, proxies={rows[4]:url})
                except:
                    print(url+"  failed")
                    continue
                else:
                    print("success")
                    return rows
    def telnetlib_test_ip(self):
        import telnetlib
        try:
            telnetlib.Telnet('127.0.0.1', port='80', timeout=20)
        except:
            print
            'connect failed'
        else:
            print
            'success'
    def thread_get_ip(self):
        # import _thread
        # print("线程启动中...")
        # ip1 = _thread.start_new_thread(self.get_ip())
        # print("线程1启动成功")
        # ip2 = _thread.start_new_thread(self.get_ip())
        # print("线程2启动成功")
        # ip3 = _thread.start_new_thread(self.get_ip())
        # print("线程3启动成功")
        # ip4 = _thread.start_new_thread(self.get_ip())
        # print("线程4启动成功")
        t1 = self.myThead()
        t2 = self.myThead()
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        p1 = t1.get_result()
        p2 = t2.get_result()
        return p1,p2
    import threading
    class myThead(threading.Thread):
        def __init__(self):
            self._result = None
        def run(self):
            result = IpPool.get_ip()
            self._result = result
        def get_result(self):
            return self._result
# i = IpPool()
# i.update()
# print(i.get_ip())
# ip1,ip2 = i.thread_get_ip()
# print(ip1,ip2)