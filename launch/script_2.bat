@echo off
setlocal

REM Read link from link.txt file
set /p link=<link.txt

REM Download archive from the provided link
echo Downloading archive from %link%...
set file=%link:~ -1%
curl -o %file% %link%

REM Extract archive using base name of the file
echo Extracting archive %file%...
set baseName=%~n0
7z x %file%

REM Delete downloaded archive
echo Deleting downloaded archive...
del %file%

REM Install python, pip and venv
echo Installing Python, pip and venv...
choco install python3
python -m ensurepip
pip install virtualenv

REM Create and activate virtual environment
echo Creating and activating virtual environment...
python -m venv %baseName%
%baseName%\Scripts\activate

echo Virtual environment created and activated.

endlocal
exit /b 0