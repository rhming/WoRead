# -*- coding: utf8 -*-
from flowdraw import WoRead
from threading import Thread
from luckdraw import LuckDraw
from bookdraw import BookDraw
from launchdraw import LaunchDraw
import time


# import sys
# import codecs
# sys.stdout = codecs.getwriter("utf8")(sys.stdout.detach())


def Template(cls):
    ts = []
    # 手机号配置
    for mobile in ['12345678901', '12345678902']:
        ts.append(Thread(target=cls(mobile).run))
    for t in ts:
        t.start()
    for t in ts:
        t.join()


def main_handler(event=None, context=None):
    
    # 总计10次
    Template(WoRead)
    # 根据触发配置 更改相应时间段
    format_localtime = int(time.strftime("%H%M", time.localtime(time.time() + 8 * 60 * 60)))
    # 总计5次
    if format_localtime < 1200:
        Template(LuckDraw)
        Template(BookDraw)
    # 总计1次
    if format_localtime >= 600 and format_localtime < 630:
        Template(LaunchDraw)
