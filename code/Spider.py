#-*-coding:utf-8-*-
from urllib2 import Request
from lxml import etree
import urllib2,jieba
import urllib
import re
from DB import DataOperate
import jieba
class InfoSpider(object):
	"""爬取微博个人信息"""
	headers = ""
	uid_list = []
	MAX_NUMBER = 5000
	uid_instance = None #数据库连接对象
	def __init__(self):

		#初始化header 和URL
		self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
				   'Cookie':'_T_WM=23abbae898e0d46c36553156789cd4ce;\
				    SUB=_2A256NaTHDeRxGeVO4lAQ-SvJzDmIHXVZ2cyPrDV6PUJbrdAKLUvVkW1LHeswrTXg_dvXGChJMnM8A_txA8Bdig..;\
				    gsid_CTandWM=4umIf2d91SNM45GJuyTgZcYq79h'
				  }
	def _request_url(self,url):
		try:
			req = urllib2.Request(url = url,headers = self.headers) #初始化Request请求对象，获得一个req实例
			res =  urllib2.urlopen(req)
			feeddata = res.read() #这里返回的是file_like object
			html = etree.HTML(feeddata)
			return html
		except urllib2.URLError, e:
			if hasattr(e,"reason"):
				print "请求数据失败，失败的原因为："+e.reason
				return None

	def getFollow(self,number):
		"""
		获取该用户的粉丝的in_number
		eg:http://weibo.cn/3092195575/follow?page=1&vt=4 该用户的3092195575
		此id 为唯一id，且有必要做唯一存储
		"""
		self.uid_instance = DataOperate()
		self.uid_list.append(number)
		for num in self.uid_list:  
			print "正在获取%d的follow uid..."% num
			pattern = re.compile('[0-9]{10}')
			for count in range(50):
				url = 'http://weibo.cn/%d/fans?vt=4&page=%d'% (num,count+1)
				# url = 'http://weibo.cn/%d/follow?page=%d&vt=4'% (num,count+1)
				html = self._request_url(url)
				list_elemet = html.xpath('//table')
				if len(list_elemet) == 0:
					break
				else:
					li = html.xpath('//table/tr/td[1]/a/@href')
					for element in li:  #解析出每一个url的10位数字的id信息
						result = re.search(pattern,element)
						if result:
							# uid_list.append(int(result.group(0)))
							temp = int(result.group(0))
							if temp not in self.uid_list:
								self.uid_instance.insert_data(temp,element) #将uid和对应的url放入到数据库中
								self.uid_list.append(temp)
								print "%d 被加进来了,数量达到%d"% (temp,len(self.uid_list))
								if len(self.uid_list) == self.MAX_NUMBER:
									print "uid_list 已达到最大值,请处理"
									self.uid_instance._commit_data()  #提交数据到数据库
									return
	def getselfInfo(self,number):
		"""
		抓取个人资料
		URL的用例为:http://weibo.cn/3092195575/info?vt=4
		"""
		url  = 'http://weibo.cn/%d/info?vt=4'% (number)
		html = self._request_url(url)
		first = html.xpath('//div[@class="c"][5]/a/text()')
		second = html.xpath('//div[@class="c"][5]/text()')
		for i in range(len(second)):
			print first[i].encode('utf-8')+' '+second[i].encode('utf-8')	
		# print  html.xpath('//div[@class="c"]/a/text()')[14].encode('utf-8')
		# print  html.xpath('//div[@class="c"]/a/text()')[15].encode('utf-8')
		#print feeddata
		print '\n------------------------------\n'.encode('utf-8')
	def getOthersInfo(self):
		"""
		抓取其它人的个人资料
		URL的用例为:http://weibo.cn/3092195575/info?vt=4
		也就是这里的中间的10位数字不同，其它都一样
		"""
		key = "黑龙江"
		area = "地区"
		self.uid_instance = DataOperate()
		temp_uid_list = self.uid_instance.select_data() #选取数据的id，信息
		temp_uid_list = list(temp_uid_list)
		for number in temp_uid_list:
			url  = 'http://weibo.cn/%s/info?vt=4'% (list(number)[0].encode('utf-8'))
			html = self._request_url(url)
			second = html.xpath('//div[@class="c"][3]/text()')
			judge = 0
			for i in range(len(second)):
				if area in second[i].encode('utf-8'):
					if key in second[i].encode('utf-8'):
						judge = 1
						break
			if judge == 1:
				temp = ''.join(second) # list to string
				print str(list(number))+' '+temp.encode('utf-8')
				self.uid_instance.update_info(list(number)[0].encode('utf-8'),temp)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
			else:
				print "the number %s need to remove from the uid_list"%(number)
				# temp_uid_list.remove(number)
				self.uid_instance.remove_data(number)
			print "------------------------------"
		self.uid_instance._commit_data()
	def crawlContent(self):
		"""
		抓取个人主页前50条原创微博，以及每条微博的赞，转发，评论，收藏
		url格式为：http://weibo.cn/u/(uid)?filter=1&page=2&vt=4
		"""
		self.uid_instance = DataOperate() # 打开数据库操作句柄
		id_list = list(self.uid_instance.select_data()) #选择出所有的Id信息,只不过这里的元素都是元组的形式
		print "~~开始抓取个人微博:~~"
		for id_element in id_list:
			for count in range(5): #只取出每个用户前5页的微博数据
				id_utf8 = list(id_element)[0].encode('utf-8')
				url = 'http://weibo.cn/u/%s?filter=1&page=%d&vt=4'%(id_utf8,count+1)
				html = self._request_url(url)
				content = html.xpath('//div[@class="c"]/div[1]/span[1]/text()') #这里返回的一页的所有的原创微博
				for i in range(len(content)): #除去中间的空白行
					temp = content[i].encode('utf-8')
					# print type(temp.strip())
					if len(temp.strip()) > 10:
						content_strip =  temp.strip()
						self.uid_instance.insert_content(id_utf8,content_strip)
					# if temp.strip():
					# 	# content.remove(content[i])
					# 	print content[i].encode('utf-8')
						print '\n-----------------------\n'
		self.uid_instance._commit_data()
	def word_analysis(self):
		# 应用结巴分词
		d = {} # 统计短语的字典
		strings = self.uid_instance = DataOperate() # 打开数据库操作句柄
		content_list = list(self.uid_instance.select_content())
		for strs in content_list:
			strs_analyse = jieba.lcut_for_search(list(strs)[0].encode('utf-8'))
			for i in strs_analyse:
				if not d.has_key(i):
					d[i] = 1
				else:
					d[i] = d[i] + 1
		li = sorted(d.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
		for i in range(500):
			if len(li[i][0].encode('utf-8'))>4: #筛选字节数大于4的字节
				print li[i][0].encode('utf-8')+' '+str(li[i][1])
		self.uid_instance._commit_data() #关闭数据库链接句柄
print u"开始抓取个人信息".encode('utf-8')
userInfo = InfoSpider()
# userInfo.getselfInfo(3092195575)
userInfo.getFollow(3092195575)
userInfo.getOthersInfo()
# print "个人信息抓取完毕"
# print "抓取的总数为:%d\n剩下的用户数为:%d"%(userInfo.MAX_NUMBER,len(userInfo.uid_list))
userInfo.crawlContent()
userInfo.word_analysis()