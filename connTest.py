import psycopg2 as psycopg  # pip install psycopg2-binary
import base64
import sys
from enum import Enum


class Entity(Enum):
    STATE = "state_t"
    EMPLOYEE = "employee_t"
    INSURNACE_PLAN = "insurancePlan_t"


class Query(Enum):
    CREATE = "insert into {}(state_name, tax_rate) values ('test2', 144);"


class PostGresDB:
    conn = cur = None

    def __init__(self, ip: str, schema: str):
        print("Connecting to postgres@{}".format(ip))
        self.conn = psycopg.connect(host=ip, database="postgres", user="postgres", password="postgres")
        self.cur = self.conn.cursor()
        self.cur.execute("set schema '{}'".format(schema))

    def exec(self, sql: str):
        self.cur.execute(sql)

    def result(self):
        return self.cur.fetchall()

    def runQuery(self, query: Query, entity: Entity):
        self.exec(query.value.format(entity.value))


def main():
    db = PostGresDB(sys.argv[1], "Payroll")
    db.runQuery(Query.CREATE, Entity.EMPLOYEE)
    print(db.result())


main()