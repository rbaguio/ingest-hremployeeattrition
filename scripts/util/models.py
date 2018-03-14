from util.initialize_data import *
import numpy as np


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
    department = ''
    subdepartment = ''
    joblevel = ''
    jobrole = ''
    promotion_date = ''
    hiring_date = ''

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
        self.department = kwargs.get('department', None)
        self.subdepartment = kwargs.get('subdepartment', None)
        self.joblevel = kwargs.get('joblevel', None)
        self.jobrole = kwargs.get('jobrole', None)
        self.hierarchy = int(roles_summary.loc[
            (roles_summary['department'] == self.department) &
            (roles_summary['jobrole'] == self.jobrole)
        ]['hierarchy'].unique())
        self.promotion_date = kwargs.get('promotion_date', None)
        self.hiring_date = kwargs.get('hiring_date', None)

    def demote(self):
        if self.joblevel == 1:
            print("Can't be demoted. You prick!")
        else:
            key = transition_dir[self.department][self.subdepartment]
            transition_mat = transition_dict[key]
            demoted_text = np.random.choice(
                a=transition_mat.index.tolist(),
                p=transition_mat[self.roleid].values.tolist()
            )

            demoted_role = roles_summary.loc[
                roles_summary['roleid'] == demoted_text
            ]

            self.department = demoted_role.department.values[0]
            self.jobrole = demoted_role.jobrole.values[0]
            self.joblevel = demoted_role.joblevel.values[0]
            self.roleid = demoted_role.roleid.values[0]
            self.hierarchy = demoted_role.hierarchy.values[0]
            self.subdepartment = demoted_role.subdepartment.values[0]


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
