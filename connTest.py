import psycopg2 as psycopg  # pip install psycopg2-binary
import base64
import sys
from enum import Enum


class Entity(Enum):
    STATE = ("state_t", "state_name, tax_rate")
    INSURNACE_PLAN = ("insurancePlan_t", "plan_id, employee_cost_for_individualPlan, employee_cost_for_familyPlan, employer_cost_for_indivudal, employer_cost_for_family")
    EMPLOYEE = ("employee_t", "e_id, first_name, last_name, ssn, job_title, salary_type, insurancePlan, email, country, state, street_name, postal_code, F01k_deduction")

class Query(Enum):
    CREATE = "insert into {0}({1}) values {2};"
    # UPDATE = "update {0} set {2} where {3} returning *;"


class PostGresDB:
    conn = cur = None

    def __init__(self, ip: str, schema: str):
        print("Connecting to postgres@{}".format(ip))
        self.conn = psycopg.connect(host=ip, database="postgres", user="postgres", password="postgres")
        self.cur = self.conn.cursor()
        self.cur.execute("set schema '{}'".format(schema))

    def exec(self, sql: str):
        self.cur.execute(sql)
        self.conn.commit()

    def result(self):
        try:
            return self.cur.fetchall()
        except psycopg.ProgrammingError as e:
            return e

    def runQuery(self, query: Query, entity: Entity, *args):
        sql = query.value.format(entity.value[0], entity.value[1], str(args))
        print("SQL: ", sql)
        self.exec(sql)
        print(db.result())

    def close(self):
        self.cur.close()
        self.conn.close()


def main():
    db = PostGresDB(sys.argv[1], "Payroll")
    db.runQuery(Query.CREATE, Entity.EMPLOYEE, 'TestID2', 'boi', 'Smith', 4201337, 'ADMIN', 'HOURLY', 'basic health', 'TechYeah@iit.edu', 'Albania', 'Illinois', 'Main Street', 1808, 25.45)
    # db.runQuery(Query.UPDATE, Entity.EMPLOYEE, )
    db.close()


main()