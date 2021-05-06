import psycopg2 as psycopg  # pip install psycopg2-binary
import base64
from enum import Enum
import subprocess
import os


class Entity(Enum):
    STATE = ("state_t", ("state_name", "tax_rate"))
    INSURNACE_PLAN = (
        "insurancePlan_t",
        (
            "plan_id",
            "employee_cost_for_individualPlan",
            "employee_cost_for_familyPlan",
            "employer_cost_for_indivudal",
            "employer_cost_for_family",
        ),
    )
    DEPENDENT = (
        "Dependent_t",
        ("d_id", "first_name", "last_name", "ssn", "benefitSelection"),
    )
    EMPLOYEE = (
        "employee_t",
        (
            "e_id",
            "first_name",
            "last_name",
            "ssn",
            "job_title",
            "salary_type",
            "insurancePlan",
            "email",
            "country",
            "state",
            "street_name",
            "postal_code",
            "F01k_deduction",
            "rate",
        ),
    )


class Multivalue(Enum):
    DEPENDENT_BENEFIT_SELECTION = ("dependent_benefitselection_m", ("d_id", "selection"))
    EMPLOYEE_BENEFIT_SELECTION = ("employee_benefitselection_m", ("e_id", "selection"))
    EMPLOYEE_PHONE = ("employee_phone_m", ("e_id", "phone"))


class Relation(Enum):
    HAS = ("has_r", ("e_id", "d_id"))
    LIVES_IN = ("lives_in_r", ("e_id", "state_name"))
    PICKS_PLAN = ("picks_plan_r", ("e_id", "plan_id"))


class DataType:
    class BenefitSelection(Enum):
        F01K_CONTRIBUTION = "401K_CONTRIBUTION"
        ATTORNEY_PLAN = "ATTORNEY_PLAN"
        LIFE_INSURANCE = "LIFE_INSURANCE"
        DENTAL = "DENTAL"
        VISION = "VISION"

    class JobTitle(Enum):
        ADMIN = "ADMIN"
        MANAGER = "MANAGER"
        EMPLOYEE = "EMPLOYEE"

    class Salary(Enum):
        HOURLY = "HOURLY"
        SALARY = "SALARY"


class Query:
    @staticmethod
    def CREATE(entity: Enum, *args):
        """SQL Create given the entity table and the appropriate initalizing parameters

        Ex: `Query.CREATE(Entity.STATE, "illinois", "456")`
        """
        if len(args) != len(entity.value[1]):
            raise ValueError("Not Matching entity parameters\n Values: {}".format(entity.value[1]))

        return "insert into {}{} values {} returning *;".format(entity.value[0], str(entity.value[1]).replace("'", ""), str(args))

    @staticmethod
    def UPDATE(entity: Enum, conditional: str, *args):
        """SQL Update given the entity table, the SQL conditional for selection, and the paremeters to set

        Ex: `Query.UPDATE(Entity.STATE, "state_name='illinois'", "tax_rate=753.12")`
        """
        sets = ""
        for s in args:
            if s:
                sets += s + ", "
        sets = sets.strip(" ,")
        return "update {} set {} where {} returning *;".format(entity.value[0], sets, conditional)

    @staticmethod
    def UPDATE_SINGLE(entity: Enum, primary_key: str, *args):
        """SQL Update a single entity given it's single primary key and the paremeters to set

        Ex: `Query.UPDATE(Entity.STATE, "illinois", "tax_rate=753.12")`
        """
        sets = ""
        for s in args:
            if s:
                sets += s + ", "
        sets = sets.strip(" ,")
        return "update {} set {} where {} returning *;".format(entity.value[0], sets, "{}='{}'".format(entity.value[1][0], primary_key))

    @staticmethod
    def DELETE(entity: Enum, conditional: str):
        """SQL Delete given the entity table and the SQL conditional for selection

        Ex: `Query.DELETE(Entity.STATE, "state_name='illinois'")`
        """
        return "delete from {} where {} returning *;".format(entity.value[0], conditional)

    @staticmethod
    def SELECT(entity: Enum, *args):
        """SQL Select given the entity table and which columns to return (returns all by default)

        Ex: `Query.SELECT(Entity.STATE, "*")`
        """
        if len(args) == 0:
            args = "*"
        return "select {} FROM {};".format(str(args).strip("()").removesuffix(",").replace("'", ""), entity.value[0])

    @staticmethod
    def SELECT_WHERE(entity: Enum, conditional: str, *args):
        """SQL Select given the entity table, the conditional , and which columns to return (returns all by default)

        Ex: `Query.SELECT_WHERE(Entity.EMPLOYEE,"e_id='1234567'", "*")`
        """
        if len(args) == 0:
            args = "*"
        return "select {} FROM {} WHERE {};".format(str(args).strip("()").removesuffix(",").replace("'", ""), entity.value[0], conditional)

    @staticmethod
    def FIND(entity: Enum, primary_key: str, *args):
        """Find an entity given it's single primary key, and which columns to return (returns all by default)

        Ex: `Query.FIND(Entity.STATE, "illinois", "*")`
        """
        if len(args) == 0:
            args = "*"
        return "select {} FROM {} WHERE {};".format(
            str(args).strip("()").removesuffix(",").replace("'", ""), entity.value[0], "{}='{}'".format(entity.value[1][0], primary_key)
        )


conn = None
cur = None

logFile = None

winCommand = 'start cmd /k powershell Get-Content postgres.log -Wait'
unixCommand = 'tail -f postgres.log'

def connect(ip: str, schema: str):
    global conn, cur, logFile
    if not conn:
        print("Connecting to postgres@{}".format(ip))
        conn = psycopg.connect(host=ip, database="postgres", user="postgres", password="postgresisthepassword")
        conn.set_session(autocommit=True)
        cur = conn.cursor()
        cur.execute("set schema '{}'".format(schema))
        logFile = open("postgres.log", 'a', 20)
        if os.name == 'nt':
            subprocess.run(winCommand, shell=True)
    else:
        print("Already connected")


def execute(sql: str):
    global conn, cur, logFile
    """Execute an SQL statement"""
    if not conn:
        print("Not connected!")
        return
    
    logFile.write("SQL: {}\n".format(sql))
    logFile.flush()
    try:
        cur.execute(sql)
    except Exception as e:
        print(e)


def result():
    global conn, cur
    """Returns whatever result an execution returns, if any"""
    if not conn:
        print("Not connected!")
        return
    try:
        return cur.fetchall()
    except psycopg.ProgrammingError:
        return None


def close():
    global conn, cur
    if not conn:
        print("Not connected!")
        return
    cur.close()
    conn.close()
