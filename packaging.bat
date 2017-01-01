@echo off

echo "----- start clean -----"
pyinstaller cli.py --clean --noconfirm
echo "----- complete clean -----"

echo "----- start build -----"
pyinstaller cli.py --onefile --name sqlitebiter_win_x64 --noconfirm
echo "----- complete build -----"

echo "----- start compress -----"
set BIN_PATH=dist/sqlitebiter_win_x64
powershell compress-archive -Force %BIN_PATH%.exe %BIN_PATH%.zip
echo "----- complete compress -----"

pause
