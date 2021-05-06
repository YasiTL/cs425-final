import sys
from postGres import Query, Entity, Multivalue, Relation, DataType
import postGres as DB
from Employee import Employee
from Dependent import Dependent


def Report1():

    DB.execute(Query.SELECT(Entity.EMPLOYEE, "e_id"))
    for ID in DB.result():
        e = Employee(ID[0])
        print(e.first_name, e.last_name, e.ssn)


if len(sys.argv) < 2:
    exit("No ip given as argument")

DB.connect(sys.argv[1], "Payroll")