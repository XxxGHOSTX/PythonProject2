# THALOS PRIME - DEVELOPMENT GUIDE

## Overview

This guide covers development workflows, coding conventions, and best practices for contributing to the THALOS PRIME system. It documents the patterns and philosophies used throughout the codebase.

---

## 🚀 Development Workflows

### DEPLOY_THALOS_PRIME.bat Workflow

This is the primary deployment script that orchestrates the complete system startup.

#### Step-by-Step Breakdown

**Step 1: Environment Setup**
```batch
REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed
    exit /b 1
)

REM Create virtual environment if missing
IF NOT EXIST .venv (
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate.bat
```

**Why This Matters**:
- Virtual environment isolates dependencies
- Prevents conflicts with system Python packages
- Ensures reproducible deployments across machines
- Windows-specific: Uses `Scripts\` not `bin/`

**Step 2: Install Dependencies**
```batch
echo [INSTALL] Upgrading pip...
python -m pip install --upgrade pip --quiet

echo [INSTALL] Installing required packages...
python -m pip install -r requirements.txt --quiet
```

**Dependencies** (`requirements.txt`):
```
numpy>=1.26.0,<2.0
flask>=3.0.0
flask-cors>=4.0.0
requests>=2.31.0
```

**Step 3: Start BIOCOMPUTING_CORE Server**
```batch
REM Check if port 5001 is in use
netstat -ano | findstr :5001 >nul
if not errorlevel 1 (
    echo [WARNING] Port 5001 is already in use
    set /p KILL_PROC="Kill existing process? (y/n): "
    if /i "!KILL_PROC!"=="y" (
        REM Find and kill process
        for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5001') do (
            taskkill /F /PID %%a
        )
    )
)

REM Start server in new window
start "BIOCOMPUTING_CORE_SERVER" /MIN python biocomputing_api_server.py --port 5001

REM Wait for server initialization (max 30 seconds)
set WAIT_COUNT=0
:WAIT_LOOP
if %WAIT_COUNT% GEQ 30 goto TIMEOUT
curl -s http://localhost:5001/api/health >nul 2>&1
if errorlevel 1 (
    timeout /t 1 >nul
    set /a WAIT_COUNT+=1
    goto WAIT_LOOP
)
```

**Why This Matters**:
- Prevents "port already in use" errors
- Automatic conflict resolution
- Graceful startup with health checks
- Timeout prevents infinite waiting

**Step 4: Launch Modules**
```batch
echo [LAUNCH] Opening Thalos Celestial interface...
start thalos_celestial.html

echo.
set /p LAUNCH_CODING="Launch Coding Agent module? (y/n): "
if /i "%LAUNCH_CODING%"=="y" (
    echo [LAUNCH] Opening Thalos Coding Agent...
    start thalos_coding_agent.html
)
```

**Step 5: Display System Status**
```batch
echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║                  THALOS PRIME DEPLOYMENT COMPLETE                    ║
echo ╚══════════════════════════════════════════════════════════════════════╝
echo.
echo [✓] BIOCOMPUTING_CORE API Server: http://localhost:5001
echo [✓] Thalos Celestial Interface: ACTIVE
echo.
echo COMMAND REFERENCES:
echo   • Check server health:  curl http://localhost:5001/api/health
echo   • Monitor server:       python biocore_monitor.py --dashboard
echo   • Reset biocore:        curl -X POST http://localhost:5001/api/reset
echo   • Stop server:          Close "BIOCOMPUTING_CORE_SERVER" window
```

---

## 🔄 Other Deployment Workflows

### Quick Launch Scripts

#### launch_thalos.bat
**Purpose**: Interactive menu for launching specific modules
```batch
echo Select interface version:
echo   1. Terminal Edition (Green Matrix)
echo   2. Celestial Navigator (Amber/Gold)
echo   3. Primary Directive (Unrestricted AI)
set /p CHOICE="Enter choice (1-3): "

