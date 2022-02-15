import pandas as pd
import numpy as np
from .revenue_earnings_estimate import revenue_earnings
from .est_income_statement import est_income_statement
from .overhead_depreciation import overhead_depreciation

class break_even_analysis:
    def __init__(self, inp_flow):
        income_statement = est_income_statement(inp_flow)
        rev_ear = revenue_earnings(inp_flow)
        ovh_depr = overhead_depreciation(inp_flow)

        # capacity utilization
        self.cap_util = income_statement.cap_util

        # Total revenue
        self.revenue = income_statement.revenue


        ## Variable cost
        #Service materials
        self.service_mat = income_statement.service_mat

        #Operating staff
        self.operating_staff = income_statement.operating_staff

        # Revenue expenses
        self.revenue_expense = rev_ear.revenue_expense

        # Spares and stores
        self.spares_and_stores = ovh_depr.stores_and_spares

        # Utilities
        self.utilities = ovh_depr.utilities

        # Total (Variable cost)
        self.total_variable_cost = (self.service_mat + self.operating_staff + self.revenue_expense +
                                    self.spares_and_stores + self.utilities)

        # Table - Variable cost
        self.table_var_cost = self.get_table_var_cost(inp_flow)


        ## Fixed cost
        # Depreciation & amortization
        self.depr_ammor = ovh_depr.table_depreciation.sum().to_numpy() + inp_flow.financial_assumptions.ammortization_of_prel

        # Administrative expenses
        self.admin_expense = rev_ear.admin_expense

        # Financial expenses (Interest on long & short debt)
        self.interest_long_short = income_statement.interest_long_short

        # Total (Fixed cost)
        self.total_fixed_cost = self.depr_ammor + self.admin_expense + self.interest_long_short

        # Table - Fixed cost
        self.table_fixed_cost = self.get_table_fixed_cost(inp_flow)


        ## Annual regulated cost
        # General expense
        self.general_expense = self.get_total_general_expenses(inp_flow)

        # Repair & maintenance
        self.repair_maintenance = ovh_depr.get_maintenance_vessel(inp_flow)

        # Total (Annual regulated cost)
        self.total_annual_reg_cost = np.array(self.general_expense) + np.array(self.repair_maintenance)

        # Table - Annual regulated cost
        self.table_annual_reg_cost = self.get_table_annual_reg_cost(inp_flow)


        ## Break-Even Calculation
        # Total fixed cost
        self.BE_total_fixed_cost = self.total_fixed_cost + self.total_annual_reg_cost / 2

        # Total variable cost
        self.BE_total_variable_cost = self.total_variable_cost + self.total_annual_reg_cost / 2

        # Break-even revenue
        self.BE_revenue = (self.BE_total_fixed_cost * self.revenue) / (self.revenue - self.BE_total_variable_cost)

        # Break-even capacity (assumed)
        self.BE_capacity_assumed = (self.BE_revenue / self.revenue) * 100

        # Break-even capacity (installed)
        self.BE_capacity_installed = (self.BE_revenue / inp_flow.revenue_capacity ) * 100

        # Table - Break-Even
        self.table_break_even = self.get_table_break_even(inp_flow)


    def get_table_var_cost(self, inp_flow):
        cols = range(1, inp_flow.financial_assumptions.report_lenght_years + 1)
        df = pd.DataFrame([self.service_mat, self.operating_staff, self.revenue_expense,
                        self.spares_and_stores, self.utilities, self.total_variable_cost], columns=cols)
        df.insert(0, "Item", ["Service materials", "Operating staff", "Revenue expenses",
                            "Spares and stores", "Utilities", "Total"])
        df.set_index("Item", inplace=True)

        return df

    def get_table_fixed_cost(self, inp_flow):
        cols = range(1, inp_flow.financial_assumptions.report_lenght_years + 1)
        df = pd.DataFrame([self.depr_ammor, self.admin_expense, self.interest_long_short,
                            self.total_fixed_cost], columns=cols)
        df.insert(0, "Item", ["Depreciation and amortization", "Administrative expenses",
                        "Financial expenses (Interest on long and short debt)", "Total"])
        df.set_index("Item", inplace=True)

        return df

    def get_table_annual_reg_cost(self, inp_flow):
        cols = range(1, inp_flow.financial_assumptions.report_lenght_years + 1)
        df = pd.DataFrame([self.general_expense, self.repair_maintenance,
                        self.total_annual_reg_cost], columns=cols)
        df.insert(0, "Item", ["General expense", "Repair and maintenance", "Total"])
        df.set_index("Item", inplace=True)

        return df

    @staticmethod
    def get_total_general_expenses(inp_flow):
        init_cost = inp_flow.general_expense["Initial Cost (BDT in lac)"].sum()
        yearly_incr = inp_flow.general_expense["Yearly Increment (BDT in lac)"].sum()
        return [(init_cost + yearly_incr * i) for i in
                range(inp_flow.financial_assumptions.report_lenght_years)]

    def get_table_break_even(self, inp_flow):
        cols = range(1, inp_flow.financial_assumptions.report_lenght_years + 1)
        df = pd.DataFrame([self.BE_total_fixed_cost, self.BE_total_variable_cost, self.BE_revenue,
                        self.BE_capacity_assumed, self.BE_capacity_installed], columns=cols)
        df.insert(0, "Item", ["Total fixed cost", "Total variable cost", "Break-even revenue",
                            "Break-even capacity (assumed)", "Break-even capacity (installed)"])
        df.set_index("Item", inplace=True)

        return df
