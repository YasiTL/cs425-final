from postGres import Query, Entity, Multivalue, Relation, DataType
import postGres as DB
from Log import log


class Dependent:

    ID = "Dependent"

    badSetup = False
    exists = False

    d_id = None
    first_name = None
    last_name = None
    ssn = None
    benefitSelection = None

    def __init__(
        self,
        d_id: str = None,
        first_name: str = None,
        last_name: str = None,
        ssn: str = None,
        benefitSelection: DataType.BenefitSelection = None,
    ):
        """ Initialize a new Dependent to be created or updated"""
        self.d_id = d_id
        DB.execute(Query.SELECT_WHERE(Entity.DEPENDENT, "d_id='{}'".format(d_id), "*"))
        self.exists = DB.result()
        if self.exists != None:
            if len(self.exists) == 0:
                self.exists = None

        if self.exists and first_name:
            log(self.ID, "Warning: Dependent already exists but options parameters were still passed")

        if not self.exists:
            if not d_id or not first_name or not last_name or not ssn or not benefitSelection:
                log(self.ID, "Dependent does not exist")
                self.badSetup = True
                self.exists = False
                return
            self.d_id = d_id
            self.first_name = first_name
            self.last_name = last_name
            self.ssn = ssn
            self.benefitSelection = benefitSelection.value
        else:
            log(self.ID, "Dependent found")
            self.exists = self.exists[0]
            self.first_name = self.exists[1]
            self.last_name = self.exists[2]
            self.ssn = self.exists[3]
            self.benefitSelection = self.exists[4]

        self.normalize()

        if self.badSetup:
            return

    def normalize(self):
        try:
            self.d_id = str(self.d_id)
            self.first_name = str(self.first_name)
            self.last_name = str(self.last_name)
            self.ssn = str(self.ssn)
            self.benefitSelection = str(self.benefitSelection)
        except:
            log(self.ID, "Failed to normalize Employee values")
            self.exists = False
            self.badSetup = True

    def create(self):
        self.normalize()
        if self.badSetup:
            log(self.ID, "Dependent is invalid")
            return
        if self.exists:
            log(self.ID, "Dependent already created, did you mean to update?")
            return
        DB.execute(Query.CREATE(Entity.DEPENDENT, self.d_id, self.first_name, self.last_name, self.ssn, self.benefitSelection))

        if DB.result():
            log(self.ID, "Created Dependent {}".format(self.d_id))

    def toString(self):
        if self.badSetup:
            log(self.ID, "Dependent is invalid")
            return
        return "{} {} | dID:{}".format(self.first_name, self.last_name, self.d_id)

    def update(self):
        self.normalize()
        if self.badSetup:
            log(self.ID, "Dependent is invalid")
            return
        if not self.exists:
            log(self.ID, "Dependent does not exist yet, did you mean to create?")
            return
        _first_name = "first_name='{}'".format(self.first_name)
        _last_name = "last_name='{}'".format(self.last_name)
        _ssn = "ssn='{}'".format(self.ssn)
        _benefitSelection = "benefitSelection='{}'".format(self.benefitSelection)
        DB.execute(Query.UPDATE_SINGLE(Entity.DEPENDENT, self.d_id, _first_name, _last_name, _ssn, _benefitSelection))
