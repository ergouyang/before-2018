import json,requests,xlsxwriter,traceback

name = []
score = []
urls = []

for i in range(0,1001,100):
    print(i)
    try:
        url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E5%8F%AF%E6%92%AD%E6%94%BE&sort=rank&page_limit=100&page_start='+str(i)
        page = requests.get(url=url)
        json_ = json.loads(page.text)['subjects']

        for data in json_:
            name.append(data.get('title'))
            
            score.append(data.get('rate'))
            urls.append(data.get('url'))
            print(str(data.get('title'))+'    '+str(data.get('rate')))
    except:
        print(traceback.format_exc())

wkb = xlsxwriter.Workbook('d:\\doubantop400.xlsx')
sheet1 = wkb.add_worksheet('movie')
sheet1.write_row('A1',['电影名','评分','url'])
sheet1.write_column(1,0,name)
sheet1.write_column(1,1,score)
sheet1.write_column(1,2,urls)
wkb.close()
