import sys
from postGres import PostGresDB, Query, Entity, Multivalue, Relation


def main():
    if len(sys.argv) < 2:
        exit("No ip given as argument")

    db = PostGresDB(sys.argv[1], "Payroll")
    # db.exec(Query.DELETE(Entity.STATE, "state_name='bongoStated'"))
    # db.exec(Query.DELETE(Entity.STATE, "state_name='bongoStated'"))
    # db.exec(Query.CREATE(Entity.STATE, "bongoStated", "456"))
    # db.exec(Query.UPDATE(Entity.STATE, "state_name='bongoStated'", "tax_rate=753.12"))
    db.exec(Query.SELECT(Entity.INSURNACE_PLAN, "*"))
    print(db.result()) #returns python object, a list
    # db.exec(Query.SELECT(Entity.EMPLOYEE, "first_name", "last_name", "job_title"))
    # db.exec(Query.CREATE(Entity.EMPLOYEE, "yes", "bomb", "job_title"))
    db.close()
    #figure out sql statement for report?


main()