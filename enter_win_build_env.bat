@echo off

set BUILD_ENV=_win_build_env

python -m virtualenv %BUILD_ENV%
cd %BUILD_ENV%
Scripts/activate.bat
