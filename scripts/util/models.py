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

    def demote(self, date_promoted):
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
            ].reset_index(drop=True)

            def random_salaryhike(role):
                dist = salary_hike_dist[(
                    role.department.values[0],
                    role.joblevel.values[0]
                )]

                return np.random.choice(dist.index, p=dist.values)

            demotion_action = Actions(
                date=date_promoted,
                employeenumber=self.employeenumber,
                roleto=demoted_role.jobrole.values[0],
                rolefrom=self.jobrole,
                department=self.department,
                salary=self.salaryhike
            )

            self.department = demoted_role.department.values[0]
            self.jobrole = demoted_role.jobrole.values[0]
            self.joblevel = demoted_role.joblevel.values[0]
            self.roleid = demoted_role.roleid.values[0]
            self.hierarchy = demoted_role.hierarchy.values[0]
            self.subdepartment = demoted_role.subdepartment.values[0]
            self.salaryhike = random_salaryhike(demoted_role)

            return demotion_action.to_series()

    def demote_n(self, date_promoted, times):
        if type(date_promoted) is not list:
            raise AssertionError('date_promoted should be a list.')
        if type(times) is not int:
            raise AssertionError('Times should be an integer.')
        if len(date_promoted) != times:
            raise AssertionError(
                'number of promotion dates should be equal to ' +
                'number of promotions.'
            )

        if times > 5:
            raise AssertionError(
                'cannot be promoted more than 5 times.'
            )

        if times < 0:
            raise AssertionError(
                'cannot be negatively demoted/promoted.'
            )
        srs_list = []
        for i, date in zip(range(times), date_promoted):
            srs_list.append(self.demote(date))
        return pd.DataFrame(srs_list)