if "%CHOICE%"=="1" start thalos_prime.html
if "%CHOICE%"=="2" start thalos_celestial.html
if "%CHOICE%"=="3" start thalos_prime_primary_directive.html
```

#### launch_biocomputing_core.bat
**Purpose**: Start BIOCORE server only
```batch
call .venv\Scripts\activate.bat
python biocomputing_api_server.py --port 5001 --debug
```

#### launch_coding_agent.bat
**Purpose**: Start TPCA server and interface
```batch
call .venv\Scripts\activate.bat
start "TPCA_SERVER" python tpca_api_server.py --port 5002
timeout /t 5
start thalos_coding_agent.html
```

### Alternative Deployment Patterns

#### AUTO_DEPLOY_STARTUP.bat
**Purpose**: Automatic startup on system boot
- Minimal console output
- Background server launch
- Auto-opens primary interface
- Logs startup to file

#### INSTANT_LAUNCH.bat
**Purpose**: Ultra-fast launch (skips checks)
- Assumes environment ready
- No dependency installation
- Direct server start
- For development iterations

#### MASTER_DEPLOY.bat
**Purpose**: Deploy all components simultaneously
- Starts all servers (BIOCORE, TPCA, HYPER-NEXTUS)
- Opens all interfaces
- Maximum resource usage
- For comprehensive testing

---

## 📝 File Naming Conventions

### Python Files

#### Core Components (Uppercase)
```
BIOCOMPUTING_CORE.py       # Core intelligence engine
THALOS_PRIME_APP.py        # Standalone application
ABSOLUTE_LAUNCH.py         # Absolute deployment script
```

**Pattern**: `COMPONENT_NAME.py`
**When to Use**: System-critical components, entry points, core engines

#### Versioned Systems (Lowercase + Version)
```
thalos_sbi_core_v6.py      # SBI version 6
thalos_sbi_core.py         # SBI latest/stable
thalos_coding_agent_core.py # TPCA core engine
```

**Pattern**: `component_name_vN.py` or `component_name.py`
**When to Use**: Evolving subsystems, version-tracked modules

#### Servers (Suffix: _server)
```
biocomputing_api_server.py  # BIOCORE API server
tpca_api_server.py         # TPCA API server
hyper_nextus_server.py     # Integration hub server
deploy_server.py           # HTML hosting server
```

**Pattern**: `component_api_server.py` or `purpose_server.py`
**When to Use**: Flask/HTTP servers, API endpoints

#### Utilities (Lowercase + Function)
```
biocore_monitor.py         # Monitoring tool
verify_system.py           # Verification script
auto_enhancer.py           # Code enhancement tool
perpetual_optimizer.py     # Optimization daemon
```

**Pattern**: `function_purpose.py`
**When to Use**: Tools, utilities, standalone scripts

### Batch Scripts

#### Deployment Scripts (Uppercase Prefix)
```
DEPLOY_THALOS_PRIME.bat    # Main deployment
AUTO_DEPLOY_STARTUP.bat    # Auto-startup
MASTER_DEPLOY.bat          # Full deployment
```

**Pattern**: `DEPLOY_*.bat` or `ACTION_TARGET.bat`

#### Launch Scripts (Lowercase Prefix)
```
launch_thalos.bat          # Interactive launcher
launch_biocomputing_core.bat
launch_coding_agent.bat
```

**Pattern**: `launch_component.bat`

#### Utility Scripts
```
VERIFY_SYSTEM.bat          # System verification
VERIFY_DEPLOYMENT.bat      # Deployment checks
setup_env.bat              # Environment setup
```

**Pattern**: `VERB_OBJECT.bat` (uppercase) or `action_object.bat` (lowercase)

### HTML Interfaces

```
thalos_prime.html                    # Terminal edition
thalos_celestial.html                # Celestial navigator
thalos_coding_agent.html             # Coding agent interface
thalos_prime_primary_directive.html  # Primary directive (unrestricted)
```

**Pattern**: `thalos_variant.html` or `thalos_feature_description.html`

### Documentation Files

#### Guides (Uppercase)
```
README.md                  # Main readme
SETUP_GUIDE.md            # Setup instructions
DEPLOYMENT_README.md      # Deployment guide
```

**Pattern**: `NAME.md` or `TOPIC_GUIDE.md`

#### Status/Reports (Uppercase + Status)
```
ABSOLUTE_STATUS.md         # Absolute status
LAUNCH_STATUS.md          # Launch status
IMPLEMENTATION_COMPLETE.md # Completion report
```

**Pattern**: `COMPONENT_STATUS.md` or `TASK_STATUS.md`

#### Technical Docs
```
TECHNICAL_SPECIFICATION.txt
SYSTEM_ARCHITECTURE.md
DEVELOPMENT_GUIDE.md
```

**Pattern**: `TECHNICAL_TOPIC.{md|txt}`

### Configuration Files

```
requirements.txt           # Core dependencies
requirements_ultimate.txt  # All dependencies
.gitignore                # Git ignore rules
```

---

## 🎨 Code Style Conventions

### ASCII Art Headers

**Standard Format**:
```python
"""
╔════════════════════════════════════════════════════════════════════════════════╗
║                                                                                ║
║                    THALOS PRIME SBI - CORE SYSTEM v6.0                         ║
║                Synthetic Biological Intelligence Framework                     ║
║                                                                                ║
║  Copyright © 2026 THALOS PRIME SYSTEMS                                         ║
║  Creator: [Author Name]                                                        ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝
"""
```

**When to Use**:
- Main entry points (THALOS_PRIME_APP.py, BIOCOMPUTING_CORE.py)
- Standalone applications
- Major subsystems
- API servers

**Simpler Format** (for utilities):
```python
"""
THALOS PRIME - UTILITY NAME
===========================

Brief description of purpose.

Author: Name
Version: X.Y
"""
```

**Batch Script Format**:
```batch
@echo off
REM ═══════════════════════════════════════════════════════════════════════════
REM THALOS PRIME - SCRIPT NAME
REM ═══════════════════════════════════════════════════════════════════════════
REM
REM Description of what this script does.
REM
REM ═══════════════════════════════════════════════════════════════════════════
```

### Logging Patterns

**Standard Logger Setup**:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [COMPONENT_NAME] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('component_name.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('COMPONENT_NAME')
```

