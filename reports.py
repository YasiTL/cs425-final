import sys
from postGres import Query, Entity, Multivalue, Relation, DataType
import postGres as DB
from Employee import Employee
from Dependent import Dependent


def checkReport():

    DB.execute(Query.SELECT(Entity.EMPLOYEE, "e_id"))
    testReport= ""
    for ID in DB.result():
        e = Employee(ID[0])
        testReport += "SSn: " + e.ssn + "\n"
        #print("SSN: " + e.ssn)
        biweeklyRate = e.rate/26
        testReport += "Rate with no deductions" + biweeklyRate + "\n"
        #print("Rate with no deductions" + biweeklyRate) # with no dedutions

        #deductions 
        #medicare
        medicarePay= biweeklyRate * 0.025
        testReport += "medicare: " + medicarePay + "\n"
        # print("medicare: " + medicarePay)

        #SS
        #depends on hourly or salery 
        if e.salary_type == DataType.Salary.HOURLY.value:
            ssPay = biweeklyRate * 0.15
            testReport += "SS: " + ssPay + "\n"
            #print("SS: " + ssPay)
        else:  
            ssPay = biweeklyRate * 0.075
            testReport += " SS: " + ssPay + "\n"
            #print("SS: " + ssPay)
            #company pays other 0.075 in their expense report

        #401k deduction
        #company matched up to 7%
        #print("401k: "+ e.F01k_deduction) 
        testReport += " 401K: " + ssPay + "\n"

        #add tax braccket stuff 
        #here 
        finalPay = biweeklyRate - medicarePay - ssPay - e.F01k_deduction
        #print("final pay: " + finalPay)
        testReport += "final pay: " + finalPay + "\n"

def w2Report():
    print("this is report 2")
    DB.execute(Query.SELECT(Entity.EMPLOYEE, "e_id"))
    for ID in DB.result():
        e = Employee(ID[0])
        print(e.first_name, e.ssn, e.rate)

def expenseReport():
    print("this is report 3")
