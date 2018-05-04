# _*_coding: utf-8 _*_

########################################################################################
#
# 才客网职业信息采集
# URL：http://www.caikevip.com/position-mgl.html?id=555
# 采集内容：职业名称、城市、学历要求、工作经验要求、需求数量、工作职责、职位要求、顾问姓名、URL
#
# Author: YangZheng
# Date: 2018年 01月 23日 星期二 10:56:03 CST
# Email: yangzheng@lezhi.com
#
########################################################################################

import requests
import time
import MySQLdb


def getCurrentTime():
    """
    格式化当前时间并返回
    :return:格式化的当前时间
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


def getJobs():
    """
    发送请求获取数据并解析
    :return: 返回所有招聘信息
    """
    api_url = 'http://www.caikevip.com/pf/position/jdinfo'
    base_url = 'http://www.caikevip.com/position-mgl.html?id={}'
    params = {
        "jd_id": 0,
        "flag": 1
    }
    job = list()

    for id in range(0, 1000):  # 0~878
        params['jd_id'] = id
        # 发送post请求，接收json数据
        r = requests.post(api_url, params=params)
        json_data = r.json()

        # 跳过没有信息的页面
        if json_data['code'] != 0:
            continue

        url = base_url.format(id)
        print(getCurrentTime() + " crawling " + url)

        # 采集内容：职业名称、城市、学历要求、工作经验要求、薪水、需求数量、工作职责、职位要求、顾问姓名、URL
        job_info = dict()
        job_info['name'] = json_data['data']['body_info']['name']
        job_info['city'] = json_data['data']['body_info']['city']
        job_info['education'] = json_data['data']['body_info']['education']
        job_info['worktime'] = json_data['data']['body_info']['worktime']
        job_info['salary'] = json_data['data']['body_info']['salary']
        job_info['number'] = json_data['data']['base_info']['number']
        job_info['job_duty'] = json_data['data']['descipt_info']['job_duty']
        job_info['requirement'] = json_data['data']['descipt_info']['ability_requirement']
        job_info['hh_name'] = json_data['data']['hh_info']['ename']
        job_info['url'] = url
        job.append(job_info)

        # 休息5秒再访问
        # time.sleep(2)

    return job


def saveJobs(jobs):
    """
    将所有职位存入Mysql中
    :param jobs:所有招聘信息，有字典组成的list
    """
    # 打开数据库连接
    db = MySQLdb.connect("192.168.1.2", "root", "666", "yz_caiji_caike")
    db.set_character_set("utf8")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # 建表sql语句
    """create table jobs( 
    id int(4) primary key not null auto_increment,  
    name varchar(50) not null, 
    city varchar(15), 
    education varchar(20), 
    worktime varchar(20), 
    salary varchar(15), 
    number int, 
    job_duty varchar(500), 
    requirement varchar(500), 
    hh_name varchar(20), 
    url varchar(200) 
    )ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;"""

    # 插表sql语句，这里使用批量插入，效率更高 参考：http://blog.csdn.net/colourless/article/details/41444069
    sql = 'insert into jobs (name, city, education, worktime, salary, number, job_duty, ' \
          'requirement, hh_name, url) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    param = list()
    for job in jobs:
        param.append([job['name'], job['city'], job['education'], job['worktime'], job['salary'],
                      job['number'], job['job_duty'], job['requirement'], job['hh_name'], job['url']])

    cursor.executemany(sql, param)
    # 只有执行插入时需要commit
    db.autocommit(on="jobs")

    # 释放资源
    cursor.close()
    db.close()


if __name__ == '__main__':
    jobs = getJobs()
    saveJobs(jobs)


