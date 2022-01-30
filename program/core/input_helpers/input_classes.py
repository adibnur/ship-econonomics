import pandas as pd
from math import ceil
from . import key_match_helpers

class staff_salary:
    def __init__(self, df_dir, sheet_name, yearly_bonus_in_months=2):
        self.df = pd.read_excel(df_dir, sheet_name)
        self.df = key_match_helpers.staff_salary_matcher(self.df)

        self.df['Annual Salary (BDT in lac)'] = self.df['No. of Persons'] * self.df['Monthly Salary (in BDT)'] * 12 / 10**5
        self.salary_sub_total = self.df['Annual Salary (BDT in lac)'].sum()
        self.festival_bonus = self.salary_sub_total / 6
        self.total = self.salary_sub_total + self.festival_bonus

class technical_inputs:
    def __init__(self, df_dir):
        self.df_revenue = pd.read_excel(df_dir, sheet_name='Revenue Earnings')
        self.df_revenue['Yearly Revenue (BDT in Lac)'] = (self.df_revenue['Number of Trip / Month'] * 12
            * self.df_revenue['Vessel carrying capacity (MT)'] * self.df_revenue['Freight Charge / MT (BDT)']
            * self.df_revenue['No. of vessels'] * 2 / 100000)

        self.df_service_mat = pd.read_excel(df_dir, sheet_name='Service Materials')
        self.df_service_mat['Cost per Year (BDT in Lac)'] = self.df_service_mat['Cost per Month'] * 12 / (10**5)

        self.df_equipment = pd.read_excel(df_dir, sheet_name='Equipment Cost')
        self.df_equipment['Total Cost (BDT in Lac)'] = self.df_equipment['Unit Cost (BDT in Lac)'] * self.df_equipment['No. of Units']

        self.df_misc = pd.read_excel(df_dir, sheet_name='Misc. Cost')
        self.df_misc['Yearly Cost (BDT in lac)'] = self.df_misc['Monthly Cost (in BDT)'] * 12 / (10**5)

        self.df_expenses = pd.read_excel(df_dir, sheet_name='Expenses')

class financial_assumptions:
    def __init__(self, df_dir):
        self.df = pd.read_excel(df_dir, sheet_name='Economic Assumptuions')
        self.df = self.df.set_index('Description')

        self.days_of_operation = self.df.loc['Days of Operation Per Year (days)', 'Value']

        self.capacity_util_1st = self.df.loc['Capacity Utilization', 'Value']
        self.capacity_util_incr = self.df.loc['Capacity Utilization', 'Unnamed: 3']
        self.capacity_util_max = self.df.loc['Capacity Utilization', 'Unnamed: 4']

        self.stock_work_in_process = 3

        self.wage_incr = self.df.loc['Annual Increment of wages and salaries', 'Value']

        self.depreciation_rate = self.df.loc['Depreciation rates in straight line method', 'Value']

        self.loan_period = self.df.loc['Total Loan Period (Years)', 'Value']

        self.interest_rate = self.df.loc['Interest on Capital Loan', 'Value']

        self.construction_period = self.df.loc['Construction Period (months)', 'Value']

        self.grace_period = self.df.loc['Grace Period (months)', 'Value']

        self.freq_installments = self.df.loc['Frequency of Installments (months)', 'Value']

        self.num_installments_IDCP = self.df.loc['Total Number of Installments for Interest During Grace Period', 'Value']

        # calculated. Can be taken as input, but doesn't seem necessary at the moment
        #self.num_installments_principal = self.df.loc['Total Number of Installments for Principal Loan', 'Value']
        self.num_installments_principal =  (self.loan_period * 12 - (self.construction_period + self.grace_period)) / self.freq_installments

        #should we keep this as input?
        self.rate_of_revenue_expenditure = self.df.loc['Rate of Revenue Expenditure', 'Value']

        #remove this from inputs. formula = preliminary expenses * 1.88 / 20 (verify)
        self.ammortization_of_prel = 1.88

        self.debt_equity = {'Debt' : self.df.loc['Debt : Equity Ratio', 'Value'],
                            'Equity' : self.df.loc['Debt : Equity Ratio', 'Unnamed: 3']}

        # calculated. not for input
        self.report_lenght_years = self.loan_period - (self.construction_period + self.grace_period) / 12
        self.report_lenght_years = ceil(self.report_lenght_years)


    def __repr__(self):
        return '\n'.join([f'{i} : {self.__dict__[i]}' for i in self.__dict__.keys() if i!='df'])
