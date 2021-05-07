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
    premium = 0

    DB.execute(Query.SELECT(Entity.EMPLOYEE, "e_id"))
    for ID in DB.result():
        e = Employee(ID[0])
        wage = e.rate * e.hours
        if e.salary_type == DataType.Salary.SALARY.value:
            wage = e.rate
            bonuses += rnd(0, int(e.rate)) + e.rate % 1
            bonusCount += 1
            social += 0.075 * wage
        employeeWages += wage
        f01k += wage * min(float(e.F01k_deduction) / 100.0, 0.07)
        employeeCount += 1
        premium += e.getInsurnacePlanCost() / 2

    repo += """
---------[ COMPANY EXPENSE REPORT ]---------
    
    Employee Wages @ {} : ${}
    Bonuses @ {} : ${}
    401K Contributions : ${}
    Social Security Contribution @ {} : ${}
    Insurance Premiums : ${}
    
    """.format(
        employeeCount, employeeWages, bonusCount, bonuses, round(f01k, 2), bonusCount, social, premium
    )

    return repo