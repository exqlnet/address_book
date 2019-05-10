from tkinter import *
from tkinter import ttk
from TreeDataView import TreeDataView
from database import Student


"""设置窗口"""
root = Tk()
root.wm_title('学生信息管理系统')
root.geometry("1000x500+50+50")


def refresh(query_type=None, keyword=""):
    students = []
    if query_type == "xh":
        student = Student.find_student_by_xh(keyword)
        if student:
            students.append(student)
    elif query_type == "xm":
        students.extend(Student.find_student_by_xm(keyword))
    else:
        students = Student.get_all()

    tdv1.clear()
    for student in students:
        tdv1.insert('', 'end', values=student.to_tuple())


def tdv_id_to_xh(tdv_id):
    return str(tdv1.item(tdv_id)["values"][0])


def delete_command():
    tdv_ids = tdv1.selection()
    xhs = [tdv_id_to_xh(_id) for _id in tdv_ids]
    Student.batch_delete(*xhs)
    tdv1.delete(*tdv_ids)


def modify_command():
    tdv_ids = tdv1.selection()
    if len(tdv_ids) != 1:
        return

    student_info = Student.find_student_by_xh(tdv_id_to_xh(tdv_ids[0]))[0]
    modify_window = NewWindow(root, student_info=student_info)


"""创建菜单"""
menu = Menu(root, tearoff=0)
menu.add_command(label="删除", command=delete_command)
menu.add_command(label="修改", command=modify_command)


def pop_menu(event):
    # print(selected_values)
    menu.post(event.x_root, event.y_root)


class NewWindow(Toplevel):

    def __init__(self, parent, student_info=None):
        Toplevel.__init__(self, parent)
        self.geometry("300x250+50+50")
        self.student_info = student_info
        self.create_window()

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
        root.withdraw()
        self.bind("<Destroy>", self._destory)
        if self.student_info:
            self.wm_title("修改学生信息")
        else:
            self.wm_title("添加学生")
        self.render_content(student_info=self.student_info)
        self.mainloop()

    def _destory(self, event):
        self.destroy()
        root.deiconify()

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
        root.deiconify()
        refresh()


button_frame = ttk.Frame(root)


def search_callback():
    keyword = input_search.get()
    students = Student.query(keyword)
    tdv1.clear()
    for student in students:
        tdv1.insert('', 'end', values=student.to_tuple())


btn_new = ttk.Button(button_frame, text="添加", command=lambda: NewWindow(root))
btn_refresh = ttk.Button(button_frame, text="刷新", command=refresh)

# 搜索部分
label_search = ttk.Label(button_frame, text="查找(输入关键字)：")
input_search = ttk.Entry(button_frame)
btn_search = ttk.Button(button_frame, text="搜索", command=search_callback)

btn_new.grid(row=1, column=0)
btn_refresh.grid(row=1, column=1)
label_search.grid(row=2, column=0)
input_search.grid(row=2, column=1)
btn_search.grid(row=2, column=2)
button_frame.pack()

"""创建表格"""
# 初始化表格
tree_columns = ['学号', '姓名', '性别', '出生日期', '班级', '电话', '身份证号', '家庭住址']
tdv1 = TreeDataView(root, tree_columns, scrollbar_x=True, scrollbar_y=True, right_click=pop_menu)
refresh()

# 绑定右键事件
btn_new.bind("<Button-3>", pop_menu)


tdv1.pack(fill='both', expand=1)


root.mainloop()
