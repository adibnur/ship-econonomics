import pandas as pd
import numpy as np
from .IRR import IRR

class payback_period:
    def __init__(self, inp_flow):
        stop = False
        # set max number of years in report to 100 if lifetime is given 4 digit input
        if len(str(int(inp_flow.financial_assumptions.project_lifetime))) > 3:
            max_years = 100 - inp_flow.financial_assumptions.report_lenght_years
        else:
            max_years = inp_flow.financial_assumptions.project_lifetime - inp_flow.financial_assumptions.report_lenght_years
        step_years = 0

        while not stop:
            irr = IRR(inp_flow)

            # Net Receipt
            self.net_receipt = irr.net_receipt

            # Discounted Cash Flow at X%
            self.disc_column = [(1/(1+inp_flow.financial_assumptions.disc_rate_payback_period)**i)
                                for i in range(inp_flow.financial_assumptions.report_lenght_years+1)]

            # Present Value at X%
            self.present_val_col = np.array(self.disc_column) * self.net_receipt

            # Cumulative Net Cash Flow after Discounting
            self.cum_cashflow_discounted = np.cumsum(self.present_val_col)

            # Stop if break even is reached. else increase report age by 1 year
            step_years += 1
            if len(np.where(self.cum_cashflow_discounted >= 0)[0]) > 0:
                self.payback_period = np.where(self.cum_cashflow_discounted >= 0)[0][0]
                stop = True
            elif step_years > max_years:
                self.payback_period = r'N/A'
                stop = True
            else:
                inp_flow.financial_assumptions.report_lenght_years += 1


        # Table - Pay Back Period
        self.table_payback_period = self.get_table_payback_period(inp_flow)


    def get_table_payback_period(self, inp_flow):
        df = pd.DataFrame({
        "Year" : range(inp_flow.financial_assumptions.report_lenght_years+1),
        "Net Receipt" : self.net_receipt,
        f"Discounted Cash Flow at {round(inp_flow.financial_assumptions.disc_rate_payback_period*100, 2)}%" : self.disc_column,
        f"Present Value at {round(inp_flow.financial_assumptions.disc_rate_payback_period*100, 2)}%" : self.present_val_col,
        "Cumulative Net Cash Flow after Discounting" : self.cum_cashflow_discounted
        })

        return df
