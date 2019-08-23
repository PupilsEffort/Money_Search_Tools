#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'whynot'
# __time__   = '2019/1/11 2:43 PM'

import requests
import re
import time
#http://www.beianbeian.com/search-1/%E4%BA%ACICP%E8%AF%81030173%E5%8F%B7?jdfwkey=njtqn1
#http://www.beianbeian.com/search/wanmei.com

pattern1 = re.compile(u'<a href="(.*?)">\[反查\]')
pattern2 = re.compile(u'<a href="/go\?url=(.*?)" target="_blank">')
pattern3 = re.compile(u'MainPage:"(.*?)"')


def get_brother(domain):
    lst = []
    dict = {}
    _ = domain.strip()
    try:
        _ = _.strip()
        lst.append(_)
        req3 = requests.get('http://icp.chinaz.com/ajaxsync.aspx?at=beiansl&callback=jQuery111305952303145188234_1541415249827&host=' + _ +'&type=host&_=1541415249828')
        c = re.findall(pattern3,req3.text)
        for _c in c:
            for _a in _c.split(' '):
                _a = _a.replace('www.','')
                _a = _a.replace('izhuye.','')
                _a = _a.replace('zhuye.','')
                lst.append(_a)

        req1 = requests.get('http://www.beianbeian.com/search/' + _)
        a = pattern1.search(req1.text)

        time.sleep(4)
        if a:
            req2 = requests.get(u'http://www.beianbeian.com/' + a.group(1))
            b = re.findall(pattern2,req2.text)
            for __ in b:
                __ = __.replace('www.','')
                __ = __.replace('izhuye..','')
                __ = __.replace('zhuye..','')
                lst.append(__)
        #print _ +  '-' * 10 + (str(set(lst)))
        dict[_] = set(lst)
        return (dict)
    except Exception,e:
        print(e)

if __name__ == "__main__":
    for _ in ['jd.com']:
        print(get_brother(_))