import psycopg2 as psycopg  # pip install psycopg2-binary
import base64
import sys


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


def main():
    db = PostGresDB(sys.argv[1], "Payroll")
    db.exec("select * from state_t")

    print(db.result())


main()