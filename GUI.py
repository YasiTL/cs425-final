import tkinter as tk
from tkinter import ttk
from functools import partial
from postGres import DataType
from Employee import Employee
from Dependent import Dependent
import postGres as DB
import Auth
import expenseReport

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
            Auth.signIn(user.get(), passw.get())
            if Auth.getTitle():
                self.make_Menu()

        tk.Button(self.frame, text="Login", command=signIn).grid(row=4, column=1)

        self.menuPage = Menu(master=self.master, app=self.app)

        global enterCallback
        enterCallback = signIn

    def start(self):
        self.frame.grid(row=1, column=1)

    def make_Menu(self):
        global enterCallback
        enterCallback = None
        self.frame.grid_forget()
        self.menuPage.start()


class Menu(tk.Frame):
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.frame = tk.Frame(self.master)

        self.topLabel = tk.Label(self.frame, text=Auth.getString())
        self.topLabel.grid()

        # Menu Options
        self.comapnySpendingReportButton = tk.Button(self.frame, text="Company Spending Report", command=self.goToReport3Page)
        self.report3Page = Report_3(master=self.master, app=self.app)

        self.manageAllUsersButton = tk.Button(self.frame, text="Manage Users", command=self.manageUsersPage)
        self.manageUsersPage = ManageUsers(master=self.master, app=self.app)

        self.addDependentButton = tk.Button(self.frame, text="Add Dependent", command=self.addDependentPage)
        self.addDependentPage = AddDependentPage(master=self.master, app=self.app)

    def start(self):
        # On start display of Menu, do the following:
        self.topLabel.configure(text="Menu\n{}".format(Auth.getString()))

        self.manageMyselfButton = tk.Button(self.frame, text="Edit My Profile", command=self.manageMyselfPage)
        self.manageMyselfPage = ManageMyselfPage(master=self.master, app=self.app)
        self.addDependentButton.grid()

        if Auth.getTitle() == DataType.JobTitle.ADMIN:
            self.comapnySpendingReportButton.grid()
            self.manageAllUsersButton.grid()
            self.manageMyselfButton.grid()
        elif Auth.getTitle() == DataType.JobTitle.MANAGER:
            self.manageAllUsersButton.grid()
            self.manageMyselfButton.grid()
        else:
            pass
            self.manageMyselfButton.grid()

        def signOut():
            Auth.signOut()
            self.goToSignInPage()

        tk.Button(self.frame, text="Sign Out", command=signOut).grid()

        self.frame.grid(row=1, column=1)

    def manageUsersPage(self):
        self.frame.grid_forget()
        self.manageUsersPage.start()

    def manageMyselfPage(self):
        self.frame.grid_forget()
        self.manageMyselfPage.start()

    def addDependentPage(self):
        self.frame.grid_forget()
        self.addDependentPage.start()

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
        global enterCallback
        enterCallback = self.searchFunction
        self.frame.grid(row=1, column=1)

    def go_back(self):
        global enterCallback
        enterCallback = None
        self.frame.grid_forget()
        Menu(master=self.master, app=self.app).start()

    def goToUserPage(self):
        global enterCallback
        enterCallback = None
        self.frame.grid_forget()
        UserPage(master=self.master, app=self.app).start()

    def goToAddUserPage(self):
        global enterCallback
        enterCallback = None
        self.frame.grid_forget()
        AddUserPage(master=self.master, app=self.app).start()

    def searchFunction(self):
        global currentEmployee
        currentEmployee = Employee(self.employeeIdSearchBox.get())
        if currentEmployee.exists:
            self.goToUserPage()
        else:
            tk.Label(self.frame, text="Cannot find employee").grid(row=4, column=1)


