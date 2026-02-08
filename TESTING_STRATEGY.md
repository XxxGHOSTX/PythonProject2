# THALOS PRIME - TESTING STRATEGY

## Overview

This document outlines the testing approach for the THALOS PRIME system. While the project currently has limited formal test infrastructure, it employs several testing mechanisms and patterns that ensure system reliability.

---

## ⚠️ Current Testing Status

### Formal Test Infrastructure

**Status**: ❌ **Not Implemented**

**Findings**:
- No dedicated test files (`test_*.py` or `*_test.py`)
- No `tests/` directory
- No pytest or unittest test suites
- No CI/CD test automation

**Why This Works**:
The system uses alternative validation approaches:
1. Runtime error handling with graceful degradation
2. Auto-recovery mechanisms that detect and fix issues
3. Integration reports that track system health
4. Health check endpoints for validation
5. Manual verification via deployment scripts

---

## 🔍 Current Testing Mechanisms

### 1. Import Validation

**Pattern**: Try-except blocks verify module availability at runtime

```python
# Example from biocomputing_api_server.py
try:
    from BIOCOMPUTING_CORE import get_biocomputing_core, BiologicalResponse
    BIOCORE_AVAILABLE = True
    logger.info("✓ BIOCOMPUTING_CORE loaded successfully")
except ImportError as e:
    BIOCORE_AVAILABLE = False
    logger.warning(f"✗ BIOCOMPUTING_CORE not available: {e}")
except Exception as e:
    BIOCORE_AVAILABLE = False
    logger.error(f"✗ Error loading BIOCOMPUTING_CORE: {e}")
```

**Coverage**:
- All major component imports (BIOCORE, SBI, TPCA)
- Availability flags set at module level
- Logged for monitoring

**Validation**:
```bash
# Check logs for import status
grep "loaded successfully" biocore_api.log
grep "not available" biocore_api.log
```

### 2. Endpoint Health Checks

**Pattern**: HTTP endpoints verify component functionality

```python
# Example health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Comprehensive health check."""
    return jsonify({
        'status': 'healthy',
        'biocomputing_core': 'operational' if BIOCORE_AVAILABLE else 'unavailable',
        'database': 'connected' if db.is_connected() else 'disconnected',
        'uptime_seconds': time.time() - start_time,
        'request_count': request_counter,
        'error_count': error_counter
    })
```

**Testing Health Checks**:
```powershell
# BIOCORE health
curl http://localhost:5001/api/health
# Expected: {"status": "healthy", "biocomputing_core": "operational"}

# TPCA health
curl http://localhost:5002/api/health
# Expected: {"status": "online", "version": "8.0"}

# All servers
.\VERIFY_SYSTEM.bat
```

### 3. Integration Reports

**Mechanism**: `infinite_integration.py` generates automated health reports

**Process**:
```python
def scan_integration_health():
    """Scan all files for integration issues."""
    
    report = {
        'cycle': cycle_number,
        'files_scanned': scan_all_files(),
        'missing_imports': check_imports(),
        'missing_files': check_file_references(),
        'syntax_errors': check_syntax(),
        'integration_status': test_all_components()
    }
    
    save_report(f"integration_report_cycle_{cycle}.json", report)
    return report
```

**Generated Files**: `integration_report_cycle_N.json` (N = 1-51)

**Validation**:
```powershell
# Check latest integration report
Get-Content integration_report_cycle_51.json | ConvertFrom-Json

# Verify all components available
$report = Get-Content integration_report_cycle_51.json | ConvertFrom-Json
$report.integration_status
```

### 4. AST-Based Syntax Validation

**Pattern**: Python's `ast` module validates syntax at integration time

```python
import ast

def validate_python_file(file_path):
    """Validate Python file syntax."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        ast.parse(code)
        return {'valid': True, 'file': str(file_path)}
    
    except SyntaxError as e:
        return {
            'valid': False,
            'file': str(file_path),
            'error': str(e),
            'line': e.lineno
        }
```

**Coverage**:
- All Python files scanned
- Syntax errors detected before runtime
- Reported in integration cycles

### 5. Configuration Validation

**Pattern**: Dataclass type hints and post-init validation