**Log Message Conventions**:
```python
# Success messages
logger.info("BIOCOMPUTING_CORE initialized successfully")

# Warnings (recoverable issues)
logger.warning("Port 5001 in use, attempting fallback to 5002")

# Errors (but continuing)
logger.error(f"Failed to process query: {e}")

# Debug information
logger.debug(f"Processing query with {len(tokens)} tokens")

# Critical failures
logger.critical("BIOCOMPUTING_CORE failed to initialize")
```

**Component Name Conventions**:
- BIOCORE_API (biocomputing_api_server.py)
- TPCA_API (tpca_api_server.py)
- DEPLOY_SERVER (deploy_server.py)
- BIOCORE (BIOCOMPUTING_CORE.py)
- SBI_CORE (thalos_sbi_core_v6.py)

### Dataclass Usage

**Configuration Objects**:
```python
from dataclasses import dataclass, field
from typing import Optional, List, Dict

@dataclass
class ThalosConfig:
    """Configuration for THALOS Prime system."""
    
    # Required fields
    vocab_size: int = 65536
    embedding_dim: int = 768
    hidden_dim: int = 3072
    
    # Optional fields with defaults
    num_layers: int = 24
    num_heads: int = 12
    max_seq_length: int = 4096
    
    # Complex defaults
    special_tokens: Dict[str, int] = field(default_factory=lambda: {
        'PAD': 0, 'UNK': 1, 'BOS': 2, 'EOS': 3
    })
    
    # Post-initialization validation
    def __post_init__(self):
        if self.vocab_size <= 0:
            raise ValueError("vocab_size must be positive")
        if self.embedding_dim % self.num_heads != 0:
            raise ValueError("embedding_dim must be divisible by num_heads")
```

**Request/Response Structures**:
```python
@dataclass
class NeuralQuery:
    """Structured query for biocomputing core."""
    query_text: str
    domain: Optional[DomainCategory] = None
    context: Optional[Dict[str, Any]] = None
    priority: int = 5  # 1-10
    timestamp: Optional[datetime] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.domain is None:
            self.domain = self._infer_domain()
    
    def _infer_domain(self) -> DomainCategory:
        """Infer domain from query text."""
        # Implementation here
        pass
```

