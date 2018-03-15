from util.initialize_data import *
import numpy as np

np.random.seed(2000)


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
    hierarchy = ''

    def __init__(self, *dat, **kwargs):
        for dict in dat:
            for key in dict:
                setattr(self, key, dict[key])

        for key in kwargs:
            setattr(self, key, kwargs[key])

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
