# -*- coding: utf-8 -*-
import json
import random
import requests


class InfoSpider:
    def __init__(self):
        #self.proxy_list =['http://' + proxy['Ip'] + ':' + str(proxy['Port']) for proxy in self.get_proxy()]
        self.proxy_list = ['http://110.167.30.50:8060', 'http://139.196.90.80:80', 'http://103.233.158.34:8080', 'http://112.17.184.45:8060', 'http://116.209.59.150:9999', 'http://125.126.197.154:9999', 'http://122.114.232.137:808', 'http://1.202.245.84:8080', 'http://116.209.52.22:9999', 'http://116.209.58.81:9999', 'http://117.158.189.238:9999', 'http://111.43.70.58:51547', 'http://101.248.64.72:80', 'http://112.91.218.21:9000', 'http://110.52.235.27:9999', 'http://125.40.109.154:44641', 'http://111.177.190.197:9999', 'http://116.209.54.74:9999', 'http://106.105.219.15:8080', 'http://125.72.70.46:8060', 'http://110.52.235.129:9999', 'http://106.15.42.179:33543', 'http://111.177.191.113:9999', 'http://116.209.59.31:9999', 'http://111.177.187.116:9999', 'http://123.121.128.81:8060', 'http://111.177.167.218:9999', 'http://111.177.179.64:9999', 'http://116.209.53.210:9999', 'http://116.209.52.158:9999']
        self._bool = True
        self.retry_time = 0
        
    def __call__(self, mid, proxies=None):
        self.result = {}
        self.proxies = {'http':proxies} if proxies else None
        self.session = requests.Session()
        
        self.get_info(mid)
        if not self._bool:
            return {'mid':mid}
        self.get_stat(mid)
        self.get_upstat(mid)
        return self.result
    
    def get_proxy(self):
        api = 'http://gec.ip3366.net/api/?key=20190406100218868&getnum=30&anonymoustype=3&area=1&formats=2&proxytype=0'
        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
            }
        resp = requests.get(api, headers=headers)
        return resp.json()
    
    def http_get(self, url):
        proxy = random.choice(self.proxy_list)
        try:
            resp = self.session.get(url, headers={'User-Agent':random.choice(self.ua)}, proxies={'http': proxy}, timeout=(3.05, 30))
        except (requests.ConnectTimeout, requests.exceptions.ProxyError):
            self.proxy_list.remove(proxy)
            raise Exception
        else:    
            if resp.status_code == 200:
                return json.loads(resp.text)
            else:
                print(resp.status_code)
                self._bool = False
    
    def get_info(self, mid):
        url = 'http://api.bilibili.com/x/space/acc/info?mid=%d&jsonp=jsonp' % mid
        try:
            info = self.http_get(url)
        except Exception:
            self.get_info(mid)
        else:
            if info:
                info = info.get('data')
                if not info:
                    self._bool = False
                    return
                d = {
                     'mid': info['mid'], 'name': info['name'], 'sex': info['sex'],
                     'sign': info['sign'], 'level': info['level'], 
                     'birthday': info['birthday'], 'coins': info['coins']
                }
                self.result.update(d)
            else:
                self._bool = False
        
    
    def get_stat(self, mid):
        url = 'http://api.bilibili.com/x/relation/stat?vmid=%d&jsonp=jsonp' % mid
        try:
            stat = self.http_get(url).get('data')
        except Exception:
            self.get_stat(mid)
        else:
            if stat:
                d = {'following': stat['following'], 'follower': stat['follower']}
                self.result.update(d)
        
    
    def get_upstat(self, mid):
        url = 'http://api.bilibili.com/x/space/upstat?mid=%d&jsonp=jsonp' % mid
        try:
            stat = self.http_get(url).get('data')
        except Exception:
            self.get_upstat(mid)
        else:
            if stat:
                stat = {"archive":stat["archive"]["view"],"article":stat["article"]["view"]}
                self.result.update(stat)
       


if __name__ == '__main__':
    Is = InfoSpider()
    print(Is(6467779))

    