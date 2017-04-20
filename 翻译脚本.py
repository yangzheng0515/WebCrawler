# -*- coding:utf-8 -*-
import urllib.request
import urllib.parse
import json

'''
用爬虫写个翻译脚本 yz
'''

while True:
    query = input('请输入要翻译的内容（exit退出）:')
    if query == 'exit':
    	break
    url = r'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=https://www.baidu.com/link'
    data = {
        'type':'AUTO',
        'i':query,
        'doctype':'json',
        'xmlVersion':'1.8',
        'keyfrom':'fanyi.web',
        'ue':'UTF-8',
        'action':'FY_BY_CLICKBUTTON',
        'typoResult':'true'
        }
    data = urllib.parse.urlencode(data).encode('utf-8')
    html = urllib.request.urlopen(url, data).read().decode('utf-8')

    target = json.loads(html)
    print('翻译结果：'+target['translateResult'][0][0]['tgt']+'\n')

'''
General
Request URL:http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=https://www.baidu.com/link
Request Method:POST
Status Code:200 OK
Remote Address:123.58.182.243:80

Response Headers
Connection:keep-alive
Content-Encoding:gzip
Content-Language:zh-CN
Content-Type:application/json;charset=utf-8
Date:Fri, 10 Feb 2017 08:40:46 GMT
Server:Tengine
Transfer-Encoding:chunked
Vary:Accept-Encoding

Request Headers
Accept:application/json, text/javascript, */*; q=0.01
Accept-Encoding:gzip, deflate
Accept-Language:zh-CN,zh;q=0.8
Connection:keep-alive
Content-Length:144
Content-Type:application/x-www-form-urlencoded; charset=UTF-8
Cookie:_ntes_nnid=15f666526e2a10aa1ff06614f005a3f1,1476967426140; OUTFOX_SEARCH_USER_ID_NCOO=261164648.0580904; P_INFO=hfuumt@163.com|1483338941|0|other|00&99|anh&1483338716&carddav#anh&340100#10#0#0|187578&0|urs&mailsettings&mail163|hfuumt@163.com; JSESSIONID=abcL09F6cC30H40TKlNOv; SESSION_FROM_COOKIE=fanyiweb; OUTFOX_SEARCH_USER_ID=142378767@60.168.68.66; ___rl__test__cookies=1486716044443
Host:fanyi.youdao.com
Origin:http://fanyi.youdao.com
Referer:http://fanyi.youdao.com/
User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36
X-Requested-With:XMLHttpRequest

Query String Parameters
view decoded
smartresult:dict
smartresult:rule
smartresult:ugc
sessionFrom:https://www.baidu.com/link

Form Data
view decoded
type:AUTO
i:%C3%A8%C2%9C%C2%98%C3%A8%C2%9B%C2%9B
doctype:json
xmlVersion:1.8
keyfrom:fanyi.web
ue:UTF-8
action:FY_BY_CLICKBUTTON
typoResult:true
'''
