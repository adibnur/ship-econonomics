def generate_chapter1_tex(inp_flow, out_path, column_color_RGB='176,224,230', alt_row_color_RGB='240,248,255'):
    out = generate_chapter1_tables(inp_flow, column_color_RGB, alt_row_color_RGB)

    with open(out_path, "w") as f:
        f.write(out)

def generate_chapter1_tables(inp_flow, column_color_RGB='176,224,230', alt_row_color_RGB='240,248,255'):
    out = generate_chapter1_1p1_1p2(inp_flow, column_color_RGB, alt_row_color_RGB)
    out += '\n' + generate_chapter1_1p3p1(inp_flow)
    out += '\n' + generate_chapter1_1p3p2(inp_flow)

    return out

def generate_chapter1_1p1_1p2(inp_flow, column_color_RGB, alt_row_color_RGB):
    out = r"\definecolor{alt_row_color}{RGB}{" + alt_row_color_RGB + "}"
    out+= r"\definecolor{table_header_color}{RGB}{" + column_color_RGB + "}"

    out += '\n' + r"""
    \section{Organization and Management}
    \vspace{1cm}
    \subsection{Manpower Requirement and Compensation}
    \def\arraystretch{1.2}
    \begin{flushleft}
    \rowcolors{2}{alt_row_color}{}
    \begin{tabular}{|p{5cm}|p{3cm}|}
        \hline

        \rowcolor{table_header_color}
        \textbf{Items} & \textbf{Value (BDT in lac)} \\ \hline
    """
    out += '\n' + f"Administrative and office staff & {round(inp_flow.staff_admin_salary, 2)} \\\\ \\hline"
    out += '\n' + f"Technical personnel & {round(inp_flow.staff_technical, 2)} \\\\ \\hline"
    out += '\n' + r"\end{tabular}"

    out += '\n' + r"""
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    \vspace{2cm}
    \section{Technical Aspects}
    \vspace{1cm}
    \rowcolors{2}{alt_row_color}{}

    \subsection{Revenue earnings capacity}
    \begin{tabular}{|p{5cm}|p{3cm}|}

            \hline
            \rowcolor{table_header_color}
            \textbf{Items} & \textbf{Value (BDT in lac)} \\ \hline
    """
    out += '\n' + f"Revenue earnings capacity & {round(inp_flow.revenue_capacity, 2)} \\\\ \\hline"

    out += '\n' + r"""\end{tabular}
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    \vspace{1cm}
    \subsection{Service materials and other expenses}
    \rowcolors{2}{alt_row_color}{}
    \begin{tabular}{|p{5cm}|p{3cm}|}

            \hline
            \rowcolor{table_header_color}
            \textbf{Items} & \textbf{Value (BDT in lac)} \\ \hline
    """
    out += '\n' + f"Service materials and other expenses & {round(inp_flow.service_mat, 2)} \\\\ \\hline"

    out += '\n' + r"""\end{tabular}
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    \vspace{1cm}
    \subsection{Machinery and Equipment}
    \rowcolors{2}{alt_row_color}{}
    \begin{tabular}{|p{5cm}|p{3cm}|}

        \hline
        \rowcolor{table_header_color}
        \textbf{Items} & \textbf{Value (BDT in lac)} \\ \hline
    """

    out += '\n' + f"Purchase / Construction of Vessel & {round(inp_flow.purchase_vessel, 2)} \\\\ \\hline"

    out += '\n' + f"Other machinery and equipment & {round(inp_flow.other_machinery, 2)} \\\\ \\hline"

    out += '\n' + f"Furniture and Office Equipment & {round(inp_flow.furniture, 2)} \\\\ \\hline"

    out += '\n' + f"Office rent & {round(inp_flow.office_rent, 2)} \\\\ \\hline"

    out += '\n' + f"Erection and Installation & {round(inp_flow.erection, 2)} \\\\ \\hline"

    out += '\n' + f"Transportation & {round(inp_flow.transportation, 2)} \\\\ \\hline"

    out += '\n' + f"Utilities & {round(inp_flow.utilities, 2)} \\\\ \\hline"

    out += '\n' + f"Security Deposit & {round(inp_flow.security_deposit, 2)} \\\\ \\hline"

    out += '\n' + f"Preliminary Expenses & {round(inp_flow.preliminary_exp, 2)} \\\\ \\hline"

    out += '\n' + f"Misc. & {round(inp_flow.misc, 2)} \\\\ \\hline"

    out += '\n' + f"Advance Payments (if any) & {round(inp_flow.adv_payments, 2)} \\\\ \\hline"

    out += '\n' + f"Cash & {round(inp_flow.cash, 2)} \\\\ \\hline"

    out += '\n' + r"""\end{tabular}
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    \vspace{1cm}
    \subsection{Repair and Maintenance}
    \rowcolors{2}{alt_row_color}{}
    \begin{tabular}{|p{5cm}|p{3cm}|p{3cm}|}

        \hline
        \rowcolor{table_header_color}
        \textbf{Items} & \textbf{Initial cost(BDT in lac)} & \textbf{Yearly increment(BDT in lac)}\\ \hline
    """
    for row in inp_flow.repair_maintenance.values:
        out += '\n' + f"{row[0]} & {row[1]} & {row[2]} \\\\ \\hline "

    out += '\n' + r"""\end{tabular}
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    \vspace{1cm}
    \subsection{General Expenses}
    \rowcolors{2}{alt_row_color}{}
    \begin{tabular}{|p{5cm}|p{3cm}|p{3cm}|}

        \hline
        \rowcolor{table_header_color}
        \textbf{Items} & \textbf{Initial cost(BDT in lac)} & \textbf{Yearly increment(BDT in lac)}\\ \hline
    """
    for row in inp_flow.general_expense.values:
        out += '\n' + f"{row[0]} & {row[1]} & {row[2]} \\\\ \\hline "


    out += '\n' + r"""\end{tabular}
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """

    return out

