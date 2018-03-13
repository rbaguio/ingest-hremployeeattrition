class Employee:
    employeenumber = ''
    gender = ''
    age = ''
    maritalstatus = ''
    education = ''
    educationfield = ''
    numcompaniesworked = ''
    priorworkxp = ''
    monthlyincome = ''
    stockoptionlevel = ''
    yearsatcompany = ''
    yearsincurrentrole = ''
    yearssincelastpromotion = ''
    yearswithcurrmanager = ''
    separated = ''
    salaryhike = ''
    roleid = ''

    def __init__(self, **kwargs):
        self.employeenumber = kwargs.get('employeenumber', None)
        self.gender = kwargs.get('gender', None)
        self.age = kwargs.get('age', None)
        self.maritalstatus = kwargs.get('maritalstatus', None)
        self.education = kwargs.get('education', None)
        self.educationfield = kwargs.get('educationfield', None)
        self.numcompaniesworked = kwargs.get('numcompaniesworked', None)
        self.priorworkxp = kwargs.get('priorworkxp', None)
        self.monthlyincome = kwargs.get('monthlyincome', None)
        self.stockoptionlevel = kwargs.get('stockoptionlevel', None)
        self.yearsatcompany = kwargs.get('yearsatcompany', None)
        self.yearsincurrentrole = kwargs.get('yearsincurrentrole', None)
        self.yearssincelastpromotion = kwargs.get(
            'yearssincelastpromotion',
            None
        )
        self.yearswithcurrmanager = kwargs.get('yearswithcurrmanager', None)
        self.separated = kwargs.get('separated', None)
        self.salaryhike = kwargs.get('salaryhike', None)
        self.roleid = kwargs.get('roleid', None)


class Actions:
    date = ''
    actions_id = ''
    report_employee_id = ''
    salary = ''
    role = ''
    department = ''

    def __init__(self):
        None


# class Hiring(Actions):


# class Termination(Actions):


# class Promotion(Actions):


# class Transfer(Actions):


class Requests:
    request_id = ''
    employee_id = ''
    role = ''
    requested = ''
