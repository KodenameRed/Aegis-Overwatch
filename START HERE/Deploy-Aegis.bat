@echo off
setlocal enabledelayedexpansion
TITLE Aegis Overwatch - Strategic Deployment v6.0-FULL-CLOUD
color 0b
cd /d "%~dp0"

:: 1. Elevation Check
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] PERMISSION DENIED: Aegis requires an Elevated Command Prompt.
    echo Please right-click this file and select "Run as Administrator".
    pause
    exit
)

echo [~] Checking Python Environment Requirements...
for /f "tokens=2" %%I in ('python -V 2^>^&1') do set "PYVER=%%I"
if "%PYVER%"=="" (
    color 0c
    echo [!] FATAL ERROR: Python is not installed or not in the system PATH.
    pause
    exit
)
echo [+] Found Python Version: !PYVER! - Proceeding...

:: --- THE PRE-FLIGHT PURGE ---
echo [*] Orchestrating clean-state environment...
schtasks /delete /tn "Aegis_Overwatch_Engine" /f >nul 2>&1
del /f /q start_engine.bat aegis_ghost.vbs Aegis-Control.bat >nul 2>&1
powershell -Command "Get-CimInstance Win32_Process -Filter \"Name = 'python.exe' OR Name = 'pythonw.exe'\" | Where-Object { $_.CommandLine -match 'aegis_' -or $_.CommandLine -match 'c2_socket' } | Invoke-CimMethod -MethodName Terminate" >nul 2>&1

set TARGET_DIR=C:\Aegis-Overwatch
if /i "%~dp0" == "%TARGET_DIR%\" goto BUILD_PHASE

:RELOCATION_PHASE
cls
echo [*] PHASE 1: Relocating to System Root [%TARGET_DIR%]...
if not exist "%TARGET_DIR%" mkdir "%TARGET_DIR%"
xcopy /E /I /H /Y "%~dp0*" "%TARGET_DIR%" >nul 2>&1

echo Relocation complete. Re-launching from System Root...
timeout /t 2 >nul
powershell -Command "Start-Process cmd -ArgumentList '/c \"\"%TARGET_DIR%\%~nx0\"\"' -Verb RunAs"
exit

:BUILD_PHASE
cls
echo ============================================================================
echo                      [ PROVISIONING NEURAL ENVIRONMENT ]
echo ============================================================================
echo.

:: --- PATH COMPATIBILITY FIX ---
:: Safely relocates dependencies into core/ to satisfy Cython bindings
if not exist "%TARGET_DIR%\core" mkdir "%TARGET_DIR%\core" >nul 2>&1
if exist "%TARGET_DIR%\Models" move /Y "%TARGET_DIR%\Models" "%TARGET_DIR%\core\" >nul 2>&1
if exist "%TARGET_DIR%\Templates" move /Y "%TARGET_DIR%\Templates" "%TARGET_DIR%\core\" >nul 2>&1
if exist "%TARGET_DIR%\data" move /Y "%TARGET_DIR%\data" "%TARGET_DIR%\core\" >nul 2>&1

:: PHASE 0: Vault Provisioning
if not exist "%TARGET_DIR%\core\.env" (
    echo [*] Generating Security manifest template [.env]...
    echo # AEGIS OVERWATCH CORE SECRETS > "%TARGET_DIR%\core\.env"
    echo AI_ENGINE_MODE=CLOUD >> "%TARGET_DIR%\core\.env"
    echo GEMINI_API_KEY=your_gemini_key_here >> "%TARGET_DIR%\core\.env"
    echo AEGIS_API_KEY=your_custom_security_password >> "%TARGET_DIR%\core\.env"
    echo VT_API_KEY=your_virustotal_key_here >> "%TARGET_DIR%\core\.env"
    echo LOCAL_MODEL_ID=llama3.2:1b >> "%TARGET_DIR%\core\.env"
    echo [+] Vault template created. UI Configuration will launch on first boot.
) else (
    echo [+] Security manifest found.
)

