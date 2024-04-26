@echo off
setlocal

set PYTHON_VERSION=3.9.7

:: Read link from link.txt
set /p LINK=<link.txt

:: Download archive from the link
curl %LINK% --output archive.zip

:: Unzip archive
tar -xf archive.zip

:: Delete downloaded archive
del archive.zip

:: Install Python
choco install python --version %PYTHON_VERSION% -y

:: Install python pip
choco install pip -y

:: Install python venv
python -m pip install virtualenv

:: Create and activate virtual environment
python -m venv myenv
myenv\Scripts\activate

endlocal
pause
::exit