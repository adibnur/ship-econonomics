from .input_helpers import input_classes

class input_flow:
    def __init__(self, df_staff, df_technical, df_financial):
        # 1. Organization and Management
        self.staff_admin_salary = input_classes.staff_salary(df_staff, sheet_name='Administrative and Office Staff').total
        self.staff_technical = input_classes.staff_salary(df_staff, sheet_name='Technical Personnel').total

        # 2. Technical Aspects
        self.revenue_capacity = input_classes.technical_inputs(df_technical).df_revenue['Yearly Revenue (BDT in Lac)'].sum()
        self.service_mat = input_classes.technical_inputs(df_technical).df_service_mat['Cost per Year (BDT in Lac)'].sum()

        # 2.3. Machinery and Equipment
        df_eqp = input_classes.technical_inputs(df_technical).df_equipment.set_index('Description')
        df_misc = input_classes.technical_inputs(df_technical).df_misc.set_index('Description')

        self.purchase_vessel = df_eqp.loc['Purchase / Construction Cost of Vessels', 'Total Cost (BDT in Lac)']
        self.other_machinery = df_eqp.loc['Other Machinery & Equipment', 'Total Cost (BDT in Lac)']
        self.furniture = df_eqp.loc['Furniture & Office Equipment', 'Total Cost (BDT in Lac)']
        self.office_rent = df_misc.loc['Office Rent', 'Yearly Cost (BDT in lac)']
        self.erection = df_eqp.loc['Erection & Installation', 'Total Cost (BDT in Lac)']
        self.transportation = df_misc.loc['Transportation', 'Yearly Cost (BDT in lac)']
        self.utilities = df_misc.loc['Water', 'Yearly Cost (BDT in lac)'] + df_misc.loc['Power', 'Yearly Cost (BDT in lac)']
        self.security_deposit = df_eqp.loc['Security Deposit', 'Total Cost (BDT in Lac)']
        self.preliminary_exp = df_eqp.loc['Preliminary and Start-up Costs', 'Total Cost (BDT in Lac)']
        self.misc = df_misc.loc['Misc.', 'Yearly Cost (BDT in lac)']
        self.adv_payments = df_eqp.loc['Advance Payments (if any)', 'Total Cost (BDT in Lac)']
        self.cash = df_misc.loc['Cash', 'Yearly Cost (BDT in lac)']

        # 2.4. Repair and Maintenance
        df_exp = input_classes.technical_inputs(df_technical).df_expenses

        self.repair_maintenance = df_exp[df_exp['Description'].isin(['Cargo Vessels Maintenance', 'Spares and stores'])]

        # 2.5. General Expenses
        s1 = df_exp[~(df_exp['Description']=='Cargo Vessels Maintenance')]
        self.general_expense = s1[~(s1['Description']=='Spares and stores')]

        # 3. Financial Analysis
        self.financial_assumptions = input_classes.financial_assumptions(df_financial)
