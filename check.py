import requests 
 
proxies = {'http': 'http://190.64.18.177:80'} 
response = requests.get('http://httpbin.org/ip', proxies=proxies) 
print(response.json()['origin']) # 190.64.18.162