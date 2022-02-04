from pathlib import Path
from shutil import copyfile
from glob import glob

if __name__=="__main__":
    project_name = input("Enter project name: ")

    while True:
        try:
            if Path('program\\'+project_name).is_dir():
                print("A project with the same name already exists.")
                project_name = input("Please enter a new project_name: ")
            else:
                break
        except:
            print("Invalid project name")
            project_name = input("Please enter a new project_name: ")

    while True:
        try:
            Path('program\\'+project_name).mkdir()
            break
        except:
            print("Invalid project name")
            project_name = input("Please enter a new project_name: ")

    for file in glob("program\\core\\sample_inputs\\*.xlsx"):
        copyfile(file, 'program\\'+project_name+'\\'+file.split('\\')[-1])

    #copyfile(r"program\core\input_helpers\generate_output.py", 'program\\'+project_name+'\\'+'generate_output.py')
