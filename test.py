import requests
'''代理IP地址（高匿）'''
proxy = {
  'http': 'http://1.196.177.129:9999',
  'https': 'https://1.196.177.129:9999',
}
'''head 信息'''
head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
       'Connection': 'keep-alive'}
'''http://icanhazip.com会返回当前的IP地址'''
p = requests.get('http://icanhazip.com', headers=head, proxies=proxy)
print(p.status_code)
print(p.text)