## How to install
1. Primary packages used in the project are located in the **requirements.in**  
Use `pip-compile requirements.in` to create the actual **requirements.txt** file.  
The compile command will automatically seek suitable secondary packages,  
required by the primary ones, to fulfill all version requirements.
2. Create a new venv and install specified packages `pip install -r requirements.txt`
3. Use `pip-sync` to remove all unecessary packages from the venv.
(By default, conda will install a large amount of default packages, such as Pill, Tkinter, Qt-toolkits, etc. which will cause the application to launch very slowly, when used the `onefile` mode of the `pyinstaller` since it has to always extract everything to some random temp-folder before running)
4. Activate your venv on the project folder and run `pyinstaller main.spec`. This will create two new directories: `build` and `dist`. You will find your **the application** (main.exe) in the `dist/main.app`. If it does not work, try to use the terminal version of the application in the `dist/main/main`, which will print out all generated errors.
