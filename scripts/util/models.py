from util.initialize_data import roles_summary
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
        ]['hierarchy'])
        self.promotion_date = kwargs.get('promotion_date', None)
        self.hiring_date = kwargs.get('hiring_date', None)

    def demote(self):
        deducted_level = self.joblevel - 1
        df = roles_summary.loc[
            (roles_summary['min'] <= deducted_level) &
            (roles_summary['max'] >= deducted_level) &
            (roles_summary['subdepartment'] == self.subdepartment) &
            (roles_summary['department'] == self.department) &
            (roles_summary['hierarchy'] <= self.hierarchy)
        ]

        total = sum(df['jobrole'] != self.jobrole)

        def compute_probability(row):
            if self.joblevel == 5:
                if row['jobrole'] == self.jobrole:
                        return 0.9
                else:
                        return 0.1 / total

            else:
                if row['jobrole'] == self.jobrole:
                        return 0.8
                else:
                        return 0.2 / total

        return df



        return df

    def max_promotions(self):
        current_role_min = roles_summary.loc[
            (roles_summary['department'] == self.department) &
            (roles_summary['jobrole'] == self.jobrole)
        ]['min']

        previous_promotion = sum(
            roles_summary.loc[
                (roles_summary['Department'] == self.department) &
                (roles_summary['hierarchy'] < self.hierarchy)
            ]['max']
        )

        print(self.joblevel)
        print(current_role_promotion)
        print(previous_promotion)

        return int(current_role_promotion + previous_promotion)


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
