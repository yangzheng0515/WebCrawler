#-*- coding: utf-8 -*-
import urllib
from bs4 import  BeautifulSoup
import requests
headers = {  'User-Agent' : 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; BOIE9;ZHCN)', }
url="https://weibo.cn/login/"   # 微博手机版网页
session=requests.session()
html=session.get(url,headers=headers).content
soup=BeautifulSoup(html, 'lxml')
backURL=soup.find("input",{"name":"backURL"})["value"]
backTitle=soup.find("input",{"name":"backTitle"})["value"]
vk=soup.find("input",{"name":"vk"})["value"]
capId=soup.find("input",{"name":"capId"})["value"]
tryCount=soup.find("input",{"name":"tryCount"})["value"]
submit=soup.find("input",{"name":"submit"})["value"]
imgurl=soup.find("img")["src"]
passname=soup.find("input",{"type":"password"})["name"]
action=soup.find("form")["action"]
urllib.request.urlretrieve(imgurl,"./1.jpg")
code=input(u"验证码:") #手动输入验证码
mobile="******"   #此处输入用户名
password="*******" #此处输入密码
postdata={
    "mobile":mobile,
    passname:password,
    "code":code,
    "remember":"on",
    "backURL":backURL,
    "backTitle":backTitle,
    "tryCount":tryCount,
    "vk":vk,
    "capId":capId,
    "submit":submit,
}
print(url+action)
response=session.post(url+action,data=postdata,headers=headers)
result=session.get("https://weibo.cn").text
print(result)