:: --- [UNIFICATION] Auto-Generate Aegis-Switch.bat if missing ---
if exist "%TARGET_DIR%\Aegis-Switch.bat" goto SKIP_SWITCH
echo [*] Generating C2 Ignition Switch...
(
echo @echo off
echo TITLE Aegis Overwatch - Core Orchestration Server ^(C2^)
echo color 0b
echo cd /d "%%~dp0"
echo :: 1. Elevation Check
echo net session ^>nul 2^>^&1
echo if %%errorLevel%% neq 0 ^(
echo     echo [*] Requesting Administrative Privileges...
echo     powershell -Command "Start-Process '%%~dpnx0' -Verb RunAs"
echo     exit /b
echo ^)
echo echo ============================================================================
echo echo   [ /// AEGIS OVERWATCH: IGNITION NEXUS /// ]
echo echo ============================================================================
echo echo [*] Purging ghost processes and freeing network ports...
echo powershell -Command "Get-CimInstance Win32_Process -Filter \"Name = 'python.exe' OR Name = 'pythonw.exe'\" | Where-Object { $_.CommandLine -match 'aegis_' -or $_.CommandLine -match 'c2_socket' } | Invoke-CimMethod -MethodName Terminate" ^>nul 2^>^&1
echo echo [+] Environment mathematically sterilized.
echo :: 3. Sovereign Core Auto-Start
echo echo [*] Checking for Sovereign Core Engine ^(Ollama^)...
echo tasklist /FI "IMAGENAME eq ollama.exe" 2^>NUL ^| find /I /N "ollama.exe"^>NUL
echo if "%%ERRORLEVEL%%"=="0" ^(
echo     echo [+] Ollama is already running in the background.
echo ^) else ^(
echo     if exist "%%LOCALAPPDATA%%\Programs\Ollama\ollama app.exe" ^(
echo         echo [*] Waking up local Ollama engine...
echo         start "" "%%LOCALAPPDATA%%\Programs\Ollama\ollama app.exe"
echo         timeout /t 3 ^>nul 
echo     ^) else ^(
echo         echo [!] Ollama not found in default path. If using Sovereign Mode, please start it manually.
echo     ^)
echo ^)
echo :: 4. Failsafe ASN Database Check
echo echo [*] Verifying Network Infrastructure Dependencies...
echo if not exist "core\data\GeoLite2-ASN.mmdb" ^(
echo     echo [!] ASN Database missing. Executing emergency TLS 1.2 download...
echo     if not exist "core\data" mkdir "core\data"
echo     powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-ASN.mmdb' -OutFile 'core\data\GeoLite2-ASN.mmdb'"
echo     if exist "core\data\GeoLite2-ASN.mmdb" ^(
echo         echo [+] ASN Database restored successfully.
echo     ^) else ^(
echo         color 0e
echo         echo [!] EMERGENCY DOWNLOAD FAILED. Network Sentinel will operate in degraded mode.
echo         color 0b
echo     ^)
echo ^) else ^(
echo     echo [+] ASN Database verified.
echo ^)
echo echo [*] Booting FastAPI Orchestration Server...
echo echo.
echo echo ============================================================================
echo echo  [!] IMPORTANT: DO NOT CLOSE THIS TERMINAL.
echo echo  [!] This window acts as your live C2 Console and forensic log stream.
echo echo  [!] To shut down Aegis securely, simply close this window.
echo echo ============================================================================
echo echo.
echo start /b cmd /c "timeout /t 6 ^>nul ^& start http://localhost:8000/dashboard"
echo if exist "venv\Scripts\activate.bat" ^(
echo     echo [*] Binding Virtual Environment variables...
echo     call "venv\Scripts\activate.bat"
echo     python core\aegis_server.py
echo ^) else ^(
echo     echo [!] Virtual environment not found. Falling back to system Python...
echo     python core\aegis_server.py
echo ^)
echo echo.
echo echo [X] Aegis Orchestration Server has been terminated.
echo pause
) > "%TARGET_DIR%\Aegis-Switch.bat"
:SKIP_SWITCH

if not exist "core\data" mkdir "core\data"

:: --- [CRITICAL UPGRADE] AUTOMATED MAXMIND ASN DATABASE PROVISIONING ---
echo [*] Checking for MaxMind GeoLite2-ASN Database...
if not exist "core\data\GeoLite2-ASN.mmdb" (
    echo [!] ASN Database not found. Downloading from public mirror ^(TLS 1.2 Enforced^)...
    :: Force TLS 1.2 so GitHub doesn't drop the PowerShell connection
    powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-ASN.mmdb' -OutFile 'core\data\GeoLite2-ASN.mmdb'"
    
    if exist "core\data\GeoLite2-ASN.mmdb" (
        echo [+] Offline ASN Database successfully provisioned.
    ) else (
        color 0e
        echo [!] WARNING: Failed to download ASN database. Network engine will run degraded.
        echo [!] Please check your firewall or manually place GeoLite2-ASN.mmdb in the /core/data folder.
        color 0b
    )
) else (
    echo [+] Offline ASN Database present.
)
:: ----------------------------------------------------------------------

if exist "venv\Scripts\python.exe" (
    echo [+] Existing environment detected. Checking for updates...
    goto SYNC_DEPS
)

echo [*] Initializing Virtual Environment (One-time setup)...
python -m venv venv
if %errorlevel% neq 0 (
    echo [!] VENV Creation Failed.
    pause
    exit
)

:SYNC_DEPS
echo [*] Upgrading core installer components...
"venv\Scripts\python.exe" -m pip install --upgrade pip --quiet

echo.
echo [*] SYNCING COMPONENT MANIFEST (FastAPI, ONNX, Scapy, geoip2, jinja2, etc.)...
echo [!] Visual Progress Enabled. This ensures no 10-minute hangs.
echo.
"venv\Scripts\python.exe" -m pip install onnxruntime scapy fastapi uvicorn psutil python-dotenv colorama requests geoip2 openai google-generativeai jinja2 --prefer-binary
"venv\Scripts\python.exe" -m pip install -r requirements.txt --prefer-binary

if %errorlevel% neq 0 (
    color 0c
    echo [!] Library Sync Failed. Check internet connection.
    pause
    exit
)

echo.
echo [+] Neural Environment Hardened.
echo.

echo [*] Provisioning Windows Audit Policies (Event ID 4104)...
reg add "HKEY_LOCAL_MACHINE\Software\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging" /v EnableScriptBlockLogging /t REG_DWORD /d 1 /f >nul
reg add "HKEY_LOCAL_MACHINE\Software\Policies\Microsoft\PowerShellCore\ScriptBlockLogging" /v EnableScriptBlockLogging /t REG_DWORD /d 1 /f >nul
echo [*] Forcing Windows Policy Refresh - Please wait...
gpupdate /force >nul 2>&1
echo [+] Core Windows Auditing Enabled.
echo.

echo [*] Optimizing Sovereign Core (Local LLM) Latency...
:: Write the variable to the System Machine Environment (/M)
setx OLLAMA_KEEP_ALIVE "-1" /M >nul 2>&1
:: Bounce the Ollama daemon so it inherits the new variable instantly without a PC reboot
taskkill /F /IM "ollama app.exe" >nul 2>&1
taskkill /F /IM "ollama.exe" >nul 2>&1
start "" "%LOCALAPPDATA%\Programs\Ollama\ollama app.exe" >nul 2>&1
echo [+] Ollama VRAM Hot-State enabled (Zero-latency triage unlocked).
echo.

echo [*] PHASE 2: Executing Smart Machine DNA Profiling...
echo [!] Running 3-Minute DEMO MODE network calibration in the background.
echo [!] Smart-Triage will scan local binaries and secure the HMAC whitelist.
"venv\Scripts\python.exe" core\aegis_profiler.py
if %errorlevel% neq 0 (
    color 0c
    echo [!] DNA Profiling Failed.
    pause
    exit
)
echo [+] Base DNA established and Cryptographically Sealed.
echo [+] (Use the Dashboard UI to run the 10-Minute Active Learning Calibration).
echo.
echo [*] PHASE 3: Pinning Secure Control Panel...
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
echo   Staged at: %TARGET_DIR%
echo   A shortcut has been placed on your Desktop.
echo.
echo [*] Igniting the C2 Console...
timeout /t 3 >nul
start "" "C:\Aegis-Overwatch\Aegis-Switch.bat"
exit