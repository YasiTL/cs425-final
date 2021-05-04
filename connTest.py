import sys
from postGres import Query, Entity, Multivalue, Relation
import postGres as DB


def main():
    if len(sys.argv) < 2:
        exit("No ip given as argument")

    DB.connect(sys.argv[1], "Payroll")
    # DB.execute(Query.DELETE(Entity.STATE, "state_name='bongoStated'"))
    # DB.execute(Query.DELETE(Entity.STATE, "state_name='bongoStated'"))
    # DB.execute(Query.CREATE(Entity.STATE, "bongoStated", "456"))
    # DB.execute(Query.UPDATE(Entity.STATE, "state_name='bongoStated'", "tax_rate=753.12"))
    DB.execute(Query.SELECT(Entity.INSURNACE_PLAN, "*"))
    print(DB.result())  # returns python object, a list
    # DB.execute(Query.SELECT(Entity.EMPLOYEE, "first_name", "last_name", "job_title"))
    # DB.execute(Query.CREATE(Entity.EMPLOYEE, "yes", "bomb", "job_title"))
    DB.close()
    # figure out sql statement for report?


main()