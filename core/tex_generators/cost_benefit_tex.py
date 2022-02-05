def generate_tex_file(cost_benefit, out_path):
    out = r"""
    \documentclass{article}
    \usepackage[utf8]{inputenc}
    \usepackage{fullpage}
    \usepackage[table]{xcolor}
    \renewcommand{\familydefault}{\sfdefault}


    \begin{document}

    \begin{flushleft}
    \begin{huge}
    \textbf{Annex XII Cost-Benefit Analysis}
    \end{huge}
    \end{flushleft}

    \vspace{1cm}

    \def\arraystretch{1.2}
    \begin{flushleft}

    \begin{tabular}{|p{1cm}|p{1cm}|p{2cm}|p{1cm}|p{2cm}|p{1cm}|p{2cm}|p{2cm}|p{1cm}|}
        \hline
        \rowcolor[HTML]{03c8a8}
        """

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
        \rowcolor[HTML]{03c8a8}
        """
    out += r"\textbf{Benefit Cost Ratio} &" + f"{round(cost_benefit.cost_benefit_ratio, 2)}" + " \\\\ \hline"

    out += r"""
    \end{tabular}
    \end{flushleft}

    \end{document}
    """
    with open(out_path, "w") as f:
        f.write(out)
