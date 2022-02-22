from . import annex_lib

class project_metrics:
    def __init__(self, inp_flow):
        est_inc = annex_lib.est_income_statement(inp_flow)
        rev_ear = annex_lib.revenue_earnings(inp_flow)
        ovh_dpr = annex_lib.overhead_depreciation(inp_flow)
        work_cap = annex_lib.working_capital(inp_flow)
        break_even = annex_lib.break_even_analysis(inp_flow)
        debt_serv = annex_lib.debt_service_coverage(inp_flow)
        cost_benefit = annex_lib.cost_benefit_analysis(inp_flow)
        payback_period = annex_lib.payback_period(inp_flow)
        irr = annex_lib.IRR(inp_flow)

        # array-like
        self.value_service_sold = rev_ear.value_service_sold
        self.cost_of_revenue = est_inc.cost_of_revenue
        self.gross_profit = est_inc.gross_profit
        self.total_operating_exp = est_inc.total_operating_exp
        self.operating_profit = est_inc.operating_profit
        self.tot_non_operating_exp = est_inc.total_operating_exp
        self.net_profit = est_inc.net_profit
        self.manufacturing_overhead = ovh_dpr.table_overhead.sum().to_list()
        self.working_cap_req = work_cap.table_main[1:].sum().to_list()
        self.total_fixed_cost = break_even.total_fixed_cost
        self.total_variable_cost = break_even.total_variable_cost
        self.BE_capacity_assumed = break_even.BE_capacity_assumed
        self.debt_service_ratio = debt_serv.debt_service_ratio

        # single value
        self.cost_benefit_ratio = cost_benefit.cost_benefit_ratio
        self.payback_period = payback_period.payback_period
        self.irr = irr.irr

class sensitivity:
    def __init__(self, inp_flow):
        self.project_metrics = project_metrics(inp_flow)

    @staticmethod
    def get_var_sensitivity(var:str, inp_flow) -> float:
        """
        computes the ratio of percentage change of metrics for specified variable
        """
        pass
