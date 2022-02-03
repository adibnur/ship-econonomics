import pandas as pd
import numpy as np
from .financial_report import financial_report
from .est_income_statement import est_income_statement

class cost_benefit_analysis:
    def __init__(self, inp_flow):
        income_statement = est_income_statement(inp_flow)

        capital_cost_1 = financial_report(inp_flow).df_project_cost.loc[["Vessel Purchase / Construction",
                                    "Furniture & Fixture", "Security deposit for office advance & utitlities"],
                                    "Total (BDT in Lac)"].sum()

        self.capital_cost = [capital_cost_1] + [0] * inp_flow.financial_assumptions.report_lenght_years

        self.operating_cost = [0] + (income_statement.service_mat + income_statement.operating_staff
                            + income_statement.overheads + income_statement.total_operating_exp).tolist()

        self.total_cost = np.array(self.capital_cost) + self.operating_cost

        self.disc_column = [(1/(1+inp_flow.financial_assumptions.disc_rate_payback_period)**i)
                            for i in range(inp_flow.financial_assumptions.report_lenght_years+1)]

        self.present_val_cost = self.total_cost * self.disc_column

        self.revenue = [0] + income_statement.revenue.tolist()

        self.present_val_revenue = np.array(self.revenue) * self.disc_column

        self.table = self.get_table(inp_flow)

        self.cost_benefit_ratio = self.table["Present Value of Revenue"].sum() / self.table["Present Value of Cost"].sum()


    def get_table(self, inp_flow):
        df = pd.DataFrame({
        "Year" : range(inp_flow.financial_assumptions.report_lenght_years+1),
        "Capital Cost" : self.capital_cost,
        "Operating Cost" : self.operating_cost,
        "Total Cost" : self.total_cost,
        f"Discounted Cash Flow at {round(inp_flow.financial_assumptions.disc_rate_payback_period*100, 2)}%" : self.disc_column,
        "Present Value of Cost" : self.present_val_cost,
        "Revenue" : self.revenue,
        f"Discounted Cash Flow at {round(inp_flow.financial_assumptions.disc_rate_payback_period*100, 2)}%" : self.disc_column,
        "Present Value of Revenue" : self.present_val_revenue
        })

        return df
