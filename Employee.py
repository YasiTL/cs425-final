from postGres import Query, Entity, Multivalue, Relation, DataType
import postGres as DB


class Employee:

    badSetup = False

    exists = False

    e_id = None
    first_name = None
    last_name = None
    ssn = None
    job_title = None
    salary_type = None
    insurancePlan = None
    email = None
    country = None
    state = None
    street_name = None
    postal_code = None
    F01k_deduction = None

    Dependents = set()
    PhoneNumbers = set()
    Benefits = set()

    def __init__(
        self,
        e_id: str,
        first_name: str = None,
        last_name: str = None,
        ssn: str = None,
        job_title: DataType.JobTitle = None,
        salary_type: DataType.Salary = None,
        insurancePlan: str = None,
        email: str = None,
        country: str = None,
        state: str = None,
        street_name: str = None,
        postal_code: int = None,
        F01k_deduction: int = None,
    ):
        """ Initialize a new Employee to be created or updated"""
        self.e_id = e_id
        DB.execute(Query.SELECT_WHERE(Entity.EMPLOYEE, "e_id='{}'".format(e_id), "*"))
        self.exists = DB.result()

        if self.exists and first_name:
            print("Warning: Employee already exists but options parameters were still passed")

        if not self.exists:
            if (
                not first_name
                or not last_name
                or not ssn
                or not job_title
                or not salary_type
                or not insurancePlan
                or not email
                or not country
                or not state
                or not street_name
                or not postal_code
                or not F01k_deduction
            ):
                print("Employee does not exist")
                self.badSetup = True
                return
            self.first_name = first_name
            self.last_name = last_name
            self.ssn = ssn
            self.job_title = job_title.value
            self.salary_type = salary_type.value
            self.insurancePlan = insurancePlan
            self.email = email
            self.country = country
            self.state = state
            self.street_name = street_name
            self.postal_code = postal_code
            self.F01k_deduction = F01k_deduction
        else:
            print("Employee found")
            self.exists = self.exists[0]
            self.first_name = self.exists[1]
            self.last_name = self.exists[2]
            self.ssn = self.exists[3]
            self.job_title = self.exists[4]
            self.salary_type = self.exists[5]
            self.insurancePlan = self.exists[6]
            self.email = self.exists[7]
            self.country = self.exists[8]
            self.state = self.exists[9]
            self.street_name = self.exists[10]
            self.postal_code = self.exists[11]
            self.F01k_deduction = self.exists[12]

        DB.execute(Query.FIND(Entity.STATE, self.state))
        found = DB.result()
        if not found:
            print("Employee State {} not found".format(self.state))
            self.badSetup = True

        DB.execute(Query.FIND(Entity.INSURNACE_PLAN, self.insurancePlan))
        found = DB.result()
        if not found:
            print("Employee State {} not found".format(self.insurancePlan))
            self.badSetup = True

        if self.badSetup:
            return

        DB.execute(Query.FIND(Relation.HAS, self.e_id))
        self.Dependents = DB.result()

        DB.execute(Query.FIND(Multivalue.EMPLOYEE_PHONE, self.e_id))
        self.PhoneNumbers = DB.result()

        DB.execute(Query.FIND(Multivalue.EMPLOYEE_BENEFIT_SELECTION, self.e_id))
        self.Benefits = DB.result()

    def addDependent(self, d_id: str):
        self.Dependents.add(d_id)

    def addPhoneNumber(self, phoneNum: int):
        self.PhoneNumbers.add(phoneNum)

    def addBenefit(self, benefit: DataType.BenefitSelection):
        self.Benefits.add(benefit)

    def removeDependent(self, d_id: str):
        try:
            self.Dependents.remove(d_id)
        except KeyError:
            pass

    def removePhoneNumber(self, phoneNum: int):
        try:
            self.PhoneNumbers.remove(phoneNum)
        except KeyError:
            pass

    def removeBenefit(self, benefit: DataType.BenefitSelection):
        try:
            self.Benefits.remove(benefit)
        except KeyError:
            pass

    def create(self):
        if self.exists:
            print("Employee already created, did you mean to update?")
            return
        DB.execute(
            Query.CREATE(
                Entity.EMPLOYEE,
                self.e_id,
                self.first_name,
                self.last_name,
                self.ssn,
                self.job_title,
                self.salary_type,
                self.insurancePlan,
                self.email,
                self.country,
                self.state,
                self.street_name,
                self.postal_code,
                self.F01k_deduction,
            )
        )

        if DB.result():
            print("Created employee {}".format(self.e_id))

        for d in self.Dependents:
            DB.execute(Query.CREATE(Relation.HAS, self.e_id, d))

        for p in self.PhoneNumbers:
            DB.execute(Query.CREATE(Multivalue.EMPLOYEE_PHONE, self.e_id, p))

        for b in self.Benefits:
            DB.execute(Query.CREATE(Multivalue.EMPLOYEE_BENEFIT_SELECTION, self.e_id, b))

    def update(self):
        if not self.exists:
            print("Employee does not exist yet, did you mean to create?")
            return
        self.first_name = "first_name='{}'".format(self.first_name)
        self.last_name = "last_name='{}'".format(self.last_name)
        self.ssn = "ssn='{}'".format(self.ssn)
        self.job_title = "job_title='{}'".format(self.job_title)
        self.salary_type = "salary_type='{}'".format(self.salary_type)
        self.insurancePlan = "insurancePlan='{}'".format(self.insurancePlan)
        self.email = "email='{}'".format(self.email)
        self.country = "country='{}'".format(self.country)
        self.state = "state='{}'".format(self.state)
        self.street_name = "street_name='{}'".format(self.street_name)
        self.postal_code = "postal_code='{}'".format(self.postal_code)
        self.F01k_deduction = "F01k_deduction='{}'".format(self.F01k_deduction)
        DB.execute(
            Query.UPDATE_SINGLE(
                Entity.EMPLOYEE,
                self.e_id,
                self.first_name,
                self.last_name,
                self.ssn,
                self.job_title,
                self.salary_type,
                self.insurancePlan,
                self.email,
                self.country,
                self.state,
                self.street_name,
                self.postal_code,
                self.F01k_deduction,
            )
        )

        # for d in self.Dependents:
        #     DB.execute(Query.CREATE(Relation.HAS, self.e_id, d))

        # for p in self.PhoneNumbers:
        #     DB.execute(Query.CREATE(Multivalue.EMPLOYEE_PHONE, self.e_id, p))

        # for b in self.Benefits:
        #     DB.execute(Query.CREATE(Multivalue.EMPLOYEE_BENEFIT_SELECTION, self.e_id, b))
