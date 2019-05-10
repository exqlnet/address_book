from tkinter import *
from tkinter import ttk
from TreeDataView import TreeDataView
from DbTool import UserTool

user_tool = UserTool()

"""设置窗口"""
root = Tk()
root.wm_title('通信录')


def refresh(query_type=None, keyword=""):
    users = []
    if query_type == "user_id":
        user = user_tool.get_by_id(user_id=keyword)
        if user:
            users.append(user)
    elif query_type == "name":
        users.extend(user_tool.get_by_name(name=keyword))
    else:
        users = user_tool.get_all()

    tdv1.clear()
    for user in users:
        tdv1.insert('', 'end', values=user.to_tuple())


def tdv_id_to_user_id(tdv_id):
    return tdv1.item(tdv_id)["values"][0]


def delete_command():
    tdv_ids = tdv1.selection()
    user_ids = [tdv_id_to_user_id(_id) for _id in tdv_ids]
    user_tool.batch_delete(*user_ids)
    tdv1.delete(*tdv_ids)


def modify_command():
    tdv_ids = tdv1.selection()
    if len(tdv_ids) != 1:
        return

    user_info = user_tool.get_by_id(tdv_id_to_user_id(tdv_ids[0]))
    modify_window = NewWindow(root, user_info=user_info)


"""创建菜单"""
menu = Menu(root, tearoff=0)
menu.add_command(label="删除", command=delete_command)
menu.add_command(label="修改", command=modify_command)


def pop_menu(event):
    # print(selected_values)
    menu.post(event.x_root, event.y_root)


class NewWindow(Toplevel):

    def __init__(self, parent, user_info=None):
        Toplevel.__init__(self, parent)
        self.user_info = user_info
        self.create_window()

    def render_content(self, user_info=None):
        # 创建输入框
        label = ttk.Label(self, text="输入用户信息")
        self.entry_name = Entry(self)
        self.entry_phone = Entry(self)
        self.entry_remark = Entry(self)
        bt_submit = ttk.Button(self, text="保存", command=self.save_info)
        label_name = ttk.Label(self, text="姓名：")
        label_phone = ttk.Label(self, text="电话：")
        label_remark = ttk.Label(self, text="备注：")

        if user_info:
            self.entry_name.insert(0, user_info.name)
            self.entry_phone.insert(0, user_info.phone)
            self.entry_remark.insert(0, user_info.remark)

        label.grid(row=0)
        label_name.grid(row=1, column=0)
        label_phone.grid(row=2, column=0)
        label_remark.grid(row=3, column=0)
        self.entry_name.grid(row=1, column=1)
        self.entry_phone.grid(row=2, column=1)
        self.entry_remark.grid(row=3, column=1)
        bt_submit.grid(row=4)

    def create_window(self):
        root.withdraw()
        self.bind("<Destroy>", self._destory)
        self.wm_title("添加新用户")
        self.render_content(user_info=self.user_info)
        self.mainloop()

    def _destory(self, event):
        self.destroy()
        root.deiconify()

    def save_info(self):
        name = self.entry_name.get()
        phone = self.entry_phone.get()
        remark = self.entry_remark.get()
        if self.user_info:
            user_tool.modify(self.user_info.user_id, name=name, phone=phone, remark=remark)
        else:
            user_tool.add(name=name, phone=phone, remark=remark)
        self.destroy()
        root.deiconify()
        refresh()


button_frame = ttk.Frame(root)


def command_search_name():
    name = entry_search_name.get()
    refresh("name", name)


def command_search_id():
    user_id = entry_search_id.get()
    refresh("user_id", user_id)


btn_new = ttk.Button(button_frame, text="添加", command=lambda: NewWindow(root))

btn_refresh = ttk.Button(button_frame, text="刷新", command=refresh)

# 搜索部分
label_search_name = ttk.Label(button_frame, text="按姓名找：")
label_search_id = ttk.Label(button_frame, text="按编号找：")
entry_search_name = ttk.Entry(button_frame)
entry_search_id = ttk.Entry(button_frame)
btn_search_name = ttk.Button(button_frame, text="搜索", command=command_search_name)
btn_search_id = ttk.Button(button_frame, text="搜索", command=command_search_id)

btn_refresh.grid(row=0, column=1)
btn_new.grid(row=0, column=0)
label_search_id.grid(row=1, column=0)
label_search_name.grid(row=2, column=0)
entry_search_id.grid(row=1, column=1)
entry_search_name.grid(row=2, column=1)
btn_search_id.grid(row=1, column=2)
btn_search_name.grid(row=2, column=2)
button_frame.pack()

"""创建表格"""
# 初始化表格
tree_columns = ['通信录编号', '姓名', '电话', '备注']
tdv1 = TreeDataView(root, tree_columns, scrollbar_x=True, scrollbar_y=True, right_click=pop_menu)
refresh()

# 绑定右键事件
btn_new.bind("<Button-3>", pop_menu)


tdv1.pack(fill='both', expand=1)


root.mainloop()
