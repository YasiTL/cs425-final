from postGres import Query, Entity, Multivalue, Relation, DataType
import postGres as DB

currentTitle = None


def signIn(first_name: str, e_id: str):
    global currentTitle
    """ Sign in given first name and e_id of employee """
    DB.execute(Query.SELECT_WHERE(Entity.EMPLOYEE, "first_name='{}' and e_id='{}'".format(first_name, e_id), "job_title"))
    try:
        currentTitle = DataType.JobTitle(DB.result()[0][0])
    except IndexError:
        currentTitle = None


def signOut():
    global currentTitle
    """ Sign out """
    currentTitle = None


def getTitle():
    global currentTitle
    """Get the title of who is currently signed in, used for getting access level

    Returns `None` if employee does not exist, or no one is signed in
    """
    return currentTitle