def generate_tex_file(debt_service, out_path, column_color='b0e0e6'):
    out = r"""\documentclass[10pt, a4paper]{article}
    \usepackage[utf8]{inputenc}
    \usepackage{fullpage}
    \usepackage[table]{xcolor}
    \renewcommand{\familydefault}{\sfdefault}

    \begin{document}"""

    out += get_tex_table(debt_service=debt_service, column_color=column_color)

    out += r"\end{document}"
    with open(out_path, "w") as f:
        f.write(out)

def get_tex_table(debt_service, column_color='b0e0e6'):
    out = r"""
    \begin{huge}
    \textbf{Debt-Service Coverage Ratio}
    \end{huge}

    \vspace{1cm}

    \def\arraystretch{1.2}
    \begin{flushleft}

    \begin{tabular}{|p{3cm}|c|c|c|c|c|c|c|c|}
    \multicolumn{9}{r}{BDT in Lac}\\
        \hline
        """
    out += r"\rowcolor[HTML]" + "{" + column_color + "}"

    out += r"\multicolumn{1}{|c|}{} & \multicolumn{8}{c|}{\textbf{Year}}\\ \hline"

    out += r"\rowcolor[HTML]" + "{" + column_color + "}"

    out += r"\textbf{Item} & "

    columns = ' '.join([f"\\textbf{'{'+str(col)+'}'} &" for col in debt_service.table_debt_service.columns])[:-2] + "\\\\ \\hline \n"
    out += columns

    out += r"\rowcolor[HTML]" + "{" + column_color + "}"

    out += r"\multicolumn{9}{|c|}{\textbf{Cash Accrual}}\\ \hline"


    out += r"\textbf{Operating profit}" + ' '.join([f"& {round(i,2)}" for i in debt_service.operating_profit]) + " \\\\ \\hline"

    #out += r"\textbf{Interest on project loan}" + ' '.join([f"& {round(i,2)}" for i in debt_service.interest_project_loan]) + " \\\\ \\hline"

    out += r"\textbf{Total}"  + ' '.join([f"& {round(i,2)}" for i in debt_service.total_cash_accrual]) + " \\\\ \\hline"

    out += r"\rowcolor[HTML]" + "{" + column_color + "}"
    out += r"\multicolumn{9}{|c|}{\textbf{Repayment}}\\ \hline"

    out += r"\textbf{Repayment on project loan}" + ' '.join([f"& {round(i,2)}" for i in debt_service.repayment_project_loan]) + " \\\\ \\hline"

    out += r"\textbf{Interest on project loan}" + ' '.join([f"& {round(i,2)}" for i in debt_service.interest_project_loan]) + " \\\\ \\hline"

    out += r"\textbf{Total}" + ' '.join([f"& {round(i,2)}" for i in debt_service.total_repayment]) + " \\\\ \\hline"

    out += r"\textbf{Debt Service Coverage (times)}" + ' '.join([f"& {round(i,2)}" for i in debt_service.debt_service_ratio]) + " \\\\ \\hline"


    out += r"""
    \end{tabular}

    \end{flushleft}
    """

    return out