class UserPage(tk.Frame):
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.frame = tk.Frame(self.master)

        # Menu Options
        self.topLabel = tk.Label(self.frame, text="Edit Current User")
        self.topLabel.grid(row=0, column=0, sticky="n")

        tk.Button(self.frame, text="Edit User", command=self.goToEditUserPage).grid()
        self.report2Page = EditUserPage(master=self.master, app=self.app)

        tk.Button(self.frame, text="Employee W2", command=self.goToReport1Page).grid()
        self.report1Page = Report_1(master=self.master, app=self.app)

        tk.Button(self.frame, text="Bi-Weekly Paycheck", command=self.goToReport2Page).grid()
        self.report2Page = Report_2(master=self.master, app=self.app)

        tk.Button(self.frame, text="Delete User", command=self.deleteUser).grid()

        tk.Button(self.frame, text="Back to Employee Search", command=self.go_back).grid()

    def start(self):
        global currentEmployee
        self.topLabel.configure(text=currentEmployee.toString())
        self.frame.grid(row=1, column=1)

    def go_back(self):
        self.frame.grid_forget()
        ManageUsers(master=self.master, app=self.app).start()

    def manageUsersPage(self):
        self.frame.grid_forget()
        ManageUsers(master=self.master, app=self.app).start()

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
        DB.execute(DB.Query.DELETE(DB.Entity.EMPLOYEE, "e_id='{}'".format(currentEmployee.e_id)))
        self.go_back


