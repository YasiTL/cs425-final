import sys
import Auth
from postGres import Query, Entity, Multivalue, Relation, DataType
import postGres as DB
from Employee import Employee
from Dependent import Dependent
from random import randint as rnd


def checkReport():
    biweeklyReport = ""
    ssn = ""
    biweeklyPay = 0
    stateTax = 0
    federalTax = 0
    socialsPay = 0
    medicarePay = 0
    F01kPay = 0
    insurancePay = 0
    finalPay = 0

    DB.execute(Query.SELECT(Entity.EMPLOYEE, "e_id"))

    # get current employee
    e = Auth.getCurrentEmployee()
    ssn = e.ssn

    if e.salary_type == DataType.Salary.HOURLY.value:
        biweeklyPay = round(e.hours * e.rate, 2)
    else:
        biweeklyPay = round(e.rate / 26, 2)

    sTax = biweeklyPay * e.getTaxRate()
    stateTax = round(sTax, 2)

    if e.rate < 10000:
        fTax = biweeklyPay * 0.01
    elif e.rate < 40000:
        fTax = biweeklyPay * 0.02
    elif e.rate < 85000:
        fTax = biweeklyPay * 0.04
    elif e.rate < 163301:
        fTax = biweeklyPay * 0.06
    elif e.rate < 207351:
        fTax = biweeklyPay * 0.08
    else:
        fTax = biweeklyPay * 0.09

    federalTax = round(fTax, 2)

    # SS
    if e.salary_type == DataType.Salary.HOURLY.value:
        ssPay = biweeklyPay * 0.15
        socialsPay = round(ssPay, 2)
    else:
        ssPay = biweeklyPay * 0.075
        socialsPay = round(ssPay, 2)
        # company pays other 0.075 in their expense report

    # medicare
    mcPay = biweeklyPay * 0.025
    medicarePay = round(mcPay, 2)

    # 401k deduction
    F01kPay = round(biweeklyPay * (e.F01k_deduction / 100), 2)
    # company matched up to 7%

    insurancePay = round(float(e.getInsurnacePlanCost()), 2)
    # here
    finalPay = round(biweeklyPay - stateTax - federalTax - socialsPay - medicarePay - F01kPay - insurancePay, 2)

    biweeklyReport += """
---------[ BIWEEKLY CHECK REPORT ]---------
    
    SSN : {}
    income no deductions: ${}
    state tax: ${}
    federal tax: ${}
    social security contribution: ${}
    medicare contribution: ${}
    401k contribution: ${}
    insurance cost: ${}
    Final pay: ${}
    """.format(
        ssn, biweeklyPay, stateTax, federalTax, socialsPay, medicarePay, F01kPay, insurancePay, finalPay
    )

    return biweeklyReport


def w2Report():
    # print("this is report 2")
    # 52 weeks yearly
    w2ReportText = "here it will show"
    DB.execute(Query.SELECT(Entity.EMPLOYEE, "e_id"))
    for ID in DB.result():
        e = Employee(ID[0])
        print(e.first_name, e.ssn, e.rate)
    return w2ReportText


def expenseReport():
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