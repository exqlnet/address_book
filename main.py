from tkinter import *
from tkinter import ttk
from TreeDataView import TreeDataView
from database import Student
import json

"""
本模块定义了程序的界面
定义了多个函数用于按钮点击事件
定义了一些可复用的函数
"""


class LoginWindow(Tk):
    """登录窗口"""

    def __init__(self):
        Tk.__init__(self)
        self.title("登录")
        self.geometry("200x100")
        label_admin = Label(self, text="管理员登录")
        label_username = Label(self, text="用户名")
        label_password = Label(self, text="密码")
        self.label_feedback = Label(self, text="")
        label_admin.grid(row=0, column=0)
        label_username.grid(row=1, column=0)
        label_password.grid(row=2, column=0)
        self.label_feedback.grid(row=4, column=0)
        self.entry_username = Entry(self, width="20")
        self.entry_password = Entry(self, width="20")
        bt_login = Button(self, text="登录", command=self.to_main)
        self.entry_username.grid(row=1, column=1)
        self.entry_password.grid(row=2, column=1)
        bt_login.grid(row=3, column=0)

    def check(self, username, password):
        """用于检查管理员用户名密码是否正确"""
        with open("admins.json", "r") as file:
            admins = json.load(file)
            for admin in admins:
                if admin["username"] == username and admin["password"] == password:
                    return True
        return False

    def to_main(self):
        print("to main called")
        if self.check(self.entry_username.get(), self.entry_password.get()):
            print("create new")
            self.withdraw()
            MainWindow(self)
            # main_window.grab_set()
            print("ok")
        else:
            msg = Message(self, text="用户名或密码错误")
            msg.grid(row=3, column=1)
            # self.label_feedback.config(text="用户名或密码错误")


class NewWindow(Toplevel):
    """弹出窗口类"""
    def __init__(self, parent, student_info=None):

        super().__init__(parent)
        self.parent = parent
        self.geometry("300x250")
        self.student_info = student_info
        self.create_window()
        self.parent.withdraw()
        self.mainloop()

    def render_content(self, student_info=None):
        # 创建输入框
        label = ttk.Label(self, text="输入用户信息")
        self.entry_xh = Entry(self, width=200)
        self.entry_xm = Entry(self, width=200)
        self.entry_xb = Entry(self, width=200)
        self.entry_csrq = Entry(self, width=200)
        self.entry_bjmc = Entry(self, width=200)
        self.entry_dh = Entry(self, width=200)
        self.entry_sfzh = Entry(self, width=200)
        self.entry_jtzz = Entry(self, width=200)
        bt_submit = ttk.Button(self, text="保存", command=self.save_info)
        label_xh = ttk.Label(self, text="学号：")
        label_xm = ttk.Label(self, text="姓名：")
        label_xb = ttk.Label(self, text="性别：")
        label_csrq = ttk.Label(self, text="出生日期：")
        label_bjmc = ttk.Label(self, text="班级：")
        label_dh = ttk.Label(self, text="电话：")
        label_sfzh = ttk.Label(self, text="身份证号：")
        label_jtzz = ttk.Label(self, text="家庭住址：")

        if student_info:
            self.entry_xh.insert(0, student_info.xh)
            self.entry_xm.insert(0, student_info.xm)
            self.entry_xb.insert(0, student_info.xb)
            self.entry_csrq.insert(0, student_info.csrq)
            self.entry_bjmc.insert(0, student_info.bjmc)
            self.entry_dh.insert(0, student_info.dh)
            self.entry_sfzh.insert(0, student_info.sfzh)
            self.entry_jtzz.insert(0, student_info.jtzz)

        label.grid(row=0)
        label_xh.grid(row=1, column=0)
        label_xm.grid(row=2, column=0)
        label_xb.grid(row=3, column=0)
        label_csrq.grid(row=4, column=0)
        label_bjmc.grid(row=5, column=0)
        label_dh.grid(row=6, column=0)
        label_sfzh.grid(row=7, column=0)
        label_jtzz.grid(row=8, column=0)
        self.entry_xh.grid(row=1, column=1)
        self.entry_xm.grid(row=2, column=1)
        self.entry_xb.grid(row=3, column=1)
        self.entry_csrq.grid(row=4, column=1)
        self.entry_bjmc.grid(row=5, column=1)
        self.entry_dh.grid(row=6, column=1)
        self.entry_sfzh.grid(row=7, column=1)
        self.entry_jtzz.grid(row=8, column=1)

        bt_submit.grid(row=9)

    def create_window(self):
        self.bind("<Destroy>", self._destroy)
        if self.student_info:
            self.wm_title("修改学生信息")
        else:
            self.wm_title("添加学生")
        self.render_content(student_info=self.student_info)

    def _destroy(self, event):
        self.parent.deiconify()
        self.parent.refresh()
        self.destroy()

    def save_info(self):
        xh = self.entry_xh.get()
        xm = self.entry_xm.get()
        xb = self.entry_xb.get()
        csrq = self.entry_csrq.get()
        bjmc = self.entry_bjmc.get()
        dh = self.entry_dh.get()
        sfzh = self.entry_sfzh.get()
        jtzz = self.entry_jtzz.get()
        Student(xh, xm, xb, csrq, bjmc, dh, sfzh, jtzz).save()
        self.destroy()


