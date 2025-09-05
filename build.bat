@echo off
echo Installing PyInstaller if not already installed...
pip install pyinstaller

echo Running PyInstaller...
pyinstaller --onefile  ^
--add-data "tor-expert-bundle-windows-i686-13.5.3;tor-expert-bundle-windows-i686-13.5.3" ^
main.py

echo Build complete. Check the 'dist' folder for the executable.
pause
