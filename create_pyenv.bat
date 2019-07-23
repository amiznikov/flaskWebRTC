python -m venv pyenv
@echo cmd.exe "/k cd %%CD%%\pyenv\Scripts & activate.bat & cd %%CD%%">pyenv.bat
@echo cmd.exe "/c cd %%CD%%\pyenv\Scripts & activate.bat & cd %%CD%% & pip freeze > requirements.txt">update_requirments.bat
call pyenv.bat
