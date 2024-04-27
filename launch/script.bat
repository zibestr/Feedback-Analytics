@echo off
setlocal


:: Read link from link.txt
set /p LINK=<link.txt

:: Read link from link.txt
set /p LINK=<link.txt

echo Downloading archive from %link%...
:: Download archive from the link
curl -OL %link% --output archive.zip

:: Unzip archive
tar -xf models.zip

:: Delete downloaded archive
del models.zip



:: Download Python installer using curl
echo Downloading Python installer...
curl -l https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe -o python-3.12.3-amd64.exe
python-3.12.3-amd64.exe

echo Python installation completed.
:: Install python pip
python -m pip install --upgrade pip
:: Install python venv
python -m pip install virtualenv
:: Create and activate virtual environment
python -m venv myenv
myenv\Scripts\activate
endlocal
pause
::exit