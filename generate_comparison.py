from pathlib import Path
import os

def get_verified_project_name():
    project_name = input(">")
    while not Path('Projects\\'+project_name).is_dir():
        print("No such project found. Please enter an existing project's name.")
        project_name = input(">")

    while not Path('Projects\\'+project_name+'\\Output Files\\Report.tex').is_file():
        print(f"Please generate output for project {project_name} before continuing.")
        print("Enter project name:")
        project_name = input(">")

    return project_name

def generate_diff_file(p1, p2):
    output_file = f"Projects\\{p2}\\Output Files\\comparison {p1}.tex"
    p1_dir = f"Projects\\{p1}\\Output Files\\Report.tex"
    p2_dir = f"Projects\\{p2}\\Output Files\\Report.tex"

    diff_command = f"latexdiff \"{p1_dir}\" \"{p2_dir}\" > \"{output_file}\""
    os.system(diff_command)

    return output_file #returns path of generated diff file

if __name__=='__main__':
    print("Enter project names to generate comparinson.")
    print("Enter first project's name:")
    p1 = get_verified_project_name()
    print("Enter second project's name:")
    p2 = get_verified_project_name()

    out_diff_path = generate_diff_file(p1, p2)

    with open(out_diff_path, 'r') as f:
        diff_tex = f.read()
        diff_tex = diff_tex.replace(r"\documentclass{report}",
                        r"""
                        \documentclass{report}
                        \usepackage{soulutf8}
                        """)
        diff_tex = diff_tex.replace(r"\providecommand{\DIFadd}[1]{{\protect\color{blue}\uwave{#1}}}",
                        r"\providecommand{\DIFadd}[1]{{\protect\hl{#1}}}")
        diff_tex = diff_tex.replace(r"\providecommand{\DIFdel}[1]{{\protect\color{red}\sout{#1}}}",
                        r"\providecommand{\DIFdel}[1]{}")


    os.system(f"del \"{out_diff_path}\"")

    with open(out_diff_path, 'w') as f:
        f.write(diff_tex)
