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
# Author: YangZheng
# Date: 2018年 01月 24日 星期三 09:19:03 CST
# Email: yangzheng@lezhi.com
#
########################################################################################

import requests
import time
import MySQLdb
# from lxml import etree
from bs4 import BeautifulSoup
import re
try:
    import cookielib
except:
    import http.cookiejar as cookielib
# from urllib import parse
# from multiprocessing import Pool


def getCurrentTime():
    """
    格式化当前时间并返回
    :return:格式化的当前时间
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


class Clawer(object):
    def __init__(self):
        self.session = requests.session()
        self.session.cookies = cookielib.LWPCookieJar(filename='cookies')
        self.login_url = "https://cn.100offer.com/signin"
        self.post_url = 'https://cn.100offer.com/talents/sign_in.json'
        self.headers = {
            "accept": "*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "content-length": 166,
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://cn.100offer.com",
            "referer": "https://cn.100offer.com/signin",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "x-csrf-token": self.getXCsrfToken(),
            "x-requested-with": "XMLHttpRequest",
        }
        self.params = {
            "utf8": "✓",
            "talent[email]": "",
            "talent[password]": "",
            "refer": "",
            "talent[remember_me]": 1,
            "commit": "确定"
        }
        # self.params = parse.urlencode(self.params)

        # 尝试用cookie登录
        try:
            self.session.cookies.load(ignore_discard=True)
            print(getCurrentTime() + " Cookies已加载")
        except:
            print(getCurrentTime() + " 没有Cookies可加载")

        # 打开数据库连接
        self.db = MySQLdb.connect("192.168.1.2", "root", "666", "yz_caiji_100offer")
        self.db.set_character_set("utf8")
        # 使用cursor()方法获取操作游标
        self.cursor = self.db.cursor()


    def getXCsrfToken(self):
        """
        获取登陆界面中的x-csrf-token，并返回
        这里注意获取该登录页面的随机参数和登录时提交表单，要使用同一个session，
        如果不是同一个session，获取的参数与提交表单是的参数不一致，导致验证不通过
        :return: 返回x-csrf-token
        """
        login_page = self.session.get(self.login_url)
        bs = BeautifulSoup(login_page.text, "lxml")
        # x_csrf_token = bs.find('meta', {'name': 'csrf-token'}).get('content')
        x_csrf_token = bs.head.find_all("meta")[8].attrs['content']
        return x_csrf_token

    def isLogin(self):
        url = "https://cn.100offer.com/profile"
        page = self.session.get(url)
        # print(page.text)
        bs = BeautifulSoup(page.text, "lxml")
        try:
            header_bar = bs.find("div", {"class": "header-bar"}).get_text()
            if header_bar == "个人信息":
                return True
        except AttributeError:
            return False

    def login(self):
        # 使用邮箱帐号登录
        self.params['talent[email]'] = input('Please input your account:')
        self.params['talent[password]'] = input('Please input your password:')
        login_page = self.session.post(self.post_url, params=self.params, headers=self.headers)
        if login_page.json()["success"] is True:
            print(getCurrentTime() + " 邮箱登录成功")
            # 保存最新cookie
            self.session.cookies.save()
            return True
        else:
            print(getCurrentTime() + " 邮箱登录失败")
            return False

    def getJobInfo(self, job_info_url):
        """
        内容页采集内容：职位名称 公司名称 薪资 工作经验要求 学历要求 教育经历要求 城市
                     上次活跃时间 技能要求 公司福利 职位介绍 工作地点 URL 职位ID
        :param job_info_url: offer内容页的url
        :return: 一个职位的所有信息
        """
        job_info = dict()

        try:
            print(getCurrentTime(), "parsing", job_info_url)
            response = self.session.get(job_info_url)
            bs = BeautifulSoup(response.text, "lxml")
            info_block = bs.find("div", {"class": "position-info-block p-4-4"})
            job_info["name"] = info_block.find("div", {"class": "home-title"}).get_text()
            job_info["company"] = info_block.find("p").get_text()
            job_info["worktime"] = info_block.find_all("div", {"class": "blog-text info-item mr20"})[0].get_text()
            job_info["education"] = info_block.find_all("div", {"class": "blog-text info-item mr20"})[1].get_text()
            job_info["edu_experience"] = info_block.find_all("div", {"class": "blog-text info-item mr20"})[2].get_text()
            job_info["salary"] = info_block.find("div", {"class": "h3-font info-item mr30"}).get_text()
            job_info["city"] = info_block.find("div", {"class": "blog-text info-item"}).get_text()
            last_time = info_block.find("div", {"class": "refresh-time p-font mt20"}).get_text()
            # 上次活跃时间：2018.01.25 13:22  ->  2018.01.25 13:22
            job_info["last_active_time"] = re.findall('[0-9]{4}.[0-9]{2}.[0-9]{2} [0-9]{2}:[0-9]{2}', last_time)[0]
            skills = info_block.find_all("div", {"class": "new-tag tag-3 mr10 mt10"})
            job_info["skills"] = [s.get_text() for s in skills]
            ski = ""
            for x in job_info["skills"]:
                ski = ski + x + " "
            job_info["skills"] = ski
            job_info["welfare"] = info_block.find("div", {"class": "content mt10 p-font"}).get_text()
            job_info["job_introduction"] = info_block.find("div", {"class": "content mt10 p-font lh36"}).get_text()
            job_info["workplace"] = info_block.find_all("div", {"class": "content mt10 p-font"})[1].get_text()
        except AttributeError:
            print(getCurrentTime(), job_info_url, "解析错误")
        except Exception as e:
            print(getCurrentTime(), job_info_url, e)
        finally:
            return job_info

    def getJobList(self, start_page, end_page=-1):
        """
        获取列表页所有offer的职位ID、职位URL、是否推荐内容并返回
        :return:
        """
        job_list_url = "https://cn.100offer.com/job_positions/positions_list?locations=all&company_size=all" \
                       "&degree=all&industry=all&work_year=0%2C11&page={}"
        job_info_base_url = "https://cn.100offer.com/job_positions/{}"

        end_page = start_page if end_page == -1 else end_page
        for page in range(start_page, end_page + 1):  # 1-187
            try:
                print(getCurrentTime(), "crawling", job_list_url.format(page))
                response = self.session.get(job_list_url.format(page))
                # text还是乱码，所以将是否推荐和url保存下来，其他信息在详情页获取
                html = response.text.encode('utf-8').decode('unicode_escape')
                bs = BeautifulSoup(html, "lxml")
                job_ids = []
                for i in bs.find_all("a", {"class": "h3-font"}):
                    job_ids.append(i.get("href").split("/")[-1])

                recommends = list()
                for i, info in enumerate(bs.find_all("div", {"class": "position-info"})):
                    recommends.append(1 if info.find_all("div", {"class": "new-tag tag-2"}) else 0)

                for i, job_id in enumerate(job_ids):
                    recommend = recommends[i]
                    job_info_url = job_info_base_url.format(job_id)     # 职位URL
                    job_info = self.getJobInfo(job_info_url)
                    job_info["job_id"] = job_id
                    job_info["recommend"] = recommend
                    job_info["url"] = job_info_url
                    # print(job_info)
                    # jobs.append(job_info)
                    yield job_info

            except AttributeError:
                print(getCurrentTime(), job_list_url.format(page), "解析出错")
                continue
            except Exception as e:
                print(getCurrentTime(), job_list_url.format(page),e)
                continue

    def saveJobs(self, jobs):
        """
        将所有职位存入Mysql中
        :param jobs:所有招聘信息，有字典组成的list
        """

        # 建表sql语句
        """
        create table jobs( 
        id int(4) primary key not null auto_increment,  
        job_id int(10) not null,
        recommend int(2),
        url varchar(200),
        name varchar(50) not null,
        company varchar(50),
        worktime varchar(20), 
        education varchar(20), 
        edu_experience varchar(30),
        salary varchar(20), 
        city varchar(15), 
        last_active_time varchar(30),
        skills varchar(80),
        welfare varchar(150),
        job_introduction varchar(1000),
        workplace varchar(30)    
        )ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
        """
        # 插表sql语句
        insert_sql = 'insert into jobs (job_id, recommend, url, name, company, worktime, education, edu_experience, ' \
                     'salary, city, last_active_time, skills, welfare, job_introduction, workplace) ' \
                     'values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        param = list()
        for job in jobs:
            param.append([job['job_id'], job['recommend'], job['url'], job['name'], job['company'], job['worktime'],
                          job['education'], job['edu_experience'], job['salary'], job['city'], job['last_active_time'],
                          job['skills'], job['welfare'], job['job_introduction'], job['workplace']])

        self.cursor.executemany(insert_sql, param)
        # 只有执行插入时需要commit
        self.db.autocommit(on="jobs")

        # 释放资源
        self.cursor.close()
        self.db.close()

    def run(self):
        if self.isLogin():
            print(getCurrentTime() + " cookie登录成功")
        else:
            if self.login() is False: return

        jobs = self.getJobList(1)
        self.saveJobs(jobs)


if __name__ == '__main__':
    Clawer().run()