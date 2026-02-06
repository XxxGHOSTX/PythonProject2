# ═══════════════════════════════════════════════════════════════════════════════
#  THALOS PRIME - PowerShell Launcher
#  Supports all interfaces with automatic venv activation
# ═══════════════════════════════════════════════════════════════════════════════

param(
    [Parameter(Position=0)]
    [ValidateSet("sbi", "prime", "celestial", "directive", "coding", "server", "all")]
    [string]$App = "coding"
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host ""
Write-Host "  ╔═══════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "  ║           THALOS PRIME - PowerShell Launcher v1.0                     ║" -ForegroundColor Cyan
Write-Host "  ╚═══════════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Navigate to project root
Set-Location $ProjectRoot

# Create venv if missing
if (-not (Test-Path ".venv")) {
    Write-Host "[SETUP] Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
}

# Activate venv
$ActivateScript = Join-Path $ProjectRoot ".venv\Scripts\Activate.ps1"
if (Test-Path $ActivateScript) {
    & $ActivateScript
} else {
    Write-Host "[WARN] Could not activate venv, using system Python" -ForegroundColor Yellow
}

# Install requirements
Write-Host "[SETUP] Checking dependencies..." -ForegroundColor Gray
python -m pip install -r requirements.txt -q 2>$null

# Find a free port
$Port = 8080
for ($p = 8080; $p -le 8090; $p++) {
    $listener = $null
    try {
        $listener = New-Object System.Net.Sockets.TcpListener([System.Net.IPAddress]::Any, $p)
        $listener.Start()
        $Port = $p
        $listener.Stop()
        break
    } catch {
        continue
    } finally {
        if ($listener) { $listener.Stop() }
    }
}

Write-Host "[INFO] Using port $Port" -ForegroundColor Green

# URL mapping
$Urls = @{
    "sbi"       = "thalos_sbi_app.py"
    "prime"     = "THALOS_PRIME_APP.py"
    "celestial" = "thalos_celestial.html"
    "directive" = "thalos_prime_primary_directive.html"
    "coding"    = "thalos_coding_agent.html"
}

function Start-StaticServer {
    param([int]$ServerPort)

    $ServerScript = @"
import http.server
import socketserver
import os
os.chdir(r'$ProjectRoot')
with socketserver.TCPServer(('', $ServerPort), http.server.SimpleHTTPRequestHandler) as httpd:
    print(f'Server running on port $ServerPort')
    httpd.serve_forever()
"@

    Start-Process -FilePath "python" -ArgumentList "-c", "`"$ServerScript`"" -WindowStyle Minimized
    Start-Sleep -Seconds 2
}

switch ($App) {
    "sbi" {
        Write-Host "[LAUNCH] Starting Thalos SBI App..." -ForegroundColor Cyan
        python thalos_sbi_app.py
    }
    "prime" {
        Write-Host "[LAUNCH] Starting Thalos Prime App..." -ForegroundColor Cyan
        python THALOS_PRIME_APP.py
    }
    "celestial" {
        Write-Host "[LAUNCH] Starting Celestial Navigator..." -ForegroundColor Cyan
        Start-StaticServer -ServerPort $Port
        Start-Process "http://localhost:$Port/thalos_celestial.html"
        Write-Host "[INFO] Celestial Navigator opened at http://localhost:$Port/thalos_celestial.html" -ForegroundColor Green
    }
    "directive" {
        Write-Host "[LAUNCH] Starting Primary Directive..." -ForegroundColor Cyan
        Start-StaticServer -ServerPort $Port
        Start-Process "http://localhost:$Port/thalos_prime_primary_directive.html"
        Write-Host "[INFO] Primary Directive opened at http://localhost:$Port/thalos_prime_primary_directive.html" -ForegroundColor Green
    }
    "coding" {
        Write-Host "[LAUNCH] Starting CODING AGENT (Superior SBI)..." -ForegroundColor Magenta
        Start-StaticServer -ServerPort $Port
        Start-Process "http://localhost:$Port/thalos_coding_agent.html"
        Write-Host ""
        Write-Host "  ⚡ THALOS PRIME CODING AGENT is now running!" -ForegroundColor Magenta
        Write-Host "  URL: http://localhost:$Port/thalos_coding_agent.html" -ForegroundColor White
        Write-Host ""
    }
    "server" {
        Write-Host "[LAUNCH] Starting deployment server..." -ForegroundColor Cyan
        python deploy_server.py $Port
    }
    "all" {
        Write-Host "[LAUNCH] Starting all interfaces..." -ForegroundColor Cyan
        Start-StaticServer -ServerPort $Port
        Start-Sleep -Seconds 1
        Start-Process "http://localhost:$Port/thalos_prime.html"
        Start-Process "http://localhost:$Port/thalos_celestial.html"
        Start-Process "http://localhost:$Port/thalos_prime_primary_directive.html"
        Start-Process "http://localhost:$Port/thalos_coding_agent.html"
        Write-Host "[INFO] All interfaces opened!" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