**Why Dataclasses**:
- Type hints for IDE support
- Automatic `__init__`, `__repr__`, `__eq__`
- Immutability option with `frozen=True`
- Default values and factories
- Post-initialization hooks

---

## 🛡️ Error Handling Philosophy

### Graceful Degradation

**Core Principle**: System should never crash completely. Components fail gracefully and continue operating.

**Implementation Pattern**:
```python
# Import with availability flag
try:
    from BIOCOMPUTING_CORE import get_biocomputing_core
    BIOCORE_AVAILABLE = True
except ImportError as e:
    logger.warning(f"BIOCOMPUTING_CORE not available: {e}")
    BIOCORE_AVAILABLE = False

# Use with fallback
if BIOCORE_AVAILABLE:
    try:
        response = biocore.process_query(query)
    except Exception as e:
        logger.error(f"Biocore error: {e}, using fallback")
        response = generate_fallback_response(query)
else:
    response = generate_fallback_response(query)
```

### Auto-Recovery Mechanisms

**Pattern 1: Auto-Reset on Error**
```python
def process_with_auto_reset(query):
    global error_count
    
    try:
        result = process_query(query)
        error_count = 0  # Reset on success
        return result
    except Exception as e:
        error_count += 1
        logger.error(f"Processing error #{error_count}: {e}")
        
        if error_count >= ERROR_THRESHOLD:
            logger.info("Auto-reset triggered")
            reset_component()
            error_count = 0
        
        raise
```

**Pattern 2: Time-Based Reset**
```python
def get_component_with_timeout():
    global component, last_reset
    
    current_time = time.time()
    time_since_reset = current_time - last_reset
    
    if time_since_reset > RESET_INTERVAL:
        logger.info("Time-based reset triggered")
        component = initialize_component()
        last_reset = current_time
    
    return component
```

**Pattern 3: Retry with Exponential Backoff**
```python
def process_with_retry(query, max_retries=3):
    for attempt in range(max_retries):
        try:
            return process_query(query)
        except TransientError as e:
            wait_time = 2 ** attempt  # 1s, 2s, 4s
            logger.warning(f"Attempt {attempt+1} failed, retrying in {wait_time}s")
            time.sleep(wait_time)
    
    logger.error("All retries exhausted")
    return generate_fallback_response(query)
```

### Error Logging (Not Raising)

**Philosophy**: Log errors for debugging, but continue operation.

```python
# ❌ BAD: Crashes system
def process_query(query):
    result = external_api_call(query)
    return result  # Raises exception if API fails

# ✅ GOOD: Logs and continues
def process_query(query):
    try:
        result = external_api_call(query)
        return result
    except APIError as e:
        logger.error(f"API call failed: {e}")
        return fallback_response(query)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return {"error": "Internal error", "fallback": True}
```

### Specific Exception Handling

**Pattern**: Catch specific exceptions before general ones.

```python
try:
    result = complex_operation()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
    return default_value
except KeyError as e:
    logger.error(f"Missing key: {e}")
    return {}
except ImportError as e:
    logger.warning(f"Module not available: {e}")
    FEATURE_AVAILABLE = False
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
    return None
```

---

## 🔌 Adding New API Endpoints

### Flask Server Pattern

**Step 1: Define Endpoint**
```python
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for browser access

@app.route('/api/new_endpoint', methods=['POST'])
def new_endpoint():
    """
    Process new type of request.
    
    Request JSON:
        {
            "param1": "value1",
            "param2": "value2"
        }
    
    Response JSON:
        {
            "result": "...",
            "metadata": {...}
        }
    """
    try:
        # Parse request
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        param1 = data.get('param1')
        param2 = data.get('param2')
        
        # Validate
        if not param1:
            return jsonify({"error": "param1 is required"}), 400
        
        # Process
        result = process_function(param1, param2)
        
        # Return
        return jsonify({
            "result": result,
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "version": "1.0"
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Endpoint error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
```

