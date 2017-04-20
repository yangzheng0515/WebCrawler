import urllib.request
import urllib.error

# url = r'http://www.xxxxxx.com'
# request = urllib.request.Request(url)
# try:
#     html = urllib.request.urlopen(request).read()
# except urllib.error.URLError as e:
#     print(e.reason)

# req = urllib.request.Request('http://blog.csdn.net/yangzheng0515')
# try:
# 	urllib.request.urlopen(req)
# except urllib.error.HTTPError as e:
# 	print(e.code)
# except urllib.error.URLError as e:
# 	print(e.reason)
# else:
# 	print("OK")

req = urllib.request.Request('http://blog.csdn.net/yangzheng0515')
try:
	urllib.request.urlopen(req)
except urllib.error.URLError as e:
	if hasattr(e, 'reason'):
		print(e.reason)
	else:
		print("OK")