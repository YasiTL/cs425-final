import sys
from postGres import Query, Entity, Multivalue, Relation, DataType
import postGres as DB
import Auth


def main():
    if len(sys.argv) < 2:
        exit("No ip given as argument")

    DB.connect(sys.argv[1], "Payroll")

    Auth.signIn("Yasi", 1234567)

    clearance = Auth.getTitle()

    if clearance == DataType.JobTitle.ADMIN:
        print("is Admin")


main()