class AddDependentPage(tk.Frame):
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.frame = tk.Frame(self.master)

        tk.Label(self.frame, text="Add Dependent Page").grid(row=0, column=1)

        benifits = list()

        for b in list(DataType.BenefitSelection):
            benifits.append(b.value)

        benifit = tk.StringVar(self.frame)
        benifit.set(benifits[0])

        tk.Label(self.frame, text="dID").grid(row=1, column=0)
        self.d_id = tk.Entry(self.frame)
        self.d_id.grid(row=1, column=1)

        tk.Label(self.frame, text="First name").grid(row=2, column=0)
        self.first_name = tk.Entry(self.frame)
        self.first_name.grid(row=2, column=1)

        tk.Label(self.frame, text="Last name").grid(row=3, column=0)
        self.last_name = tk.Entry(self.frame)
        self.last_name.grid(row=3, column=1)

        tk.Label(self.frame, text="ssn").grid(row=4, column=0)
        self.ssn = tk.Entry(self.frame)
        self.ssn.grid(row=4, column=1)

        tk.Label(self.frame, text="Benifits").grid(row=7, column=0)
        tk.OptionMenu(self.frame, benifit, *benifits).grid(row=7, column=1)

        def create():
            newDependent = Dependent(
                self.d_id.get(),
                self.first_name.get(),
                self.last_name.get(),
                self.ssn.get(),
                DataType.BenefitSelection(benifit.get().upper()),
            )
            newDependent.create()

        def back():
            self.go_back()

        tk.Button(self.frame, text="Create", command=create).grid(sticky="s")
        tk.Button(self.frame, text="Go Back", command=back).grid(sticky="s")

        global enterCallback
        enterCallback = create

    def start(self):
        self.frame.grid(row=1, column=1)

    def go_back(self):
        global enterCallback
        enterCallback = None
        self.frame.grid_forget()
        ManageUsers(master=self.master, app=self.app).start()


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

        tk.Label(self.frame, text="eID").grid(row=1, column=0)
        self.e_id = tk.Entry(self.frame)
        self.e_id.grid(row=1, column=1)

        tk.Label(self.frame, text="First name").grid(row=2, column=0)
        self.first_name = tk.Entry(self.frame)
        self.first_name.grid(row=2, column=1)

        tk.Label(self.frame, text="Last name").grid(row=3, column=0)
        self.last_name = tk.Entry(self.frame)
        self.last_name.grid(row=3, column=1)

        tk.Label(self.frame, text="ssn").grid(row=4, column=0)
        self.ssn = tk.Entry(self.frame)
        self.ssn.grid(row=4, column=1)

        tk.Label(self.frame, text="Job title").grid(row=5, column=0)
        tk.OptionMenu(self.frame, title, *titles).grid(row=5, column=1)

        tk.Label(self.frame, text="Salary type").grid(row=6, column=0)
        tk.OptionMenu(self.frame, payType, *payTypes).grid(row=6, column=1)

        tk.Label(self.frame, text="Insurance plan").grid(row=7, column=0)
        tk.OptionMenu(self.frame, insurance, *insurances).grid(row=7, column=1)

        tk.Label(self.frame, text="Email").grid(row=8, column=0)
        self.email = tk.Entry(self.frame)
        self.email.grid(row=8, column=1)

        tk.Label(self.frame, text="Country").grid(row=9, column=0)
        self.country = tk.Entry(self.frame)
        self.country.grid(row=9, column=1)

        tk.Label(self.frame, text="State").grid(row=10, column=0)
        tk.OptionMenu(self.frame, state, *states).grid(row=10, column=1)

        tk.Label(self.frame, text="Street Name").grid(row=11, column=0)
        self.street_name = tk.Entry(self.frame)
        self.street_name.grid(row=11, column=1)

        tk.Label(self.frame, text="Postal Code").grid(row=12, column=0)
        self.postal_code = tk.Entry(self.frame)
        self.postal_code.grid(row=12, column=1)

        tk.Label(self.frame, text="401k Deduction").grid(row=13, column=0)
        self.F01k_deduction = tk.Entry(self.frame)
        self.F01k_deduction.grid(row=13, column=1)

        tk.Label(self.frame, text="Rate").grid(row=14, column=0)  # TODO: change label based on hourly or salaried
        self.rate = tk.Entry(self.frame)
        self.rate.grid(row=14, column=1)

        tk.Label(self.frame, text="Hours").grid(row=15, column=0)  # TODO: change label based on hourly or salaried
        self.hours = tk.Entry(self.frame)
        self.hours.grid(row=15, column=1)

        self.DependentsTreeview = ListboxEditable(self.frame, list(), 17, 0)
        self.PhoneNumbersTreeview = ListboxEditable(self.frame, list(), 17, 1)
        self.BenefitsTreeview = ListboxEditable(self.frame, list(), 17, 2)

        tk.Button(self.frame, text="Add Dependent", command=self.DependentsTreeview.addPlaceRow).grid(row=16, column=0)
        tk.Button(self.frame, text="Add Number", command=self.PhoneNumbersTreeview.addPlaceRow).grid(row=16, column=1)
        tk.Button(self.frame, text="Add Benefit", command=self.BenefitsTreeview.addPlaceRow).grid(row=16, column=2)

        self.DependentsTreeview.placeListBoxEditable()
        self.PhoneNumbersTreeview.placeListBoxEditable()
        self.BenefitsTreeview.placeListBoxEditable()

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
                float(self.rate.get()),
                int(self.hours.get()),
            )
            newBoi.Dependents = set(self.DependentsTreeview.getList())
            newBoi.PhoneNumbers = set(self.PhoneNumbersTreeview.getList())
            newBoi.Benefits = set(self.BenefitsTreeview.getList())
            newBoi.create()

        def back():
            self.go_back()

        tk.Button(self.frame, text="Create", command=create).grid(sticky="s")
        tk.Button(self.frame, text="Go Back", command=back).grid(sticky="s")

        global enterCallback
        enterCallback = create

    def start(self):
        self.frame.grid(row=1, column=1)

    def go_back(self):
        global enterCallback
        enterCallback = None
        self.frame.grid_forget()
        ManageUsers(master=self.master, app=self.app).start()


# Colors
colorActiveTab = "#CCCCCC"  # Color of the active tab
colorNoActiveTab = "#EBEBEB"  # Color of the no active tab


