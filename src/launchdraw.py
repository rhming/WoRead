# -*- coding:utf8 -*-
import re
import requests
from lxml import etree
from flowdraw import WoRead


class LaunchDraw(WoRead):

    def __init__(self, mobile):
        super(LaunchDraw, self).__init__(mobile)

        self.isdrawtoday = False

    def index(self):
        '''
        活动首页 html
        return text/html
        '''
        self.session.headers.update({
            "Accept": "text/html, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://st.woread.com.cn/touchextenernal/readluchdraw/index.action"
        })
        url = 'https://st.woread.com.cn/touchextenernal/readluchdraw/goldegg.action'
        resp = self.session.post(url=url)

        cookies = resp.cookies.get_dict()
        if cookies.get('JSESSIONID', False):
            self.CookieDict.update(cookies)
            self.saveCookie()
            self.session.headers['Cookie'] = self.CookieDictToString()

        e = etree.HTML(resp.text)
        if e.xpath("//div[@class='cardStateTex']/span/text()")[2].find("今日 已打卡") > -1:
            self.isdrawtoday = True

        cardList = e.xpath("//div[@class='cardBtn noCarded']/div[2]/@onclick")

        for cardText in cardList:
            # print(cardText)
            if cardText.find('fillDrawTimes') == -1:
                continue
            date_string = re.findall(
                r".+fillDrawTimes\('(\d+)'.+", cardText)[0]
            # print(date_string)
            self.fillDrawTimes(date_string)
            self.flushTime(20)

    def fillDrawTimes(self, date_string):
        '''
        param date_string 20210601
        补签 
        return text/html
        '''
        print(f'{date_string}补签')
        self.session.headers.update({
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://st.woread.com.cn/touchextenernal/readluchdraw/index.action"
        })
        url = f'https://st.woread.com.cn/touchextenernal/readluchdraw/fillDrawTimes.action?date={date_string}'
        resp = self.session.get(url=url)
        print(resp.json())
        {
            "code": "0000",
            "message": "上报成功",
            "list": [
                {
                    "clockindate": "20210624",
                    "continuityDays": 3,
                    "clockintime": "2021-06-24 18:59:53",
                    "continuityFlag": 1,
                    "source": 42,
                    "activeindex": 6640,
                    "useraccount": "13018974080"
                },
                {
                    "clockindate": "20210623",
                    "continuityDays": 2,
                    "clockintime": "2021-06-24 19:33:25",
                    "continuityFlag": 1,
                    "source": 42,
                    "activeindex": 6640,
                    "useraccount": "13018974080"
                },
                {
                    "clockindate": "20210622",
                    "continuityDays": 1,
                    "clockintime": "2021-06-24 19:35:37",
                    "continuityFlag": 0,
                    "source": 42,
                    "activeindex": 6640,
                    "useraccount": "13018974080"
                }
            ]
        }

    def addDrawTimes(self):
        '''
        打卡
        return json
        '''
        self.session.headers.update({
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "http://st.woread.com.cn/touchextenernal/contentread/chapter.action?cntindex=1623825&authorname=null&cntname=null&bookcover=null&catid=118609&volumeallindex=2545291&chapterallindex=97507088&chapterseno=1&pageIndex=10821&cardid=11982&payType=NDI3MzJGMTg1RDQ5MDVBOURFQUYyODgxNkJEN0NFQ0M%3D&cntrarflag=1&finishflag=1"
        })
        url = 'http://st.woread.com.cn/touchextenernal/readluchdraw/addDrawTimes.action'
        resp = self.session.post(url=url)
        print(resp.json())
        {
            "code": "0000",
            "list": [
                {
                    "clockindate": "20210624",
                    "continuityDays": 1,
                    "clockintime": "2021-06-24 18:59:53",
                    "continuityFlag": 0,
                    "source": 42,
                    "activeindex": 6640,
                    "useraccount": "13018974080"
                }
            ],
            "message": "上报成功",
            "innercode": "0000"
        }

    def doDraw(self, acticeindex):
        '''
        抽奖
        return json
        '''
        self.session.headers.update({
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Referer": "https://st.woread.com.cn/touchextenernal/readluchdraw/index.action"
        })
        url = 'https://st.woread.com.cn/touchextenernal/readluchdraw/doDraw.action'
        data = {
            "acticeindex": acticeindex
        }
        resp = self.session.post(url=url, data=data)
        print(resp.json())
        {
            "prizedesc": "蜻蜓FM月卡",
            "datetime": "20210624191953",
            "code": "0000",
            "prizetype": "2",
            "message": "1",
            "innercode": "0000"
        }

    def run(self):
        try:
            self.index()
            if not self.isdrawtoday:
                self.addDrawTimes()
            for acticeindex in [
                "QjUxRUZCMURBRUUyMzM2NTgwNUY2NzZGRTgxRUZGQUQ=",  # //一次 看视频20日流量
                "NzFGQzM2Mjc4RDVGNUM4RTIyMzk4MkQ3OUNEMkZFOUE=",  # //默认
                "OTJGMDkwNjk0Mjc4MjU2MkQyQjIyMzRGRDRGQzk4MzA=",  # //额外
            ]:
                print(f'{self.mobile}抽奖-{acticeindex}')
                self.doDraw(acticeindex)
                self.flushTime(3)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    import sys
    import codecs
    sys.stdout = codecs.getwriter("utf8")(sys.stdout.detach())
    LaunchDraw('13018974080').run()
