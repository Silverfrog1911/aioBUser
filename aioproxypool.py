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
        
    def start(self):
        self.vset = 'vproxies' # redis集合, 存储有效的代理
        n = 0 # 用于间隔标识，每十次检验一次sproxies中代理是否有效
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
        '''
            取出sproxies中代理，检验其有效性
        '''
        proxy_list = self.r.smembers(self.rset) 
        self.run(proxy_list)
        
    def get_proxy(self):
        '''
            这个函数有点多余，不过我喜欢这样写
        '''
        proxy_list = self.get_api()
        if proxy_list:
            self.r.sadd(self.rset, *proxy_list)
            self.run(proxy_list)
        
    def get_api(self):
        '''
            获取代理(http://127.0.0.1:12306)，返回列表
        '''
        pass
    
    
    async def get(self, proxy, session):
        '''
            协程函数，每个协程运行的函数
        '''
        try:
            async with session.get(self.url, timeout=10, proxy=proxy) as resp:
                if resp.status == 200:
                    self.r.sadd(self.vset, proxy)
        # 这三个异常都是代理失效造成的            
        except (aiohttp.ClientError, aiohttp.client_exceptions.ClientConnectorError, asyncio.TimeoutError):
            pass
        
       
    
    async def main(self, proxy_list):
        '''
            所有协程
        '''
        tasks = []
        async with asyncio.Semaphore(500):
            session = aiohttp.ClientSession(headers=self.headers)
            for proxy in proxy_list:
                task = asyncio.ensure_future(self.get(proxy, session))
                tasks.append(task)
            await asyncio.wait(tasks)
            await session.close()
        
    def run(self, proxy_list):
        '''
            运行协程
        '''
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.main(proxy_list))
        loop.run_until_complete(asyncio.sleep(0))
        loop.close()
        
           
        
if __name__ == '__main__':
    g = GetProxies()
    g.start()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