class ListboxEditable(object):
    """A class that emulates a listbox, but you can also edit a field"""

    def __init__(self, frameMaster, _list, row, column):
        self.frameMaster = frameMaster
        self.list = list(_list)
        self.rows = list()
        self.row = row
        self.column = column

        i = 0
        for row in self.list:
            self.addRow(row)

            i = i + 1

    def addRow(self, text):
        row = tk.Label(
            self.frameMaster,
            text=text,
            bg=colorActiveTab,
            fg="black",
            width=10,
        )
        self.rows.append(row)

        row.bind("<Button-1>", lambda event, a=row: self.changeBackground(a))
        row.bind("<Double-1>", lambda event, a=row: self.changeToEntry(a))
        row.bind("<Delete>", lambda event, a=row: self.delete(a))
        return row

    def addPlaceRow(self, text="Edit Me"):
        newRow = self.addRow(text)
        newRow.grid(row=self.row + len(self.rows) - 1, column=self.column)

    def getRowPos(self, row):
        ind = self.row
        for _row in self.rows:
            if row == _row:
                return ind
            ind = ind + 1

    # Place
    def placeListBoxEditable(self):
        ind = self.row
        for row in self.rows:
            row.grid(row=ind, column=self.column)
            ind = ind + 1
        return ind

    # Action to do when one click
    def changeBackground(self, row):
        for _row in self.rows:
            _row.configure(bg=colorActiveTab)

        row.configure(bg=colorNoActiveTab)
        row.focus_set()

    # Action to do when double-click
    def changeToEntry(self, row):
        self.entryVar = tk.StringVar()
        self.entryActive = ttk.Entry(self.frameMaster, textvariable=self.entryVar, width=10)
        self.entryActive.grid(row=self.getRowPos(row), column=self.column)
        self.entryActive.focus_set()
        self.entryActive.insert(0, row.cget("text"))

        self.entryActive.bind("<FocusOut>", lambda event, a=row: self.saveEntryValue(a))
        self.entryActive.bind("<Return>", lambda event, a=row: self.saveEntryValue(a))

    # Action to do when focus out from the entry
    def saveEntryValue(self, row):
        self.entryActive.grid_forget()
        row.grid(row=self.getRowPos(row), column=self.column)
        row.configure(text=self.entryVar.get())

    def delete(self, row):
        row.grid_remove()  # TODO: improve placement, shift rows up when deleted
        row.pack_forget()
        self.rows.remove(row)

    def getList(self):
        rtn = list()
        for row in self.rows:
            rtn.append(row["text"])
        return rtn


