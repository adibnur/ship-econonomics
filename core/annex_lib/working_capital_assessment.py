import pandas as pd
import numpy as np

class working_capital:
    def __init__(self, inp_flow):
        self.tied_up_period  = {"Fuel & other materials" : 30,
                                "Inventory of consumables" : 3,
                                "Spares & accessories" : 3,
                                "Inventory of ready service" : 3,
                                "Work in progress" : 3,
                                "Account receiveables" : 15,
                                "Operating staffs" : 3,
                                "Administrative & General expenses" : 3,
                                "Utilities" : 3}

        # capacity utilization
        self.cap_util = [round(min([inp_flow.financial_assumptions.capacity_util_1st +
                 inp_flow.financial_assumptions.capacity_util_incr * i,
                 inp_flow.financial_assumptions.capacity_util_max]), 3)
                 for i in range(inp_flow.financial_assumptions.report_lenght_years)]
        self.cap_util = np.array(self.cap_util)

        # Fuel & other materials
        self.fuel_and_other = (self.tied_up_period["Fuel & other materials"] / inp_flow.financial_assumptions.days_of_operation) * inp_flow.service_mat * self.cap_util

        # Spares & accessories
        self.spares_and_acc = self.get_spares_and_acc(inp_flow)

        # Inventory of ready service
        self.inventory_ready = [inp_flow.revenue_capacity * self.cap_util[i] *
                                self.tied_up_period["Inventory of ready service"] /
                                inp_flow.financial_assumptions.days_of_operation for i in
                                range(inp_flow.financial_assumptions.report_lenght_years)]

        # Work in progress
        self.work_in_progress = [inp_flow.service_mat * self.cap_util[i] * self.tied_up_period["Work in progress"]
                                / inp_flow.financial_assumptions.days_of_operation for i in
                                range(inp_flow.financial_assumptions.report_lenght_years)]

        # Account receiveables
        self.account_rec = [inp_flow.revenue_capacity * self.cap_util[i] * self.tied_up_period["Account receiveables"]
                            / inp_flow.financial_assumptions.days_of_operation for i in
                            range(inp_flow.financial_assumptions.report_lenght_years)]

        # Cash
        self.cash = [inp_flow.cash * self.cap_util[i] for i in range(inp_flow.financial_assumptions.report_lenght_years)]


        ## *Inventory of consumables
        # Operating staffs
        self.operating_staff = self.get_operating_staff(inp_flow)
        #Administrative & General expenses
        self.admin_and_general_exp = self.get_admin_general_exp(inp_flow)
        #Utilities
        self.utils = self.get_utils(inp_flow)

        # Tables
        #*Inventory of consumables
        self.table_inventory = pd.DataFrame([self.operating_staff, self.admin_and_general_exp, self.utils],
                            columns=range(1,inp_flow.financial_assumptions.report_lenght_years+1),
                            index=['Operating staffs', 'Administrative & General expenses', 'Utilities'])

        #main table - working capital assessment
        self.table_main = pd.DataFrame([self.cap_util, self.fuel_and_other, self.table_inventory.sum(), self.spares_and_acc,
              self.inventory_ready, self.work_in_progress, self.account_rec, self.cash],
              columns=range(1,inp_flow.financial_assumptions.report_lenght_years+1),
              index=['Capacity utilization', 'Fuel & other materials', 'Inventory of consumables',
              'Spares & accessories', 'Inventory of ready service', 'Work in progress', 'Account receiveables', 'Cash'])



    def get_spares_and_acc(self, inp_flow):
        init_cost = inp_flow.repair_maintenance.set_index("Description").loc['Spares and stores', 'Initial Cost (BDT in lac)']
        yearly_incr = inp_flow.repair_maintenance.set_index("Description").loc['Spares and stores', 'Yearly Increment (BDT in lac)']
        return [(init_cost + yearly_incr * i) * self.cap_util[i] *
                self.tied_up_period["Spares & accessories"] * (365 / 12) /
                inp_flow.financial_assumptions.days_of_operation for i in
                range(inp_flow.financial_assumptions.report_lenght_years)]

    def get_operating_staff(self, inp_flow):
        oper_staff = np.array([inp_flow.staff_technical *
                  (1 + inp_flow.financial_assumptions .wage_incr)**i * self.cap_util[i]
                  for i in range(inp_flow.financial_assumptions.report_lenght_years)])

        return oper_staff * self.tied_up_period["Operating staffs"] * (365/12) / inp_flow.financial_assumptions.days_of_operation

    def get_admin_general_exp(self, inp_flow):
        gen_exp = np.array([inp_flow.general_expense.values[0][1] + inp_flow.general_expense.values[0][2]*j for j in range(inp_flow.financial_assumptions.report_lenght_years)])
        if len(inp_flow.general_expense.values) > 1:
            for i in inp_flow.general_expense.values[1:]:
                gen_exp += [i[1] + i[2]*j for j in range(inp_flow.financial_assumptions.report_lenght_years)]

        gen_exp = gen_exp * np.array(self.cap_util)

        admin_exp = np.array([inp_flow.staff_admin_salary *
                      (1 + inp_flow.financial_assumptions.wage_incr)**i * self.cap_util[i]
                      for i in range(inp_flow.financial_assumptions.report_lenght_years)])

        return (gen_exp + admin_exp) * self.tied_up_period["Inventory of ready service"] * (365/12) / inp_flow.financial_assumptions.days_of_operation

    def get_utils(self, inp_flow):
        utils = np.array([inp_flow.utilities  * self.cap_util[i]
                          for i in range(inp_flow.financial_assumptions.report_lenght_years)])

        return utils * self.tied_up_period["Utilities"] * (365/12) / inp_flow.financial_assumptions.days_of_operation
