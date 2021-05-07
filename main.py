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

    Log.init()
    DB.connect(sys.argv[1], "Payroll")
    # print(reports.checkReport())
    GUI.init()


main()
