from copy import deepcopy
import pandas as pd

class required_freight_rate:
    def __init__(self, inp_flow):
        inp_flow = deepcopy(inp_flow)

        self.rfr = self.RFR_by_Secant_Method(inp_flow)

        inp_flow.revenue_capacity = inp_flow.get_revenue_capacity(self.rfr)
        self.net_receipt_rfr = self.get_net_receipt(inp_flow)

        self.table = self.get_RFR_table(inp_flow)


    def get_net_receipt(self, inp_flow):
        from .est_income_statement import est_income_statement
        from .financial_report import financial_report
        income_statement = est_income_statement(inp_flow)

        net_receipt_1 = financial_report(inp_flow).df_project_cost.loc[["Vessel Purchase / Construction",
                                    "Furniture and Fixture", "Security deposit for office advance and utitlities"],
                                    "Total (BDT in Lac)"].sum() * (-1)

        net_receipt = [net_receipt_1] +  (income_statement.revenue - (income_statement.service_mat
                            + income_statement.operating_staff + income_statement.overheads) -
                            income_statement.total_operating_exp).tolist()

        return net_receipt

    def RFR_by_Secant_Method(self, inp_flow, xi=500, xim1=600):
        """
        Secant method for finding RFR where NPV == 0
        """
        inp_flow = deepcopy(inp_flow)
        disc_rate = inp_flow.financial_assumptions.rfr_discount_rate

        def f(freight_rate): # return sum of dcf of net receipt
            i_flow = deepcopy(inp_flow)
            i_flow.revenue_capacity = inp_flow.get_revenue_capacity(freight_rate)
            return sum([i * (1/((1+disc_rate)**e)) for e, i in enumerate(self.get_net_receipt(i_flow))])

        run = True
        steps = 0
        while run:
            xi_new = xi - ( f(xi)*(xi - xim1) ) / ( f(xi) - f(xim1) )
            xim1 = xi
            xi = xi_new
            inp_flow.revenue_capacity = inp_flow.get_revenue_capacity(xi_new)
            steps += 1
            if steps==10**6 or abs(f(xi)) < 10**(-4):
                run = False

        return xi

    def get_RFR_table(self, inp_flow):
        disc_column = [(1/(1+inp_flow.financial_assumptions.rfr_discount_rate)**i)
                    for i in range(inp_flow.financial_assumptions.report_lenght_years+1)]

        df = pd.DataFrame({
            "Net Receipt at RFR" : self.net_receipt_rfr,
            f"Discount at {round(inp_flow.financial_assumptions.rfr_discount_rate*100)}%" : disc_column,
            "DCF" : [i*j for i,j in zip(self.net_receipt_rfr, disc_column)]
        }
        )

        return df
