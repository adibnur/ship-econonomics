def generate_tex_file(payback_period, out_path):
    out = r"""
    \documentclass{article}
    \usepackage[utf8]{inputenc}
    \usepackage{fullpage}
    \usepackage[table]{xcolor}
    \renewcommand{\familydefault}{\sfdefault}


    \begin{document}

    \begin{flushleft}
    \begin{huge}
    \textbf{Annex XIV Payback Period}
    \end{huge}
    \end{flushleft}

    \vspace{1cm}

    \def\arraystretch{1.2}
    \begin{flushleft}

    \begin{tabular}{|p{2cm}|p{2cm}|p{2cm}|p{2cm}|p{2cm}|}
        \hline
        \rowcolor[HTML]{03c8a8}
        """

    columns = ' '.join([f"\\textbf{'{'+col+'}'} &" for col in payback_period.table_payback_period.columns]).replace('%', '\\%')[:-2] + "\\\\ \\hline \n"
    out += columns

    rows = ''
    for row in payback_period.table_payback_period.values:
        rows += f"{int(row[0])} & " + ' '.join([f"{round(i,2)} &" for i in row[1:]])[:-1] + "\\\\ \\hline \n"

    out += rows

    out += r"""
    \end{tabular}

    \end{flushleft}

    \end{document}"""

    with open(out_path, "w") as f:
        f.write(out)
