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

        self.irr = self.IRR_by_Secant_Method()

        self.disc_column = [(1/(1+self.irr)**i) for i in range(inp_flow.financial_assumptions.report_lenght_years+1)]

        self.present_val_col = np.array(self.disc_column) * self.net_receipt

        self.table_irr = self.get_table_irr(inp_flow)


    def get_table_irr(self, inp_flow):
        df = pd.DataFrame({
        "Year" : range(inp_flow.financial_assumptions.report_lenght_years+1),
        "Net Receipt" : self.net_receipt,
        f"Discounted Cash Flow at {round(self.irr*100, 2)}%" : self.disc_column,
        f"Present Value at {round(self.irr*100, 2)}%" : self.present_val_col
        })

        return df

    def IRR_by_Secant_Method(self, xi=.15, xim1=0.25):
        """
        Secant method for finding IRR root where NPV == 0
        """
        f = lambda x : sum([i * (1/((1+x)**e)) for e, i in enumerate(self.net_receipt)])

        run = True
        steps = 0
        while run:
            xi_new = xi - ( f(xi)*(xi - xim1) ) / ( f(xi) - f(xim1) )
            xim1 = xi
            xi = xi_new
            steps += 1
            if steps==10**3 or abs(f(xi)) < 10**(-4):
                run = False

        return xi