class MainWindow(Toplevel):

    def refresh(self):
        students = Student.get_all()
        self.tdv1.clear()
        for student in students:
            self.tdv1.insert('', 'end', values=student.to_tuple())

    def tdv_id_to_xh(self, tdv_id):
        return str(self.tdv1.item(tdv_id)["values"][0])

    def delete_command(self):
        tdv_ids = self.tdv1.selection()
        xhs = [self.tdv_id_to_xh(_id) for _id in tdv_ids]
        Student.batch_delete(*xhs)
        self.tdv1.delete(*tdv_ids)

    def modify_command(self):
        tdv_ids = self.tdv1.selection()
        if len(tdv_ids) != 1:
            return

        student_info = Student.find_student_by_xh(self.tdv_id_to_xh(tdv_ids[0]))[0]
        modify_window = NewWindow(self, student_info=student_info)

    def search_callback(self):
        keyword = self.input_search.get()
        students = Student.query(keyword)
        self.tdv1.clear()
        for student in students:
            self.tdv1.insert('', 'end', values=student.to_tuple())

    def _destroy(self, event):
        exit(0)

    def __init__(self, parent):
        """设置窗口"""
        print("init...")
        super().__init__(parent)
        print("parent init done...")
        self.parent = parent
        self.geometry("560x320")
        self.bind("<Destroy>", self._destroy)
        button_frame = ttk.Frame(self)
        btn_new = ttk.Button(button_frame, text="添加", command=lambda: NewWindow(self))
        btn_refresh = ttk.Button(button_frame, text="刷新", command=self.refresh)

        print("create search...")
        # 搜索部分
        self.label_search = ttk.Label(button_frame, text="查找(输入关键字)：")
        self.input_search = ttk.Entry(button_frame)
        self.btn_search = ttk.Button(button_frame, text="搜索", command=self.search_callback)

        print("render widget")
        btn_new.grid(row=1, column=0)
        btn_refresh.grid(row=1, column=1)
        self.label_search.grid(row=2, column=0)
        self.input_search.grid(row=2, column=1)
        self.btn_search.grid(row=2, column=2)
        button_frame.pack()

        """创建表格"""
        print("creating table")
        # 初始化表格
        tree_columns = ['学号', '姓名', '性别', '出生日期', '班级', '电话', '身份证号', '家庭住址']
        self.tdv1 = TreeDataView(self, tree_columns, scrollbar_x=True, scrollbar_y=True, right_click=self.pop_menu)
        self.refresh()

        # 创建右键菜单
        self.create_menu()

        # 绑定右键事件
        print("binding callback")
        btn_new.bind("<Button-3>", self.pop_menu)
        self.tdv1.pack(fill='both', expand=1)

        self.mainloop()

    def create_menu(self):
        """创建菜单"""
        self.menu = Menu(self, tearoff=0)
        self.menu.add_command(label="删除", command=self.delete_command)
        self.menu.add_command(label="修改", command=self.modify_command)

    def pop_menu(self, event):
        # print(selected_values)
        self.menu.post(event.x_root, event.y_root)


def start():
    login_window = LoginWindow()
    login_window.mainloop()


start()
