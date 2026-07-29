---
name: windows-batch-scripting
description: "Use when writing .bat/.cmd scripts for Windows automation."
category: software-development
tags: [batch, bat, cmd, windows, scripting, automation]
---
# Windows Batch Scripting

Writing production-grade .bat/.cmd scripts for Windows automation.

## Structure

```batch
@echo off
setlocal enabledelayedexpansion

REM === CONFIG ===
set "APP_NAME=MyTool"
set "LOG_FILE=%~dpn0.log"

REM === MAIN ===
call :check_admin
call :do_work
goto :eof

REM === FUNCTIONS ===
:check_admin
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting admin...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)
goto :eof

:do_work
echo Working...
goto :eof
```

## Key Patterns

### Argument Parsing
```batch
if "%~1"==""     echo No args & exit /b 1
if /I "%~1"=="/?"  call :help & exit /b 0
if /I "%~1"=="--help"  call :help & exit /b 0
set "ACTION=%~1"
set "TARGET=%~2"
shift /1
```

### Error Handling
```batch
call :some_func
if %errorlevel% neq 0 (
    echo ERROR: Function failed with code %errorlevel%
    exit /b %errorlevel%
)
```

### For Loops
```batch
REM Files in directory
for %%f in (*.txt) do echo %%f

REM Line-based (command output)
for /f "tokens=*" %%l in ('dir /b *.txt') do echo %%l

REM Delimited parsing
for /f "tokens=1,2 delims=," %%a in (data.csv) do echo %%a = %%b

REM Range
for /l %%i in (1,1,10) do echo %%i
```

### String Operations
```batch
set "var=hello world"
echo %var:~0,5%     REM hello
echo %var:~6%       REM world
echo %var:world=there%  REM hello there
if /I "%var%"=="hello world" echo match
```

### Delayed Expansion (important!)
```batch
setlocal enabledelayedexpansion
set "count=0"
for %%f in (*.txt) do (
    set /a count+=1
    echo !count!: %%f     REM use !var! not %%var%% inside loops
)
```

### File/Dir Checks
```batch
if exist "C:\path\file.txt" echo exists
if not exist "C:\path\" mkdir "C:\path"
if defined MYVAR echo MYVAR is set
```

### Admin Elevation
```batch
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Elevating...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)
```

## Common Functions

```batch
:log
echo [%date% %time%] %* >> "%LOG_FILE%"
goto :eof

:confirm
set /p ans="%* [y/N] "
if /I "%ans%"=="y" exit /b 0
exit /b 1

:die
echo FATAL: %*
pause
exit /b 1
```

## Pitfalls

- **%errorlevel%** must be checked IMMEDIATELY after command -- gets overwritten
- **Delayed expansion** needed for !var! inside loops and if blocks
- **Spaces in paths** -- always quote: "C:\Program Files\..."
- **`%~dp0`** gives script directory with trailing backslash
- **`set /p`** leaves variable unchanged if user presses Enter (not empty)
- **`findstr`** is the closest to grep -- use `findstr /i pattern file`
- **PowerShell** is better for anything beyond basic scripting -- consider switching
