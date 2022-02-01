import pandas as pd
import numpy as np
from .financial_report import financial_report
from .est_income_statement import est_income_statement

class IRR:
    def __init__(self, inp_flow):
        income_statement = est_income_statement(inp_flow)

        net_receipt_1 = financial_report(inp_flow).df_project_cost.loc[["Vessel Purchase / Construction",
                                    "Furniture & Fixture", "Security deposit for office advance & utitlities"],
                                    "Total (BDT in Lac)"].sum() * (-1)

        self.net_receipt = [net_receipt_1] +  (income_statement.revenue - (income_statement.service_mat
                            + income_statement.operating_staff + income_statement.overheads) -
                            income_statement.total_operating_exp).tolist()

        self.irr = np.irr(self.net_receipt)

        self.disc_column = [(1/(1+self.irr)**i) for i in range(inp_flow.financial_assumptions.report_lenght_years+1)]

        self.present_val_col = np.array(self.disc_column) * self.net_receipt

        self.table_irr = self.get_table_irr(inp_flow)


    def get_table_irr(self, inp_flow):
        #cols = ["Year", "Net Receipt",	f"Discounted Cash Flow at {round(self.irr*100)}%",	"Present Value at 15%"]
        #data = np.array([range(inp_flow.financial_assumptions.report_lenght_years+1),
        #                self.net_receipt, self.disc_column, self.irr]).T
        df = pd.DataFrame({
        "Year" : range(inp_flow.financial_assumptions.report_lenght_years+1),
        "Net Receipt" : self.net_receipt,
        f"Discounted Cash Flow at {round(self.irr*100, 2)}%" : self.disc_column,
        f"Present Value at {round(self.irr*100, 2)}%" : self.present_val_col
        })

        return df