```python
from dataclasses import dataclass

@dataclass
class ThalosConfig:
    """Configuration with built-in validation."""
    vocab_size: int = 65536
    embedding_dim: int = 768
    num_heads: int = 12
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if self.vocab_size <= 0:
            raise ValueError("vocab_size must be positive")
        
        if self.embedding_dim % self.num_heads != 0:
            raise ValueError("embedding_dim must be divisible by num_heads")
        
        if self.num_heads not in [8, 12, 16]:
            raise ValueError("num_heads must be 8, 12, or 16")
```

**Testing**:
```python
# Valid configuration
config = ThalosConfig(vocab_size=65536, embedding_dim=768, num_heads=12)
# ✓ Works

# Invalid configuration
config = ThalosConfig(vocab_size=-1)
# ✗ Raises ValueError
```

### 6. Deployment Verification Scripts

**Scripts**:
- `VERIFY_SYSTEM.bat` - Comprehensive system check
- `VERIFY_DEPLOYMENT.bat` - Deployment validation
- `biocore_monitor.py` - Runtime monitoring

**Example: VERIFY_SYSTEM.bat**
```batch
echo [1/5] Checking Python installation...
python --version || goto ERROR

echo [2/5] Checking virtual environment...
if not exist .venv\Scripts\python.exe goto ERROR

echo [3/5] Checking core files...
if not exist BIOCOMPUTING_CORE.py goto ERROR
if not exist thalos_sbi_core_v6.py goto ERROR

echo [4/5] Checking dependencies...
.\.venv\Scripts\pip.exe list | findstr numpy || goto ERROR
.\.venv\Scripts\pip.exe list | findstr flask || goto ERROR

echo [5/5] Testing BIOCOMPUTING_CORE...
.\.venv\Scripts\python.exe -c "from BIOCOMPUTING_CORE import get_biocomputing_core; print('OK')" || goto ERROR

echo.
echo ╔══════════════════════════════════════════╗
echo ║    ✓ ALL VERIFICATIONS PASSED            ║
echo ╚══════════════════════════════════════════╝
exit /b 0

:ERROR
echo ✗ VERIFICATION FAILED
exit /b 1
```

---

## 🧪 Recommended Testing Strategy

### Phase 1: Unit Testing (Priority: High)

**Objective**: Test individual components in isolation

**Recommended Framework**: pytest

**Setup**:
```bash
# Install pytest
pip install pytest pytest-cov

# Create test directory
mkdir tests
```

**Test Structure**:
```
tests/
├── __init__.py
├── test_biocomputing_core.py
├── test_sbi_core.py
├── test_tpca_core.py
├── test_api_servers.py
└── conftest.py
```

**Example Test: test_biocomputing_core.py**
```python
import pytest
from BIOCOMPUTING_CORE import (
    get_biocomputing_core,
    NeuralQuery,
    DomainCategory,
    BiologicalResponse
)

class TestBiocomputingCore:
    """Unit tests for BIOCOMPUTING_CORE."""
    
    @pytest.fixture
    def biocore(self):
        """Create biocore instance for testing."""
        return get_biocomputing_core()
    
    def test_core_initialization(self, biocore):
        """Test that biocore initializes correctly."""
        assert biocore is not None
        assert hasattr(biocore, 'process_query')
    
    def test_domain_inference(self):
        """Test automatic domain classification."""
        query = NeuralQuery(query_text="What is a black hole?")
        assert query.domain == DomainCategory.ASTROPHYSICS
        
        query = NeuralQuery(query_text="Write a Python function")
        assert query.domain == DomainCategory.CODE_GENERATION
    
    def test_query_processing(self, biocore):
        """Test query processing returns valid response."""
        query = NeuralQuery(query_text="Test query")
        response = biocore.process_query(query)
        
        assert isinstance(response, BiologicalResponse)
        assert response.response_text is not None
        assert 0 <= response.confidence <= 1
    
    def test_confidence_scoring(self, biocore):
        """Test confidence scores are reasonable."""
        queries = [
            "What is quantum entanglement?",
            "asdfghjkl"  # Nonsense query
        ]
        
        responses = [biocore.process_query(NeuralQuery(q)) for q in queries]
        
        # Real query should have higher confidence
        assert responses[0].confidence > responses[1].confidence
    
    def test_cross_domain_synthesis(self, biocore):
        """Test cross-domain connection detection."""
        query = NeuralQuery(query_text="How does quantum mechanics affect black holes?")
        response = biocore.process_query(query)
        
        # Should identify both quantum mechanics and astrophysics
        assert len(response.cross_domain_connections) > 0
```

