@echo off
:: 1. Force the terminal to stay in your project folder
cd /d "C:\Windows\Aegis-Project"

:: 2. Launch using the FULL PATH to the background Python
start "" "C:\Windows\Aegis-Project\venv\Scripts\pythonw.exe" "C:\Windows\Aegis-Project\Hive_Orchestrator.pyw"

:: 3. Close the temporary batch window immediately
exit