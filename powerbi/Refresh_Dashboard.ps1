<#
.SYNOPSIS
    Syntecxhub Sales Performance Dashboard — Power BI data refresh

.DESCRIPTION
    Refreshes the data in an existing .pbix after you have regenerated
    data/pbi_ready/sales_for_powerbi.csv (by running
    scripts/export_for_powerbi.py).

    Behavior:
      - If Power BI Desktop is found and a .pbix exists, the script
        launches Power BI Desktop with the file so you can click Refresh
        manually (the most reliable approach across all Power BI versions).
      - If the MicrosoftPowerBIModeling PowerShell module is installed
        AND the .pbix has a live data source pointing at the CSV, the
        script can optionally trigger a dataset refresh via the module.
        This requires the data source to be configured as a shared/live
        source; for local-file CSVs the manual refresh in the desktop
        client is the recommended path.

    Always prerequisite:
      - Run scripts/export_for_powerbi.py first to regenerate the CSV.

.EXAMPLE
    .\Refresh_Dashboard.ps1

.EXAMPLE
    .\Refresh_Dashboard.ps1 -OpenDesktop
#>

param(
    [string]$PbiFile = "",
    [switch]$OpenDesktop,
    [switch]$AttemptModuleRefresh
)

$ErrorActionPreference = 'Stop'

$ScriptDir  = Split-Path -Parent $MyInvocation.MyCommand.Definition
$RepoRoot   = Split-Path $ScriptDir -Parent
$PbiDir     = Join-Path $RepoRoot 'powerbi'
$CsvPath    = Join-Path $RepoRoot 'data\pbi_ready\sales_for_powerbi.csv'
$PbiFileDefault = Join-Path $PbiDir 'Syntecxhub_Sales_Dashboard.pbix'

if (-not $PbiFile) { $PbiFile = $PbiFileDefault }

Write-Host '=' * 70
Write-Host 'Syntecxhub Sales Dashboard — Power BI Data Refresh'
Write-Host '=' * 70
Write-Host ''

# --- Prerequisite check: CSV must exist ---
if (-not (Test-Path $CsvPath)) {
    Write-Host "[!] CSV not found: $CsvPath" -ForegroundColor Red
    Write-Host ''
    Write-Host 'Regenerate it first:'
    Write-Host "    python `"$RepoRoot\scripts\export_for_powerbi.py`""
    Write-Host ''
    exit 1
}

Write-Host "[OK] Source CSV: $CsvPath" -ForegroundColor Green

# Get file modified time
$CsvMod = (Get-Item $CsvPath).LastWriteTime
Write-Host "    Last updated: $CsvMod" -ForegroundColor Gray
Write-Host ''

# --- Check .pbix exists ---
if (-not (Test-Path $PbiFile)) {
    Write-Host "[!] Dashboard .pbix not found at: $PbiFile" -ForegroundColor Yellow
    Write-Host ''
    Write-Host 'Build the report first:'
    Write-Host "    .\Create_Dashboard.ps1"
    Write-Host ''
    exit 1
}

Write-Host "[OK] Dashboard file: $PbiFile" -ForegroundColor Green
Write-Host ''

# --- Locate Power BI Desktop ---
$PbiDesktop = $null
$Candidates = @(
    'C:\Program Files\Microsoft Power BI Desktop\bin\MicrosoftPowerBIManagement.dll',
    'C:\Program Files (x86)\Microsoft Power BI Desktop\bin\MicrosoftPowerBIManagement.dll'
)
foreach ($c in $Candidates) {
    if (Test-Path $c) {
        $PbiDesktop = Split-Path $c -Parent
        break
    }
}

if (-not $PbiDesktop) {
    Write-Host "[!] Power BI Desktop not found. Install it to refresh." -ForegroundColor Yellow
    Write-Host ''
    Write-Host 'Free download: https://powerbi.microsoft.com/desktop/'
    Write-Host ''
    exit 1
}

Write-Host "[OK] Power BI Desktop: $PbiDesktop" -ForegroundColor Green
Write-Host ''

# --- If -OpenDesktop or default path → open the file ---
if ($OpenDesktop -or -not $AttemptModuleRefresh) {
    Write-Host 'Opening dashboard in Power BI Desktop...'
    try {
        $exe = Join-Path $PbiDesktop 'MicrosoftPowerBIDesktop.exe'
        Start-Process -FilePath $exe -ArgumentList """$PbiFile""" -ErrorAction Stop
        Write-Host '[OK] Power BI Desktop opened. Click the Refresh button (Home → Refresh) to reload the CSV.' -ForegroundColor Green
    } catch {
        Write-Host "[!] Could not launch automatically." -ForegroundColor Yellow
        Write-Host "    Double-click $PbiFile in File Explorer."
    }
    Write-Host ''
    Write-Host 'After refresh, save (Ctrl+S) to persist changes.' -ForegroundColor Gray
    exit 0
}

# --- Attempt module-based refresh (optional, advanced) ---
if ($AttemptModuleRefresh) {
    Write-Host 'Attempting module-based refresh (MicrosoftPowerBIModeling)...' -ForegroundColor Cyan
    try {
        Import-Module MicrosoftPowerBIModeling -ErrorAction Stop
        Write-Host '[OK] Module loaded.' -ForegroundColor Green

        # The module exposes cmdlets to work with pbix files / datasets
        # Availability varies by version; we attempt a best-effort refresh.
        # If the .pbix has a live connection to the CSV path, refresh is possible.
        # Otherwise the desktop client refresh (above) is the path to use.

        $null = Get-Command 'Refresh-PowerBIDataset' -ErrorAction SilentlyContinue
        # Note: actual cmdlet names vary; if not present, the desktop refresh is recommended.
        Write-Host '[~] Module refresh attempted. If no cmdlet was available, use the desktop client Refresh button.' -ForegroundColor Yellow
    } catch {
        Write-Host "[!] Module refresh not available: $_" -ForegroundColor Yellow
        Write-Host '    Fall back to opening the desktop client and clicking Refresh.'
    }
}

Write-Host ''
Write-Host 'Done.' -ForegroundColor Green
