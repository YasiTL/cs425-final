import psycopg2 as psycopg  # pip install psycopg2-binary
import base64
import sys
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


class Query:
    @staticmethod
    def CREATE(entity: Entity, *args):
        return "insert into {}{} values {};".format(entity.value[0], str(entity.value[1]).replace("'", ""), str(args))

    @staticmethod
    def UPDATE(entity: Entity, conditional: str, *args):
        sets = ""
        for s in args:
            sets += s + " "
        return "update {} set {} where {} returning *;".format(entity.value[0], sets, conditional)

    @staticmethod
    def DELETE(entity: Entity, conditional: str):
        return "delete from {} where {} returning *;".format(entity.value[0], conditional)


# 99.127.217.73


class PostGresDB:
    conn = cur = None

    def __init__(self, ip: str, schema: str):
        print("Connecting to postgres@{}".format(ip))
        self.conn = psycopg.connect(host=ip, database="postgres", user="postgres", password="postgres")
        self.cur = self.conn.cursor()
        self.cur.execute("set schema '{}'".format(schema))

    def exec(self, sql: str):
        print("SQL: ", sql)
        self.cur.execute(sql)
        self.conn.commit()
        print(self.result())

    def result(self):
        try:
            return self.cur.fetchall()
        except psycopg.ProgrammingError as e:
            return e

    def close(self):
        self.cur.close()
        self.conn.close()


def main():
    db = PostGresDB(sys.argv[1], "Payroll")
    db.exec(Query.DELETE(Entity.STATE, "state_name='bongoState'"))
    db.exec(Query.CREATE(Entity.STATE, "bongoStated", "456"))
    db.exec(Query.UPDATE(Entity.STATE, "state_name='bongoStated'", "tax_rate=753.12"))
    db.close()


main()