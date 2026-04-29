@echo off
setlocal enabledelayedexpansion
TITLE Aegis Overwatch - Strategic Deployment v6.0-FULL-CLOUD
color 0b
cd /d "%~dp0"

echo.
echo ==================================================================
echo [ AEGIS DEPLOYMENT - FULL DEBUG MODE ]
echo ==================================================================
echo.

:: 1. Elevation Check
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] PERMISSION DENIED: Run as Administrator.
    pause
    exit
)

echo [~] Python check...
for /f "tokens=2" %%I in ('python -V 2^>^&1') do set "PYVER=%%I"
echo [+] Found Python: !PYVER!

:: Pre-flight cleanup
echo [*] Cleaning old processes...
powershell -Command "Get-CimInstance Win32_Process -Filter \"Name = 'python.exe' OR Name = 'pythonw.exe'\" | Where-Object { $_.CommandLine -match 'aegis_' -or $_.CommandLine -match 'c2_socket' } | Invoke-CimMethod -MethodName Terminate" >nul 2>&1

set TARGET_DIR=C:\Aegis-Overwatch
if /i "%~dp0" == "%TARGET_DIR%\" goto BUILD_PHASE

:RELOCATION_PHASE
echo [*] Relocating to C:\Aegis-Overwatch...
if not exist "%TARGET_DIR%" mkdir "%TARGET_DIR%"
xcopy /E /I /H /Y "%~dp0*" "%TARGET_DIR%" >nul 2>&1
powershell -Command "Start-Process cmd -ArgumentList '/c \"\"%TARGET_DIR%\%~nx0\"\"' -Verb RunAs"
exit

:BUILD_PHASE
cls
echo ============================================================================
echo                      [ PROVISIONING NEURAL ENVIRONMENT ]
echo ============================================================================

:: Vault
if not exist "%TARGET_DIR%\.env" (
    echo [*] Creating .env template...
    echo # AEGIS OVERWATCH CORE SECRETS > "%TARGET_DIR%\.env"
    echo AI_ENGINE_MODE=CLOUD >> "%TARGET_DIR%\.env"
    echo GEMINI_API_KEY=your_gemini_key_here >> "%TARGET_DIR%\.env"
    echo AEGIS_API_KEY=your_custom_security_password >> "%TARGET_DIR%\.env"
    echo VT_API_KEY=your_virustotal_key_here >> "%TARGET_DIR%\.env"
    echo LOCAL_MODEL_ID=llama3.2:1b >> "%TARGET_DIR%\.env"
)

:: Regenerate Switch.bat every time
del /f /q "%TARGET_DIR%\Aegis-Switch.bat" >nul 2>&1

:: VENV - FORCE CLEAN REINSTALL
echo [*] Setting up Virtual Environment...
if exist "venv" (
    echo [!] Old venv found - deleting for clean install...
    rd /s /q venv
)
python -m venv venv
if %errorlevel% neq 0 (
    echo [!] VENV creation failed!
    pause
    exit
)

echo [*] Upgrading pip...
"venv\Scripts\python.exe" -m pip install --upgrade pip --quiet

echo.
echo [*] Installing ALL dependencies (with full debug output)...
echo     This may take a few minutes...
echo.

"venv\Scripts\python.exe" -m pip install --upgrade --prefer-binary ^
    fastapi uvicorn starlette jinja2 python-multipart psutil python-dotenv colorama requests geoip2 openai google-generativeai onnxruntime scapy --no-cache-dir

"venv\Scripts\python.exe" -m pip install -r requirements.txt --prefer-binary --no-cache-dir

echo.
echo [+] Neural Environment Hardened.
echo     Checking for jinja2...
"venv\Scripts\python.exe" -c "import jinja2; print('[+] jinja2 installed successfully')" 2>nul || echo [!] jinja2 STILL MISSING!