class EditUserPage(tk.Frame):
    def __init__(self, master=None, app=None):
        global currentEmployee
        self.master = master
        self.app = app
        self.frame = tk.Frame(self.master)

        self.master = master
        self.app = app
        self.frame = tk.Frame(self.master)

        self.topLabel = tk.Label(self.frame, text="Edit User Page")
        self.topLabel.grid(row=0, column=1)

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

        self.title = tk.StringVar(self.frame)
        self.title.set(currentEmployee.job_title)

        self.payType = tk.StringVar(self.frame)
        self.payType.set(currentEmployee.salary_type)

        self.insurance = tk.StringVar(self.frame)
        self.insurance.set(currentEmployee.insurancePlan)

        self.state = tk.StringVar(self.frame)
        self.state.set(currentEmployee.state)

        tk.Label(self.frame, text="eID").grid(row=1, column=0)
        self.e_id = tk.Entry(self.frame)
        self.e_id.insert(0, currentEmployee.e_id)
        self.e_id.grid(row=1, column=1)
        self.e_id.configure(state="disable")

        tk.Label(self.frame, text="First name").grid(row=2, column=0)
        self.first_name = tk.Entry(self.frame)
        self.first_name.insert(0, currentEmployee.first_name)
        self.first_name.grid(row=2, column=1)

        tk.Label(self.frame, text="Last name").grid(row=3, column=0)
        self.last_name = tk.Entry(self.frame)
        self.last_name.insert(0, currentEmployee.last_name)
        self.last_name.grid(row=3, column=1)

        tk.Label(self.frame, text="ssn").grid(row=4, column=0)
        self.ssn = tk.Entry(self.frame)
        self.ssn.insert(0, currentEmployee.ssn)
        self.ssn.grid(row=4, column=1)

        tk.Label(self.frame, text="Job title").grid(row=5, column=0)
        tk.OptionMenu(self.frame, self.title, *titles).grid(row=5, column=1)

        tk.Label(self.frame, text="Salary type").grid(row=6, column=0)
        tk.OptionMenu(self.frame, self.payType, *payTypes).grid(row=6, column=1)

        tk.Label(self.frame, text="Insurance plan").grid(row=7, column=0)
        tk.OptionMenu(self.frame, self.insurance, *insurances).grid(row=7, column=1)

        tk.Label(self.frame, text="Email").grid(row=8, column=0)
        self.email = tk.Entry(self.frame)
        self.email.insert(0, currentEmployee.email)
        self.email.grid(row=8, column=1)

        tk.Label(self.frame, text="Country").grid(row=9, column=0)
        self.country = tk.Entry(self.frame)
        self.country.insert(0, currentEmployee.country)
        self.country.grid(row=9, column=1)

        tk.Label(self.frame, text="State").grid(row=10, column=0)
        tk.OptionMenu(self.frame, self.state, *states).grid(row=10, column=1)

        tk.Label(self.frame, text="Street Name").grid(row=11, column=0)
        self.street_name = tk.Entry(self.frame)
        self.street_name.insert(0, currentEmployee.street_name)
        self.street_name.grid(row=11, column=1)

        tk.Label(self.frame, text="Postal Code").grid(row=12, column=0)
        self.postal_code = tk.Entry(self.frame)
        self.postal_code.insert(0, currentEmployee.postal_code)
        self.postal_code.grid(row=12, column=1)

        tk.Label(self.frame, text="401k Deduction").grid(row=13, column=0)
        self.F01k_deduction = tk.Entry(self.frame)
        self.F01k_deduction.insert(0, currentEmployee.F01k_deduction)
        self.F01k_deduction.grid(row=13, column=1)

        tk.Label(self.frame, text="Rate").grid(row=14, column=0)  # TODO: change label based on hourly or salaried
        self.rate = tk.Entry(self.frame)
        self.rate.insert(0, currentEmployee.rate)
        self.rate.grid(row=14, column=1)

        tk.Label(self.frame, text="Hours").grid(row=15, column=0)  # TODO: change label based on hourly or salaried
        self.hours = tk.Entry(self.frame)
        self.hours.insert(0, currentEmployee.hours)
        self.hours.grid(row=15, column=1)

        self.DependentsTreeview = ListboxEditable(self.frame, list(currentEmployee.Dependents), 17, 0)
        self.PhoneNumbersTreeview = ListboxEditable(self.frame, list(currentEmployee.PhoneNumbers), 17, 1)
        self.BenefitsTreeview = ListboxEditable(self.frame, list(currentEmployee.Benefits), 17, 2)

        tk.Button(self.frame, text="Add Dependent", command=self.DependentsTreeview.addPlaceRow).grid(row=16, column=0)
        tk.Button(self.frame, text="Add Number", command=self.PhoneNumbersTreeview.addPlaceRow).grid(row=16, column=1)
        tk.Button(self.frame, text="Add Benefit", command=self.BenefitsTreeview.addPlaceRow).grid(row=16, column=2)

        self.DependentsTreeview.placeListBoxEditable()
        self.PhoneNumbersTreeview.placeListBoxEditable()
        self.BenefitsTreeview.placeListBoxEditable()

        tk.Button(self.frame, text="Update", command=self.update).grid(sticky="s")
        tk.Button(self.frame, text="Back", command=self.go_back).grid(sticky="s")

    def update(self):
        global currentEmployee
        currentEmployee.first_name = self.first_name.get()
        currentEmployee.last_name = self.last_name.get()
        currentEmployee.ssn = self.ssn.get()
        currentEmployee.job_title = self.title.get()
        currentEmployee.salary_type = self.payType.get()
        currentEmployee.insurancePlan = self.insurance.get()
        currentEmployee.email = self.email.get()
        currentEmployee.country = self.country.get()
        currentEmployee.state = self.state.get()
        currentEmployee.street_name = self.street_name.get()
        currentEmployee.postal_code = self.postal_code.get()
        currentEmployee.F01k_deduction = self.F01k_deduction.get()
        currentEmployee.rate = self.rate.get()
        currentEmployee.hours = self.hours.get()
        currentEmployee.Dependents = set(self.DependentsTreeview.getList())
        currentEmployee.PhoneNumbers = set(self.PhoneNumbersTreeview.getList())
        currentEmployee.Benefits = set(self.BenefitsTreeview.getList())
        currentEmployee.update()

    def start(self):
        # global enterCallback
        # enterCallback = self.update
        self.topLabel.configure(text="Edit User : {}".format(currentEmployee.toString()))
        self.frame.grid(row=1, column=1)

    def go_back(self):
        # global enterCallback
        # enterCallback = None
        self.frame.grid_forget()
        UserPage(master=self.master, app=self.app).start()


