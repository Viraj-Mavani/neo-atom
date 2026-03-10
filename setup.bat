@echo off
echo ==============================================
echo Neo-Atom Virtual Environment Setup
echo ==============================================

echo [1/3] Creating Python Virtual Environment (venv)...
python -m venv venv

echo [2/3] Activating venv...
call venv\Scripts\activate.bat

echo [3/3] Upgrading pip and installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo ==============================================
echo Setup Complete!
echo To begin developing, ensure you are using the venv by running:
echo   call venv\Scripts\activate.bat
echo ==============================================
pause
