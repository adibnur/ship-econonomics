"""
This is for use in generating outputs from created project folders only
"""
from pathlib import Path
from core import annex_lib
from core import tex_generators
from core.map_inputs import input_flow

if __name__=='__main__':
    project_name = input("Enter project name: ")
    while not Path('Projects\\'+project_name).is_dir():
        print("There are no projects named - " + project_name)
        project_name = input("Please enter a new project_name: ")

    project_path = 'Projects\\'+project_name

    inp_flow = input_flow(
        df_staff= project_path + '\\input_staff.xlsx',
        df_technical= project_path + '\\input_technical.xlsx',
        df_financial= project_path + '\\input_financial.xlsx'
    )

    # Make output directory for storing .tex output files
    Path(project_path + "\\Output Files").mkdir()

    # Generating IRR .tex file
    irr = annex_lib.IRR(inp_flow)
    tex_generators.IRR_tex.generate_tex_file(irr, project_path+"\\Output Files\\IRR.tex")
