"""
This is for use in generating outputs from created project folders only
"""
from pathlib import Path
from core import annex_lib
from core import tex_generators
from core.map_inputs import input_flow

if __name__=='__main__':
    project_name = input("Enter project name: ")

    while True:
        try:
            Path('Projects/'+project_name).is_dir()
            break
        except:
            print("Invalid project name")
            project_name = input("Please enter a valid project name: ")

    while not Path('Projects/'+project_name).is_dir():
        print("There are no projects named - " + project_name)
        project_name = input("Please enter a new project_name: ")

    project_path = 'Projects/'+project_name

    inp_flow = input_flow(
        df_staff= project_path + '/input_staff.xlsx',
        df_technical= project_path + '/input_technical.xlsx',
        df_financial= project_path + '/input_financial.xlsx'
    )

    # Make output directory for storing .tex output files
    Path(project_path + "/Output Files").mkdir(exist_ok=True)
    Path(project_path + "/Output Files/Appendix").mkdir(exist_ok=True)

    # Generating IRR .tex file
    irr = annex_lib.IRR(inp_flow)
    tex_generators.IRR_tex.generate_appendix_tex(irr, project_path+"/Output Files/Appendix/IRR.tex")

    # Generating Cost Benefit Analysis .tex file
    cba = annex_lib.cost_benefit_analysis(inp_flow)
    tex_generators.cost_benefit_tex.generate_appendix_tex(cba, project_path+"/Output Files/Appendix/Cost Benefit Analysis.tex")

    # Generating Debt Service Coverage Ratio .tex file
    dscr = annex_lib.debt_service_coverage(inp_flow)
    tex_generators.debt_service_tex.generate_appendix_tex(dscr, project_path+"/Output Files/Appendix/Debt Service Coverage.tex")

    # Generating Payback Period .tex file
    pbp = annex_lib.payback_period(inp_flow)
    tex_generators.payback_period_tex.generate_appendix_tex(pbp, project_path+"/Output Files/Appendix/Payback Period.tex")

    # Generating Break Even Analysis .tex file
    bea = annex_lib.break_even_analysis(inp_flow)
    tex_generators.break_even_tex.generate_appendix_tex(bea, project_path+"/Output Files/Appendix/Break Even Analysis.tex")

    # Generating Chapter 1
    tex_generators.chapter_1.generate_chapter1_tex(inp_flow, project_path+"/Output Files/Appendix/Chapter 1.tex")

    # Generating Report
    tex_generators.report.generate_report_tex(inp_flow, project_path+"/Output Files/Report.tex")
