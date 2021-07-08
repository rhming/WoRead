# -*- coding:utf8 -*-
import os
import json
import execjs
import requests
from time import sleep
from lxml import etree
from random import randint
from urllib.parse import urlencode

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class WoRead:

    def __init__(self, mobile):
        self.mobile = mobile
        self.session = requests.Session()
        self.session.headers = requests.structures.CaseInsensitiveDict({
            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; MI 8 SE Build/OPM1.171019.019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36; unicom{version:android@8.0703,desmobile:%s};devicetype{deviceBrand:Xiaomi,deviceModel:MI 8 SE};{yw_code:}' % mobile,
            'Origin': 'http://st.woread.com.cn'
        })

        self.CookieDict = {}
        self.CookieString = ''

        self.CookieString = self.readCookie()
        self.CookieDict = self.CookieStringToDict()
        self.session.headers['Cookie'] = self.CookieString

    def getEncryptMobile(self):
        with open(BASE_DIR + '/security.js', 'r', encoding='utf8') as fr:
            securityJs = fr.read()
        scriptText = '''
        function getEncryptMobile(mobile) {
            var modulus = "00A828DB9D028A4B9FC017821C119DFFB8537ECEF7F91D4BC06DB06CC8B4E6B2D0A949B66A86782D23AA5AA847312D91BE07DC1430C1A6F6DE01A3D98474FE4511AAB7E4E709045B61F17D0DC4E34FB4BE0FF32A04E442EEE6B326D97E11AE8F23BF09926BF05AAF65DE34BB90DEBDCEE475D0832B79586B4B02DEED2FC3EA10B3";
            var exponent = "010001";
            var key = window.RSAUtils.getKeyPair(exponent, '', modulus);
            mobile = window.RSAUtils.encryptedString(key, mobile);
            return mobile
        }
        '''
        scriptText = 'var window = {};' + securityJs + scriptText
        ctx = execjs.compile(scriptText)
        EncryptMobile = ctx.call('getEncryptMobile', self.mobile)
        return EncryptMobile

    def flushTime(self, timeout):
        for _ in range(timeout, 0, -1):
            sleep(1)

    def CookieDictToString(self):
        return '; '.join(['='.join([k, self.CookieDict[k]]) for k in self.CookieDict])

    def CookieStringToDict(self):
        return {
            item.split('=', 1)[0]: item.split('=', 1)[1] for item in self.CookieString.split('; ')
        }

    def saveCookie(self):
        resp = requests.post(
            url="https://isolatemac.pythonanywhere.com/store/", 
            data={
                "key": self.mobile + "WoRead", 
                "value": self.CookieDictToString()
            }, 
            headers={
                "Authorization": "",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
            }
        )
        print(resp.json())

    def readCookie(self):
        resp = requests.get(
            url="https://isolatemac.pythonanywhere.com/store/", 
            params={"account": self.mobile + "WoRead"}, 
            headers={
                "Authorization": "",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
            }
        )
        message = resp.json()
        data = message["msg"]
        return data[self.mobile + "WoRead"]

    def index(self):
        self.session.headers['X-Requested-With'] = 'com.sinovatech.unicom.ui'
        url = f'https://st.woread.com.cn/touchextenernal/read/index.action?channelid=18000827&type=1&yw_code=&desmobile={self.mobile}&version=android@8.0703'
        resp = self.session.get(url=url)
        self.CookieDict.update(resp.cookies.get_dict())

        cookies = resp.cookies.get_dict()
        if cookies.get('JSESSIONID', False):
            self.CookieDict.update(cookies)
            self.saveCookie()
            self.session.headers['Cookie'] = self.CookieDictToString()

    def login(self):
        url = 'https://st.woread.com.cn/touchextenernal/common/shouTingLogin.action'
        data = {
            'phonenum': self.getEncryptMobile()
        }
        self.session.headers['Origin'] = 'http://st.woread.com.cn'
        self.session.headers['Referer'] = f'https://st.woread.com.cn/touchextenernal/read/index.action?channelid=18000827&type=1&yw_code=&desmobile={self.mobile}&version=android@8.0703'
        self.session.headers['X-Requested-With'] = 'XMLHttpRequest'
        resp = self.session.post(url=url, data=data)
        print(self.mobile + ' ' + resp.text)
        self.CookieDict.update(resp.cookies.get_dict())
        self.saveCookie()
        self.session.headers['Cookie'] = self.CookieDictToString()

    def popupListInfo(self):
        url = 'https://st.woread.com.cn/touchextenernal/read/popupListInfo.action'
        resp = self.session.post(url=url)
        try:
            resp.json()
            return True
        except:
            return False

    def getGrowScore(self):
        url = 'http://st.woread.com.cn/touchextenernal/read/getGrowScore.action'
        resp = self.session.post(url=url, allow_redirects=False)
        print(self.mobile + ' ' + resp.text)

    def ajaxUpdatePersonReadtime(self):
        url = 'http://st.woread.com.cn/touchextenernal/contentread/ajaxUpdatePersonReadtime.action'
        data = {
            'cntindex': '2254283',
            'cntname': '带刺的朋友',
            'time': '2'
        }
        data = urlencode(data).encode('utf8')
        resp = self.session.post(url=url, data=data)
        print(self.mobile + ' ' + resp.text)

    def sendRightOfGoldCoin(self, sendTry=1):
        url = 'http://st.woread.com.cn/touchextenernal/readActivity/sendRightOfGoldCoin.action?userType=112&homeArea=036&homeCity=360'
        resp = self.session.get(url=url)
        print(self.mobile + ' ' + resp.text)
        data = resp.json()
        if data['innercode'] == '2003':
            return 0
        if data['innercode'] == '2004':
            pass
        if data['innercode'] == '2008':
            return 0
        if data['innercode'] != '0000' and sendTry > 0:
            self.flushTime(120)
            self.ajaxUpdatePersonReadtime()
            self.sendRightOfGoldCoin(sendTry - 1)
        else:
            data = resp.json()
            return data['message']['daySurplus']

    def checkRightOfGoldCoin(self):
        url = 'http://st.woread.com.cn/touchextenernal/readActivity/checkRightOfGoldCoin.action'
        resp = self.session.get(url=url)
        print(self.mobile + ' ' + resp.text)
        try:
            data = resp.json()
            return data['message']['ptimes'] + 1
        except:
            return 11

    def run(self):
        if not self.popupListInfo():
            self.index()
            self.login()
        self.session.headers['Referer'] = 'http://st.woread.com.cn/touchextenernal/contentread/chapter.action?cntindex=2254283&authorname=null&cntname=null&bookcover=null&catid=118381&volumeallindex=2937704&chapterallindex=109243887&chapterseno=1&pageIndex=10681&cardid=11854&payType=NDI3MzJGMTg1RDQ5MDVBOURFQUYyODgxNkJEN0NFQ0M%3D&cntrarflag=1&finishflag=1'
        start = self.checkRightOfGoldCoin()
        if start == 11:
            return
        print(f'{self.mobile}第{start}次'.center(64, '-'))
        self.getGrowScore()
        self.flushTime(60)
        for _ in range(3):
            self.ajaxUpdatePersonReadtime()
            if _ < 2:
                self.flushTime(120)
            else:
                self.flushTime(randint(25, 30))
        self.sendRightOfGoldCoin()

