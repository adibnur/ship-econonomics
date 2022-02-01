import pandas as pd
import numpy as np
from .revenue_earnings_estimate import revenue_earnings
from .overhead_depreciation import overhead_depreciation

class est_income_statement:
    def __init__(self, inp_flow):
        # capacity utilization
        self.cap_util = [round(min([inp_flow.financial_assumptions.capacity_util_1st +
                 inp_flow.financial_assumptions.capacity_util_incr * i,
                 inp_flow.financial_assumptions.capacity_util_max]), 3)
                 for i in range(inp_flow.financial_assumptions.report_lenght_years)]
        self.cap_util = np.array(self.cap_util)

        # Revenue at capacity utilization
        rev_ear = revenue_earnings(inp_flow)
        self.revenue = rev_ear.value_service_sold


        ##Cost of Revenue
        # Service Material
        self.service_mat = self.cap_util * inp_flow.service_mat

        # Operating Staffs
        self.operating_staff = [inp_flow.staff_technical  *
                (1 + inp_flow.financial_assumptions.wage_incr)**(i)
                for i in range(inp_flow.financial_assumptions.report_lenght_years)] * self.cap_util

        # Overheads
        # Depreciation
        overhead_depr = overhead_depreciation(inp_flow)
        self.overheads = overhead_depr.table_overhead.sum().to_numpy()
        self.depreciation = overhead_depr.table_depreciation.sum().to_numpy()

        # Total Cost of Revenue
        self.cost_of_revenue = self.service_mat + self.operating_staff + self.overheads + self.depreciation

        # Gross Profit
        self.gross_profit = self.revenue - self.cost_of_revenue

        # Table - Cost of Revenue
        self.table_cost_of_revenue = self.get_table_cost_of_revenue(inp_flow)


        ## Operating Expenses
        #Administrative and general expenses
        self.admin_general_exp = self.get_admin_general_exp(inp_flow)

        #Revenue and other expenses at the rate X%
        self.rev_and_other_exp = rev_ear.revenue_expense

        #Total Operating Expense
        self.total_operating_exp = self.admin_general_exp + self.rev_and_other_exp

        #Operating Profit
        self.operating_profit = self.gross_profit - self.total_operating_exp

        #Table - Operating Expenses
        self.table_operating_exp = self.get_table_operating_exp(inp_flow)


        ## Non-Operating Expense
        # Interest on: Long and short term debt.
        self.interest_long_short = np.array(rev_ear.interest_debt_exp) + np.array(rev_ear.interest_working_cap)

        # Amortization of preliminary expenses
        self.ammortization_perl_exp = [inp_flow.financial_assumptions.ammortization_of_prel] * inp_flow.financial_assumptions.report_lenght_years

        # Total Non-Operating Expense
        self.tot_non_operating_exp = self.interest_long_short + self.ammortization_perl_exp

        # Net Profit
        self.net_profit = self.operating_profit - self.tot_non_operating_exp

        # Table - Non-Operating Expense
        self.table_non_operating_exp = self.get_table_non_operating_exp(inp_flow)


    def get_table_cost_of_revenue(self, inp_flow):
        cols = range(1, inp_flow.financial_assumptions.report_lenght_years + 1)
        df = pd.DataFrame([self.service_mat, self.operating_staff, self.overheads,
                self.depreciation, self.cost_of_revenue, self.gross_profit], columns=cols)

        df.insert(0, "Item", ["Service Material", "Operating Staffs", "Overheads",
                    "Depreciation", "Total Cost of Revenue", "Gross Profit"])
        df.set_index("Item", inplace=True)

        return df

    def get_admin_general_exp(self, inp_flow):
        gen_exp = np.array([inp_flow.general_expense.values[0][1] + inp_flow.general_expense.values[0][2]*j for j in range(inp_flow.financial_assumptions.report_lenght_years)])
        if len(inp_flow.general_expense.values) > 1:
            for i in inp_flow.general_expense.values[1:]:
                gen_exp += [i[1] + i[2]*j for j in range(inp_flow.financial_assumptions.report_lenght_years)]

        gen_exp = gen_exp

        admin_exp = np.array([inp_flow.staff_admin_salary *
                      (1 + inp_flow.financial_assumptions.wage_incr)**i * self.cap_util[i]
                      for i in range(inp_flow.financial_assumptions.report_lenght_years)])

        return (gen_exp + admin_exp)

    def get_table_operating_exp(self, inp_flow):
        cols = range(1, inp_flow.financial_assumptions.report_lenght_years + 1)
        df = pd.DataFrame([self.admin_general_exp, self.rev_and_other_exp,
                        self.operating_profit, self.operating_profit], columns=cols)

        df.insert(0, "Item", ["Administrative and general expenses",
                f"Revenue and other expenses at the rate {inp_flow.financial_assumptions.rate_of_revenue_expenditure * 100}%",
                "Total Operating Expense", "Operating Profit"])
        df.set_index("Item", inplace=True)

        return df

    def get_table_non_operating_exp(self, inp_flow):
        cols = range(1, inp_flow.financial_assumptions.report_lenght_years + 1)
        df = pd.DataFrame([self.interest_long_short, self.ammortization_perl_exp,
                        self.tot_non_operating_exp, self.net_profit], columns=cols)

        df.insert(0, "Item", ["Interest on: Long and short term debt.",
                "Amortization of preliminary expenses", "Total Non-Operating Expense", "Net Profit"])
        df.set_index("Item", inplace=True)

        return df
