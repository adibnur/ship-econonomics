def generate_tex_file(IRR, out_path, column_color='b0e0e6'):
    out = r"""\documentclass{article}
    \usepackage[utf8]{inputenc}
    \usepackage{fullpage}
    \usepackage[table]{xcolor}
    \renewcommand{\familydefault}{\sfdefault}


    \begin{document}"""

    out += get_tex_table(IRR=IRR, column_color=column_color)

    out += r"\end{document}"
    with open(out_path, "w") as f:
        f.write(out)

def get_tex_table(IRR, column_color='b0e0e6'):
    out = r"""
    \begin{flushleft}
    \begin{huge}
    \textbf{Internal Rate of Return}
    \end{huge}
    \end{flushleft}

    \vspace{1cm}

    \def\arraystretch{1.2}
    \begin{flushleft}

    \begin{tabular}{|p{2cm}|p{2cm}|p{2cm}|p{2cm}|}
    \multicolumn{4}{r}{BDT in Lac}\\
        \hline
        """
    out += r"\rowcolor[HTML]" + "{" + column_color + "}"

    columns = ' '.join([f"\\textbf{'{'+col+'}'} &" for col in IRR.table_irr.columns]).replace('%', '\\%')[:-2] + "\\\\ \\hline \n"
    out += columns

    rows = ''
    for row in IRR.table_irr.values:
        rows += f"{int(row[0])} & " + ' '.join([f"{round(i,2)} &" for i in row[1:]])[:-1] + "\\\\ \\hline \n"

    out += rows


    out += "\\multicolumn{3}{|c|}{\\textbf{NPV}} & " + f"{round(IRR.table_irr.T.values[-1].sum(), 2)}" + " \\\\ \\hline \n"

    out += r"""
    \end{tabular}

    \vspace{1cm}

    \begin{tabular}{|p{5cm}|c|}

        \hline
        """

    out += r"\rowcolor[HTML]" + "{" + column_color + "}"

    out += "\\textbf{Internal Rate of Return} &" + f"{round(IRR.irr*100, 2)}" + "\% \\\\ \hline \n"

    out += r"""
    \end{tabular}
    \end{flushleft}
    """
    return out
