import pymysql

conn = pymysql.connect(  # 连接本地数据库
    host="localhost",
    user="root",  # 要填root
    password="htht0928",  # 填上自己的密码
    database="doubanbook",  # 数据库名
    charset="utf8"
)
cur = conn.cursor()
create_books_table_sql = """
     CREATE TABLE `books`(
    `book_name` VARCHAR(20) NOT NULL UNIQUE,
    `author` VARCHAR(20) NOT NULL,
    `press` VARCHAR(20),
    `publishing_year` VARCHAR(10),
    `score` FLOAT,
    `rating_num` INTEGER,
    `page_num` VARCHAR(10),
    `price` VARCHAR(10),
    `ISBN` VARCHAR(30),
    `content_introduction` VARCHAR(2000),
    `cover_url` VARCHAR(100),
    `readers` VARCHAR (400)
    )
"""

try:
    cur.execute(create_books_table_sql)
except Exception as e:
    print(e)
    conn.rollback()
