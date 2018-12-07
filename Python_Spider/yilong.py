import requests, json, re, xlsxwriter
import traceback
class yilong():
    def yilong_comment(info, city_name):
        count = 0
        for hotel_id, hotel_name, review_count in info:  # 对于每一家酒店
            count += 1
            print('now I am get the ' + str(count) + ' th page,the hotel\'s name is ' + str(hotel_name))
            # print(hotel_id)
            # print(hotel_name)
            # print(review_count)
            username = []
            content = []
            scoretotal = []
            commentcount = []  # 返回的json中写的
            userrank = []  # 用户等级
            time = []  # "commentDateTime":"2017-07-07 用户评论时间
            travelType = []  # 旅行方式
            roomTypeName = []
            for page_index in range(1, int(int(review_count) / 100) + 2, 1):
                url = 'http://m.elong.com/hotel/api/morereviewnew?hotelid=' + str(
                    hotel_id) + '&commenttype=1&pagesize=100&pageindex=' + str(page_index) + '&mainId=0&esdnum=9196917'

                headers = {
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate, sdch',
                    'Accept-Language': 'zh-CN,zh;q=0.8',
                    'Connection': 'keep-alive',
                    'Cookie': 'CookieGuid=1a8880aa-4f0d-4b0f-8c97-e52d2d178573; SessionGuid=00c6ddec-64ee-4776-9a14-6057a49270a8; Esid=8e852714-7af7-48ff-94e4-36d28f924d11; \
                    s_eVar44=sgbrandzone; CitySearchHistory=0101%23%E5%8C%97%E4%BA%AC%E5%B8%82%23beijing%23; com.eLong.CommonService.OrderFromCookieInfo=Status=1&Orderfromtype=\
                    5&Isusefparam=0&Pkid=51023&Parentid=4600&Coefficient=0.0&Makecomefrom=0&Cookiesdays=0&Savecookies=0&Priority=9000; ShHotel=CityID=0101&CityNameCN=%E5%8C%97%E4\
                    %BA%AC%E5%B8%82&CityName=%E5%8C%97%E4%BA%AC%E5%B8%82&OutDate=2017-07-09&CityNameEN=beijing&InDate=2017-07-08; s_cc=true; SHBrowseHotel=cn=50101077%2C%2C%2C%2C%\
                    2C%2C%3B90914560%2C%2C%2C%2C%2C%2C%3B&; s_visit=1; s_sq=elongcom%3D%2526pid%253Dhotel.elong.com%25252F50101077%25252F%2526pidt%253D1%2526oid%253Djavascript%252\
                    53Avoid(0)%2526ot%253DA; H5CookieId=8a00bc2f-380c-4463-88ba-4e45e837e7c3; businessLine=hotel; H5Channel=mnoreferseo%2CSEO; H5SessionId=2581D347C4A64C3EDC07969968\
                    C74FFB; cityid=0101; route=7fbf8090634af19a2246b39009778d36; indate=2017-07-07; outdate=2017-07-08; H5ff4detail=""; _fid=j4tefvsr-355b-483f-affb-7db312781cd9; pag\
                    e_time=1499401737010%2C1499401742149%2C1499401757112%2C1499401847772%2C1499401928546%2C1499402089717%2C1499402354577%2C1499402364922%2C1499404022346; _RF1=171.113.\
                    115.200; _RSG=FB4MGt0eO8BlNwlmg1V0KA; _RGUID=b218a00d-d058-42cf-a500-7c1ab0bfa5ef',
                    'Host': 'm.elong.com',
                    'Referer': 'http://m.elong.com/hotel/50101077/review/good.html',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36',
                    'X-Requested-With': 'XMLHttpRequest'
                }
                try:
                    page = requests.get(url=url, headers=headers, timeout=15)
                    #json_ = json.loads(page.text)
                    json_ = page.json()
                    commentcount = json_["commentCount"]
                    json_ =json_["comments"]
                    username = json_['userName']
                    content=json_['content']
                    scoretotal = json_['commentScoreTotal']

                    userrank = json_['userRank']
                    time = json_['commentDateTime']
                    travelType = json_['travelType']
                    roomTypeName = json_['roomTypeName']
                except:
                    print(traceback.format_exc())
                    page = requests.get(url=url, headers=headers,timeout = 15)
                    try:
                        json_ = json.loads(page.text)["comments"]
                        for data in json_:
                            username.append(data.get('userName'))
                            content.append(data.get('content'))
                            scoretotal.append(data.get('commentScoreTotal'))
                            commentcount.append(data.get('commentCount'))
                            userrank.append(data.get('userRank'))
                            time.append(data.get('commentDateTime'))
                            travelType.append(data.get('travelType'))
                            roomTypeName.append(data.get('roomTypeName'))
                    except:
                        print(traceback.format_exc())
                        print('出错，出错URL为：' + str(url))
                        # 建议使用xlwrite
                        """wbk = xlwt.Workbook()  # 将结果写入到EXCEL
            sheet1 = wbk.add_sheet('content', cell_overwrite_ok=True)
            title = ['用户名', '评论', '评分', '总数', '用户等级', '评论时间', '旅行方式']
            for i in range(0,7):
                sheet1.write(0,i,title[i])
            for index in range(2, len(username)+2):
                try:
                    sheet1.write(index, 0, username[index+1])  # write（行,列,写入的内容）
                except:
                    sheet1.write(index, 0, "")
                try:
                    sheet1.write(index, 1, content[index+1])
                except:
                    sheet1.write(index, 1, "")
                try:
                    sheet1.write(index, 2, scoretotal[index+1])
                except:
                    sheet1.write(index, 2, "")
                try:
                    sheet1.write(index, 3, commentcount[index+1])
                except:
                    sheet1.write(index, 3, "")
                try:
                    sheet1.write(index, 4, userrank[index+1])
                except:
                    sheet1.write(index, 4, "")
                try:
                    sheet1.write(index, 5, time[index+1])
                except:
                    sheet1.write(index, 5, "")
                try:
                    sheet1.write(index, 6, travelType[index+1])
                except:
                    sheet1.write(index, 6, "")
                try:
                    sheet1.write(index, 7, roomTypeName[index+1])
                except:
                    sheet1.write(index, 7, "")"""
            try:
                save_path = 'D:\\' + str(city_name) + '9\\' + str(hotel_name) + '_' + str(hotel_id) + '_' + str(len(username)) + '&' + str(review_count) + '.xlsx'
                comm_wk = xlsxwriter.Workbook(save_path)
                print('writing to excle...')
                sheet1 = comm_wk.add_worksheet('评论')
                title = ['用户名', '评论', '评分', '总数', '用户等级', '评论时间', '旅行方式', '房屋类型']
                sheet1.write_row('A1', title)
                row = 1
                sheet1.write_column(row, 0, username)
                sheet1.write_column(row, 1, content)
                sheet1.write_column(row, 2, scoretotal)
                sheet1.write_column(row, 3, commentcount)
                sheet1.write_column(row, 4, userrank)
                sheet1.write_column(row, 5, time)
                sheet1.write_column(row, 6, travelType)
                sheet1.write_column(row, 7, roomTypeName)
                comm_wk.close()
                print('writing to excle Done!')
            except:
                print(traceback.format_exc())
            """try:
                save_path = 'D:\\'+str(city_name)+'\\' + str(hotel_name)+'_'+str(hotel_id)+'_'+str(len(username))+'&'+str(review_count) + '.xls'
                wbk.save(save_path)"""

    def get_hotel(citys):
        # 获取酒店总数

        for city_name, city_id in citys:
            url = 'http://hotel.elong.com/' + str(city_name)
            page = requests.get(url)
            mod = r'id="hotelCount">(.*?)</span>家酒店满足条件'
            hotel_count = re.compile(mod).findall(page.text)
            print(hotel_count[0])

        hotel_page_headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': 'CookieGuid=1a8880aa-4f0d-4b0f-8c97-e52d2d178573; SessionGuid=00c6ddec-64ee-4776-9a14-6057a49270a8; Esid=8e852714-7af7-48ff-94e4-36d28f924d11; \
                s_eVar44=sgbrandzone; CitySearchHistory=0101%23%E5%8C%97%E4%BA%AC%E5%B8%82%23beijing%23; com.eLong.CommonService.OrderFromCookieInfo=Status=1&Orderfromty\
                pe=5&Isusefparam=0&Pkid=51023&Parentid=4600&Coefficient=0.0&Makecomefrom=0&Cookiesdays=0&Savecookies=0&Priority=9000; ShHotel=CityID=0101&CityNameCN=%E5%\
                8C%97%E4%BA%AC%E5%B8%82&CityName=%E5%8C%97%E4%BA%AC%E5%B8%82&OutDate=2017-07-09&CityNameEN=beijing&InDate=2017-07-08; s_cc=true; SHBrowseHotel=cn=5010107\
                7%2C%2C%2C%2C%2C%2C%3B90914560%2C%2C%2C%2C%2C%2C%3B&; s_visit=1; s_sq=elongcom%3D%2526pid%253Dhotel.elong.com%25252F50101077%25252F%2526pidt%253D1%2526oi\
                d%253Djavascript%25253Avoid(0)%2526ot%253DA; H5CookieId=8a00bc2f-380c-4463-88ba-4e45e837e7c3; businessLine=hotel; H5Channel=mnoreferseo%2CSEO; H5SessionId\
                =2581D347C4A64C3EDC07969968C74FFB; route=7fbf8090634af19a2246b39009778d36; _fid=j4tefvsr-355b-483f-affb-7db312781cd9; page_time=1499401737010%2C149940174214\
                9%2C1499401757112%2C1499401847772%2C1499401928546%2C1499402089717%2C1499402354577%2C1499402364922%2C1499404022346%2C1499404467066; _RF1=171.113.115.200; _R\
                SG=FB4MGt0eO8BlNwlmg1V0KA; _RGUID=b218a00d-d058-42cf-a500-7c1ab0bfa5ef; indate=2017-07-07; outdate=2017-07-08; cityid=0101; H5ff4list=""',
            'Host': 'm.elong.com',
            'Referer': 'http://m.elong.com/hotel/0101/nlist/',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        info = []
        hotel_count = ['0']
        for city_name, city_id in citys:  # 每一个城市的
            page_count = 0
            for index in range(0, int(int(hotel_count[0]) / 20) + 2, 1):  # 每一家酒店  爬取各个酒店的id、name 和评论数
                hotel_page_url = 'http://m.elong.com/hotel/api/list?city=' + str(city_id) + '&pageindex=' + str(index) + '&indate=2017-07-08&outdate=2017-07-09'
                hotel_page = requests.get(url=hotel_page_url, headers=hotel_page_headers)
                page_count += 1
                print('正在爬取' + str(city_name) + '第' + str(page_count) + '页的酒店信息')
                hotel_datas = json.loads(hotel_page.text)['hotelList']
                try:
                    for hotel_data in hotel_datas:
                        mode = r'hotel/(.*?)/#'
                        hotel_url = hotel_data.get('detailPageUrl')
                        _id = re.compile(mode).findall(hotel_url)
                        count = hotel_data.get('totalCommentCount')
                        name = hotel_data.get('hotelName')
                        t = (_id[0], name, count)
                        info.append(t)
                except:
                    pass
                    print('出错：' + hotel_page_url)
        print(info)
        print(len(info))
        return info

    citys = [[('beijing', '0101')], [('shanghai', '0201')], [('guangzhou', '2001')], [('shenzhen', '2003')]]
    for city in citys:
        info = get_hotel(city)
        yilong_comment(info, city_name=city[0][0])


a = yilong()