**Step 2: Add Health Check**
```python
@app.route('/api/new_endpoint/health', methods=['GET'])
def new_endpoint_health():
    """Health check for new endpoint."""
    return jsonify({
        "status": "healthy",
        "endpoint": "new_endpoint",
        "version": "1.0"
    }), 200
```

**Step 3: Update Main Handler**
```python
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5003)
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()
    
    logger.info(f"Starting server on port {args.port}")
    app.run(host='127.0.0.1', port=args.port, debug=args.debug)
```

**Step 4: Document in README**
```markdown
### New Endpoint

**URL**: `http://localhost:5003/api/new_endpoint`
**Method**: POST
**Purpose**: Does something useful

**Request**:
```json
{
    "param1": "value",
    "param2": 123
}
```

**Response**:
```json
{
    "result": "processed",
    "metadata": {"timestamp": "..."}
}
```
```

### HTML Interface Integration

**Step 1: Add API Call Function**
```javascript
async function callNewEndpoint(param1, param2) {
    const apiUrl = 'http://localhost:5003/api/new_endpoint';
    
    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                param1: param1,
                param2: param2
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
        
    } catch (error) {
        console.error('API call failed:', error);
        // Fallback to offline mode
        return generateOfflineResponse(param1, param2);
    }
}
```

**Step 2: Add UI Elements**
```html
<div class="input-section">
    <label for="param1">Parameter 1:</label>
    <input type="text" id="param1" placeholder="Enter value...">
    
    <label for="param2">Parameter 2:</label>
    <input type="number" id="param2" placeholder="123">
    
    <button onclick="handleSubmit()">Submit</button>
</div>

<div class="output-section" id="output">
    <!-- Results appear here -->
</div>
```

**Step 3: Add Event Handler**
```javascript
async function handleSubmit() {
    const param1 = document.getElementById('param1').value;
    const param2 = parseInt(document.getElementById('param2').value);
    
    // Show loading state
    document.getElementById('output').innerHTML = 'Processing...';
    
    // Call API
    const result = await callNewEndpoint(param1, param2);
    
    // Display result
    document.getElementById('output').innerHTML = `
        <div class="result">
            <h3>Result:</h3>
            <pre>${JSON.stringify(result, null, 2)}</pre>
        </div>
    `;
}
```

---

## 🎨 HTML Interface Development Patterns

### Standard Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Thalos Interface Name</title>
    
    <!-- External libraries (from CDN) -->
    <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    
    <style>
        /* Styles here */
        body {
            background: #000;
            color: #0f0;
            font-family: 'Courier New', monospace;
        }
    </style>
</head>
<body>
    <!-- HTML structure -->
    
    <script>
        // JavaScript code
        
        // Configuration
        const CONFIG = {
            API_URL: 'http://localhost:5001/api/biocompute',
            FALLBACK_MODE: true,
            DEBUG: false
        };
        
        // Main functions
        async function initialize() {
            // Setup code
        }
        
        // Event listeners
        document.addEventListener('DOMContentLoaded', initialize);
    </script>
</body>
</html>
```

### Visual Theme Patterns

**Terminal/Matrix Theme** (Green):
```css
:root {
    --primary-color: #0f0;
    --background: #000;
    --text-glow: 0 0 10px #0f0, 0 0 20px #0f0;
}

body {
    background: var(--background);
    color: var(--primary-color);
    text-shadow: var(--text-glow);
}
```

**Celestial Theme** (Amber/Gold):
```css
:root {
    --primary-color: #ffa500;
    --secondary-color: #ffd700;
    --background: #000;
    --glow: 0 0 15px #ffa500;
}

.cosmic-element {
    color: var(--primary-color);
    box-shadow: var(--glow);
}
```

### Animation Patterns

**Particle System** (Three.js):
```javascript
function createParticleSystem() {
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    
    for (let i = 0; i < particleCount * 3; i += 3) {
        positions[i] = Math.random() * 200 - 100;
        positions[i + 1] = Math.random() * 200 - 100;
        positions[i + 2] = Math.random() * 200 - 100;
    }
    
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    
    const material = new THREE.PointsMaterial({
        color: 0x00ff00,
        size: 2,
        transparent: true,
        opacity: 0.8
    });
    
    const particles = new THREE.Points(geometry, material);
    scene.add(particles);
    
    return particles;
}
```

