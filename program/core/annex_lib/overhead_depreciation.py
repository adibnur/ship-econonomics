import pandas as pd
import numpy as np

class overhead_depreciation:
    def __init__(self, inp_flow):
        # capacity utilization
        self.cap_util = [round(min([inp_flow.financial_assumptions.capacity_util_1st +
                 inp_flow.financial_assumptions.capacity_util_incr * i,
                 inp_flow.financial_assumptions.capacity_util_max]), 3)
                 for i in range(inp_flow.financial_assumptions.report_lenght_years)]
        self.cap_util = np.array(self.cap_util)

        #Stores & Spares
        self.stores_and_spares = self.get_stores_and_spares(inp_flow)
        #Repair & Maintenance - Cargo Vessels
        self.maintenance_vessel = self.get_maintenance_vessel(inp_flow)
        #Utilities
        self.utilities = inp_flow.utilities * self.cap_util
        #Rent, Tax & Insurance etc.
        self.office_rent = inp_flow.office_rent  * self.cap_util
        #Other overheads
        self.other_overheads = self.get_other_overheads(inp_flow)

        #Depreciation: Cargo Vessel
        self.vessel_depr = [inp_flow.purchase_vessel *
                            inp_flow.financial_assumptions.depreciation_rate *
                            (1 - inp_flow.financial_assumptions.depreciation_rate)**i
                            for i in range(inp_flow.financial_assumptions.report_lenght_years)]

        #Depreciation: Furniture & fixtures
        self.furniture_depr = [inp_flow.furniture * inp_flow.financial_assumptions.depreciation_rate *
                            (1 - inp_flow.financial_assumptions.depreciation_rate)**i
                            for i in range(inp_flow.financial_assumptions.report_lenght_years)]

        #Table - Depreciation
        self.table_depreciation = self.get_table_depreciation(inp_flow)

        #Table - Overhead
        self.table_overhead = self.get_table_overhead(inp_flow)


    @staticmethod
    def get_stores_and_spares(inp_flow):
        init_cost = inp_flow.repair_maintenance.set_index("Description").loc['Spares and stores', 'Initial Cost (BDT in lac)']
        yearly_incr = inp_flow.repair_maintenance.set_index("Description").loc['Spares and stores', 'Yearly Increment (BDT in lac)']
        return [(init_cost + yearly_incr * i) for i in
                range(inp_flow.financial_assumptions.report_lenght_years)]

    @staticmethod
    def get_maintenance_vessel(inp_flow):
        init_cost = inp_flow.repair_maintenance.set_index("Description").loc['Cargo Vessels Maintenance', 'Initial Cost (BDT in lac)']
        yearly_incr = inp_flow.repair_maintenance.set_index("Description").loc['Cargo Vessels Maintenance', 'Yearly Increment (BDT in lac)']
        return [(init_cost + yearly_incr * i) for i in
                range(inp_flow.financial_assumptions.report_lenght_years)]

    @staticmethod
    def get_other_overheads(inp_flow):
        init_cost = inp_flow.general_expense .set_index("Description").loc['Other', 'Initial Cost (BDT in lac)']
        yearly_incr = inp_flow.general_expense .set_index("Description").loc['Other', 'Yearly Increment (BDT in lac)']
        return [(init_cost + yearly_incr * i) for i in
                range(inp_flow.financial_assumptions.report_lenght_years)]

    def get_table_depreciation(self, inp_flow):
        cols = range(1, inp_flow.financial_assumptions.report_lenght_years + 1)
        df = pd.DataFrame([self.vessel_depr, self.furniture_depr], columns=cols)
        df.insert(0, "Description", ["Cargo Vessels",	"Furniture & Fixture"])
        df.set_index("Description", inplace=True)

        return df

    def get_table_overhead(self, inp_flow):
        cols = range(1, inp_flow.financial_assumptions.report_lenght_years + 1)
        df = pd.DataFrame([self.stores_and_spares, self.maintenance_vessel,
                    self.utilities, self.office_rent, self.other_overheads], columns=cols)
        df.insert(0, "Item", ["Stores & Spares", "Repair & Maintenance - Vessels",
                    "Utilities", "Rent, Tax & Insurance etc.", "Other overheads"])
        df.set_index("Item", inplace=True)

        return df
