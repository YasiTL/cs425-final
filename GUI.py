import tkinter as tk
from functools import partial

# Just set the current employee id + data at the start, so all of the pages can access the data.
g_currentEmployeeId = 1
g_currentEmployeeData = ()

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
        tk.Button(self.frame, text='Company Spending Report', command=self.goToReport3Page).grid()
        self.report3Page = Report_3(master=self.master, app=self.app)

        tk.Button(self.frame, text='Manage Users',
                  command=self.manageUsersPage).grid()
        self.manageUsersPage = ManageUsers(master=self.master, app=self.app)

        tk.Button(self.frame, text='Sign Out',
                    command=self.goToSignInPage).grid()

    def start(self):
        self.frame.grid(row=1, column=1)

    def manageUsersPage(self):
        self.frame.grid_forget()
        self.manageUsersPage.start()

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


class ManageUsers(tk.Frame):
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.frame = tk.Frame(self.master)

        # Components
        tk.Label(self.frame, text="Manage Users Page").grid(row=0, column=1, sticky = "n")

        tk.Button(self.frame, text='Add User', command=self.goToAddUserPage).grid(row=1, column=1)

        tk.Label(self.frame, text='Search by employee id: ').grid(row=2, column=1, sticky="w", padx = (0, 260))

        self.employeeIdSearchBox = tk.Entry(self.frame)
        self.employeeIdSearchBox.grid(row=2, column=1)

        tk.Button(self.frame, text='Search', command=self.searchFunction).grid(row=2, column=1, padx = (200, 0))

        tk.Button(self.frame, text='Go Back', command=self.go_back).grid(row=3, column=1)

    def start(self):
        self.frame.grid(row=1, column=1)

    def go_back(self):
        self.frame.grid_forget()
        Menu(master=self.master, app=self.app).start()
    
    def goToUserPage(self):
        self.frame.grid_forget()
        UserPage(master=self.master, app=self.app).start()
    
    def goToAddUserPage(self):
        self.frame.grid_forget()
        AddUserPage(master=self.master, app=self.app).start()

    def searchFunction(self):
        if (self.employeeIdSearchBox.get()):
            # TODO: Do searching here
            print("Search Function must run on: ", self.employeeIdSearchBox.get())
            self.goToUserPage()
        else:
            tk.Label(self.frame, text='Cannot find employee').grid(row=3, column=1, sticky = 's', pady = (50, 0))

class UserPage(tk.Frame):
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.frame = tk.Frame(self.master)

        # Menu Options
        tk.Label(self.frame, text="Edit Current User").grid(row=0, column=0, sticky = "n")

        tk.Button(self.frame, text='Edit User', command=self.goToEditUserPage).grid()
        self.report2Page = EditUserPage(master=self.master, app=self.app)

        tk.Button(self.frame, text='Employee W2', command=self.goToReport1Page).grid()
        self.report1Page = Report_1(master=self.master, app=self.app)

        tk.Button(self.frame, text='Bi-Weekly Paycheck', command=self.goToReport2Page).grid()
        self.report2Page = Report_2(master=self.master, app=self.app)

        tk.Button(self.frame, text='Delete User', command=self.deleteUser).grid()

        tk.Button(self.frame, text='Back to Employee Search', command=self.go_back).grid()
    
    def start(self):
        self.frame.grid(row=1, column=1)
    
    def go_back(self):
        self.frame.grid_forget()
        UserPage(master=self.master, app=self.app).start()
    
    def manageUsersPage(self):
        self.frame.grid_forget()
        self.manageUsersPage.start()

    def goToReport1Page(self):
        self.frame.grid_forget()
        self.report1Page.start()

    def goToReport2Page(self):
        self.frame.grid_forget()
        self.report2Page.start()
    
    def goToEditUserPage(self):
        self.frame.grid_forget()
        EditUserPage(master=self.master, app=self.app).start()
    
    def deleteUser(self):
        # TODO: Delete User
        print("DELETE USER")
        self.go_back

class AddUserPage(tk.Frame):
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.frame = tk.Frame(self.master)

        tk.Label(self.frame, text='Add User Page').grid(row=0, column=1)

        # TODO: Place correct fields.
        tk.Label(self.frame, text='First Name').grid(row=0, column=0)
        self.firstNameField = tk.Entry(self.frame)
        self.firstNameField.grid(row=0, column=1)

        tk.Label(self.frame, text='Last Name').grid(row=1, column=0)
        self.lastNameField = tk.Entry(self.frame)
        self.lastNameField.grid(row=1, column=1)

        tk.Label(self.frame, text='Address').grid(row=2, column=0)
        self.addressField = tk.Entry(self.frame)
        self.addressField.grid(row=2, column=1)

        tk.Label(self.frame, text='Suffering').grid(row=3, column=0)
        self.sufferingField = tk.Entry(self.frame)
        self.sufferingField.grid(row=3, column=1)

        tk.Label(self.frame, text='Test').grid(row=4, column=0)
        self.testField = tk.Entry(self.frame)
        self.testField.grid(row=4, column=1)

        tk.Button(self.frame, text='Go Back', command=self.go_back).grid(sticky="s")

    def start(self):
        self.frame.grid(row=1, column=1)

    def go_back(self):
        self.frame.grid_forget()
        ManageUsers(master=self.master, app=self.app).start()

class EditUserPage(tk.Frame):
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.frame = tk.Frame(self.master)

        tk.Label(self.frame, text='Edit User Page').grid(row=0, column=1)
        # TODO : ADD FIELDS, AND FILL THEM WITH CONTENT FROM THE DATABASE. ON SUBMIT, PUSH ALL THE DATA.
        tk.Button(self.frame, text='Go back to Employee Page', command=self.go_back).grid(row=1, column=1)
    
    def start(self):
        self.frame.grid(row=1, column=1)

    def go_back(self):
        self.frame.grid_forget()
        UserPage(master=self.master, app=self.app).start()

# Employee Bi weekly paycheck
class Report_1(tk.Frame):
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.frame = tk.Frame(self.master)

        # Components
        tk.Label(self.frame, text="Report 1").grid()
        tk.Button(self.frame, text='Go back to Employee Dash', command=self.go_back).grid()

    def start(self):
        self.frame.grid(row=1, column=1)

    def go_back(self):
        self.frame.grid_forget()
        UserPage(master=self.master, app=self.app).start()

# Employee W2
class Report_2(tk.Frame):
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.frame = tk.Frame(self.master)

        # Components
        tk.Label(self.frame, text="Report 2").grid()
        tk.Button(self.frame, text='Go to Employee Dash', command=self.go_back).grid()

    def start(self):
        self.frame.grid(row=1, column=1)

    def go_back(self):
        self.frame.grid_forget()
        UserPage(master=self.master, app=self.app).start()


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
