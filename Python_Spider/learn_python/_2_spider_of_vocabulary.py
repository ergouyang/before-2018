import requests
import json
import traceback
import xlsxwriter

keys = ['CET4','GAMT','NGEE','NCEE','CET6','TEM'
        ,'TOEFL','GRE','IELTS','NONE']#四级、GAMT、考研、高考、六级、英专、托福、GRE、雅思、无主题
keys =['CET6']
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4620.400 QQBrowser/9.7.13014.400',
    'Cookie':'__utmt=1; _gat=1; captcha_needed=True; language_code=zh-CN; __utma=183787513.2000382027.1523607130.1524246736.1524249657.2; __utmb=183787513.9.10.1524249657; __utmc=183787513; __utmz=183787513.1524249657.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; locale=zh-cn; sessionid=.eJyrVopPLC3JiC8tTi2KT0pMzk7NS1GyUkrJSsxLz9dLzs8rKcpM0gMp0YPKFuv55qek5jhB1eogG5AJ1GtoYGBiYWJkZlALADKiIIE%3A1f9azS%3Ak1rH23I7Gv5z6Biey4ZRL_67OjE; userid=100484260; auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im1vYmlsZV82OTg4MDM4MDA5IiwiZGV2aWNlIjowLCJpc19zdGFmZiI6ZmFsc2UsImlkIjoxMDA0ODQyNjAsImV4cCI6MTUyNTExMzc3MX0.Im7TcG69vhG7v4XvtdoztwWq_Vb73EPZ9sJQjeCuGbk; csrftoken=kRQbiSLqkSMJK7dvmUdN4ntc1OZFOXqo; _ga=GA1.2.2000382027.1523607130; userid=100484260',
    'Host':'www.shanbay.com'
}
for key in keys:
    url = 'https://www.shanbay.com/api/v1/vocabtest/vocabularies/?category='+key
    voc = []
    voc_mean = []
    voc_rank = []
    voc_pk = []
    voc_len = []
    A = []
    B = []
    C = []
    D = []
    RIGHT = []
    count = 0
    for i in range(10):#每个url抓取40次，获取每次url返回的json
        for data in json.loads(requests.get(url=url,headers=headers).text).get('data'):#处理json中的每一个单词
            voc.append(data.get('content'))
            voc_pk_num = data.get('pk')
            voc_pk.append(voc_pk_num)
            voc_rank.append(data.get('rank'))
            voc_len.append(len(data.get('content')))
            num = 0
            choise = ['A','B','C','D']
            for selects in data.get('definition_choices'):#处理每个单词的意思
                if(selects.get('pk')==(voc_pk_num)):
                    voc_mean.append(selects.get('definition'))
                    print('NO.'+str(count))
                    count += 1
                    RIGHT.append(choise[num])
                if(num==0):
                    A.append(selects.get('definition'))
                    num+=1
                elif(num==1):
                    B.append(selects.get('definition'))
                    num+=1
                elif(num==2):
                    C.append(selects.get('definition'))
                    num+=1
                elif(num==3):
                    D.append(selects.get('definition'))
                    num+=1
    try:
        # save_path = 'C:\\Users\yangergou\Desktop\\vocabulary\\'+key+'.xlsx'
        save_path = 'C:\\Users\yangergou\Desktop\\vocabulary\\vocabulary.xlsx'
        wk = xlsxwriter.Workbook(save_path)
        sheet = wk.add_worksheet('news')
        sheet_title = ['voc','mean','rank','pk','len','category','A','B','C','D','RIGHT']
        sheet.write_row('A1', sheet_title)
        sheet.write_column(1, 0, voc)
        sheet.write_column(1, 1, voc_mean)
        sheet.write_column(1, 2, voc_rank)
        sheet.write_column(1, 3, voc_pk)
        sheet.write_column(1, 4, voc_len)
        sheet.write_column(1, 6, A)
        sheet.write_column(1, 7, B)
        sheet.write_column(1, 8, C)
        sheet.write_column(1, 9, D)
        sheet.write_column(1, 10, RIGHT)
        print(save_path+' has completed')
    except:
        print(traceback.format_exc())