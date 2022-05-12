from copy import deepcopy
import numpy as np
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
        rfr = annex_lib.required_freight_rate(inp_flow)

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
        self.rfr = rfr.rfr

class sensitivity:
    def __init__(self, inp_flow):
        pass

    @staticmethod
    def get_var_sensitivity(var:str, inp_flow, _range=(70,210), _step=10) -> list:
        """
        computes the ratio of percentage change of metrics for specified variable
        """
        inp_flow = deepcopy(inp_flow)

        if get_ipython().__class__.__name__=='ZMQInteractiveShell':
            from tqdm.notebook import tqdm
        else:
            from tqdm import tqdm

        try:
            var_value = inp_flow.__dict__[var]
        except KeyError:
            var_value = inp_flow.financial_assumptions.__dict__[var]

        out = [[], []]
        for i in tqdm(range(_range[0], _range[1], _step)):
            pcntg = i/100

            try:
                inp_flow.__dict__[var] = var_value * (pcntg)
            except KeyError:
                inp_flow.financial_assumptions.__dict__[var] = var_value * (pcntg)

            out[0].append(var_value * (pcntg))
            out[1].append(project_metrics(inp_flow))

        return out

    @staticmethod
    def get_fuel_sensitivity(inp_flow, _range=(70,210), _step=10) -> list:
        """
        computes the ratio of percentage change of metrics for fuel price
        """
        from .input_helpers.input_classes import technical_inputs
        ti = technical_inputs('core\\sample_inputs\\input_technical.xlsx')
        to_ded = ti.df_service_mat[~(ti.df_service_mat.Item=='Fuel & Lubricant')]['Cost per Year (BDT in Lac)'].sum()

        inp_flow = deepcopy(inp_flow)
        if get_ipython().__class__.__name__=='ZMQInteractiveShell':
            from tqdm.notebook import tqdm
        else:
            from tqdm import tqdm

        var_value = inp_flow.service_mat - to_ded

        out = [[], []]
        for i in tqdm(range(_range[0], _range[1], _step)):
            pcntg = i/100

            inp_flow.service_mat = var_value * (pcntg)

            out[0].append(var_value * (pcntg))
            out[1].append(project_metrics(inp_flow))

        out[0] = [i/var_value for i in out[0]]

        return out

    @staticmethod
    def get_debt_ratio_sensitivity(inp_flow, pctg_range_list=range(10, 101, 1)) -> list:
        """
        computes the ratio of percentage change of metrics for change in Debt ratio
        returns sensitivity for 10% to 100% Debt ratios
        """
        inp_flow = deepcopy(inp_flow)
        if get_ipython().__class__.__name__=='ZMQInteractiveShell':
            from tqdm.notebook import tqdm
        else:
            from tqdm import tqdm

        out = [[], [], []]
        for i in tqdm(pctg_range_list):
            pcntg = i/100

            inp_flow.financial_assumptions.debt_equity['Debt'] = pcntg
            inp_flow.financial_assumptions.debt_equity['Equity'] = 1 - pcntg

            out[0].append(pcntg)
            out[1].append(project_metrics(inp_flow))

        return out

    @staticmethod
    def get_num_trips_sensitivity(inp_flow, avg_monthly_trips=np.linspace(2,4,101)):
        if get_ipython().__class__.__name__=='ZMQInteractiveShell':
                from tqdm.notebook import tqdm
        else:
            from tqdm import tqdm

        from .input_helpers.input_classes import technical_inputs
        dfrev = technical_inputs('core\\sample_inputs\\input_technical.xlsx').df_revenue

        out = [[], []] # [[<num_avg_trips>], [<project_metrics>]]
        for avg_trips in tqdm(avg_monthly_trips):
            iflow = deepcopy(inp_flow)
            iflow.revenue_capacity = ((dfrev['Vessel carrying capacity (MT)'] * dfrev['No. of vessels'] *
                                       dfrev['Freight Charge / MT (BDT)'] * 2 * avg_trips*12) / 10**5)[0]

            out[0].append(avg_trips)
            out[1].append(project_metrics(iflow))

        return out