:: Windows policies
echo [*] Provisioning Windows Audit Policies...
reg add "HKEY_LOCAL_MACHINE\Software\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging" /v EnableScriptBlockLogging /t REG_DWORD /d 1 /f >nul
gpupdate /force >nul 2>&1
echo [+] Core Windows Auditing Enabled.

:: Ollama
echo [*] Optimizing Sovereign Core (Local LLM)...
setx OLLAMA_KEEP_ALIVE "-1" /M >nul 2>&1
taskkill /F /IM "ollama app.exe" >nul 2>&1
taskkill /F /IM "ollama.exe" >nul 2>&1

if not exist "%LOCALAPPDATA%\Programs\Ollama\ollama app.exe" (
    echo [*] Installing Ollama automatically...
    powershell -Command "irm https://ollama.com/install.ps1 | iex"
    timeout /t 20 >nul
)
if exist "%LOCALAPPDATA%\Programs\Ollama\ollama app.exe" (
    start "" "%LOCALAPPDATA%\Programs\Ollama\ollama app.exe" >nul 2>&1
    echo [+] Ollama started.
)

:: Profiler
echo [*] Running Smart Machine DNA Profiling...
"venv\Scripts\python.exe" aegis_profiler.py
if %errorlevel% neq 0 (
    echo [!] DNA Profiling failed!
    pause
    exit
)
echo [+] Base DNA established.

:: Shortcut
echo [*] Creating Desktop Shortcut...
set SCRIPT="%TEMP%\AegisLink.vbs"
echo Set oWS = WScript.CreateObject("WScript.Shell") > %SCRIPT%
echo sLinkFile = oWS.ExpandEnvironmentStrings("%%USERPROFILE%%\Desktop\Aegis Overwatch.lnk") >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "C:\Aegis-Overwatch\Aegis-Switch.bat" >> %SCRIPT%
echo oLink.WorkingDirectory = "C:\Aegis-Overwatch" >> %SCRIPT%
echo oLink.IconLocation = "C:\Aegis-Overwatch\aegis.ico" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%
cscript /nologo %SCRIPT% >nul 2>&1
del %SCRIPT%

echo.
echo ============================================================================
echo [ 🛡️ AEGIS OVERWATCH: DEPLOYMENT COMPLETE ]
echo ============================================================================
echo.

:: Generate final switch (clean version)
echo [*] Generating final Aegis-Switch.bat...
(
echo @echo off
echo TITLE Aegis Overwatch - Core Orchestration Server ^(C2^)
echo color 0b
echo cd /d "%%~dp0"
echo net session ^>nul 2^>^&1
echo if %%errorLevel%% neq 0 ^(powershell -Command "Start-Process '%%~dpnx0' -Verb RunAs" ^& exit /b^)
echo echo ============================================================================
echo echo   [ /// AEGIS OVERWATCH: IGNITION NEXUS /// ]
echo echo ============================================================================
echo powershell -Command "Get-CimInstance Win32_Process -Filter \"Name = 'python.exe' OR Name = 'pythonw.exe'\" ^| Where-Object { $_.CommandLine -match 'aegis_' -or $_.CommandLine -match 'c2_socket' } ^| Invoke-CimMethod -MethodName Terminate" ^>nul 2^>^&1
echo echo [+] Environment mathematically sterilized.
echo if exist "%%LOCALAPPDATA%%\Programs\Ollama\ollama app.exe" ^(start "" "%%LOCALAPPDATA%%\Programs\Ollama\ollama app.exe" ^& timeout /t 3 ^>nul^)
echo echo [*] Booting FastAPI Orchestration Server...
echo timeout /t 6 ^>nul
echo start http://localhost:8000/dashboard
echo if exist "venv\Scripts\activate.bat" ^(call "venv\Scripts\activate.bat"^)
echo python aegis_server.py
echo pause
) > "Aegis-Switch.bat"

echo [*] Igniting C2 Console...
start "" "C:\Aegis-Overwatch\Aegis-Switch.bat"
echo.
echo Press any key to close deploy window...
pause >nul
exit