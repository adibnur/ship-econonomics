def generate_tex_file(break_even, out_path, column_color='b0e0e6'):
    out = get_tex_table(break_even=break_even, column_color=column_color)
    with open(out_path, "w") as f:
        f.write(out)

def get_tex_table(break_even, column_color='b0e0e6'):
    out = r"""
    \documentclass[10pt, a4paper]{article}
    \usepackage[utf8]{inputenc}
    \usepackage{fullpage}
    \usepackage[table]{xcolor}
    \renewcommand{\familydefault}{\sfdefault}

    \begin{document}

    \begin{huge}
    \textbf{Break-even Analysis}
    \end{huge}

    \vspace{1cm}

    \def\arraystretch{1.2} %extra padding in the table
    \begin{flushleft}

    \begin{tabular}{|p{3cm}|c|c|c|c|c|c|c|c|}
        \multicolumn{9}{r}{BDT in Lac}\\
        \hline
        %\multicolumn{9}{|c|}{\textbf{Break-even Analysis}}\\ \hline
        """

    out += '\n' + r"\rowcolor[HTML]" + "{" + column_color + "}"
    out += '\n' + r"\multicolumn{1}{|c|}{} & \multicolumn{8}{c|}{\textbf{Year}}\\ \hline"
    out += '\n' + r"\rowcolor[HTML]" + "{" + column_color + "}"
    out += '\n' + '\\textbf{Item} & ' + ' '.join(["\\textbf{"+str(i)+"} &" for i in break_even.table_var_cost.columns])[:-1] + '\\\\ \\hline'

    out += '\n' + r'\textbf{Capacity utilization in \%} & ' + ' '.join([f"{(i*100)} &" for i in break_even.cap_util])[:-1] + '\\\\ \\hline'

    out += '\n' + r'\textbf{Revenue} & ' + ' '.join([f"{(round(i, 2))} &" for i in break_even.revenue])[:-1] + '\\\\ \\hline'

    out += '\n' + r"\rowcolor[HTML]" + "{" + column_color + "}"

    out += '\n' + r"\multicolumn{9}{|c|}{\textbf{Variable cost}}\\ \hline"

    for ix, row in zip(break_even.table_var_cost.index, break_even.table_var_cost.values):
        out += '\n' + r"\textbf{"+ix+"}" + ' '.join([f" & {round(i, 2)}" for i in row]) + r'\\ \hline' + '\n'

    out += '\n' + r"\rowcolor[HTML]" + "{" + column_color + "}"
    out += '\n' + r"\multicolumn{9}{|c|}{\textbf{Total fixed cost}}\\ \hline"

    for ix, row in zip(break_even.table_fixed_cost.index, break_even.table_fixed_cost.values):
        out += '\n' + r"\textbf{"+ix+"}" + ' '.join([f" & {round(i, 2)}" for i in row]) + r'\\ \hline' + '\n'

    out += '\n' + r"\rowcolor[HTML]" + "{" + column_color + "}"

    out += '\n' + r"\multicolumn{9}{|c|}{\textbf{Annual regulated cost}}\\ \hline"

    for ix, row in zip(break_even.table_annual_reg_cost.index, break_even.table_annual_reg_cost.values):
        out += '\n' + r"\textbf{"+ix+"}" + ' '.join([f" & {round(i, 2)}" for i in row]) + r'\\ \hline' + '\n'

    for ix, row in zip(break_even.table_break_even.index, break_even.table_break_even.values):
        out += '\n' + r"\textbf{"+ix+"}" + ' '.join([f" & {round(i, 2)}" for i in row]) + r'\\ \hline' + '\n'

    out += '\n' + r"""
    \end{tabular}

    \end{flushleft}

    \end{document}
    """

    return out