def generate_chapter1_1p3p1(inp_flow):
    from ..annex_lib.financial_report import financial_report
    fr = financial_report(inp_flow)

    out = r"""
    \vspace{1cm}
    \section{Financial Analysis}
    \vspace{1cm}
    \subsection{Project Cost}
    \rowcolors{2}{alt_row_color}{}
    \begin{tabular}{|p{5cm}|c|c|c|}
        \hline

        \rowcolor{table_header_color}
        \textbf{Items} & \textbf{Equity} & \textbf{Bank-Debt} & \textbf{Total (BDT in Lac)} \\ \hline
    """

    for ix, row in zip(fr.df_project_cost.index, fr.df_project_cost.values):
        out += f"{ix} & {round(row[0], 2)} & {round(row[1], 2)} & {round(row[2], 2)} \\\\ \\hline \n"

    out += f"Working capital requirement & {round(fr.working_capital_equity,2)} & {round(fr.working_capital_debt,2)} & {round(fr.working_capital_total,2)} \\\\ \\hline \n"

    out += r"\textbf{Total cost of project} & " + f"{round(fr.total_cost_equity,2)} & {round(fr.total_cost_debt,2)} & {round(fr.total_cost_total,2)} \\\\ \\hline \n"

    out += r"""
    \end{tabular}
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """

    return out

def generate_chapter1_1p3p2(inp_flow):
    df = inp_flow.financial_assumptions.df.copy()
    df.loc['Capacity Utilization', ['Value', 'Unnamed: 3', 'Unnamed: 4']] = df.loc['Capacity Utilization', ['Value', 'Unnamed: 3', 'Unnamed: 4']].apply(lambda x : str(x*100)+r'\%')
    df.loc['Annual Increment of wages and salaries', 'Value'] = str(df.loc['Annual Increment of wages and salaries', 'Value']*100)+r'\%'
    df.loc['Depreciation rates in straight line method', 'Value'] = str(df.loc['Depreciation rates in straight line method', 'Value']*100)+r'\%'
    df.loc['Interest on Capital Loan', 'Value'] = str(df.loc['Interest on Capital Loan', 'Value']*100)+r'\%'
    df.loc['Rate of Revenue Expenditure', 'Value'] = str(df.loc['Rate of Revenue Expenditure', 'Value']*100)+r'\%'
    df.loc['Debt : Equity Ratio', ['Value', 'Unnamed: 3']] = df.loc['Debt : Equity Ratio', ['Value', 'Unnamed: 3']].apply(lambda x : str(x*100)+r'\%')
    df.loc['Discount Rate for Payback Period', 'Value'] = str(df.loc['Discount Rate for Payback Period', 'Value']*100)+r'\%'
    df.loc['Discount Rate for Cost Benefit Analysis', 'Value'] = str(df.loc['Discount Rate for Cost Benefit Analysis', 'Value']*100)+r'\%'

    df = df.fillna('').reset_index().set_index('Sn').fillna('')


    out = r"""
    \newpage
    \subsection{Assumptions for Earnings Forecast}
    \rowcolors{2}{alt_row_color}{}
    \begin{tabular}{|p{5cm}|p{3cm}|p{3cm}|p{3cm}|}
        \hline

        \rowcolor{table_header_color}
        \textbf{Items} & \textbf{Value} & &   \\ \hline
    """

    for row in df.values:
        out += f"{row[0]} & {row[1]} & {row[2]} & {row[3]} \\\\ \\hline \n"

    out += r"""
    \end{tabular}

    \end{flushleft}
    """

    return out
