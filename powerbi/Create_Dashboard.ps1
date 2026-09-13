<#
.SYNOPSIS
    Syntecxhub Sales Performance Dashboard — Power BI build helper

.DESCRIPTION
    Attempts to open the existing .pbix (if present) via the
    MicrosoftPowerBIModeling / Power BI PowerShell module. If no
    module or .pbix is found, prints step-by-step manual import
    instructions.

    Prerequisites (optional, for automation):
      - Power BI Desktop installed
      - PowerShell module MicrosoftPowerBIModeling (or the legacy
        PBI PowerShell module) — install with:
          Install-Module MicrosoftPowerBIModeling -Scope CurrentUser
        Note: the desktop client is still required to open/save .pbix.
        PowerShell scripting of the .pbix file format directly is limited
        without the desktop app; this script focuses on the refresh flow
        and data preparation.

    Always-run prerequisite (regardless of automation):
      - Run scripts/export_for_powerbi.py first so that
        data/pbi_ready/sales_for_powerbi.csv is up to date.

.EXAMPLE
    .\Create_Dashboard.ps1
#>

param(
    [string]$PbiDesktopPath = "",
    [string]$PbiFile = "",
    [switch]$OpenAfterBuild
)

$ErrorActionPreference = 'Stop'

# --- Resolve paths relative to the repo root ---
$ScriptDir  = Split-Path -Parent $MyInvocation.MyCommand.Definition
$RepoRoot   = Split-Path $ScriptDir -Parent
$PbiDir     = Join-Path $RepoRoot 'powerbi'
$CsvPath    = Join-Path $RepoRoot 'data\pbi_ready\sales_for_powerbi.csv'
$PbiFileDefault = Join-Path $PbiDir 'Syntecxhub_Sales_Dashboard.pbix'

if (-not $PbiFile) { $PbiFile = $PbiFileDefault }

Write-Host '=' * 70
Write-Host 'Syntecxhub Sales Dashboard — Power BI Build Helper'
Write-Host '=' * 70
Write-Host ''