class ManageMyselfPage(tk.Frame):
    def __init__(self, master=None, app=None):
        global currentEmployee
        currentEmployee = Auth.getCurrentEmployee()
        self.master = master
        self.app = app
        self.frame = tk.Frame(self.master)

        self.master = master
        self.app = app
        self.frame = tk.Frame(self.master)

        self.topLabel = tk.Label(self.frame, text="Edit User Page")
        self.topLabel.grid(row=0, column=1)

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

        self.title = tk.StringVar(self.frame)
        self.title.set(currentEmployee.job_title)

        self.payType = tk.StringVar(self.frame)
        self.payType.set(currentEmployee.salary_type)

        self.insurance = tk.StringVar(self.frame)
        self.insurance.set(currentEmployee.insurancePlan)

        self.state = tk.StringVar(self.frame)
        self.state.set(currentEmployee.state)

        tk.Label(self.frame, text="eID").grid(row=1, column=0)
        self.e_id = tk.Entry(self.frame)
        self.e_id.insert(0, currentEmployee.e_id)
        self.e_id.grid(row=1, column=1)
        self.e_id.configure(state="disable")

        tk.Label(self.frame, text="First name").grid(row=2, column=0)
        self.first_name = tk.Entry(self.frame)
        self.first_name.insert(0, currentEmployee.first_name)
        self.first_name.grid(row=2, column=1)

        tk.Label(self.frame, text="Last name").grid(row=3, column=0)
        self.last_name = tk.Entry(self.frame)
        self.last_name.insert(0, currentEmployee.last_name)
        self.last_name.grid(row=3, column=1)

        tk.Label(self.frame, text="ssn").grid(row=4, column=0)
        self.ssn = tk.Entry(self.frame)
        self.ssn.insert(0, currentEmployee.ssn)
        self.ssn.grid(row=4, column=1)

        tk.Label(self.frame, text="Job title").grid(row=5, column=0)
        jobTitleOptionMenu = tk.OptionMenu(self.frame, self.title, *titles)
        jobTitleOptionMenu.grid(row=5, column=1)
        if currentEmployee.job_title != "ADMIN":
            jobTitleOptionMenu.configure(state="disable")

        tk.Label(self.frame, text="Salary type").grid(row=6, column=0)
        salaryOptionMenu = tk.OptionMenu(self.frame, self.payType, *payTypes)
        salaryOptionMenu.grid(row=6, column=1)
        if currentEmployee.job_title != "ADMIN":
            salaryOptionMenu.configure(state="disable")

        tk.Label(self.frame, text="Insurance plan").grid(row=7, column=0)
        tk.OptionMenu(self.frame, self.insurance, *insurances).grid(row=7, column=1)

        tk.Label(self.frame, text="Email").grid(row=8, column=0)
        self.email = tk.Entry(self.frame)
        self.email.insert(0, currentEmployee.email)
        self.email.grid(row=8, column=1)

        tk.Label(self.frame, text="Country").grid(row=9, column=0)
        self.country = tk.Entry(self.frame)
        self.country.insert(0, currentEmployee.country)
        self.country.grid(row=9, column=1)

        tk.Label(self.frame, text="State").grid(row=10, column=0)
        tk.OptionMenu(self.frame, self.state, *states).grid(row=10, column=1)

        tk.Label(self.frame, text="Street Name").grid(row=11, column=0)
        self.street_name = tk.Entry(self.frame)
        self.street_name.insert(0, currentEmployee.street_name)
        self.street_name.grid(row=11, column=1)

        tk.Label(self.frame, text="Postal Code").grid(row=12, column=0)
        self.postal_code = tk.Entry(self.frame)
        self.postal_code.insert(0, currentEmployee.postal_code)
        self.postal_code.grid(row=12, column=1)

        tk.Label(self.frame, text="401k Deduction").grid(row=13, column=0)
        self.F01k_deduction = tk.Entry(self.frame)
        self.F01k_deduction.insert(0, currentEmployee.F01k_deduction)
        self.F01k_deduction.grid(row=13, column=1)

        tk.Label(self.frame, text="Rate").grid(row=14, column=0)  # TODO: change label based on hourly or salaried
        self.rate = tk.Entry(self.frame)
        self.rate.insert(0, currentEmployee.rate)
        self.rate.grid(row=14, column=1)
        if currentEmployee.job_title != "ADMIN":
            self.rate.configure(state="disable")

        tk.Label(self.frame, text="Hours").grid(row=15, column=0)  # TODO: change label based on hourly or salaried
        self.hours = tk.Entry(self.frame)
        self.hours.insert(0, currentEmployee.hours)
        self.hours.grid(row=15, column=1)

        self.DependentsTreeview = ListboxEditable(self.frame, list(currentEmployee.Dependents), 17, 0)
        self.PhoneNumbersTreeview = ListboxEditable(self.frame, list(currentEmployee.PhoneNumbers), 17, 1)
        self.BenefitsTreeview = ListboxEditable(self.frame, list(currentEmployee.Benefits), 17, 2)

        tk.Button(self.frame, text="Add Dependent", command=self.DependentsTreeview.addPlaceRow).grid(row=16, column=0)
        tk.Button(self.frame, text="Add Number", command=self.PhoneNumbersTreeview.addPlaceRow).grid(row=16, column=1)
        tk.Button(self.frame, text="Add Benefit", command=self.BenefitsTreeview.addPlaceRow).grid(row=16, column=2)

        self.DependentsTreeview.placeListBoxEditable()
        self.PhoneNumbersTreeview.placeListBoxEditable()
        self.BenefitsTreeview.placeListBoxEditable()

        tk.Button(self.frame, text="Update", command=self.update).grid(sticky="s")
        tk.Button(self.frame, text="Back", command=self.go_back).grid(sticky="s")

    def update(self):
        global currentEmployee
        currentEmployee.first_name = self.first_name.get()
        currentEmployee.last_name = self.last_name.get()
        currentEmployee.ssn = self.ssn.get()
        currentEmployee.job_title = self.title.get()
        currentEmployee.salary_type = self.payType.get()
        currentEmployee.insurancePlan = self.insurance.get()
        currentEmployee.email = self.email.get()
        currentEmployee.country = self.country.get()
        currentEmployee.state = self.state.get()
        currentEmployee.street_name = self.street_name.get()
        currentEmployee.postal_code = self.postal_code.get()
        currentEmployee.F01k_deduction = self.F01k_deduction.get()
        currentEmployee.rate = self.rate.get()
        currentEmployee.hours = self.hours.get()
        currentEmployee.Dependents = set(self.DependentsTreeview.getList())
        currentEmployee.PhoneNumbers = set(self.PhoneNumbersTreeview.getList())
        currentEmployee.Benefits = set(self.BenefitsTreeview.getList())
        currentEmployee.update()

    def start(self):
        # global enterCallback
        # enterCallback = self.update
        self.topLabel.configure(text="Edit User : {}".format(currentEmployee.toString()))
        self.frame.grid(row=1, column=1)

    def go_back(self):
        # global enterCallback
        # enterCallback = None
        self.frame.grid_forget()
        Menu(master=self.master, app=self.app).start()


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
        self.report = tk.Label(self.frame, text="Update")
        self.report.grid()
        tk.Button(self.frame, text="Go Back", command=self.go_back).grid()

    def start(self):
        self.report.configure(text=expenseReport.report())
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
        global enterCallback
        if enterCallback != None:
            enterCallback()

    root.bind("<Return>", func)

    app = RootApp(root=root)
    root.mainloop()
    return app
