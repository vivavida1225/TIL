import requests

url = 'http://apis.data.go.kr/B552061/frequentzoneLg/getRestFrequentzoneLg'
params ={'serviceKey' : 'b580c79eed65cde4a467bf7533bc3bbd6cd3b51732d4ef5983f29900c2b449ab', 'searchYearCd' : '2017', 'siDo' : '11', 'guGun' : '200', 'type' : 'xml', 'numOfRows' : '10', 'pageNo' : '1' }

response = requests.get(url, params=params)
print(response.content)