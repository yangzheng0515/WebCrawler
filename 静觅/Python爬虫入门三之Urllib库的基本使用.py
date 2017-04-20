# coding:utf-8
import urllib.request
import sys
import io
# 1.分分钟扒一个网页下来
'''
关于urllib

urlopen(url, data, timeout)
第一个参数url即为URL，第二个参数data是访问URL时要传送的数据，第三个timeout是设置超时时间。
第二三个参数是可以不传送的，data默认为空None，timeout默认为 socket._GLOBAL_DEFAULT_TIMEOUT

推荐使用下面的Request
因为在构建请求时还需要加入好多内容，通过构建一个request，
服务器响应请求得到应答，这样显得逻辑上清晰明确。  
'''

'''
url = r'http://www.baidu.com'
response = urllib.request.urlopen(url)
print(response.read())
'''


url = r'http://www.baidu.com'
url = r'https://mail.qq.com/'
request = urllib.request.Request(url)
response = urllib.request.urlopen(request)
html = response.read()
print(html)

'''
# POST方式
import urllib
import urllib2
 
values = {"username":"1016903103@qq.com","password":"XXXX"}
data = urllib.urlencode(values) 
url = "https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn"
request = urllib2.Request(url,data)
response = urllib2.urlopen(request)
print response.read()

现在我们模拟登陆CSDN，当然上述代码可能登陆不进去，因为CSDN还有个流水号的字段，
没有设置全，比较复杂在这里就不写上去了，在此只是说明登录的原理。一般的登录网站一般是这种写法。

我们需要定义一个字典，名字为values，参数我设置了username和password，
下面利用urllib的urlencode方法将字典编码，命名为data，构建request时传入两个参数，
url和data，运行程序，返回的便是POST后呈现的页面内容。
'''


'''
GET方式：

至于GET方式我们可以直接把参数写到网址上面，直接构建一个带参数的URL出来即可。


import urllib
import urllib2

values={}
values['username'] = "1016903103@qq.com"
values['password']="XXXX"
data = urllib.urlencode(values) 
url = "http://passport.csdn.net/account/login"
geturl = url + "?"+data
request = urllib2.Request(geturl)
response = urllib2.urlopen(request)
print response.read()
'''