<#
.SYNOPSIS
    Aegis-Hydrate: Exports Sysmon logs and current configuration for ML analysis.
.DESCRIPTION
    This script automates the collection of the last 1000 Sysmon events into a 
    valid XML format and dumps the active Sysmon configuration to a text file.
#>

# 1. Configuration & Paths
# $PSScriptRoot ensures files are saved in the same folder as this script
$ReportPath = "$PSScriptRoot\Sysmon_Report_Final.xml"
$ConfigPath = "$PSScriptRoot\sysmon_config.txt"
$MaxEvents = 10000

Write-Host "[*] Starting Aegis-Hydrate Data Collection..." -ForegroundColor Cyan

# 2. Export Current Sysmon Configuration
Write-Host "[+] Exporting active Sysmon configuration..." -ForegroundColor Yellow
try {
    & C:\Windows\sysmon64.exe -c | Out-File -FilePath $ConfigPath -Encoding utf8
    Write-Host "    [OK] Config saved to: $ConfigPath" -ForegroundColor Green
} catch {
    Write-Host "    [!] Error exporting config. Ensure Sysmon is installed." -ForegroundColor Red
}

# 3. Export & Format Sysmon Logs
Write-Host "[+] Exporting last $MaxEvents Sysmon events to XML..." -ForegroundColor Yellow

# Start the XML file with a proper root element for Python ingestion
Set-Content -Path $ReportPath -Value "<Events>"

try {
    $events = Get-WinEvent -LogName "Microsoft-Windows-Sysmon/Operational" -MaxEvents $MaxEvents -ErrorAction Stop
    
    foreach ($event in $events) {
        # Append the XML fragment for each event
        Add-Content -Path $ReportPath -Value $event.ToXml()
    }
    
    # Close the root element
    Add-Content -Path $ReportPath -Value "</Events>"
    Write-Host "    [OK] Report saved to: $ReportPath" -ForegroundColor Green
} catch {
    Write-Host "    [!] No Sysmon events found or access denied." -ForegroundColor Red
    # Ensure file isn't left open/invalid if it fails
    Add-Content -Path $ReportPath -Value "</Events>"
}

Write-Host "[*] Hydration Complete. Ready for Python Analysis." -ForegroundColor Cyan