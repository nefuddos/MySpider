#-*-coding:utf-8-*-
from urllib2 import Request
from lxml import etree
import urllib2
import urllib
import re
import DB.DataOperate

class InfoSpider(object):
	"""爬取微博个人信息"""
	headers = ""
	uid_list = []
	MAX_NUMBER = 50
	def __init__(self):
		#初始化header 和URL
		self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
				   'Cookie':'_T_WM=af09e1bc6745545f572ef0d319187b6a;\
				    SUB=_2A256ErTDDeRxGeVO4lAQ-SvJzDmIHXVZ_NyLrDV6PUJbrdANLVLckW1LHetWfRVH7MdDTQynC0YadO38LQurkg..;\
				    gsid_CTandWM=4uH0b1311zkjJRRfzNcCncYq79h'
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
					for element in li:
						result = re.search(pattern,element)
						if result:
							# uid_list.append(int(result.group(0)))
							temp = int(result.group(0))
							if temp not in self.uid_list:
								self.uid_list.append(temp)
								print "%d 被加进来了,数量达到%d"% (temp,len(self.uid_list))
								if len(self.uid_list) == self.MAX_NUMBER:
									print "uid_list 已达到最大值,请处理"
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
		for number in self.uid_list:
			url  = 'http://weibo.cn/%d/info?vt=4'% (number)
			html = self._request_url(url)
			second = html.xpath('//div[@class="c"][3]/text()')
			judge = 0
			for i in range(len(second)):
				if area in second[i].encode('utf-8'):
					if key in second[i].encode('utf-8'):
						judge = 1
						break
			if judge == 1:
				for i in range(len(second)):
					print second[i].encode('utf-8')
					# 这里的用户数据需要存入数据库                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
			else:
				print "the number %d need to remove from the uid_list"%(number)
				self.uid_list.remove(number)
			print "------------------------------"
	def saveInfo(self):
		"""
		将信息存入到数据库中
		"""
	def crawlInfo(self):
		"""
		抓取个人主页前50条原创微博，以及每条微博的赞，转发，评论，收藏
		url格式为：http://weibo.cn/u/(uid)?filter=1
		"""
		print "~~开始抓取个人微博:~~\n"
		url = 'http://weibo.cn/u/3857934673?filter=1'
		html = self._request_url(url)

		content = html.xpath('//div[@class="c"]/div[1]/span[1]/text()')
		for i in range(len(content)): #除去中间的空白行
			temp = content[i].encode('utf-8')
			# print type(temp.strip())
			if len(temp.strip()) > 10:
				print temp.strip()
			# if temp.strip():
			# 	# content.remove(content[i])
			# 	print content[i].encode('utf-8')
				print '\n-----------------------\n'
print "开始抓取个人信息"
userInfo = InfoSpider()
# userInfo.getselfInfo(3092195575)
userInfo.getFollow(3092195575)
userInfo.getOthersInfo()
# print "个人信息抓取完毕"
# print "抓取的总数为:%d\n剩下的用户数为:%d"%(userInfo.MAX_NUMBER,len(userInfo.uid_list))
# userInfo.crawlInfo()