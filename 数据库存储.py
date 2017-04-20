# -*- coding:utf-8 -*-
from urllib import request
from bs4 import BeautifulSoup
import io
import sys
import pymssql

# 五 数据库存储爬取的信息（SQL Server）
'''
连接失败
'''

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码  
url = r'http://www.jianshu.com'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
page = request.Request(url, headers = headers)
page_info = request.urlopen(page).read().decode('utf-8')
soup = BeautifulSoup(page_info, 'html.parser')
titles = soup.find_all('a', 'article-title')
for title in titles:
    print(title.string)

# mysql连接信息（字典形式）
db_config = {
    'host': '127.0.0.1',
#    'port': 3306,
    'user': 'sa',
    'password': '***',
    'database': 'pytest',
    'charset': 'utf-8'
}

# 获得数据库连接
#conn = pymssql.connect(**db_config)
# 数据库配置，获得连接（参数方式）
conn = pymssql.connect(host='172.0.0.1',user='sa',password='0628',database='pytest',charset="utf8")

try:
	# 获得数据库游标
    with connect.cursor() as cursor:
        sql = 'insert into title(title, url) values(%s, %s)'
        for u in titles:
        	# 执行sql语句
            cursor.execute(sql, (u.string, r'http://www.jianshu.com' + u.attrs['href']))
    # 事务提交
    conn.commit()
finally:
    conn.close()
