import pandas as pd
import numpy as np
from .est_income_statement import est_income_statement
from .revenue_earnings_estimate import revenue_earnings

class debt_service_coverage:
    def __init__(self, inp_flow):
        income_statement = est_income_statement(inp_flow)
        rev_ear = revenue_earnings(inp_flow)

        ## Cash accrual
        # Operating Profit
        self.operating_profit = income_statement.operating_profit

        # Interest on Project Loan - Keeping out ot calculation - Seems wrong
        #self.interest_project_loan = income_statement.interest_long_short

        # Total - Cash accrual
        self.total_cash_accrual = np.array(self.operating_profit)

        ## Repayment

        # Repayment of Project Loan
        self.repayment_project_loan = rev_ear.principal_debt_exp

        # Interest on Project loan
        self.interest_project_loan = rev_ear.interest_debt_exp

        # Total - Repayment
        self.total_repayment = np.array(self.repayment_project_loan) + self.interest_project_loan


        self.debt_service_ratio = self.total_cash_accrual / self.total_repayment
        ## Debt Service Coverage Ratio (Times)


        # Table - Debt Service Coverage
        self.table_debt_service = self.get_table_debt_service(inp_flow)


    def get_table_debt_service(self, inp_flow):
        cols = range(1, inp_flow.financial_assumptions.report_lenght_years + 1)
        df = pd.DataFrame([self.operating_profit, self.total_cash_accrual, self.repayment_project_loan,
                        self.interest_project_loan, self.total_repayment,
                        self.debt_service_ratio], columns=cols)

        df.insert(0, "Item", ["Operating Profit", "Total - Cash accrual",
                    "Repayment of Project Loan", "Interest on Project loan",
                    "Total - Repayment", "Debt Service Coverage Ratio (Times)"])
        df.set_index("Item", inplace=True)

        return df
