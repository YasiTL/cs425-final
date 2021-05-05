import tkinter as tk
from functools import partial
from postGres import DataType
from Employee import Employee
import postGres as DB
import Auth

currentEmployee = Employee
enterCallback = None


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
        global enterCallback

        self.master = master
        self.app = app
        self.frame = tk.Frame(self.master)

        # Components
        tk.Label(self.frame, text="Sign In").grid(row=1, column=1)

        tk.Label(self.frame, text="Username").grid()
        user = tk.Entry(self.frame)
        user.grid(row=2, column=1)

        tk.Label(self.frame, text="Password").grid()
        passw = tk.Entry(self.frame, show="*")
        passw.grid(row=3, column=1)

        def signIn():
            global enterCallback
            Auth.signIn(user.get(), passw.get())
            if Auth.getTitle():
                enterCallback = None
                self.make_Menu()

        enterCallback = signIn

        tk.Button(self.frame, text="Login", command=signIn).grid(row=4, column=1)

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

        tk.Label(self.frame, text="Menu").grid()

        # Menu Options
        tk.Button(self.frame, text="Company Spending Report", command=self.goToReport3Page).grid()
        self.report3Page = Report_3(master=self.master, app=self.app)

        tk.Button(self.frame, text="Manage Users", command=self.manageUsersPage).grid()
        self.manageUsersPage = ManageUsers(master=self.master, app=self.app)

        def signOut():
            Auth.signOut()
            self.goToSignInPage()

        tk.Button(self.frame, text="Sign Out", command=signOut).grid()

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
        tk.Label(self.frame, text="Manage Users Page").grid(row=0, column=1, sticky="n")

        tk.Button(self.frame, text="Add User", command=self.goToAddUserPage).grid(row=1, column=1)

        tk.Label(self.frame, text="Search by employee id: ").grid(row=2, column=1, sticky="w", padx=(0, 260))

        self.employeeIdSearchBox = tk.Entry(self.frame)
        self.employeeIdSearchBox.grid(row=2, column=1)

        tk.Button(self.frame, text="Search", command=self.searchFunction).grid(row=2, column=1, padx=(200, 0))

        tk.Button(self.frame, text="Go Back", command=self.go_back).grid(row=3, column=1)

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
        if self.employeeIdSearchBox.get():
            currentEmployee = Employee(self.employeeIdSearchBox.get())
            if currentEmployee.exists:
                self.goToUserPage()
        else:
            tk.Label(self.frame, text="Cannot find employee").grid(row=3, column=1, sticky="s", pady=(50, 0))


