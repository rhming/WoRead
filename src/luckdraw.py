# -*- coding: utf8 -*-
from lxml import etree
from flowdraw import WoRead


class LuckDraw(WoRead):

    def __init__(self, mobile):
        super(LuckDraw, self).__init__(mobile)
        print(self.session.headers)

    def index(self):
        self.session.headers['X-Requested-With'] = 'com.sinovatech.unicom.ui'
        url = f'http://st.woread.com.cn/touchextenernal/seeadvertluckdraw/index.action?channelid=18000677&backTo=YDSY&yw_code=&desmobile={self.mobile}&version=android@8.0703'
        resp = self.session.get(url=url)
        resp.encoding = 'utf8'
        # print(resp.text)

        cookies = resp.cookies.get_dict()
        if cookies.get('JSESSIONID', False):
            self.CookieDict.update(cookies)
            self.saveCookie()
            self.session.headers['Cookie'] = self.CookieDictToString()

        e = etree.HTML(resp.text)
        num = int(e.xpath('string(//sapn[@id="drawNum_id"])'))
        self.CookieDict.update(resp.cookies.get_dict())
        return num

    def doDraw(self, acticeindex):
        url = 'http://st.woread.com.cn/touchextenernal/seeadvertluckdraw/doDraw.action'
        '''
                5-21(over): jRFMzZCMEM0MjJGRjZFMkQ3RUVFN0ZERTEyQUI4MTc=
                6-21(over): QjRFMzZCMEM0MjJGRjZFMkQ3RUVFN0ZERTEyQUI4MTc=
                6-21(start): NzJBQTQxMEE2QzQwQUE2MDYxMEI5MDNGQjFEMEEzODI=
        '''
        data = {
            'acticeindex': acticeindex,
            'userType': '112_3001',
            'homeArea': '075',
            'homeCity': '759'
        }
        # data['acticeindex'] = 'jRFMzZCMEM0MjJGRjZFMkQ3RUVFN0ZERTEyQUI4MTc='
        self.session.headers['Referer'] = f'http://st.woread.com.cn/touchextenernal/seeadvertluckdraw/index.action?channelid=18000677&backTo=YDSY&yw_code=&desmobile={self.mobile}&version=android@8.0703'
        resp = self.session.post(url=url, data=data)
        print(acticeindex + ' ' + resp.text)

    def run(self):
        try:
            num = self.index()
            if num == 0:
                print('抽奖次数已用完...')
                return
            print(f'#luckdraw#第{6 - num}次抽奖...')
            self.doDraw('NzJBQTQxMEE2QzQwQUE2MDYxMEI5MDNGQjFEMEEzODI=')
            if num == 1:
                self.flushTime(3)
                self.doDraw('QjRFMzZCMEM0MjJGRjZFMkQ3RUVFN0ZERTEyQUI4MTc=')
        except Exception as e:
            print(e)
