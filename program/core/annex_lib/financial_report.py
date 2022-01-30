import pandas as pd

class financial_report:
    def __init__(self, inp_flow):
        ixs = [
            "Vessel Purchase / Construction",
            "Furniture & Fixture",
            "Security deposit for office advance & utitlities",
            "Preliminary & startup expense"
        ]

        tot_col = [
            iflow.purchase_vessel,
            iflow.furniture,
            iflow.security_deposit + iflow.adv_payments,
            iflow.preliminary_exp
        ]

        self.df_project_cost = pd.DataFrame(tot_col, columns=["Total (BDT in Lac)"], index=ixs)

        self.df_project_cost.insert(0, "Equity (BDT in Lac)", df["Total (BDT in Lac)"]*iflow.financial_assumptions.debt_equity["Equity"])
        self.df_project_cost.insert(1, "Bank-debt (BDT in Lac)", df["Total (BDT in Lac)"]*iflow.financial_assumptions.debt_equity["Debt"])

        #self.working_capital_total = 
