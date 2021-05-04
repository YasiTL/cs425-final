import sys
from postGres import PostGresDB, Query, Entity, Multivalue, Relation
from signIn import signIn


def main():
    if len(sys.argv) < 2:
        exit("No ip given as argument")

    db = PostGresDB(sys.argv[1], "Payroll")
    auth = signIn(db)
    
    auth.signIn("Yasi", 1234567)
    
    print(auth.getTitle())


main()