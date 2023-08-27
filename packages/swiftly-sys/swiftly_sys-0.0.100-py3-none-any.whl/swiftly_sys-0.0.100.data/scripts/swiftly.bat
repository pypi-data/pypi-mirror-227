@echo off
setlocal enabledelayedexpansion

:: Check if the first argument is "activate"
echo Before activate check
if "%~1"=="activate" (
    echo Inside activate check
    call :activate
    exit /b 0
)
echo After activate check



:: Define the activate function
:activate
:: Run check_swiftly from swiftly.core.main.py
for /f %%i in ('python3 -c "from swiftly.core.main import check_swiftly; check_swiftly()"') do set result=%%i

:: Handle the result
if "%result%"=="makealive" (
    call :makealive
    exit /b 0
) else if "%result%"=="exit" (
    exit /b 0
) else if "%result%"=="continue" (
    :: Continue with the rest of the script
) else (
    echo Unexpected result from check_swiftly: %result%
    exit /b 1
)

:: Update swiftly
python3 -c "from swiftly.core.main import update_swiftly; update_swiftly()"

:: Get swiftly project name
for /f %%i in ('python3 -c "from swiftly.utils.get import get_name; print(get_name())"') do set project_name=%%i
set SWIFTLY_PROJECT_NAME=%project_name%
set SWIFTLY_PROJECT_LOCATION=%cd%

:: Modify the shell prompt (Note: This might not work as expected in Batch)
set OLD_PS1=%PROMPT%
:: git pull
python3 -c "from swiftly.utils.git import git_pull; git_pull()"

:: Get swiftly project runtime
for /f %%i in ('python3 -c "from swiftly.utils.get import get_runtime; print(get_runtime())"') do set runtime=%%i

:: Source the appropriate script and run the activate function
call swiftly-%runtime%.bat
call :activate_%runtime%

:: Modify the prompt (Note: This might not work as expected in Batch)
set PROMPT=(swiftly %SWIFTLY_PROJECT_NAME%) %OLD_PS1%
set SWIFTLY_ACTIVATED=true

goto :eof
