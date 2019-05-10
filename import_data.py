import sqlite3

conn = sqlite3.connect("data.db")
cu = conn.cursor()
sql = """
create table if not exists students (
    xh VARCHAR (10),
    xm VARCHAR (32),
    xb VARCHAR (8),
    csrq VARCHAR (8),
    bjmc VARCHAR (32),
    dh VARCHAR (11),
    sfzh VARCHAR (18),
    jtzz VARCHAR (64)
)
"""
cu.execute("drop table if exists students")
cu.execute(sql)

"""数据表: 学号、姓名、性别、出生日期、班级、手机号码、身份证号码、家庭住址"""
students = [
    ("1016030426", "月初", "男", "19990101", "计科2班", "18288888888", "230349199901010234", "北京市"),
    ("1016030427", "淮竹", "女", "19990101", "计科1班", "18288888888", "230349199901010234", "北京市"),
    ("1016030428", "王富贵", "女", "19990101", "计科1班", "18288888888", "230349199901010234", "王权霸业"),
    ("1016030429", "苏苏", "女", "19990101", "计科1班", "18288888888", "230349199901010234", "涂山市"),
]

for student in students:
    cu.execute("insert into students values(?, ?, ?, ?, ?, ?, ?, ?)", student)

conn.commit()