# --- Step 0: confirm the CSV is ready ---
if (-not (Test-Path $CsvPath)) {
    Write-Host "[!] Power BI–ready CSV not found at:" -ForegroundColor Yellow
    Write-Host "    $CsvPath" -ForegroundColor Yellow
    Write-Host ''
    Write-Host 'Run this first:'
    Write-Host "    python `"$RepoRoot\scripts\export_for_powerbi.py`""
    Write-Host ''
    exit 1
}

Write-Host "[OK] Source CSV present: $CsvPath" -ForegroundColor Green
Write-Host ''

# --- Step 1: check Power BI Desktop ---
$PbiFound = $false
$PbixExists = Test-Path $PbiFile

if (-not $PbiDesktopPath) {
    # Common install locations
    $Candidates = @(
        'C:\Program Files\Microsoft Power BI Desktop\bin\MicrosoftPowerBIManagement.dll',
        'C:\Program Files (x86)\Microsoft Power BI Desktop\bin\MicrosoftPowerBIManagement.dll'
    )
    foreach ($c in $Candidates) {
        if (Test-Path $c) {
            $PbiDesktopPath = Split-Path $c -Parent
            break
        }
    }
}

if ($PbiDesktopPath) {
    Write-Host "[OK] Power BI Desktop found at: $PbiDesktopPath" -ForegroundColor Green
    $PbiFound = $true
} else {
    Write-Host "[!] Power BI Desktop not found in standard locations." -ForegroundColor Yellow
    Write-Host '    Automation is limited — see manual steps below.'
    Write-Host ''
}

# --- Step 2: check for PowerShell module (optional) ---
$ModuleAvailable = $false
try {
    $null = Get-Module -ListAvailable MicrosoftPowerBIModeling
    $ModuleAvailable = $true
} catch {
    # module not installed — that's fine
}

if ($ModuleAvailable) {
    Write-Host "[OK] MicrosoftPowerBIModeling module available." -ForegroundColor Green
} else {
    Write-Host "[~] MicrosoftPowerBIModeling module not installed." -ForegroundColor Yellow
    Write-Host '    Install (optional, for advanced scripting):'
    Write-Host '      Install-Module MicrosoftPowerBIModeling -Scope CurrentUser'
    Write-Host ''
}

Write-Host '-' * 70
Write-Host 'Build / Open decision'
Write-Host '-' * 70
Write-Host ''

# --- If .pbix exists and Power BI Desktop is found → open for refresh ---
if ($PbixExists -and $PbiFound) {
    Write-Host "[INFO] Existing dashboard found: $PbiFile" -ForegroundColor Cyan
    Write-Host ''
    Write-Host 'Options:'
    Write-Host '  1. Open in Power BI Desktop and click Refresh (recommended).'
    Write-Host '  2. Run Refresh_Dashboard.ps1 for a headless refresh (if saved data source is configured).'
    Write-Host ''
    if ($OpenAfterBuild) {
        Write-Host "Opening $PbiFile in Power BI Desktop ..." -ForegroundColor Cyan
        try {
            $exe = Join-Path $PbiDesktopPath 'MicrosoftPowerBIDesktop.exe'
            Start-Process -FilePath $exe -ArgumentList """$PbiFile""" -ErrorAction Stop
            Write-Host '[OK] Power BI Desktop opened.' -ForegroundColor Green
        } catch {
            Write-Host "[!] Could not launch Power BI Desktop automatically." -ForegroundColor Yellow
            Write-Host "    Try double-clicking $PbiFile in File Explorer."
        }
    } else {
        Write-Host 'Run with -OpenAfterBuild to open the file automatically.'
        Write-Host ''
    }
} elseif ($PbixExists) {
    Write-Host "[INFO] Dashboard .pbix exists but Power BI Desktop is not installed on this machine." -ForegroundColor Yellow
    Write-Host '    Open it on a machine that has Power BI Desktop, then Refresh.'
    Write-Host ''
} else {
    Write-Host "[INFO] No dashboard .pbix found yet." -ForegroundColor Cyan
    Write-Host '    Build the report manually (recommended first time) or use the script'
    Write-Host '    to open a blank Power BI Desktop for you to import the CSV.'
    Write-Host ''
}

# --- Manual steps (always printed) ---
Write-Host '=' * 70
Write-Host 'MANUAL IMPORT STEPS (works whether or not automation is available)'
Write-Host '=' * 70
Write-Host ''
Write-Host '1. Open Power BI Desktop (free download from Microsoft).'
Write-Host ''
Write-Host '2. Get Data:'
Write-Host "   Home -> Get Data -> Text/CSV -> select $CsvPath"
Write-Host ''
Write-Host '3. Power Query - verify column types:'
Write-Host '   Order_Date        -> Date'
Write-Host '   Year, Month, DayOfWeekNum  -> Whole Number'
Write-Host '   Sales, Profit, Profit_Margin_Pct  -> Decimal Number'
Write-Host '   IsWeekend  -> True/False'
Write-Host '   Then Close & Apply.'
Write-Host ''
Write-Host '4. Sort-by-aid setup:'
Write-Host '   - Select MonthName column -> Column tools -> Sort by column -> Month'
Write-Host '   - Select DayOfWeek -> Sort by column -> DayOfWeekNum'
Write-Host ''
Write-Host '5. Copy-paste DAX measures:'
Write-Host '   Modeling -> New measure -> paste each block from DAX_Measures.txt'
Write-Host ''
Write-Host '6. Build 4 pages per powerbi/dashboard_spec.md'
Write-Host ''
Write-Host '7. Save as:'
Write-Host "   $PbiFile"
Write-Host ''

# --- If Power BI Desktop is available and no .pbix exists, optionally launch ---
if ($PbiFound -and -not $PbixExists) {
    $reply = Read-Host 'Launch Power BI Desktop now to build the report? (y/n)'
    if ($reply -eq 'y' -or $reply -eq 'Y') {
        try {
            $exe = Join-Path $PbiDesktopPath 'MicrosoftPowerBIDesktop.exe'
            Start-Process -FilePath $exe -ErrorAction Stop
            Write-Host '[OK] Power BI Desktop launched.' -ForegroundColor Green
        } catch {
            Write-Host "[!] Could not launch. Try double-clicking the desktop shortcut." -ForegroundColor Yellow
        }
    }
}

Write-Host ''
Write-Host 'Done.' -ForegroundColor Green

