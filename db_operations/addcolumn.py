import pymysql

conn = pymysql.connect(  # 连接本地数据库
    host="localhost",
    user="root",  # 要填root
    password="htht0928",  # 填上自己的密码
    database="doubanbook",  # 数据库名
    charset="utf8"
)
cur = conn.cursor()
sql = "alter table douban_book_users add password VARCHAR(40) not null default '123456'"
# 给爬取下来的用户增添密码字段，默认为123456

try:
    cur.execute(sql)
    conn.commit()
except Exception as e:
    print(e)
    conn.rollback()
