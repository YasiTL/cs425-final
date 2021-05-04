import sys
from postGres import Query, Entity, Multivalue, Relation, DataType
import postGres as DB
import Auth
from Employee import Employee


def main():
    if len(sys.argv) < 2:
        exit("No ip given as argument")

    DB.connect(sys.argv[1], "Payroll")

    Auth.signIn("Yasi", 1234567)

    clearance = Auth.getTitle()

    if clearance == DataType.JobTitle.ADMIN:
        print("is Admin")

    e0 = Employee(
        "newBoi",
        "yakuza",
        "boiboi",
        4567,
        DataType.JobTitle.EMPLOYEE,
        DataType.Salary.HOURLY,
        "basic health",
        "bonga@bonga.com",
        "yes",
        "Illinois",
        "what",
        773302,
        21,
    )
    e0.create()
    e0.first_name = "newName"
    e0.update()


main()