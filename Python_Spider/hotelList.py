import requests

url = 'http://api.test.lohoo.com/rest'


query_str = {
    'data': {
    'CityId':'0101'
}
}

r = requests.get(url,query_str)


print(r.status_code)


json = open('hotellist.json','wt')
json.write(r.text)
json.close()