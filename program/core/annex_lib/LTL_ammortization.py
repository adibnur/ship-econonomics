import pandas as pd
from .financial_report import financial_report

class LTL_ammortization:
    def __init__(self, inp_flow):
        self.implementation_period = inp_flow.financial_assumptions.construction_period
        self.grace_period =  inp_flow.financial_assumptions.grace_period
        self.principal = financial_report(inp_flow).df_project_cost["Bank-debt (BDT in Lac)"].sum()
        self.interest_rate = inp_flow.financial_assumptions.interest_rate
        self.IDGP = self.principal * (self.grace_period / 12) * self.interest_rate
        self.total_residual_principal = self.principal + self.IDGP
        self.first_installment_time = self.implementation_period + self.grace_period + inp_flow.financial_assumptions.freq_installments
        self.num_installments = inp_flow.financial_assumptions.num_installments_principal
        self.installments_per_year = round(12 / inp_flow.financial_assumptions.freq_installments)
        self.installment_amount = round(
            ( self.total_residual_principal * (self.interest_rate / self.installments_per_year) *
            (1 + (self.interest_rate / self.installments_per_year))**self.num_installments ) /
            ( (1 + (self.interest_rate / self.installments_per_year))**self.num_installments - 1)
        )
        self.table_ammortization = self.get_ammortization_table(inp_flow)



    def get_ammortization_table(self, inp_flow):
        cols = ["Installment Number", "Month after Distribution", "Residual Principal",
        "Principal Repayment", "Interest Repayment", "Total Installment"]

        #Installment Number column
        nins = range(1, self.num_installments+1)
        #Month after Distribution column
        mad = range(self.first_installment_time, self.first_installment_time +
            inp_flow.financial_assumptions.freq_installments *(self.num_installments),
            inp_flow.financial_assumptions.freq_installments)

        #Interest Repayment 1st row
        int_rep = round(self.total_residual_principal * self.interest_rate / self.installments_per_year)
        d = [[nins[0], mad[0], self.total_residual_principal, self.installment_amount - int_rep, int_rep, self.installment_amount]]

        for e,i in enumerate(zip(nins[1:], mad[1:])):
            i_nins, i_mad = i[0], i[1]
            #Residual Principal ith row
            i_residual = d[e][2] - d[e][3]
            #Interest Repayment ith row
            i_int_rep = round(i_residual * self.interest_rate / self.installments_per_year)
            d.append([i_nins, i_mad, i_residual, self.installment_amount - i_int_rep, i_int_rep, self.installment_amount])

        return pd.DataFrame(d, columns=cols)
