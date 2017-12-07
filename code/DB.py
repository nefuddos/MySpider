#-*-coding:utf-8-*-
import sys  
import MySQLdb  
  
# reload(sys)  
# sys.setdefaultencoding('utf-8')  
class DataOperate:
	# 定义一些常量
	username = "root"
	password = "admin"
	cur = None
	db = None
	def __init__(self):
		"""
		初始化一些登陆的用户名和密码的信息，选择数据库
		"""
		self.db = MySQLdb.connect(
							 host='localhost',
                             user=self.username,
							 passwd=self.password,
							 charset='utf8mb4',
							 db='spider')  
		self.cur = self.db.cursor()  
	def select_data(self):
		# 选择数据
		sql = 'select ID from info'
		self.cur.execute(sql)
		return self.cur.fetchall()
	def select_content(self):
		sql = 'select details from cont'
		self.cur.execute(sql)
		return self.cur.fetchall()
	def insert_data(self,uid,url):
		# 插入数据
		sql = "insert into info(ID,DETAIL) values(%s,%s)"
		self.cur.execute(sql,(uid,url))
	def insert_content(self,uid,content):
		sql = "insert into cont values(%s,%s)"
		self.cur.execute(sql,(uid,content))
	def update_info(self,uid,content):
		sql = "update info set CONTENT = %s where ID = %s"
		self.cur.execute(sql,(content,uid))
	def remove_data(self,uid):
		sql = "delete from info where ID = %s"
		self.cur.execute(sql,uid)		
	def _commit_data(self):
		# 释放数据库的游标
		self.cur.close()
		self.db.commit()
		self.db.close()
#if __name__  == '__main__':
#	obj = DataOperate()
	#obj.insert_data('123','www.baidu.com')
# 	obj.remove_data('123')
#	print obj.select_data()
