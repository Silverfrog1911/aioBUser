# -*- coding: utf-8 -*-
import asyncio
import aiohttp
import time
import json
import redis
import requests


class GetProxies:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.61 Safari/537.36',
        }
        self.url = 'http://api.bilibili.com/x/space/acc/info?mid=2&jsonp=jsonp' # 用于验证代理的URL
        self.r = redis.Redis(decode_responses=True)
        self.rset = 'sproxies' # redis集合, 存储已提取的代理
        
#    
    def start(self):
        self.vset = 'vproxies' # redis集合, 存储有效的代理
        n = 0
        while True:
            n += 1
            if n == 10:
                print('--开始验证已获取代理--')
                self.test_proxy()
                n = 0
            print('---开始获取代理---')
            self.get_proxy()
            print('---获取完成，代理池数量：(%d)---' % self.r.scard(self.vset))
            time.sleep(5)
            
    def test_proxy(self):
        proxy_list = self.r.smembers(self.rset) 
        self.run(proxy_list)
        
    def get_proxy(self):
        proxy_list = self.get_api()
        if proxy_list:
            self.r.sadd(self.rset, *proxy_list)
            self.run(proxy_list)
#            p_list = [x for x in proxy_list if not self.r.sismember(self.rset, x)]
#            if p_list:
#                print('去重后代理数量为：%d' % len(p_list))
#                self.r.sadd(self.rset, *p_list)
#                self.run(p_list)
        
    def get_api(self):
        api = 'http://gec.ip3366.net/api/?key=20190406100218868&getnum=500&area=1&formats=2&proxytype=01'
        resp = requests.get(api, headers=self.headers)
        try:
            data = json.loads(resp.text, strict=False)
            return ['http://' + proxy['Ip'] + ':' + str(proxy['Port']) for proxy in data]
             
        except json.decoder.JSONDecodeError:
            print('JSONDecodeError')
    
    async def get(self, proxy, session):
        '''
        '''
        try:
            async with session.get(self.url, timeout=10, proxy=proxy) as resp:
                if resp.status == 200:
                    self.r.sadd(self.vset, proxy)
                    
        except (aiohttp.ClientError, aiohttp.client_exceptions.ClientConnectorError, asyncio.TimeoutError):
            pass
        
       
    
    async def main(self, proxy_list):
        tasks = []
        async with asyncio.Semaphore(500):
            session = aiohttp.ClientSession(headers=self.headers)
            for proxy in proxy_list:
                task = asyncio.ensure_future(self.get(proxy, session))
                tasks.append(task)
            await asyncio.wait(tasks)
            await session.close()
        
    def run(self, proxy_list):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.main(proxy_list))
        loop.run_until_complete(asyncio.sleep(0))
        loop.close()
        
           
        
if __name__ == '__main__':
    g = GetProxies()
    g.start()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
