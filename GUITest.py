import tkinter as tk

class RootApp:
    def __init__(self, root=None):
        self.root = root
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.root.minsize(600,600)
        self.root.maxsize(600,600)

        tk.Label(self.frame, text='Sign In').pack()
        # tk.Entry(root, text = 'Username').pack()
        # tk.Entry(root, text = 'Password').pack()
        tk.Button(self.frame, text='Login', command=self.make_Menu).pack()

        self.menuPage = Menu(master=self.root, app=self)

    def main_page(self):
        self.frame.pack()

    def make_Menu(self):
        self.frame.pack_forget()
        self.menuPage.start()

class Menu(tk.Frame):
    def __init__(self, master=None, app=None):
        # Set master, app, and frame
        self.master = master
        self.app = app
        self.frame = tk.Frame(self.master)

        tk.Label(self.frame, text='Page 1').pack()
        tk.Button(self.frame, text='Edit User', command=self.make_EditUser).pack()

        # Menu Components
        self.editUser = EditUser(master=self.master, app=self.app)
        # self.reports = Reports(master=self.root, app=self)

    def start(self):
        self.frame.pack()

    def make_EditUser(self):
        self.frame.pack_forget()
        self.editUser.start()


class EditUser(tk.Frame):
    def __init__(self, master=None, app=None):
        # Set master, app, and frame
        self.master = master
        self.app = app
        self.frame = tk.Frame(self.master)

        tk.Label(self.frame, text="Edit User Page").pack(side="top", fill="x", pady=10)

    def start(self):
        self.frame.pack()



root = tk.Tk()
app = RootApp(root=root)
root.mainloop()