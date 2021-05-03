from postGres import PostGresDB, Query, Entity, Multivalue, Relation, DataType


class signIn:

    jobTitle = DataType.JobTitle
    db = PostGresDB

    def __init__(self, database: PostGresDB):
        self.db = database
        self.jobTitle = None

    def signIn(self, id: str):
        self.db.exec(Query.SELECT_WHERE(Entity.EMPLOYEE, "e_id='{}'".format(id)))

    def signOut(self):
        self.jobTitle = None

    def getTitle(self):
        return self.jobTitle