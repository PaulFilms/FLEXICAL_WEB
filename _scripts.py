import os
import subprocess

print()
print("START FLEXICAL WEB SCRIPT ------------")
print()

print("SYS PATH:")
print(os.getcwd())
print()

print("VENV Activate ... [Write 1 to continue]")
if input("_ ") == "1":
    venv_path = os.path.join(os.getcwd(), r".venv\Scripts\activate.bat")
    subprocess.call(venv_path, shell=True, stdout=subprocess.PIPE)

print("UPDATE pip modules ... [Write 1 to continue]")
if input("_ ") == "1":
    # pip install git+https://github.com/PaulFilms/PyReports.git@main -U
    subprocess.run(["pip", "install", "git+https://github.com/PaulFilms/PyReports@main", "-U"])
    # pip install git+https://github.com/PaulFilms/Flexical@main -U
    subprocess.run(["pip", "install", "git+https://github.com/PaulFilms/Flexical@main", "-U"]) 
print()

print("FIN ------------------------------")
print()

# Instalación de un modulo editable (-e) (--editable)
# pip install -e git+https://github.com/PaulFilms/pydeveloptools.git#egg=pydeveloptools