from .. import tex_generators
from .. import annex_lib

def generate_report_tex(inp_flow, out_path):
    out = r"""
    \documentclass{report}
    \usepackage[utf8]{inputenc}
    \usepackage{fullpage}
    \usepackage[table]{xcolor}
    \usepackage[a4paper, width=150mm, top=25mm, bottom=25mm]{geometry}
    \renewcommand{\familydefault}{\sfdefault}

    \begin{document}
    \thispagestyle{empty}
    \vspace*{\fill}
    \noindent
    \makebox[\textwidth]{\Huge \textbf{Project Report}}
    \vfill

    \newpage
    \chapter{Project Parameters and Financial Assumptions}
    """

    out += tex_generators.chapter_1.generate_chapter1_tables(inp_flow)

    out += "\\newpage \n"
    out += "\\chapter{Detailed Calculation} \n"

    irr = annex_lib.IRR(inp_flow)
    out += tex_generators.IRR_tex.get_tex_table(irr)

    out += "\\newpage \n"
    bea = annex_lib.break_even_analysis(inp_flow)
    out += tex_generators.break_even_tex.get_tex_table(bea)

    out += "\\newpage \n"
    cba = annex_lib.cost_benefit_analysis(inp_flow)
    out += tex_generators.cost_benefit_tex.get_tex_table(cba)

    out += "\\newpage \n"
    pbp = annex_lib.payback_period(inp_flow)
    out += tex_generators.payback_period_tex.get_tex_table(pbp)

    out += "\\newpage \n"
    dscr = annex_lib.debt_service_coverage(inp_flow)
    out += tex_generators.debt_service_tex.get_tex_table(dscr)


    out += "\n \\end{document}"
    

    with open(out_path, "w") as f:
        f.write(out)
