# _*_coding: utf-8 _*_

########################################################################################
#
# 100offer招聘信息采集
# 入口页/列表页：https://cn.100offer.com/job_positions
# 内容页：https://cn.100offer.com/job_positions/11890
# 列表页采集内容：职位ID、职位URL、是否推荐
# 内容页采集内容：职位名称 公司名称 薪资 工作经验要求 学历要求 教育经历要求 城市
#              上次活跃时间 技能要求 公司福利 职位介绍 工作地点 URL 职位ID
#
# 帐号： 用户名：hfyanhai@163.com，密码：******
#
# Author: YangZheng
# Date: 2018年 01月 24日 星期三 09:19:03 CST
# Email: yangzheng@lezhi.com
#
########################################################################################

import requests
from bs4 import BeautifulSoup
import time


class Spider(object):
    def __init__(self):
        """
        初始化信息
        """
        self.session = requests.session()
        token = self.get_init_cookies()
        self.login(token)

    def get_init_cookies(self):
        """
        访问登录页面，获得初始cookies
        :return:
        """
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Cache-Control': 'no-cache',
            'Host':' cn.100offer.com',
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0',
        }
        self.session.headers.update(headers)
        resp = self.session.get('https://cn.100offer.com/signin')
        bsobj = BeautifulSoup(resp.content, 'lxml')
        return bsobj.find('meta', {'name': 'csrf-token'}).get('content')

    def login(self, token):
        """
        访问登录页面
        :param token:表单token
        :return:
        """
        headers = {
            'Accept': '*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Cache-Control': 'no-cache',
            'Content-Length': '141',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'cn.100offer.com',
            'Pragma': 'no-cache',
            'Referer': 'https://cn.100offer.com/signin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0',
            'X-CSRF-Token': token,
            'X-Requested-With': 'XMLHttpRequest'
        }
        params = {
            'utf8': '✓',
            'talent[email]': 'hfyanhai@163.com',
            'talent[password]': 'xinanhui',
            'refer': '',
            'talent[remember_me]': '0',
            'commit': '确定'
        }
        self.session.headers.update(headers)
        time.sleep(1)
        resp = self.session.post('https://cn.100offer.com/talents/sign_in.json', data=params)
        print(resp)
        print(resp.content)


if __name__ == '__main__':
    Spider()