**Matrix Rain** (Canvas 2D):
```javascript
function drawMatrixRain() {
    ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    ctx.fillStyle = '#0f0';
    ctx.font = '15px monospace';
    
    for (let i = 0; i < drops.length; i++) {
        const text = String.fromCharCode(0x30A0 + Math.random() * 96);
        ctx.fillText(text, i * fontSize, drops[i] * fontSize);
        
        if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
            drops[i] = 0;
        }
        drops[i]++;
    }
    
    requestAnimationFrame(drawMatrixRain);
}
```

---

## 💻 PowerShell Commands for Debugging

### Server Management

**Check if Server is Running**:
```powershell
# Check port status
netstat -ano | findstr :5001

# Expected output if running:
#   TCP    127.0.0.1:5001    0.0.0.0:0    LISTENING    12345
```

**Kill Server Process**:
```powershell
# Find process ID
$processId = (Get-NetTCPConnection -LocalPort 5001).OwningProcess

# Kill process
Stop-Process -Id $processId -Force
```

**Start Server in Background**:
```powershell
# Start minimized
Start-Process python -ArgumentList "biocomputing_api_server.py --port 5001" -WindowStyle Minimized

# Start completely hidden
Start-Process python -ArgumentList "biocomputing_api_server.py --port 5001" -WindowStyle Hidden
```

### Health Checking

**Test Server Health**:
```powershell
# Using curl
curl http://localhost:5001/api/health

# Using Invoke-RestMethod (native PowerShell)
Invoke-RestMethod -Uri "http://localhost:5001/api/health" -Method GET
```

**Send Test Query**:
```powershell
# Prepare JSON payload
$body = @{
    query = "What is a black hole?"
    session_id = "test_session"
} | ConvertTo-Json

# Send POST request
$response = Invoke-RestMethod `
    -Uri "http://localhost:5001/api/biocompute" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

# Display response
$response | ConvertTo-Json -Depth 10
```

### Monitoring

**Monitor Server Logs in Real-Time**:
```powershell
# Tail log file (Windows equivalent)
Get-Content -Path "biocore_api.log" -Wait -Tail 20
```

**Check System Resources**:
```powershell
# Memory usage
Get-Process python | Select-Object Name, Id, @{Name="Memory(MB)";Expression={[math]::Round($_.WorkingSet / 1MB, 2)}}

# CPU usage over time
while ($true) {
    Get-Process python | Select-Object Name, CPU
    Start-Sleep -Seconds 5
}
```

### Troubleshooting

**Find Python Processes**:
```powershell
# List all Python processes
Get-Process python -ErrorAction SilentlyContinue | Format-Table Id, ProcessName, StartTime

# Kill all Python processes
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
```

**Check Virtual Environment**:
```powershell
# Verify virtual environment exists
Test-Path .\.venv\Scripts\python.exe

# Check Python version in venv
.\.venv\Scripts\python.exe --version

# List installed packages
.\.venv\Scripts\pip.exe list
```

**Reset Everything**:
```powershell
# Stop all servers
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force

# Delete virtual environment
Remove-Item .\.venv -Recurse -Force

# Recreate from scratch
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### Automated Monitoring Script

