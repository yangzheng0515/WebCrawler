#coding:utf-8
import urllib.request
import re
import sys

#处理页面标签类
class Tool:
    #去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"",x)
        x = re.sub(self.replaceTD,"",x)
        x = re.sub(self.replacePara,"",x)
        x = re.sub(self.replaceBR,"",x)
        x = re.sub(self.removeExtraTag,"",x)
        #strip()将前后多余内容删除
        return x.strip()
		
		


class BDTB(object):
	def __init__(self, baseUrl, isOnlySeeLZ):
		self.baseUrl = baseUrl
		self.seeLZ = r'?see_lz=' + str(isOnlySeeLZ)
		self.tool = Tool()

	def getPage(self, pageNum):
		url = self.baseUrl + self.seeLZ + r'&pn=' + str(pageNum)
		request = urllib.request.Request(url)
		page = urllib.request.urlopen(request).read().decode('utf-8')
		#print(page)
		return page

	def getTitle(self):
		page = self.getPage(1)
		pattern = re.compile(r'<h3 class="core_title_txt.*?>(.*?)</h3>', re.S)
		result = re.search(pattern, page)
		if result:
			#print(result.group(1).strip())  # 没有strip()也行，，那么strip是干嘛的？   strip()将前后多余内容删除
			return result.group(1).strip()
		else:
			print("title none")
			return None

	def getPageNum(self):
		page = self.getPage(1)
		pattern = re.compile(r'<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>', re.S)
		result = re.search(pattern, page)
		if result:
			#print(result.group(1).strip())
			return result.group(1).strip()
		else:
			print("pageNum none")
			return None

	def getContent(self):
		page = self.getPage(1)
		pattern = re.compile(r'<div id="post_content_.*?<br>(.*?)</div>', re.S)
		result = re.findall(pattern, page)
		#floor = 1
		return result
		# for item in result:
		# 	#print(item)
		# 	if item != '' and item != None and item != '\n':
		# 	    print(str(floor) + '楼-------------------------------------------------------')
		# 	    print(self.tool.replace(item))
		# 	    floor += 1




def main():
    file = open(sys.path[0] + r'\百度贴吧NBA.txt', 'w')
    bdtb = BDTB('http://tieba.baidu.com/p/3138733512', 1)
    pageNum = int(bdtb.getPageNum())
    for i in range(pageNum):
        page = i + 1
        bdtb = BDTB('http://tieba.baidu.com/p/3138733512', 1)
        title = bdtb.getTitle()
        file.write(title + '\n' + '\n')
        #bdtb.getPageNum()
        results = bdtb.getContent()
        floor = 1
        for item in results:
            #print(item)
            if item != '' and item != None and item != '\n':
                file.write(str(floor) + '楼-------------------------------------------------------\n')
                file.write(bdtb.tool.replace(item) + '\n')
                #print(str(floor) + '楼-------------------------------------------------------')
                #print(self.tool.replace(item))
                floor += 1
        file.write("下一页\n")


if __name__ == '__main__':
    main()