class UserPage(tk.Frame):
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.frame = tk.Frame(self.master)

        # Menu Options
        tk.Label(self.frame, text="Edit Current User").grid(row=0, column=0, sticky="n")

        tk.Button(self.frame, text="Edit User", command=self.goToEditUserPage).grid()
        self.report2Page = EditUserPage(master=self.master, app=self.app)

        tk.Button(self.frame, text="Employee W2", command=self.goToReport1Page).grid()
        self.report1Page = Report_1(master=self.master, app=self.app)

        tk.Button(self.frame, text="Bi-Weekly Paycheck", command=self.goToReport2Page).grid()
        self.report2Page = Report_2(master=self.master, app=self.app)

        tk.Button(self.frame, text="Delete User", command=self.deleteUser).grid()

        tk.Button(self.frame, text="Back to Employee Search", command=self.go_back).grid()

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

        tk.Label(self.frame, text="Add User Page").grid(row=0, column=1)

        titles = list()
        payTypes = list()
        insurances = list()
        states = list()

        for t in list(DataType.JobTitle):
            titles.append(t.value)

        for s in list(DataType.Salary):
            payTypes.append(s.value)

        DB.execute(DB.Query.SELECT(DB.Entity.INSURNACE_PLAN, "*"))
        for i in DB.result():
            insurances.append(i[0])

        DB.execute(DB.Query.SELECT(DB.Entity.STATE, "*"))
        for s in DB.result():
            states.append(s[0])

        title = tk.StringVar(self.frame)
        title.set(titles[0])

        payType = tk.StringVar(self.frame)
        payType.set(payTypes[0])

        insurance = tk.StringVar(self.frame)
        insurance.set(insurances[0])

        state = tk.StringVar(self.frame)
        state.set(states[0])

        tk.Label(self.frame, text="eID").grid(row=0, column=0)
        self.e_id = tk.Entry(self.frame)
        self.e_id.grid(row=0, column=1)

        tk.Label(self.frame, text="First name").grid(row=1, column=0)
        self.first_name = tk.Entry(self.frame)
        self.first_name.grid(row=1, column=1)

        tk.Label(self.frame, text="Last name").grid(row=2, column=0)
        self.last_name = tk.Entry(self.frame)
        self.last_name.grid(row=2, column=1)

        tk.Label(self.frame, text="ssn").grid(row=3, column=0)
        self.ssn = tk.Entry(self.frame)
        self.ssn.grid(row=3, column=1)

        tk.Label(self.frame, text="Job title").grid(row=4, column=0)
        tk.OptionMenu(self.frame, title, *titles).grid(row=4, column=1)

        tk.Label(self.frame, text="Salary type").grid(row=5, column=0)
        tk.OptionMenu(self.frame, payType, *payTypes).grid(row=5, column=1)

        tk.Label(self.frame, text="Insurance plan").grid(row=6, column=0)
        tk.OptionMenu(self.frame, insurance, *insurances).grid(row=6, column=1)

        tk.Label(self.frame, text="Email").grid(row=7, column=0)
        self.email = tk.Entry(self.frame)
        self.email.grid(row=7, column=1)

        tk.Label(self.frame, text="Country").grid(row=8, column=0)
        self.country = tk.Entry(self.frame)
        self.country.grid(row=8, column=1)

        tk.Label(self.frame, text="State").grid(row=9, column=0)
        tk.OptionMenu(self.frame, state, *states).grid(row=9, column=1)

        tk.Label(self.frame, text="Street Name").grid(row=10, column=0)
        self.street_name = tk.Entry(self.frame)
        self.street_name.grid(row=10, column=1)

        tk.Label(self.frame, text="Postal Code").grid(row=11, column=0)
        self.postal_code = tk.Entry(self.frame)
        self.postal_code.grid(row=11, column=1)

        tk.Label(self.frame, text="401k Deduction").grid(row=12, column=0)
        self.F01k_deduction = tk.Entry(self.frame)
        self.F01k_deduction.grid(row=12, column=1)

        def create():
            newBoi = Employee(
                self.e_id.get(),
                self.first_name.get(),
                self.last_name.get(),
                self.ssn.get(),
                DataType.JobTitle(title.get().upper()),
                DataType.Salary(payType.get().upper()),
                insurance.get(),
                self.email.get(),
                self.country.get(),
                state.get(),
                self.street_name.get(),
                int(self.postal_code.get()),
                int(self.F01k_deduction.get()),
            )
            newBoi.create()

        global enterCallback

        enterCallback = create

        def back():
            global enterCallback
            enterCallback = None
            self.go_back()

        tk.Button(self.frame, text="Create", command=create).grid(sticky="s")
        tk.Button(self.frame, text="Go Back", command=back).grid(sticky="s")

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

        tk.Label(self.frame, text="Edit User Page").grid(row=0, column=1)
        # TODO : ADD FIELDS, AND FILL THEM WITH CONTENT FROM THE DATABASE. ON SUBMIT, PUSH ALL THE DATA.
        tk.Button(self.frame, text="Go back to Employee Page", command=self.go_back).grid(row=1, column=1)

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
        tk.Button(self.frame, text="Go back to Employee Dash", command=self.go_back).grid()

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
        tk.Button(self.frame, text="Go to Employee Dash", command=self.go_back).grid()

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
        tk.Button(self.frame, text="Go Back", command=self.go_back).grid()

    def start(self):
        self.frame.grid(row=1, column=1)

    def go_back(self):
        self.frame.grid_forget()
        Menu(master=self.master, app=self.app).start()


def init():
    root = tk.Tk()

    # Create a 3 by 3 grid.
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(2, weight=1)

    def func(event):
        if enterCallback != None:
            enterCallback()

    root.bind("<Return>", func)

    app = RootApp(root=root)
    root.mainloop()
    return app
