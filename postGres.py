import psycopg2 as psycopg  # pip install psycopg2-binary
import base64
from enum import Enum


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


class DataType(Enum):
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
        VISION = "VISION"

    class Salary(Enum):
        HOURLY = "HOURLY"
        SALARY = "SALARY"


class Query:
    @staticmethod
    def CREATE(entity: Entity, *args):
        """SQL Create given the entity table and the appropriate initalizing parameters

        Ex: `Query.CREATE(Entity.STATE, "illinois", "456")`
        """
        if len(args) != len(entity.value[1]):
            raise ValueError("Not Matching entity parameters\n Values: {}".format(entity.value[1]))

        return "insert into {}{} values {} returning *;".format(entity.value[0], str(entity.value[1]).replace("'", ""), str(args))

    @staticmethod
    def UPDATE(entity: Entity, conditional: str, *args):
        """SQL Update given the entity table, the SQL conditional for selection, and the paremeters to set

        Ex: `Query.UPDATE(Entity.STATE, "state_name='illinois'", "tax_rate=753.12")`
        """
        sets = ""
        for s in args:
            sets += s + " "
        return "update {} set {} where {} returning *;".format(entity.value[0], sets, conditional)

    @staticmethod
    def DELETE(entity: Entity, conditional: str):
        """SQL Delete given the entity table and the SQL conditional for selection

        Ex: `Query.DELETE(Entity.STATE, "state_name='illinois'")`
        """
        return "delete from {} where {} returning *;".format(entity.value[0], conditional)

    @staticmethod
    def SELECT(entity: Entity, *args):
        """SQL Select given the entity table and which columns to return

        Ex: `Query.SELECT(Entity.STATE, "*")`
        """
        return "select {} FROM {};".format(str(args).strip("()").removesuffix(",").replace("'", ""), entity.value[0])


class PostGresDB:
    conn = cur = None

    def __init__(self, ip: str, schema: str):
        print("Connecting to postgres@{}".format(ip))
        self.conn = psycopg.connect(host=ip, database="postgres", user="postgres", password="postgres")
        self.cur = self.conn.cursor()
        self.cur.execute("set schema '{}'".format(schema))

    def exec(self, sql: str):
        """Execute an SQL statement"""
        print("SQL: ", sql)
        self.cur.execute(sql)
        self.conn.commit()
        # val = self.result()
        # print(val)
        # if type(val) == "list":
        # return val

    def result(self):
        """Returns whatever result an execution returns, if any"""
        try:
            return self.cur.fetchall()
        except psycopg.ProgrammingError:
            return None

    def close(self):
        self.cur.close()
        self.conn.close()
