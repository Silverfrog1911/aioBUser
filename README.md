# 版本
python3.5以上

# 依赖库
pymongo、redis、requests、aiohttp

# 注意
1、Redis服务开启  
2、mongodb服务开启  
3、如果报协程数量太多的错误，可以将aiouser.py里的once参数设置小一点  
4、aioproxypool.py请补全代理接口，否则无法运行

# 其他
1、懒得加多进程，直接运行两个py文件  
2、爬虫是直接从Redis取代理，也可以用aiohttp做个api，但会损失一点效率，我觉得没有必要  
3、B站用户数据存储在mongodb的bilibili.user

# 联系方式(有问题欢迎留言)
CSDN：https://blog.csdn.net/Qwertyuiop2016/article/details/89226209   
Email：kanade@blisst.cn   
GitHub: https://github.com/kanadeblisst/aioBUser 
