from util.initialize_data import *
import numpy as np
import pandas as pd

np.random.seed(seed)

department_dict = {
    'Sls': 'Sales',
    'R&D': 'Research & Development',
    'HmR': 'Human Resources',
}

role_dict = {
    'hmnr': 'Human Resources',
    'mngr': 'Manager',
    'lbrt': 'Laboratory Technician',
    'rsrs': 'Research Scientist',
    'hltr': 'Healthcare Representative',
    'mnfd': 'Manufacturing Director',
    'rsrd': 'Research Director',
    'slsr': 'Sales Representative',
    'slse': 'Sales Executive',
}


class Actions:
    date = ''
    actions_id = ''
    supervisornumber = ''
    employeenumber = ''
    salary = ''
    roleto = ''
    rolefrom = ''
    joblevelto = ''
    joblevelfrom = ''
    department = ''
    action_type = ''

    def __init__(self, *args, **kwargs):
        self.date = ''
        self.actions_id = ''
        self.supervisornumber = ''
        self.employeenumber = ''
        self.salary = ''
        self.roleto = ''
        self.rolefrom = ''
        self.joblevelto = ''
        self.joblevelfrom = ''
        self.department = ''
        self.action_type = ''

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
    def __init__(self, *args, **kwargs):
        self.employeenumber = ''
        self.gender = ''
        self.age = ''
        self.maritalstatus = ''
        self.education = ''
        self.educationfield = ''
        self.numcompaniesworked = ''
        self.priorworkxp = ''
        self.monthlyincome = ''
        self.stockoptionlevel = ''
        self.yearsatcompany = ''
        self.yearsincurrentrole = ''
        self.yearssincelastpromotion = ''
        self.yearswithcurrmanager = ''
        self.separated = ''
        self.salaryhike = ''
        self.roleid = ''
        self.department = ''
        self.subdepartment = ''
        self.joblevel = ''
        self.jobrole = ''
        self.promotion_date = ''
        self.hiring_date = ''
        self.termination_date = ''
        self.hierarchy = ''

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

            return pd.Series()
        else:
            key = transition_dir[self.department][self.subdepartment]
            transition_mat = transition_dict[key]

            if sum(transition_mat[self.roleid].values.tolist()) == 1:
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
                    roleto=self.jobrole,
                    rolefrom=demoted_role.jobrole.values[0],
                    joblevelto=self.joblevel,
                    joblevelfrom=demoted_role.joblevel.values[0],
                    department=self.department,
                    salary=self.salaryhike,
                    action_type='promotion'
                )

                self.department = demoted_role.department.values[0]
                self.jobrole = demoted_role.jobrole.values[0]
                self.joblevel = demoted_role.joblevel.values[0]
                self.roleid = demoted_role.roleid.values[0]
                self.hierarchy = demoted_role.hierarchy.values[0]
                self.subdepartment = demoted_role.subdepartment.values[0]
                self.salaryhike = random_salaryhike(demoted_role)

                return demotion_action.to_series()
            else:
                return pd.Series()

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
            srs = self.demote(date)
            if not srs.empty:
                srs_list.append(srs)

        # print(srs_list)
        return pd.DataFrame(srs_list)

    def randomize(self, df=e_records_df, yearsfrom=2017):
        for key in df.columns:
            if key not in ['hiring_date', 'termination_date', 'promotion_date', 'department', 'subdepartment', 'jobrole', 'joblevel', 'hierarchy']:
                if hasattr(self, key):
                    setattr(self, key, np.random.choice(
                        a=df[key].value_counts(
                            normalize=True).sort_index().index,
                        p=df[key].value_counts(
                            normalize=True).sort_index().values
                    ))

        self.hiring_date = get_relative_date(
            self.yearsatcompany,
            date(yearsfrom, 12, 31)
        )

        role_id_split = self.roleid.split('-')

        self.department = department_dict[role_id_split[0]]
        self.joblevel = int(role_id_split[1])
        self.jobrole = role_dict[role_id_split[2]]
        self.subdepartment = subdepartment_dict[(self.department, self.jobrole)]
        self.hierarchy = hierarchy_dict[(self.department, self.jobrole)]
        self.termination_date = randomize_termination(
            self.hiring_date,
            yearsfrom
        )

        print(self.hiring_date)
        print(self.termination_date)

        print('An Employee was just randomly generated!')
        if self.termination_date < self.hiring_date:
            input('ERROR!!!')

        return self

    def to_series(self):
        return pd.Series({key: value for key, value in self.__dict__.items()})
