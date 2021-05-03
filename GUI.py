import tkinter as tk

class RootApp:
    def __init__(self, root=None):
        self.root = root
        self.frame = tk.Frame(self.root, width=600, height=600)
        self.frame.grid(row=1, column=1)

        # MIN AND MAX SIZE OF WINDOW
        self.root.minsize(600, 600)
        self.root.maxsize(600, 600)

        self.frame.grid_forget()
        SignIn(master=root, app=self).start()

class SignIn(tk.Frame):
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.frame = tk.Frame(self.master)

        # Components
        tk.Label(self.frame, text='Sign In').grid(row=1, column=1)

        tk.Label(self.frame, text='Username').grid()
        tk.Entry(self.frame).grid(row=2, column=1)

        tk.Label(self.frame, text='Password').grid()
        tk.Entry(self.frame, show='*').grid(row=3, column=1)
        tk.Button(self.frame, text='Login', command=self.make_Menu).grid(row=4, column=1)

        self.menuPage = Menu(master=self.master, app=self.app)

    def start(self):
        self.frame.grid(row=1, column=1)

    def make_Menu(self):
        self.frame.grid_forget()
        self.menuPage.start()


class Menu(tk.Frame):
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.frame = tk.Frame(self.master)

        
        tk.Label(self.frame, text='Menu').grid()

        # Menu Options
        tk.Button(self.frame, text='Report 1', command=self.goToReport1Page).grid()
        self.report1Page = Report_1(master=self.master, app=self.app)

        tk.Button(self.frame, text='Report 2', command=self.goToReport2Page).grid()
        self.report2Page = Report_2(master=self.master, app=self.app)

        tk.Button(self.frame, text='Report 3', command=self.goToReport3Page).grid()
        self.report3Page = Report_3(master=self.master, app=self.app)

        tk.Button(self.frame, text='Edit User',
                  command=self.goToEditUserPage).grid()
        self.editUserPage = EditUser(master=self.master, app=self.app)

        tk.Button(self.frame, text='Sign Out',
                    command=self.goToSignInPage).grid()

    def start(self):
        self.frame.grid(row=1, column=1)

    def goToEditUserPage(self):
        self.frame.grid_forget()
        self.editUserPage.start()

    def goToReport1Page(self):
        self.frame.grid_forget()
        self.report1Page.start()

    def goToReport2Page(self):
        self.frame.grid_forget()
        self.report2Page.start()

    def goToReport3Page(self):
        self.frame.grid_forget()
        self.report3Page.start()
    
    def goToSignInPage(self):
        self.frame.grid_forget()
        SignIn(master=self.master, app=self.app).start()


class EditUser(tk.Frame):
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.frame = tk.Frame(self.master)

        # Components
        tk.Label(self.frame, text="Edit User Page").grid()
        tk.Button(self.frame, text='Go Back', command=self.go_back).grid()

    def start(self):
        self.frame.grid(row=1, column=1)

    def go_back(self):
        self.frame.grid_forget()
        Menu(master=self.master, app=self.app).start()


class Report_1(tk.Frame):
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.frame = tk.Frame(self.master)

        # Components
        tk.Label(self.frame, text="Report 1").grid()
        tk.Button(self.frame, text='Go Back', command=self.go_back).grid()

    def start(self):
        self.frame.grid(row=1, column=1)

    def go_back(self):
        self.frame.grid_forget()
        Menu(master=self.master, app=self.app).start()


class Report_2(tk.Frame):
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.frame = tk.Frame(self.master)

        # Components
        tk.Label(self.frame, text="Report 2").grid()
        tk.Button(self.frame, text='Go Back', command=self.go_back).grid()

    def start(self):
        self.frame.grid(row=1, column=1)

    def go_back(self):
        self.frame.grid_forget()
        Menu(master=self.master, app=self.app).start()


class Report_3(tk.Frame):
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.frame = tk.Frame(self.master)

        # Components
        tk.Label(self.frame, text="Report 3").grid()
        tk.Button(self.frame, text='Go Back', command=self.go_back).grid()

    def start(self):
        self.frame.grid(row=1, column=1)

    def go_back(self):
        self.frame.grid_forget()
        Menu(master=self.master, app=self.app).start()


root = tk.Tk()

# Create a 3 by 3 grid.
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)

app = RootApp(root=root)
root.mainloop()
