from util.initialize_data import transition_dir, transition_dict,\
    roles_summary, salary_hike_dist, e_records_df

import numpy as np
import pandas as pd

np.random.seed(2000)


class Actions:
    date = ''
    actions_id = ''
    supervisornumber = ''
    employeenumber = ''
    salary = ''
    roleto = ''
    rolefrom = ''
    department = ''

    def __init__(self, *args, **kwargs):
        for dict in args:
            for key in dict:
                if hasattr(self, key):
                    setattr(self, key, dict[key])
                else:
                    raise KeyError(
                        f'Actions class does not have a/an {key} attribute.'
                    )

        for key in kwargs:
                if hasattr(self, key):
                    setattr(self, key, kwargs[key])
                else:
                    raise KeyError(
                        f'Actions class does not have a/an {key} attribute.'
                    )

    def to_series(self):
        return pd.Series({key: value for key, value in self.__dict__.items()})


# class Hiring(Actions):


# class Termination(Actions):


# class Promotion(Actions):


# class Transfer(Actions):


class Requests:
    request_id = ''
    employee_id = ''
    role = ''
    requested = ''


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

    def __init__(self, *args, **kwargs):
        for dict in args:
            for key in dict:
                if hasattr(self, key):
                    setattr(self, key, dict[key])
                else:
                    raise KeyError(
                        f'Employee class does not have a/an {key} attribute.'
                    )

        for key in kwargs:
                if hasattr(self, key):
                    setattr(self, key, kwargs[key])
                else:
                    raise KeyError(
                        f'Employee class does not have a/an {key} attribute.'
                    )

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


