import pandas as pd
from .working_capital_assessment import working_capital

class financial_report:
    def __init__(self, inp_flow):
        ixs = [
            "Vessel Purchase / Construction",
            "Furniture & Fixture",
            "Security deposit for office advance & utitlities",
            "Preliminary & startup expense"
        ]

        tot_col = [
            inp_flow.purchase_vessel,
            inp_flow.furniture,
            inp_flow.security_deposit + inp_flow.adv_payments,
            inp_flow.preliminary_exp
        ]

        self.df_project_cost = pd.DataFrame(tot_col, columns=["Total (BDT in Lac)"], index=ixs)

        self.df_project_cost.insert(0, "Equity (BDT in Lac)", self.df_project_cost["Total (BDT in Lac)"]*inp_flow.financial_assumptions.debt_equity["Equity"])
        self.df_project_cost.insert(1, "Bank-debt (BDT in Lac)", self.df_project_cost["Total (BDT in Lac)"]*inp_flow.financial_assumptions.debt_equity["Debt"])

        # working capital assessment
        self.working_capital_total = working_capital(inp_flow).table_main[1].sum()
        self.working_capital_equity = self.working_capital_total * inp_flow.financial_assumptions.debt_equity["Equity"]
        self.working_capital_debt = self.working_capital_total * inp_flow.financial_assumptions.debt_equity["Debt"]

        #Total Cost of Project
        self.total_cost_total = self.df_project_cost["Total (BDT in Lac)"].sum() + self.working_capital_total
        self.total_cost_equity = self.total_cost_total * inp_flow.financial_assumptions.debt_equity["Equity"]
        self.total_cost_debt = self.total_cost_total * inp_flow.financial_assumptions.debt_equity["Debt"]
