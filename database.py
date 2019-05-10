import os
import sqlite3

columns = ["xh", "xm", "xb", "csrq", "bjmc", "dh", "sfzh", "jtzz"]

def to_students(sql, *args):
    """从数据库拿到用户信息"""
    conn = sqlite3.connect("data.db")
    cu = conn.cursor()
    cu.execute(sql, args)
    rows = cu.fetchall()
    fileds = cu.description

    students = []
    for row in rows:
        dic = {filed[0]: row[i] for i, filed in enumerate(fileds)}
        students.append(Student(**dic))
    return students


class Student:

    def __init__(self, xh, xm, xb, csrq, bjmc, dh, sfzh, jtzz):
        self.xh, self.xm, self.xb, self.csrq, self.bjmc, self.dh, self.sfzh, self.jtzz = xh, xm, xb, csrq, bjmc, dh, sfzh, jtzz

    def to_tuple(self):
        return self.xh, self.xm, self.xb, self.csrq, self.bjmc, self.dh, self.sfzh, self.jtzz

    def add(self):
        conn = sqlite3.connect("data.db")
        cu = conn.cursor()

        cu.execute("insert into students values(?, ?, ?, ?, ?, ?, ?, ?)", self.to_tuple())

    @staticmethod
    def get_all():
        return to_students("select  xh, xm, xb, csrq, bjmc, dh, sfzh, jtzz from students")

    @staticmethod
    def find_student_by_xh(xh):
        """通过学号获取学生"""
        return to_students("select  xh, xm, xb, csrq, bjmc, dh, sfzh, jtzz from students where xh like '%{}%'".format(xh))

    @staticmethod
    def find_student_by_xm(xm):
        """姓名获取用户"""
        return to_students("select  xh, xm, xb, csrq, bjmc, dh, sfzh, jtzz from students where xm like '%{}%'".format(xm))

    def delete(self):
        conn = sqlite3.connect("data.db")
        cu = conn.cursor()

        cu.execute("delete from students where xh=?", (self.xh, ))
        conn.commit()

    @staticmethod
    def batch_delete(*xhs):
        students = to_students("select  xh, xm, xb, csrq, bjmc, dh, sfzh, jtzz from students where xh in (?)", *xhs)
        for student in students:
            student.delete()

    def is_exists(self):
        conn = sqlite3.connect("data.db")
        cu = conn.cursor()
        cu.execute("select xh from students where xh=?", (self.xh,))
        rows = cu.fetchall()
        return bool(rows)

    def save(self):
        conn = sqlite3.connect("data.db")
        cu = conn.cursor()

        if self.is_exists():
            cu.execute("update students set xm=?, xb=?, csrq=?, bjmc=?, dh=?, sfzh=?, jtzz=? where xh='{}'".format(self.xh), self.to_tuple()[1:])
            conn.commit()
        else:
            cu.execute("insert into students values(?, ?, ?, ?, ?, ?, ?, ?)", self.to_tuple())
        conn.commit()

    def modify_self(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.save()

    @staticmethod
    def modify(xh, **kwargs):
        student = Student.find_student_by_xh(xh)[0]
        for k, v in kwargs.items():
            setattr(student, k, v)
        student.save()

    @staticmethod
    def query(keyword):
        sql = """
        select  xh, xm, xb, csrq, bjmc, dh, sfzh, jtzz from students where
        xh like '%{keyword}%' OR 
        xm like '%{keyword}%' OR 
        dh like '%{keyword}%' OR 
        sfzh like '%{keyword}%' OR 
        jtzz like '%{keyword}%' 
        """
        return to_students(sql.format(keyword=keyword))
