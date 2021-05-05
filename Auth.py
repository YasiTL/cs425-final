from postGres import Query, Entity, Multivalue, Relation, DataType
import postGres as DB

currentTitle = None
currentUser = None


def signIn(first_name: str, e_id: str):
    global currentTitle, currentUser
    """ Sign in given first name and e_id of employee """
    DB.execute(Query.SELECT_WHERE(Entity.EMPLOYEE, "first_name='{}' and e_id='{}'".format(first_name, e_id), "job_title"))
    try:
        currentTitle = DataType.JobTitle(DB.result()[0][0])
        currentUser = first_name
        if currentTitle:
            print("{} Signed in as {}".format(currentUser, currentTitle.value))
    except IndexError:
        print("Failed to Sign In")
        currentTitle = None
        currentUser = None


def signOut():
    global currentTitle, currentUser
    """ Sign out """
    print("{} Signed out".format(currentUser))
    currentTitle = None
    currentUser = None


def getUser():
    global currentTitle, currentUser
    """Get the name of who is currently signed in

    Returns `None` if no one is signed in
    """
    
    return currentUser

def getTitle():
    global currentTitle, currentUser
    """Get the title of who is currently signed in, used for getting access level

    Returns `None` if employee does not exist, or no one is signed in
    """
    return currentTitle