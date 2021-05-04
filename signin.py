from postGres import PostGresDB, Query, Entity, Multivalue, Relation, DataType


class signIn:

    jobTitle = DataType.JobTitle
    db = PostGresDB

    def __init__(self, database: PostGresDB):
        self.db = database
        self.jobTitle = None

    def signIn(self, first_name: str, e_id: str):
        """ Sign in given first name and e_id of employee """
        self.db.exec(Query.SELECT_WHERE(Entity.EMPLOYEE, "first_name='{}' and e_id='{}'".format(first_name, e_id), "job_title"))
        try:
            self.jobTitle = DataType.JobTitle(self.db.result()[0][0])
        except IndexError:
            self.jobTitle = None

    def signOut(self):
        """ Sign out """
        self.jobTitle = None

    def getTitle(self):
        """Get the title of who is currently signed in, used for getting access level
        
        Returns `None` if employee does not exist, or no one is signed in
        """
        return self.jobTitle