from postGres import Query, Entity, Multivalue, Relation, DataType
import postGres as DB
from Employee import Employee
from Dependent import Dependent
import math
from random import randint as rnd


def report():
    repo = ""
    employeeCount = 0
    employeeWages = 0
    bonusCount = 0
    bonuses = 0
    f01k = 0
    social = 0

    DB.execute(Query.SELECT(Entity.EMPLOYEE, "e_id"))
    for ID in DB.result():
        e = Employee(ID[0])
        wage = e.rate * e.hours
        employeeWages += wage
        f01k += wage * min(float(e.F01k_deduction) / 100.0, 0.07)
        employeeCount += 1
        if e.salary_type == DataType.Salary.SALARY.value:
            bonuses += rnd(0, int(e.rate)) + e.rate % 1
            bonusCount += 1
            social += 0.075 * wage

    repo += """
---------[ COMPANY EXPENSE REPORT ]---------
    
    Employee Wages @ {} : ${}
    Bonuses @ {} : ${}
    401K Contributions : ${}
    Social Security Contribution @ {} : ${}
    
    """.format(
        employeeCount, employeeWages, bonusCount, bonuses, int(f01k * 100) / 100, bonusCount, social
    )

    return repo