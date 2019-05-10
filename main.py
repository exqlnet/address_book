try:
    from Tkinter import *
    from ttk import *
except ImportError:  # Python 3
    from tkinter import *
    from tkinter.ttk import *


class App(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.CreateUI()
        self.LoadTable()
        self.grid(sticky = (N,S,W,E))
        parent.grid_rowconfigure(0, weight = 1)
        parent.grid_columnconfigure(0, weight = 1)

    def CreateUI(self):
        tv = Treeview(self)
        tv['columns'] = ('Sources', 'starttime', 'endtime', 'status')
        tv.heading("Sources", text='Sources', anchor='w')
        # tv.column("Sources", anchor="w")
        tv.heading('starttime', text='Start Time')
        tv.column('starttime', anchor='center', width=100)
        # tv.heading('endtime', text='End Time')
        # tv.column('endtime', anchor='center', width=100)
        # tv.heading('status', text='Status')
        # tv.column('status', anchor='center', width=100)
        tv.pack()
        self.treeview = tv
        # self.grid_rowconfigure(0, weight = 1)
        # self.grid_columnconfigure(0, weight = 1)

    def LoadTable(self):
        self.treeview.insert('', 'end', text="First", values=('10:00',
                             '10:10', 'Ok'))

class DataTable(Frame):

    def __init__(self, parent):
        super.__init__(parent)

    def create_ui(self):


def main():
    root = Tk()
    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
