from collections import defaultdict
import requests,json,xlsxwriter,datetime
def decry(password=None,data=None,key_word=None):
    #获取密钥解析结果
    def get_key(password):
        p = defaultdict()
        half_len = len(password)//2
        for v in range(0,half_len):
            p[password[v]]=password[v+half_len]
        return p
    # 获取时间列表
    def get_time(time):
        dates = []
        dt = datetime.datetime.strptime(time[0],"%Y%m%d")
        date = time[0]
        while date<=time[1]:
            dates.append(date)
            dt = dt+datetime.timedelta(1)
            date = dt.strftime("%Y%m%d")
        return dates
    #保存
    def save(data_list,time_list):
        wk = xlsxwriter.Workbook('D:\\' + str(key_word) + '.xlsx')
        print('writing to excle...')
        sheet1 = wk.add_worksheet('index')
        sheet1.write_row('A1',['时间','全部','PC','手机'])
        sheet1.write_column(1,0,time_list)
        sheet1.write_column(1,1,data_list[0])
        sheet1.write_column(1,2,data_list[1])
        sheet1.write_column(1,3,data_list[2])
        wk.close()
        print('writing to excle Done!')
    #对信息进行解密
    data_list = []
    for d_ in [data["_all"],data["_pc"],data["_wise"]]:
        s = ""
        for char in d_:
            s =s+str(get_key(password)[char])
        data_list.append(s.split(','))
    save(data_list=data_list,time_list=get_time(data["period"].split('|')))
def get_cookie(user_name,user_password):
    Data = {}
    pass
def get_data(key_words,headers=None,):
    print(key_words)
    for key_word in key_words:
        headers = {'Cookie':'BDUSS=0dBcGc1dXNXSlZtbDhlbjVRUHlPSWJxRDBxSFpOU0ZoRVdzOGp0WTZ-ek5SWjFaSVFBQUFBJCQAAAAAAAAAAAEAAAD5vIkuztLKx9K71tC1xGxvdmUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM24dVnNuHVZd'}
        url = 'http://index.baidu.com/Interface/Newwordgraph/getIndex?region=0&startdate=20170625&enddate=20170725&wordlist%5B0%5D='+str(key_word)
        def get_password(uniqid):
            password = json.loads(requests.get(url = 'http://index.baidu.com/Interface/api/ptbk',params={'uniqid':uniqid},headers=headers).text)["data"]
            print("密钥：%s"%password)
            return password
        json_ = json.loads(requests.get(url=url,headers=headers).text)
        print(json_["message"])if json_["status"]!=0 else print('获取成功')and decry(password=get_password(json_["uniqid"]),data=json_["data"][0]["index"][0],key_word=key_word)
#cookie = get_cookie(user_name=input("请输入用户名："),user_password=input("请输入密码："))
#如果登陆失败，请自行登陆，并修改headers里的cookie
key_word = input("输入关键词：")
key_word = key_word.split(',')
get_data(key_words=key_word)if key_word!=[''] else print("请输入关键词!")