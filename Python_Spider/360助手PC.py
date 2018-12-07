#coding=utf-8
__author__ = 'asus'

import requests   #如果报了 no module XXX  说明没有XXX这个模块   win+R 输入 cmd 打开命令提示符    python2:  输入 pip install XXX    python3: 输入 python -m pip install XXX   没有pip自个去装
import urllib   # 使用‘#’  是注释
import re
import time
import xlwt
import json

class xc():
    count = 0
    def pc(self):
        names = ['乐途FM Android_fm.taolue.letu','携程无线android','携程学生旅行 Android_ctrip.android.youth','携程攻略 Android_com.android.ctrip.gs',
                 '携程商户版 Android_com.ctrip.selectmerchants','携程企业商旅 Android_com.ctrip.ct','携程周末 Android_com.chanyouji.weekend',
                 '携程折扣 Android_ctrip.android.am','去哪儿旅游搜索','去哪儿司机端 Android_com.preference.driver','去哪儿火车票 Android_com.qunar.train',
                 '去哪儿酒店 Android_com.qunar.hotel','去哪儿攻略-旅行指南针 Android_com.qunar.travelplan','去哪儿兜行 Android',
                 '去哪儿生活 Android_com.qunarglory','去哪儿当地 Android_com.qunar.dangdi','去哪儿门票 Android_com.mqunar.sight',
                 '去哪儿车车 Android_com.qunar.car','途牛旅游 Android',
                 '艺龙无线android','艺龙酒店 Android_com.elong.hotel.ui','艺龙出行 Android_com.elong.go','艺龙商户版 Android_com.elong.merchant.c2c',
                 '艺龙有房 Android_com.elong.android.youfang','艺龙驴友 Android_com.elong.tourpal','艺龙汽车票 Android_com.elong.android.bus',
                 '芒果旅游 iMango Android','芒果商旅 Android_com.mangocity','芒果特卖 Android_com.mangocity_special_sale','穷游锦囊 Android',
                 '穷游折扣 Android_com.qyer.android.lastminute','穷游锦囊 Android_com.qyer.android.qyerguide','穷游清单 Android','旅游攻略',
                 '蚂蜂窝 Android_com.mfw.mfwapp','同程旅游android','同程攻略 Android_com.tongcheng.diary','同程-司导端 Android_com.ly.gjcar.driver',
                 '驴妈妈旅游andriod','酷讯机票-飞机票、机票查询、航班查询、特价机票、飞机 Android_com.kuxun.scliang.plane','酷讯旅游宝典 Android',
                 '酷讯酒店 Android_com.kuxun.scliang.hotel','淘宝旅行android','阿里旅行 Android_com.taobao.trip.merchant']
        names = ['蚂蜂窝 Android_com.mfw.mfwapp']
        count = 0
        for name in names:
            allusername = []
            allcontent = []
            allscore = []
            alltime = []
            for i in range(0,2101,50):#从360助手网址分析可以发现 &start=  后面的数字是指每页返回评论数的开始编号（如&start=50  是指从第50条评论获取）
                                       #&count=10  每一页返回评论的数量是十条   这里我们构建每一页的url（可以理解为网址吧或者API）
                url = "http://comment.mobilem.360.cn/comment/getComments?&baike="+str(name)+"&count=50&start="+str(i)
                #http://comment.mobilem.360.cn/comment/getComments?&baike=%E8%89%BA%E9%BE%99%E6%97%A0%E7%BA%BFandroid&count=10&start=
                #把每一页构建的url 添加到我们的url列表 以供下一步循环读取url使用
                print(url)
                username = []
                content = []
                score = []
                time2 = []
                headers = {'Accept': '*/*',
                       'Accept-Encoding': 'gzip, deflate, sdch',
                       'Accept-Language': 'zh-CN,zh;q=0.8',
                       'Connection': 'keep-alive',
                       'Cookie': '__guid=91251416.952602307479952000.1498625209685.9495; __huid=104s%2FOoUY6Foi8bKlKDdsaQHtCRxvJLUq5xd2Y3ylQT2w%3D',
                       'Host': 'comment.mobilem.360.cn',
                       'Referer': 'http://zhushou.360.cn/detail/index/soft_id/2947?recrefer=SE_D_%E6%90%BA%E7%A8%8B',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3143.400 QQBrowser/9.6.11451.400'}
                p = requests.get(url=url,headers=headers)#使用requests模块中的get方法 请求url 携带headers
                count = count+1
                print("loading the "+str(count)+"th page\n")
                neirong = p.text
                #print(neirong)
                mode_username  = r'"username":"(.*?)"'#添加用户名   正则表达式爬取  例如‘杨帆是个傻逼。’ 我想获得‘傻逼’这个词汇，可以使用正则式子： r‘杨帆是个（.*？）。’
                usernames = re.compile(mode_username).findall(neirong)# 将上面设计好的正则式子 作为参数传入re模块中的compile（）方法 。 使用findall() 方法 从
                for username1 in usernames:
                    username1 =  username1.encode('utf-8','ignore')
                    username1 = username1.decode('unicode_escape','ignore')
                    allusername.append(username1)

                mode_content = r'"content":"(.*?)"'#添加评论
                contents = re.compile(mode_content).findall(neirong)
                for content1 in contents:
                    #这里存在编码问题   大家自个想想
                    content1 = content1.encode('utf-8','ignore')#这里是我解决编码的一个方式 先将原文本（原文本是unicode格式）编码为utf-8格式
                    content1 = content1.decode('unicode_escape','ignore')#再将utf-8格式的文本 使用‘unicod_escape’解码    后面的‘ignore'是在解码编码的过程中将出现的编码错误忽略
                    allcontent.append(content1)

                #mode_score = r'"score":(\d+),'#添加评分
                #scores = re.compile(mode_score).findall(neirong)
                #for score1 in scores:
                #   score.append(score1)
                data = json.loads(neirong)
                data = data['data']['messages']
                print(type(data))
                for info in data:
                    allscore.append(info.get('score'))
                
                mode_time = r'"create_time":"(.*?)"'#添加时间，正则表达式       
                times = re.compile(mode_time).findall(neirong)#使用正则表达式匹配在response中的内容
                for time1 in times:#
                    alltime.append(time1)
            print(len(allusername))
            print(len(allcontent))
            print(len(alltime))
            print(len(allscore))
            wbk = xlwt.Workbook()#将结果写入到EXCEL
            sheet1 = wbk.add_sheet('content',cell_overwrite_ok=True)
            for index in range(0, len(allusername)):
                try:sheet1.write(index,0,allusername[index])#   write（行,列,写入的内容）
                except:sheet1.write(index,0,"null")
                try:sheet1.write(index,1,allcontent[index])
                except:sheet1.write(index,1,"")
                try:sheet1.write(index,2,alltime[index])
                except:sheet1.write(index,2,"")
                try:sheet1.write(index,3,allscore[index])
                except:sheet1.write(index,3,"")
            save_path = 'D:\\'+str(name)+'.xls'
            wbk.save(save_path)
                

        return allusername,allcontent,alltime,allscore
    
a = xc()
usernames,contens,times,scores=a.pc()


