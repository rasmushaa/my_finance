## How to install
1. Primary packages used in the project are located in the **requirements.in**  
Use `pip-compile requirements.in` to create the actual **requirements.txt** file.  
The compile command will automatically seek suitable secondary packages,  
required by the primary ones, to fulfill all version requirements.
2. Create a new venv and install specified packages `pip install -r requirements.txt`
3. Use `pip-sync` to remove all unecessary packages from the venv.
(By default, conda will install a large amount of default packages, such as Pill, Tkinter, Qt-toolkits, etc. which will cause the application to launch very slowly, when used the `onefile` mode of the `pyinstaller` since it has to always extract everything to some random temp-folder before running)
4. Activate your venv on the project folder and run `pyinstaller main.spec`. This will create two new directories: `build` and `dist`. You will find your **the application** (main.exe) in the `dist/main.app`. If it does not work, try to use the terminal version of the application in the `dist/main/main`, which will print out all generated errors.



## Project structure
```
my_finance/  
├── main.py  
├── main.spec  
├── requirements.in  
├── requirements.txt  
└── src/  
    ├── assets/  
    │   └── images/  
    │       └── logo.icns  
    ├── back_end/  
    │   ├── bigquery/  
    │   │   ├── __init__.py  
    │   │   └── api.py  
    │   ├── categories/  
    │   │   ├── __init__.py  
    │   │   ├── api.py  
    │   │   ├── assets.json  
    │   │   └── categories.json  
    │   ├── ml/  
    │   │   ├── __init__.py  
    │   │   ├── api.py  
    │   │   ├── model_delta.py  
    │   │   └── model.pkl  
    │   ├── parsing/  
    │   │   ├── __init__.py  
    │   │   ├── api.py  
    │   │   └── file_types.json  
    │   └── profiles/  
    │       ├── __init__.py  
    │       ├── api.py  
    │       ├── profiles.json  
    │       └── user.py  
    └── front_end/  
        ├── main_window/  
        │   ├── __init__.py  
        │   ├── dialog/  
        │   │   ├── __init__.py  
        │   │   ├── add_asset.py  
        │   │   ├── add_profile.py  
        │   │   ├── add_transaction.py  
        │   │   └── selection_from_list.py  
        │   ├── gui.py  
        │   └── gui_state.json  
        ├── tab_assets/  
        │   ├── __init__.py  
        │   ├── table/  
        │   │   ├── __init__.py  
        │   │   ├── model.py  
        │   │   └── view.py  
        │   └── window.py  
        ├── tab_transaction/  
        │   ├── __init__.py  
        │   ├── dialog/  
        │   │   ├── __init__.py  
        │   │   └── file.py  
        │   ├── table/  
        │   │   ├── __init__.py   
        │   │   ├── combo.py   
        │   │   ├── model.py   
        │   │   └── view.py   
        │   └── window.py   
        └── utils/  
            ├── __init__.py  
            └── message.py
```
