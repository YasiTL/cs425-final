import sys
from postGres import Query, Entity, Multivalue, Relation, DataType
import postGres as DB
from Employee import Employee
from Dependent import Dependent


def checkReport():

    DB.execute(Query.SELECT(Entity.EMPLOYEE, "e_id"))
    for ID in DB.result():
        e = Employee(ID[0])
        print("SSN: " + e.ssn)
        biweeklyRate = e.rate/26
        print("Rate with no deductions" + biweeklyRate) # with no dedutions
        #deductions 
        #medicare
        medicarePay= biweeklyRate * 0.025
        print("medicare: " + medicarePay)

    if len(sys.argv) < 2:
        exit("No ip given as argument")

DB.connect(sys.argv[1], "Payroll")

def w2Report():
    print("this is report 2")
    DB.execute(Query.SELECT(Entity.EMPLOYEE, "e_id"))
    for ID in DB.result():
        e = Employee(ID[0])
        print(e.first_name, e.ssn, e.rate)

def expenseReport():
    print("this is report 3")
