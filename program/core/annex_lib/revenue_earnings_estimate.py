import pandas as pd
import numpy as np
from .LTL_ammortization import LTL_ammortization
from .financial_report import financial_report

class revenue_earnings:
    def __init__(self, inp_flow):
        # capacity utilization
        self.cap_util = [round(min([inp_flow.financial_assumptions.capacity_util_1st +
                 inp_flow.financial_assumptions.capacity_util_incr * i,
                 inp_flow.financial_assumptions.capacity_util_max]), 3)
                 for i in range(inp_flow.financial_assumptions.report_lenght_years)]
        self.cap_util = np.array(self.cap_util)

        # Revenue at capacity utilization
        self.revenue_at_cap = inp_flow.revenue_capacity * self.cap_util

        # Work in Process (WIP)
        self.work_in_process = ([inp_flow.service_mat *
                                inp_flow.financial_assumptions.stock_work_in_process /
                                inp_flow.financial_assumptions.days_of_operation ] *
                                inp_flow.financial_assumptions.report_lenght_years)

        # Difference between closing and opening inventory of WIP
        self.diff_inventory_WIP = [(([0]+self.work_in_process)[i+1] - ([0]+self.work_in_process)[i])
                                    for i in range(len(self.work_in_process))]

        # Value of service available for sale
        self.val_service_available = self.revenue_at_cap - self.diff_inventory_WIP

        # Closing inventory of service
        self.closing_inventory = [0] + ((inp_flow.financial_assumptions.stock_work_in_process /
            inp_flow.financial_assumptions.days_of_operation) * self.val_service_available[1:]).tolist()

        # Difference between closing inventory of service
        self.diff_closing_inventory = self.get_diff_closing_inventory(inp_flow)

        # Value of service sold
        self.value_service_sold = self.val_service_available - self.diff_closing_inventory

        # Table - 1
        self.table_1 = self.get_table_1(inp_flow)


        # Administrative expense
        self.admin_expense = [inp_flow.staff_admin_salary *
                (1 + inp_flow.financial_assumptions.wage_incr)**(i)
                for i in range(inp_flow.financial_assumptions.report_lenght_years)] * self.cap_util

        # General expenses
        self.general_expense = self.get_general_exp(inp_flow)

        # Revenue expenses
        self.revenue_expense = self.value_service_sold * inp_flow.financial_assumptions.rate_of_revenue_expenditure

        #Table - 2
        self.table_2 = self.get_table_2(inp_flow)


        # Principal of Long Term Debt
        self.principal_debt_exp = self.get_LTL_slice_sum(inp_flow, LTL_ammortization(inp_flow), "Principal Repayment")

        # Interest of Long Term Debt
        self.interest_debt_exp = self.get_LTL_slice_sum(inp_flow, LTL_ammortization(inp_flow), "Interest Repayment")

        # Interest of Working Capital Debt
        self.interest_working_cap = [financial_report(inp_flow).working_capital_debt * inp_flow.financial_assumptions.interest_rate ] * inp_flow.financial_assumptions.report_lenght_years

        # Table - 3
        self.table_3 = self.get_table_3(inp_flow)



    def get_diff_closing_inventory(self, inp_flow):
        diff_closing_inventory = [self.val_service_available[0] *
                    inp_flow.financial_assumptions.stock_work_in_process /
                    inp_flow.financial_assumptions.days_of_operation]
        diff_closing_inventory.append(self.closing_inventory[1] - diff_closing_inventory[0])
        for i in range(2, len(self.closing_inventory)):
            diff_closing_inventory.append(self.closing_inventory[i] - self.closing_inventory[i-1])

        return diff_closing_inventory

    def get_table_1(self, inp_flow):
            cols = range(1, inp_flow.financial_assumptions.report_lenght_years + 1)
            df = pd.DataFrame([self.cap_util, self.revenue_at_cap, self.work_in_process,
                    self.diff_inventory_WIP, self.val_service_available, self.closing_inventory,
                    self.diff_closing_inventory, self.value_service_sold], columns=cols)

            df.insert(0, "Item", ["Capacity utilization", "Revenue at capacity utilization",
                                "Work in Process (WIP)", "Difference between closing and opening inventory of WIP",
                                "Value of service available for sale", "Closing inventory of service",
                                "Difference between closing inventory of service", "Value of service sold"])
            df.set_index("Item", inplace=True)

            return df

    @staticmethod
    def get_general_exp(inp_flow):
        gen_exp = []
        for i in inp_flow.general_expense.values:
            gen_exp.append(i[1] + i[2] * np.array(range(inp_flow.financial_assumptions.report_lenght_years)))

        return np.array(gen_exp).sum(axis=0)

    def get_table_2(self, inp_flow):
            cols = range(1, inp_flow.financial_assumptions.report_lenght_years + 1)
            df = pd.DataFrame([self.admin_expense, self.general_expense, self.revenue_expense], columns=cols)

            df.insert(0, "Item", ["Administrative expense", "General expenses", "Revenue expenses"])
            df.set_index("Item", inplace=True)

            return df

    @staticmethod
    def get_LTL_slice_sum(inp_flow, LTL_am, col):
        d = LTL_am.table_ammortization
        ts = (d['Month after Distribution'] - (LTL_am.implementation_period + LTL_am.grace_period)) / 12
        out_row = []
        for i in range(1, inp_flow.financial_assumptions.report_lenght_years + 1):
            out_row.append(d[(ts <= i) & (ts > i-1)][col].sum())

        return out_row

    def get_table_3(self, inp_flow):
        cols = range(1, inp_flow.financial_assumptions.report_lenght_years + 1)
        df = pd.DataFrame([self.principal_debt_exp, self.interest_debt_exp, self.interest_working_cap], columns=cols)

        df.insert(0, "Item", ["Principal of Long Term Debt", "Interest of Long Term Debt", "Interest of Working Capital Debt"])
        df.set_index("Item", inplace=True)

        return df
