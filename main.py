import sys
from postGres import Query, Entity, Multivalue, Relation, DataType
import postGres as DB
import Auth
from Employee import Employee
from Dependent import Dependent
import GUI
import reports
import Log


def main():
    if len(sys.argv) < 2:
        exit("No ip given as argument")

    # Log.init()

    DB.connect(sys.argv[1], "Payroll")

    # print(reports.checkReport())

    GUI.init()

    # d0 = Dependent("someDep")
    # d0.first_name = "whahahah"
    # d0.update()

    # Auth.signIn("Yasi", 1234567)

    # clearance = Auth.getTitle()

    # if clearance == DataType.JobTitle.ADMIN:
    #     print("is Admin")

    # e2 = Employee(111111)
    # e2.ssn = "4563786"
    # print(e2.Dependents)

    # e1 = Employee(1234567)

    # e1.addPhoneNumber(76)
    # e1.addPhoneNumber(46478)
    # e1.addBenefit(DataType.BenefitSelection.DENTAL)
    # e1.addDependent("someDep")
    # e1.addDependent("2222222")

    # e1.update()

    # e0 = Employee(
    #     "newBoi",
    #     "yakuza",
    #     "boiboi",
    #     4567,
    #     DataType.JobTitle.EMPLOYEE,
    #     DataType.Salary.HOURLY,
    #     "basic health",
    #     "bonga@bonga.com",
    #     "yes",
    #     "Illinois",
    #     "what",
    #     773302,
    #     21,
    # )
    # e0.create()
    # e0.first_name = "newName"
    # e0.update()


main()