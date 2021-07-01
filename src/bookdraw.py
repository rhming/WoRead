# -*- coding:utf8 -*-
import re
from lxml import etree
from flowdraw import WoRead
from random import choice


class BookDraw(WoRead):

    def __init__(self, mobile):
        super(BookDraw, self).__init__(mobile)

    def index(self):
        self.session.headers['X-Requested-With'] = 'com.sinovatech.unicom.ui'
        url = 'https://st.woread.com.cn/touchextenernal/openbook/index.action?channelid=18000690&backTo=YDSY'
        resp = self.session.get(url=url)
        resp.encoding = 'utf8'
        # print(resp.text)

        cookies = resp.cookies.get_dict()
        if cookies.get('JSESSIONID', False):
            self.CookieDict.update(cookies)
            self.saveCookie()
            self.session.headers['Cookie'] = self.CookieDictToString()

        self.categoryList = re.findall(r'cateIds.push\((\d+)\);', resp.text)
        drawNum = re.findall(r'var drawNum = (\d);', resp.text)[0]
        drawNum = int(drawNum)
        # print(drawNum)
        # print(self.categoryList)
        self.CookieDict.update(resp.cookies.get_dict())
        return drawNum

    def doDraw(self, num):
        url = 'https://st.woread.com.cn/touchextenernal/openbook/doDraw.action'
        self.session.headers['Origin'] = 'https://st.woread.com.cn'
        self.session.headers['Referer'] = 'https://st.woread.com.cn/touchextenernal/openbook/index.action?channelid=18000690&backTo=YDSY'
        self.session.headers['X-Requested-With'] = 'XMLHttpRequest'
        data = {
            'categoryId': choice(self.categoryList),
            'currentNum': '%d' % num
        }
        resp = self.session.post(url=url, data=data)
        result = resp.json()
        result['bookInfo'] = ''
        print(result)

    def run(self):
        try:
            drawNum = self.index()
            if drawNum == 0:
                print('抽奖次数已用完...')
                return
            print(f'#bookdraw#第{6 - drawNum}次抽奖...')
            self.doDraw(6 - drawNum)
        except Exception as e:
            print(e)
