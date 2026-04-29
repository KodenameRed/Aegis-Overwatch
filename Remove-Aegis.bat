@echo off
TITLE AEGIS OVERWATCH - Full System Removal
color 0c
cd /d "%~dp0"

:: 1. Elevation Check
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] ERROR: Administrative privileges required to remove system hooks.
    echo Please right-click this file and select "Run as Administrator".
    pause & exit
)

echo ========================================================
echo   ⚠️  WARNING: PERMANENT REMOVAL INITIATED  ⚠️
echo ========================================================
echo.
echo This will terminate all Aegis processes, revert all Windows
echo Registry security modifications, stop kernel trace sessions,
echo and delete the system-root folder (C:\Aegis-Overwatch).
echo.
set /p CONFIRM="Are you absolutely sure? (Y/N): "
if /i "%CONFIRM%" neq "Y" exit

echo.
echo [*] PHASE 1: Terminating Active Sentinels & Kernel Traces...
:: Surgically kill ONLY Python workers tied to Aegis (now looking for core/ components too)
powershell -Command "Get-CimInstance Win32_Process -Filter \"Name = 'python.exe' OR Name = 'pythonw.exe'\" | Where-Object { $_.CommandLine -match 'Orchestration_layer' -or $_.CommandLine -match 'aegis_' -or $_.CommandLine -match 'c2_socket' } | Invoke-CimMethod -MethodName Terminate" >nul 2>&1
taskkill /f /im wscript.exe /t >nul 2>&1

:: Stop any orphaned Event Tracing (ETW) sessions to prevent memory leaks
for /f "tokens=1" %%i in ('logman query -ets ^| findstr /i "aegis"') do logman stop %%i -ets >nul 2>&1

echo [*] PHASE 2: Reverting System Registry & Environment Changes...
:: Revert PowerShell ScriptBlock Auditing
reg delete "HKEY_LOCAL_MACHINE\Software\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging" /v EnableScriptBlockLogging /f >nul 2>&1
reg delete "HKEY_LOCAL_MACHINE\Software\Policies\Microsoft\PowerShellCore\ScriptBlockLogging" /v EnableScriptBlockLogging /f >nul 2>&1
gpupdate /force >nul 2>&1

:: Remove Ollama VRAM Hot-State & Bounce Daemon to apply
REG delete "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /F /V OLLAMA_KEEP_ALIVE >nul 2>&1
taskkill /F /IM "ollama app.exe" >nul 2>&1
taskkill /F /IM "ollama.exe" >nul 2>&1
start "" "%LOCALAPPDATA%\Programs\Ollama\ollama app.exe" >nul 2>&1

echo [*] PHASE 3: Scrubbing Persistence Hooks & Shortcuts...
schtasks /delete /tn "Aegis_Overwatch_Engine" /f >nul 2>&1
if exist "%USERPROFILE%\Desktop\Aegis Overwatch.lnk" del "%USERPROFILE%\Desktop\Aegis Overwatch.lnk"

echo [*] PHASE 4: Purging System Root [C:\Aegis-Overwatch]...
:: Release directory lock in case the user ran this from inside the Aegis folder
cd \
:: Give Windows a moment to release SQLite file handles after the taskkill
timeout /t 3 >nul
if exist "C:\Aegis-Overwatch" (
    rmdir /s /q "C:\Aegis-Overwatch"
)

echo.
echo ========================================================
echo [ ✅ AEGIS OVERWATCH REMOVED SUCCESSFULLY ]
echo ========================================================
echo.
echo Note: If the C:\Aegis-Overwatch folder remained, a file 
echo (like the SQLite DB) may be locked by a background process. 
echo Please reboot your PC and run this script one more time, or 
echo manually delete the folder.
echo.
pause