**Running Tests**:
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=. tests/

# Run specific test file
pytest tests/test_biocomputing_core.py

# Run with verbose output
pytest -v tests/
```

### Phase 2: Integration Testing (Priority: Medium)

**Objective**: Test component interactions

**Example Test: test_api_integration.py**
```python
import pytest
import requests
import time
import subprocess

class TestAPIIntegration:
    """Integration tests for API servers."""
    
    @pytest.fixture(scope="class")
    def biocore_server(self):
        """Start BIOCORE server for testing."""
        proc = subprocess.Popen(
            ['python', 'biocomputing_api_server.py', '--port', '5001'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        time.sleep(5)
        
        yield proc
        
        # Cleanup
        proc.terminate()
        proc.wait()
    
    def test_health_endpoint(self, biocore_server):
        """Test /api/health endpoint."""
        response = requests.get('http://localhost:5001/api/health')
        
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'healthy'
        assert data['biocomputing_core'] == 'operational'
    
    def test_query_endpoint(self, biocore_server):
        """Test /api/biocompute endpoint."""
        payload = {
            'query': 'What is a black hole?',
            'session_id': 'test_session'
        }
        
        response = requests.post(
            'http://localhost:5001/api/biocompute',
            json=payload
        )
        
        assert response.status_code == 200
        data = response.json()
        assert 'response' in data
        assert 'confidence' in data
        assert data['confidence'] > 0
    
    def test_auto_reset(self, biocore_server):
        """Test auto-reset mechanism."""
        # Get current status
        status1 = requests.get('http://localhost:5001/api/status').json()
        
        # Trigger manual reset
        reset_response = requests.post('http://localhost:5001/api/reset')
        assert reset_response.status_code == 200
        
        # Check status after reset
        status2 = requests.get('http://localhost:5001/api/status').json()
        assert status2['reset_count'] > status1['reset_count']
```

### Phase 3: End-to-End Testing (Priority: Medium)

**Objective**: Test complete workflows

**Example Test: test_deployment.py**
```python
import pytest
import subprocess
import time
import requests
from pathlib import Path

class TestDeployment:
    """End-to-end deployment tests."""
    
    def test_virtual_environment_exists(self):
        """Verify virtual environment is set up."""
        venv_python = Path('.venv/Scripts/python.exe')
        assert venv_python.exists()
    
    def test_dependencies_installed(self):
        """Verify all dependencies are installed."""
        result = subprocess.run(
            ['.venv/Scripts/pip.exe', 'list'],
            capture_output=True,
            text=True
        )
        
        required = ['numpy', 'flask', 'flask-cors', 'requests']
        for package in required:
            assert package in result.stdout.lower()
    
    def test_core_files_exist(self):
        """Verify core files exist."""
        files = [
            'BIOCOMPUTING_CORE.py',
            'thalos_sbi_core_v6.py',
            'thalos_coding_agent_core.py',
            'biocomputing_api_server.py',
            'tpca_api_server.py'
        ]
        
        for file in files:
            assert Path(file).exists(), f"Missing file: {file}"
    
    def test_full_deployment_workflow(self):
        """Test complete deployment workflow."""
        # Start BIOCORE server
        biocore_proc = subprocess.Popen(
            ['.venv/Scripts/python.exe', 'biocomputing_api_server.py', '--port', '5001'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        try:
            # Wait for initialization
            max_wait = 30
            for _ in range(max_wait):
                try:
                    response = requests.get('http://localhost:5001/api/health')
                    if response.status_code == 200:
                        break
                except:
                    pass
                time.sleep(1)
            
            # Verify server is healthy
            health = requests.get('http://localhost:5001/api/health').json()
            assert health['status'] == 'healthy'
            
            # Send test query
            query_response = requests.post(
                'http://localhost:5001/api/biocompute',
                json={'query': 'Test query'}
            )
            assert query_response.status_code == 200
            
        finally:
            biocore_proc.terminate()
            biocore_proc.wait()
```

### Phase 4: Performance Testing (Priority: Low)

**Objective**: Measure system performance under load

**Example Test: test_performance.py**
```python
import pytest
import time
import requests
import concurrent.futures

class TestPerformance:
    """Performance and load tests."""
    
    @pytest.fixture(scope="class")
    def biocore_server(self):
        """Start server for performance testing."""
        # ... (same as integration test fixture)
    
    def test_response_time(self, biocore_server):
        """Test average response time."""
        queries = [f"Test query {i}" for i in range(10)]
        times = []
        
        for query in queries:
            start = time.time()
            response = requests.post(
                'http://localhost:5001/api/biocompute',
                json={'query': query}
            )
            elapsed = time.time() - start
            times.append(elapsed)
            
            assert response.status_code == 200
        
        avg_time = sum(times) / len(times)
        print(f"Average response time: {avg_time:.3f}s")
        
        # Response should be under 5 seconds
        assert avg_time < 5.0
    
    def test_concurrent_requests(self, biocore_server):
        """Test handling concurrent requests."""
        def send_query(query_id):
            response = requests.post(
                'http://localhost:5001/api/biocompute',
                json={'query': f'Concurrent query {query_id}'}
            )
            return response.status_code == 200
        
        # Send 10 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(send_query, i) for i in range(10)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        # All should succeed
        assert all(results)
    
    def test_memory_usage(self, biocore_server):
        """Test memory doesn't leak over many requests."""
        import psutil
        
        # Get Python processes
        python_procs = [p for p in psutil.process_iter(['name']) if 'python' in p.info['name'].lower()]
        
        if not python_procs:
            pytest.skip("No Python processes found")
        
        initial_memory = sum(p.memory_info().rss for p in python_procs)
        
        # Send 100 requests
        for i in range(100):
            requests.post(
                'http://localhost:5001/api/biocompute',
                json={'query': f'Query {i}'}
            )
        
        final_memory = sum(p.memory_info().rss for p in python_procs)
        
        # Memory growth should be reasonable (< 100MB)
        growth_mb = (final_memory - initial_memory) / 1024 / 1024
        print(f"Memory growth: {growth_mb:.2f} MB")
        assert growth_mb < 100
```

---

## 🔧 Testing Tools & Utilities

### Manual Testing Tools

#### 1. biocore_monitor.py

**Purpose**: Interactive testing and monitoring tool

**Usage**:
```powershell
# Interactive dashboard
python biocore_monitor.py --dashboard

# Menu options:
#   1. Check Status
#   2. Check Health
#   3. Send Test Query
#   4. Reset Biocore
#   5. Start Monitoring
#   6. Exit
```

**Test Query Feature**:
```python
def send_test_query():
    """Send test query to BIOCORE."""
    queries = [
        "What is a black hole?",
        "Explain quantum entanglement",
        "Write a Python function to sort a list"
    ]
    
    for query in queries:
        response = requests.post(
            'http://localhost:5001/api/biocompute',
            json={'query': query}
        )
        
        print(f"Query: {query}")
        print(f"Status: {response.status_code}")
        print(f"Confidence: {response.json().get('confidence')}")
        print()
```

#### 2. verify_system.py

**Purpose**: Automated system verification

**Checks**:
- Python installation
- Virtual environment setup
- Dependency installation
- Core file existence
- Import validation
- Basic functionality tests

**Usage**:
```powershell
python verify_system.py
```

### Automated Testing Scripts

#### 3. VERIFY_DEPLOYMENT.bat

**Purpose**: Batch script for deployment verification

**Process**:
1. Check environment
2. Verify files
3. Test imports
4. Start server
5. Health check
6. Stop server

#### 4. Integration Cycle Scanner

**Purpose**: Continuous integration health monitoring

**Implementation**: `infinite_integration.py`

**Features**:
- AST-based syntax checking
- Import resolution testing
- Missing file detection
- Component availability testing
- Report generation

---

## 📋 Testing Checklist

### Before Release

- [ ] All Python files pass syntax validation (AST parsing)
- [ ] All critical imports resolve successfully
- [ ] Virtual environment activates correctly
- [ ] Dependencies install without errors
- [ ] BIOCORE server starts and responds to health checks
- [ ] TPCA server starts and responds to health checks
- [ ] HTML interfaces load without JavaScript errors
- [ ] Query processing returns valid responses
- [ ] Auto-reset mechanism triggers correctly
- [ ] Database connections work
- [ ] Log files are being created
- [ ] Integration reports show healthy status

### Manual Testing Workflow

```powershell
# 1. Clean start
Remove-Item .venv -Recurse -Force
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

# 2. Verify setup
python verify_system.py

# 3. Start system
.\DEPLOY_THALOS_PRIME.bat

# 4. Test endpoints
curl http://localhost:5001/api/health
curl http://localhost:5002/api/health

# 5. Send test queries
python biocore_monitor.py --test

# 6. Check logs
Get-Content biocore_api.log -Tail 20
Get-Content tpca_api.log -Tail 20

# 7. Monitor performance
python biocore_monitor.py --monitor --interval 10

# 8. Verify integration
$report = Get-Content integration_report_cycle_51.json | ConvertFrom-Json
$report.integration_status

# 9. Clean shutdown
# Close server windows
# Verify no hanging processes
Get-Process python
```

---

## 🚀 Future Testing Improvements

### Short-Term (High Priority)

1. **Add pytest infrastructure**
   - Create `tests/` directory
   - Write unit tests for core components
   - Add pytest to requirements.txt

2. **Implement CI/CD pipeline**
   - GitHub Actions workflow
   - Automated test execution on push
   - Code coverage reporting

3. **Add API test suite**
   - Test all endpoints
   - Test error cases
   - Test concurrent requests

### Medium-Term (Medium Priority)

4. **Add integration tests**
   - Component interaction tests
   - Database persistence tests
   - Auto-recovery mechanism tests

5. **Add performance benchmarks**
   - Response time tracking
   - Memory usage monitoring
   - Load testing

6. **Add HTML interface tests**
   - Selenium/Playwright tests
   - JavaScript unit tests
   - Browser compatibility tests

### Long-Term (Low Priority)

7. **Add property-based testing**
   - Hypothesis framework
   - Fuzz testing
   - Edge case generation

8. **Add mutation testing**
   - Code quality verification
   - Test effectiveness measurement

9. **Add security testing**
   - Penetration testing
   - SQL injection tests
   - XSS vulnerability tests

---

## 📚 Testing Resources

### Recommended Frameworks

- **pytest** - Python testing framework
- **pytest-cov** - Coverage plugin
- **requests-mock** - Mock HTTP requests
- **freezegun** - Mock datetime
- **hypothesis** - Property-based testing

### Installation

```bash
pip install pytest pytest-cov requests-mock freezegun hypothesis
```

### Example pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --cov=.
    --cov-report=html
    --cov-report=term-missing
    --ignore=.venv
    --ignore=.thalos_cache
    --ignore=.thalos_logs
```

### Example conftest.py

```python
import pytest
import subprocess
import time
from pathlib import Path

@pytest.fixture(scope="session")
def venv_python():
    """Get path to virtual environment Python."""
    venv_path = Path('.venv/Scripts/python.exe')
    if not venv_path.exists():
        pytest.skip("Virtual environment not found")
    return str(venv_path)

@pytest.fixture(scope="session")
def biocore_server(venv_python):
    """Start BIOCORE server for testing session."""
    proc = subprocess.Popen(
        [venv_python, 'biocomputing_api_server.py', '--port', '5001'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    time.sleep(5)  # Wait for startup
    
    yield proc
    
    proc.terminate()
    proc.wait()

@pytest.fixture
def test_session_id():
    """Generate unique test session ID."""
    import uuid
    return f"test_{uuid.uuid4().hex[:8]}"
```

---

## 📊 Testing Metrics

### Current Coverage (Estimated)

- **Unit Tests**: 0% (none implemented)
- **Integration Tests**: ~20% (health checks, verification scripts)
- **Manual Tests**: ~60% (deployment scripts, monitoring tools)
- **Automated Tests**: ~10% (integration reports)

### Target Coverage (Recommended)

- **Unit Tests**: 80%+ for core components
- **Integration Tests**: 60%+ for API endpoints
- **End-to-End Tests**: 40%+ for workflows
- **Performance Tests**: 20%+ for critical paths

---

## 📚 Related Documentation

- `SYSTEM_ARCHITECTURE.md` - System architecture overview
- `DEVELOPMENT_GUIDE.md` - Development workflows
- `COMPONENT_INTERACTIONS.md` - Component integration details
- `DEPLOYMENT_README.md` - Deployment guide

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-08  
**System Version**: THALOS PRIME v9.0
