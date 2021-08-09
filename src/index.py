# -*- coding: utf8 -*-
from flowdraw import WoRead
from threading import Thread
from luckdraw import LuckDraw
from bookdraw import BookDraw
from launchdraw import LaunchDraw
from prizedetail import Prize
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
    # 根据云函数触发配置 更改相应时间段
    # format_localtime 小时分钟
    format_localtime = int(time.strftime("%H%M", time.localtime(time.time() + 8 * 60 * 60)))
    # 总计5次
    if format_localtime < 1200:  # 在12点0分前执行该任务
        Template(LuckDraw)
        Template(BookDraw)
    # 总计1次
    if format_localtime >= 600 and format_localtime < 630:  # 在6点0分到6点30分之间执行该任务
        Template(LaunchDraw)
    # 自动领取抽奖奖品(时间段尽量在所有抽奖任务完成后)
    if format_localtime >= 930 and format_localtime < 1000:  # 在9点30分到10点0分之间执行该任务
        Template(Prize)
