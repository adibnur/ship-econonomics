def generate_appendix_tex(cost_benefit, out_path, column_color='b0e0e6'):
    out = get_tex_table(cost_benefit=cost_benefit, column_color=column_color)
    with open(out_path, "w") as f:
        f.write(out)

def generate_tex_file(cost_benefit, out_path, column_color='b0e0e6'):
    out = r"""\documentclass{article}
    \usepackage[utf8]{inputenc}
    \usepackage{fullpage}
    \usepackage[table]{xcolor}
    \renewcommand{\familydefault}{\sfdefault}

    \begin{document}"""

    out += get_tex_table(cost_benefit=cost_benefit, column_color=column_color)

    out += r"\end{document}"
    with open(out_path, "w") as f:
        f.write(out)

def get_tex_table(cost_benefit, column_color='b0e0e6'):
    out = r"""
    \begin{flushleft}
    \begin{huge}
    \textbf{Cost-Benefit Analysis}
    \end{huge}
    \end{flushleft}

    \vspace{1cm}

    \def\arraystretch{1.2}
    \begin{flushleft}

    \begin{tabular}{|p{1cm}|p{1.5cm}|p{1.5cm}|p{1.5cm}|p{1.75cm}|p{1.75cm}|p{1.5cm}|p{1.5cm}|p{1.75cm}|}
        \multicolumn{8}{r}{BDT in Lac}\\
        \hline
        """
    out += r"\rowcolor[HTML]" + "{" + column_color + "}"


    columns = ' '.join([f"\\textbf{'{'+col+'}'} &" for col in cost_benefit.table.columns]).replace('%', '\\%')[:-2] + "\\\\ \\hline \n"
    out += columns

    rows = ''
    for row in cost_benefit.table.values:
        rows += f"{int(row[0])} & " + ' '.join([f"{round(i,2)} &" for i in row[1:]])[:-1] + "\\\\ \\hline \n"

    out += rows


    out += r"\multicolumn{5}{|c|}{\textbf{Total}} & " + f"{round(cost_benefit.present_val_cost.sum(), 2)}" + r"  & \textbf{Total} & " + f"{round(cost_benefit.present_val_revenue.sum(), 2)}" + "\\\\ \hline"

    out += r"""
    \end{tabular}

    \vspace{1cm}

    \begin{tabular}{|p{5cm}|c|}

        \hline
        """

    out += r"\rowcolor[HTML]" + "{" + column_color + "}"

    out += r"\textbf{Benefit Cost Ratio (BCR)} &" + f"{round(cost_benefit.cost_benefit_ratio, 2)}" + ": 1" + " \\\\ \hline"

    out += r"""
    \end{tabular}
    \end{flushleft}
    """

    return out
