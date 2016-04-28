#-*-coding:utf-8-*-
import sys  
import MySQLdb  
  
# reload(sys)  
# sys.setdefaultencoding('utf-8')  
class DataOperate:
	# 定义一些常量
	username = "root"
	password = "nefu_ddos"
	cur = None
	def __init__(self):
		"""
		初始化一些登陆的用户名和密码的信息，选择数据库
		"""
		db = MySQLdb.connect(user=self.username, passwd=self.password)  
		cur = db.cursor()  
		cur.execute('use spider')
	def select_data(self):
		# 选择数据
		sql = 'select * from info'
		cur.execute(sql)
		return cur.fetchall()
	def insert_data(self):
		# 插入数据
		sql = 'insert into info values(\'1234567890\',\'个人信息\')'
		cur.execute(sql)
	def __del__(self):
		# 释放数据库的游标
		cur.close()