import sys
from postGres import PostGresDB, Query, Entity


def main():
    db = PostGresDB(sys.argv[1], "Payroll")
    db.exec(Query.DELETE(Entity.STATE, "state_name='bongoStated'"))
    db.exec(Query.CREATE(Entity.STATE, "bongoStated", "456"))
    db.exec(Query.UPDATE(Entity.STATE, "state_name='bongoStated'", "tax_rate=753.12"))
    db.exec(Query.SELECT(Entity.STATE, "*"))
    db.exec(Query.SELECT(Entity.EMPLOYEE, "first_name", "last_name", "job_title"))
    db.close()


main()