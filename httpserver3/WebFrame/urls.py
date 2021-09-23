"""
作者：zyy
日期：2021年08月29日
"""
'''
    可以接收客户端什么样的数据
'''
from views import *
urls = [
    ('/time',show_time),
    ('/hello',hello),
    ('/bye',bye)
]