**monitor_system.ps1**:
```powershell
# Continuous system monitor
while ($true) {
    Clear-Host
    Write-Host "╔══════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║         THALOS PRIME SYSTEM MONITOR                  ║" -ForegroundColor Green
    Write-Host "╚══════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""
    
    # Server status
    Write-Host "SERVER STATUS:" -ForegroundColor Cyan
    $biocore = Test-NetConnection -ComputerName localhost -Port 5001 -InformationLevel Quiet
    $tpca = Test-NetConnection -ComputerName localhost -Port 5002 -InformationLevel Quiet
    
    Write-Host "  BIOCORE (5001): " -NoNewline
    if ($biocore) { Write-Host "ONLINE" -ForegroundColor Green } else { Write-Host "OFFLINE" -ForegroundColor Red }
    
    Write-Host "  TPCA (5002):    " -NoNewline
    if ($tpca) { Write-Host "ONLINE" -ForegroundColor Green } else { Write-Host "OFFLINE" -ForegroundColor Red }
    
    Write-Host ""
    
    # Resource usage
    Write-Host "RESOURCE USAGE:" -ForegroundColor Cyan
    $pythonProcesses = Get-Process python -ErrorAction SilentlyContinue
    if ($pythonProcesses) {
        foreach ($proc in $pythonProcesses) {
            $memory = [math]::Round($proc.WorkingSet / 1MB, 2)
            $cpu = [math]::Round($proc.CPU, 2)
            Write-Host "  PID $($proc.Id): Memory: $memory MB, CPU: $cpu s"
        }
    } else {
        Write-Host "  No Python processes running" -ForegroundColor Yellow
    }
    
    Write-Host ""
    Write-Host "Press Ctrl+C to exit..." -ForegroundColor Gray
    Start-Sleep -Seconds 5
}
```

---

## 📋 Essential Commands Cheat Sheet

### Setup Commands

```powershell
# Initial setup (run once)
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

# Verify installation
python --version
pip list
```

### Deployment Commands

```powershell
# Full system deployment
.\DEPLOY_THALOS_PRIME.bat

# Quick launch (no setup)
.\INSTANT_LAUNCH.bat

# Specific components
.\launch_biocomputing_core.bat
.\launch_coding_agent.bat

# Verification
.\VERIFY_SYSTEM.bat
.\VERIFY_DEPLOYMENT.bat
```

### Server Management

```powershell
# Start servers manually
python biocomputing_api_server.py --port 5001
python tpca_api_server.py --port 5002
python hyper_nextus_server.py 5000

# With options
python biocomputing_api_server.py --port 5001 --debug --reset-interval 1800
```

### Monitoring Commands

```powershell
# Interactive dashboard
python biocore_monitor.py --dashboard

# Real-time monitoring
python biocore_monitor.py --monitor --interval 10

# Quick status check
python biocore_monitor.py

# Manual reset
python biocore_monitor.py --reset
```

### Health Checks

```powershell
# Check all servers
curl http://localhost:5001/api/health
curl http://localhost:5002/api/health
curl http://localhost:5000/api/health

# Send test query
curl -X POST http://localhost:5001/api/biocompute -H "Content-Type: application/json" -d "{\"query\":\"test\"}"
```

### Troubleshooting

```powershell
# View logs
Get-Content biocore_api.log -Tail 50
Get-Content tpca_api.log -Tail 50

# Check ports
netstat -ano | findstr :5001
netstat -ano | findstr :5002

# Kill stuck processes
Get-Process python | Stop-Process -Force

# Clean restart
.\DEPLOY_THALOS_PRIME.bat
```

---

## 🔄 Virtual Environment Management (Windows)

### Creation

```powershell
# Create virtual environment
python -m venv .venv

# Verify creation
Test-Path .\.venv\Scripts\python.exe  # Should return True
```

### Activation

```batch
REM In batch script
call .venv\Scripts\activate.bat

REM In CMD
.venv\Scripts\activate.bat
```

```powershell
# In PowerShell
.\.venv\Scripts\Activate.ps1

# If execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Common Issues

**Issue**: "cannot be loaded because running scripts is disabled"
**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Issue**: Virtual environment not activating
**Solution**:
```powershell
# Delete and recreate
Remove-Item .venv -Recurse -Force
python -m venv .venv
```

**Issue**: Wrong Python version
**Solution**:
```powershell
# Specify Python version explicitly
py -3.11 -m venv .venv
```

---

## 📚 Related Documentation

- `SYSTEM_ARCHITECTURE.md` - System architecture overview
- `COMPONENT_INTERACTIONS.md` - Component integration details
- `TESTING_STRATEGY.md` - Testing approaches
- `README.md` - Project overview
- `DEPLOYMENT_README.md` - Deployment guide

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-08  
**System Version**: THALOS PRIME v9.0
