# MySpider
毕业设计-新浪微博数据的抓取+词频的统计
##运行环境：
    python2.7+mysql5.6+Sublime Text2
##完成的功能如下：
    1：本地数据库的存储
    2：用户数据的个人信息抓取
    3：信息地域性的筛选
    4：用户原创数据的抓取
    5：分页数据的自动化抓取
    6：对用户数据词频的统计
##初始化的时候需要填写的初始化信息：
    1：微博手机站点：weibo.cn中用户登录信息的cookie
    2：Mysql数据库的建立：
        spider数据库：
          info表：ID：varchar(50), detail:varchar(200), content:text
          cont表：ID：varchar(50), details:text
       用户名，密码
