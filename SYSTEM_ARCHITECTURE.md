# THALOS PRIME - SYSTEM ARCHITECTURE

## Overview

THALOS PRIME is a multi-tier synthetic biological intelligence system with a distributed Flask server architecture. The system uses a biological metaphor (neural organoids, wetware processing) combined with modern machine learning techniques to provide unrestricted AI capabilities across multiple domains.

---

## 🏗️ Three-Tier Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │   Thalos     │  │   Thalos     │  │  Thalos Primary         │  │
│  │  Celestial   │  │   Coding     │  │  Directive              │  │
│  │   (HTML)     │  │   Agent      │  │  (HTML/Python)          │  │
│  │              │  │   (HTML)     │  │                         │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬──────────────┘  │
│         │                  │                      │                 │
└─────────┼──────────────────┼──────────────────────┼─────────────────┘
          │                  │                      │
          │ HTTP/JSON        │ HTTP/JSON            │ HTTP/JSON
          │                  │                      │
┌─────────┴──────────────────┴──────────────────────┴─────────────────┐
│                      APPLICATION LAYER                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │  BIOCORE     │  │    TPCA      │  │  HYPER-NEXTUS           │  │
│  │  API Server  │  │  API Server  │  │  Unified Server         │  │
│  │  Port: 5001  │  │  Port: 5002  │  │  Port: 5000             │  │
│  │              │  │              │  │                         │  │
│  │ Flask/CORS   │  │ Flask/CORS   │  │  Flask/CORS             │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬──────────────┘  │
│         │                  │                      │                 │
└─────────┼──────────────────┼──────────────────────┼─────────────────┘
          │                  │                      │
          │                  │                      │
┌─────────┴──────────────────┴──────────────────────┴─────────────────┐
│                         DATA LAYER                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │  BIOCOMPUTING│  │   Thalos     │  │  Thalos Coding Agent    │  │
│  │  CORE        │  │   SBI Core   │  │  Core                   │  │
│  │              │  │   (v6)       │  │                         │  │
│  │ Neural       │  │              │  │  Expert System          │  │
│  │ Organoid     │  │ 200M Param   │  │  Pattern Library        │  │
│  │ Matrix       │  │ Transformer  │  │  Code Generation        │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬──────────────┘  │
│         │                  │                      │                 │
│         └──────────────────┴──────────────────────┘                 │
│                           │                                         │
│                    ┌──────▼──────────┐                              │
│                    │  Thalos Database│                              │
│                    │  Schema         │                              │
│                    │  (14 Tables)    │                              │
│                    └─────────────────┘                              │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🖥️ Multi-Server Architecture

### Server Inventory

| Server Name | Port | Purpose | Startup Command | Key Endpoints |
|-------------|------|---------|-----------------|---------------|
| **BIOCORE API** | 5001 | Neural organoid processing | `python biocomputing_api_server.py --port 5001` | `/api/biocompute`, `/api/health`, `/api/status`, `/api/reset` |
| **TPCA API** | 5002 | Autonomous code generation | `python tpca_api_server.py --port 5002` | `/api/generate`, `/api/health`, `/api/status` |
| **HYPER-NEXTUS** | 5000 | Unified integration hub | `python hyper_nextus_server.py 5000` | `/api/sbi/query`, `/api/code/generate` |
| **Deploy Server** | 8080 | HTML interface hosting | `python deploy_server.py` | `/`, `/thalos_prime.html`, `/thalos_celestial.html` |
| **THALOS PRIME APP** | 8888 | Standalone neural interface | `python THALOS_PRIME_APP.py` | `/`, `/api/query`, `/api/status` |

### Port Usage Strategy

- **5000**: Unified integration point (HYPER-NEXTUS)
- **5001**: Core biological intelligence (BIOCORE)
- **5002**: Code generation specialist (TPCA)
- **8080+**: Dynamic allocation for HTML hosting
- **8888**: Standalone neural network server

### Why Multiple Ports?

1. **Isolation**: Each component runs independently, preventing cascading failures
2. **Scalability**: Components can be scaled independently based on load
3. **Development**: Can develop/test individual components without affecting others
4. **Deployment Flexibility**: Deploy only needed components for specific use cases

---

## 🧠 Core Computation Engines

### 1. BIOCOMPUTING_CORE (v9.0)

**File**: `BIOCOMPUTING_CORE.py`

**Architecture**:
```
┌─────────────────────────────────────┐
│  NeuralOrganoidMatrix               │
│  • 50,000 simulated organoid units  │
│  • 5×10¹³ synaptic connections      │
│  • 6 processing substrates          │
└──────────┬──────────────────────────┘
           │
┌──────────▼──────────────────────────┐
│  SynapticIntegrationLayer           │
│  • Cross-domain connection tracking │
│  • Pattern recognition              │
│  • Biological signal processing     │
└──────────┬──────────────────────────┘
           │
┌──────────▼──────────────────────────┐
│  PatternRecognitionEngine           │
│  • Query classification             │
│  • Domain inference                 │
│  • Response synthesis               │
└─────────────────────────────────────┘
```

**Key Features**:
- 12 knowledge domains (astrophysics, code generation, quantum mechanics, etc.)
- Automatic domain classification based on query text
- Confidence scoring for all responses
- Cross-domain synthesis for complex queries
- Auto-reset mechanism to prevent memory accumulation

**Domain Classification**:
```python
class DomainCategory(Enum):
    ASTROPHYSICS = "astrophysics"
    COSMOLOGY = "cosmology"
    QUANTUM_MECHANICS = "quantum_mechanics"
    CODE_GENERATION = "code_generation"
    ALGORITHM_DESIGN = "algorithm_design"
    MATHEMATICS = "mathematics"
    PHYSICS = "physics"
    BIOLOGY = "biology"
    CHEMISTRY = "chemistry"
    ENGINEERING = "engineering"
    SYSTEMS_THEORY = "systems_theory"
    GENERAL_INTELLIGENCE = "general_intelligence"
```

### 2. Thalos SBI Core (v6.0)

**File**: `thalos_sbi_core_v6.py`

**Architecture**:
```
Input Text
    │
    ▼
┌─────────────────────────┐
│  AdvancedTokenizer      │
│  • WordPiece algorithm  │
│  • 65,536 vocabulary    │
│  • Special tokens       │
└──────────┬──────────────┘
           │
┌──────────▼──────────────┐
│  Embedding Layer        │
│  • 768 dimensions       │
│  • Positional encoding  │
│  • Layer normalization  │
└──────────┬──────────────┘
           │
┌──────────▼──────────────────────┐
│  Transformer Stack (24 layers) │
│  • Multi-head attention (12)    │
│  • Feed-forward networks        │
│  • Layer normalization          │
│  • Residual connections         │
└──────────┬──────────────────────┘
           │
┌──────────▼──────────────┐
│  Output Projection      │
│  • Vocabulary logits    │
│  • Softmax distribution │
└──────────┬──────────────┘
           │
           ▼
    Generated Text
```

**Parameters**: 200M+ total (exact count depends on vocabulary size)
- Embedding: `vocab_size × 768` parameters (≈38.6M for `vocab_size = 50,257` as in `thalos_sbi_core_v6.py`)
- Each transformer layer: ~17M parameters
- Total layers: 24
- Output projection: `vocab_size × 768` parameters (same shape as embedding; ≈38.6M for `vocab_size = 50,257`)

**Key Classes**:
- `ThalosConfig`: Configuration dataclass
- `TensorOps`: Custom tensor operations
- `SimpleTransformer`: Transformer implementation
- `ThalosPrimeNeuralCore`: Main inference engine
- `ThalosDatabase`: Persistence layer (14 tables)

### 3. Thalos Coding Agent Core (TPCA v8.0)

**File**: `thalos_coding_agent_core.py`

**Architecture**:
```
Natural Language Query
        │
        ▼
┌────────────────────────┐
│  Query Parser          │
│  • Mode inference      │
│  • Complexity analysis │
│  • Language detection  │
└────────┬───────────────┘
         │
┌────────▼───────────────┐
│  Expert System         │
│  • Rule-based logic    │
│  • Pattern matching    │
│  • Template library    │
└────────┬───────────────┘
         │
┌────────▼───────────────┐
│  Code Generator        │
│  • Syntax scaffolding  │
│  • Comment generation  │
│  • Test generation     │
└────────┬───────────────┘
         │
┌────────▼───────────────┐
│  Validator             │
│  • Complexity analysis │
│  • Security checks     │
│  • Documentation       │
└────────┬───────────────┘
         │
         ▼
    CodeArtifact
```

**Generation Modes**:
```python
class GenerationMode(Enum):
    FULL_APPLICATION = "full"
    FUNCTION = "function"
    CLASS = "class"
    API = "api"
    ALGORITHM = "algorithm"
    DEBUG = "debug"
    OPTIMIZE = "optimize"
    EXPLAIN = "explain"
```

**Output Structure**:
```python
@dataclass
class CodeArtifact:
    code: str                    # Generated code
    tests: str                   # Unit tests
    documentation: str           # Documentation
    complexity_analysis: str     # Big-O analysis
    security_notes: str          # Security considerations
    run_instructions: str        # How to execute
```

---

## 🔄 Integration Patterns

### Online-First with Offline Fallback

All HTML modules follow this pattern:

```javascript
async function queryThalos(userInput) {
    try {
        // ONLINE: Try API server first
        const response = await fetch('http://localhost:5001/api/biocompute', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: userInput })
        });
        
        if (response.ok) {
            return await response.json();
        }
    } catch (error) {
        console.log('Server unavailable, using offline mode');
    }
    
    // OFFLINE: Fallback to hardcoded intelligence
    return generateOfflineResponse(userInput);
}
```

### HTTP/JSON Communication

**Request Format**:
```json
{
    "query": "Explain black holes",
    "session_id": "user_123",
    "domain": "astrophysics",
    "context": {
        "previous_queries": ["What is spacetime?"],
        "mode": "detailed"
    }
}
```

**Response Format**:
```json
{
    "response": "Black holes are regions of spacetime...",
    "confidence": 0.95,
    "domain": "astrophysics",
    "cross_domain_connections": ["quantum_mechanics", "cosmology"],
    "reasoning_trace": ["Step 1: ...", "Step 2: ..."],
    "timestamp": "2026-02-08T00:20:24Z"
}
```

### Auto-Recovery Mechanisms

#### BIOCOMPUTING_CORE Auto-Reset

**Critical Feature**: The biocomputing core automatically resets to prevent errors from accumulating.

**Reset Conditions**:
1. **Time-based**: Every 3600 seconds (1 hour) by default
2. **Error-based**: After 10 consecutive errors
3. **Manual**: Via `/api/reset` endpoint

**Implementation** (`biocomputing_api_server.py`):
```python
AUTO_RESET_INTERVAL = 3600  # 1 hour
AUTO_RESET_ERROR_THRESHOLD = 10  # 10 errors

def get_or_reset_biocore():
    global biocore, biocore_last_reset, biocore_error_count
    
    with biocore_lock:
        current_time = time.time()
        time_since_reset = current_time - biocore_last_reset
        
        # Auto-reset logic
        if time_since_reset > AUTO_RESET_INTERVAL:
            logger.info("Auto-reset: Time interval exceeded")
            biocore = get_biocomputing_core()
            biocore_last_reset = current_time
            biocore_error_count = 0
        elif biocore_error_count >= AUTO_RESET_ERROR_THRESHOLD:
            logger.info("Auto-reset: Error threshold reached")
            biocore = get_biocomputing_core()
            biocore_error_count = 0
```

**Why This Matters**:
- Prevents memory leaks from accumulated state
- Ensures consistent performance over long sessions
- Automatically recovers from transient errors
- No manual intervention required
- **Servers never crash** - they self-heal

**Monitoring Auto-Reset**:
```powershell
# Check when next reset will occur
curl http://localhost:5001/api/status

# Manually trigger reset
curl -X POST http://localhost:5001/api/reset

# Monitor in real-time
python biocore_monitor.py --monitor --interval 10
```

---

## 📊 Data Flow Diagrams

### Query Processing Flow

```
User Input (HTML Interface)
    │
    ▼
[1] POST Request to API Server
    │ {query: "...", session_id: "..."}
    │
    ▼
[2] Flask Server Receives Request
    │ • Validate JSON
    │ • Extract parameters
    │
    ▼
[3] Get/Reset Biocore (if needed)
    │ • Check auto-reset conditions
    │ • Reset if necessary
    │
    ▼
[4] Create NeuralQuery
    │ • Infer domain
    │ • Set priority
    │ • Add context
    │
    ▼
[5] BIOCOMPUTING_CORE Processing
    │ • Neural organoid simulation
    │ • Pattern recognition
    │ • Cross-domain synthesis
    │
    ▼
[6] Generate BiologicalResponse
    │ • Response text
    │ • Confidence score
    │ • Domain classification
    │ • Reasoning trace
    │
    ▼
[7] Serialize to JSON
    │ {response: "...", confidence: 0.95}
    │
    ▼
[8] HTTP Response to Client
    │
    ▼
[9] HTML Interface Updates
    │ • Display response
    │ • Update telemetry
    │ • Log to console
```

### Code Generation Flow

```
Code Request (TPCA Interface)
    │
    ▼
[1] POST to /api/generate
    │ {query: "...", language: "python", complexity: 5}
    │
    ▼
[2] ThalosCodingAgentCore.generate_code()
    │ • Parse request
    │ • Infer mode (function/class/API)
    │ • Detect language
    │
    ▼
[3] Expert System Processing
    │ • Select patterns
    │ • Apply templates
    │ • Generate scaffolding
    │
    ▼
[4] Code Generation
    │ • Main code
    │ • Unit tests
    │ • Documentation
    │
    ▼
[5] Validation
    │ • Complexity analysis
    │ • Security checks
    │ • Syntax verification
    │
    ▼
[6] CodeArtifact Assembly
    │ • Package all components
    │ • Add metadata
    │
    ▼
[7] JSON Response
    │ {code: "...", tests: "...", docs: "..."}
    │
    ▼
[8] Syntax Highlighting Display
```

### System Startup Flow

```
DEPLOY_THALOS_PRIME.bat
    │
    ▼
[1] Environment Checks
    │ • Python installed?
    │ • Virtual env exists?
    │
    ▼
[2] Create/Activate Virtual Environment
    │ • python -m venv .venv
    │ • .venv\Scripts\activate.bat
    │
    ▼
[3] Install Dependencies
    │ • pip install -r requirements.txt
    │ • numpy, flask, flask-cors, requests
    │
    ▼
[4] Check Port Availability
    │ • netstat -ano | findstr :5001
    │ • Kill existing process if needed
    │
    ▼
[5] Start BIOCORE Server
    │ • python biocomputing_api_server.py --port 5001
    │ • Wait for initialization (30s timeout)
    │
    ▼
[6] Health Check
    │ • curl http://localhost:5001/api/health
    │ • Verify {"status": "healthy"}
    │
    ▼
[7] Launch HTML Modules
    │ • start thalos_celestial.html
    │ • Optional: start thalos_coding_agent.html
    │
    ▼
[8] Display Status Dashboard
    │ • Server URL
    │ • Module status
    │ • Command references
```

---

## 🔐 Security & Persistence

### Database Schema

**File**: `thalos_database_schema.py`

**14 Core Tables**:
1. `system_config` - Global parameters
2. `sessions` - User sessions with metadata
3. `interactions` - Query-response pairs
4. `context_memory` - Conversation history
5. `model_parameters` - Encrypted neural weights
6. `embedding_cache` - Token embeddings
7. `reasoning_traces` - Decision logs
8. `confidence_scores` - Quality metrics
9. `encryption_keys` - Session-specific keys
10. `security_log` - Security events
11. `model_version_history` - Model evolution
12. `intent_patterns` - Intent templates
13. `semantic_mappings` - Vector mappings
14. `performance_metrics` - System KPIs

**Encryption**:
- AES-256-GCM for model parameters
- Per-session cryptographic keys
- Encrypted context storage
- Security event logging

### Integration Reports

**Auto-Generated Files**: `integration_report_cycle_N.json` (N = 1-51)

**Purpose**: Track system health across development cycles

**Tracked Metrics**:
```json
{
    "cycle": 50,
    "files_scanned": {
        "python": 23,
        "html": 4,
        "batch": 27,
        "markdown": 33
    },
    "missing_imports": [],
    "missing_files": [],
    "integration_status": {
        "biocore_import": true,
        "sbi_import": true,
        "coding_import": true,
        "autonomous_core": true,
        "server_running": true
    },
    "total_fixes_applied": 0
}
```

**Generation**: Automated by `infinite_integration.py`

---

## 🚀 Deployment Configurations

### Configuration 1: Full Stack (Recommended)

**Components**: All servers + all modules
**Use Case**: Complete development environment

```powershell
# Single command deployment
.\DEPLOY_THALOS_PRIME.bat
```

**Active Servers**:
- BIOCORE (5001)
- HYPER-NEXTUS (5000) - Optional
- Deploy Server (8080)

### Configuration 2: Minimal Stack

**Components**: BIOCORE + Celestial interface only
**Use Case**: Lightweight testing

```powershell
# Start BIOCORE
python biocomputing_api_server.py --port 5001

# Open interface
start thalos_celestial.html
```

### Configuration 3: Standalone Offline

**Components**: HTML modules only (no servers)
**Use Case**: Offline demonstrations

```powershell
# Direct launch
start thalos_prime_primary_directive.html
```

**Note**: Uses hardcoded offline intelligence

### Configuration 4: Code Generation Specialist

**Components**: TPCA server only
**Use Case**: Code generation tasks

```powershell
# Start TPCA
python tpca_api_server.py --port 5002

# Open coding interface
start thalos_coding_agent.html
```

---

## 📈 Monitoring & Diagnostics

### Health Check Endpoints

```powershell
# BIOCORE health
curl http://localhost:5001/api/health
# Expected: {"status": "healthy", "biocomputing_core": "operational"}

# TPCA health
curl http://localhost:5002/api/health
# Expected: {"status": "online", "version": "8.0"}

# HYPER-NEXTUS health
curl http://localhost:5000/api/health
# Expected: {"status": "operational"}
```

### Monitoring Tools

**biocore_monitor.py**:
```powershell
# Interactive dashboard
python biocore_monitor.py --dashboard

# Real-time monitoring (10s intervals)
python biocore_monitor.py --monitor --interval 10

# Quick status check
python biocore_monitor.py
```

**System Verification**:
```powershell
# Full system check
.\VERIFY_SYSTEM.bat

# Deployment verification
.\VERIFY_DEPLOYMENT.bat
```

### Log Files

- `biocore_api.log` - BIOCORE operations
- `tpca_api.log` - Code generation logs
- `deploy_server.log` - HTML hosting logs
- `autonomous_core.log` - Self-healing operations
- `optimization_log.txt` - Optimization history

---

## 🔬 Advanced Features

### Virtual Environment (Windows-Specific)

**Location**: `.\.venv\Scripts\`

**Key Files**:
- `python.exe` - Python interpreter
- `activate.bat` - Activation script
- `pip.exe` - Package manager

**Activation**:
```powershell
# Always use Scripts\ on Windows
.\.venv\Scripts\activate.bat

# NOT .venv/bin/activate (Linux/Mac)
```

**Why Virtual Environment is Mandatory**:
- Isolates dependencies from system Python
- Prevents version conflicts
- Ensures reproducible deployments
- Required by all deployment scripts

### Autonomous Operations

**Self-Healing Components**:
- `autonomous_core.py` - Continuous system monitoring
- `infinite_integration.py` - Integration health checks
- `perpetual_optimizer.py` - Performance optimization
- `auto_enhancer.py` - Code quality improvements

**Auto-Recovery Features**:
- Server auto-restart after crashes
- Import error detection and fixing
- Missing file restoration
- Syntax error correction
- Integration report generation

### "Biocomputing" Terminology

**Not Just Marketing** - Actual wetware concepts:

- **Neural Organoids**: Simulated brain tissue computational units
- **Synaptic Connections**: Information pathways between organoids
- **Wetware Processing**: Biological (organic) computation metaphor
- **Pattern Recognition**: Neural network-inspired analysis
- **Cross-Domain Synthesis**: Multi-sensory integration (like human cognition)

**Inspiration**: Actual lab-grown neural organoids used in research

---

## 📚 Related Documentation

- `DEVELOPMENT_GUIDE.md` - Development workflows and conventions
- `COMPONENT_INTERACTIONS.md` - Component integration details
- `TESTING_STRATEGY.md` - Testing approaches and patterns
- `DEPLOYMENT_README.md` - Deployment instructions
- `TECHNICAL_SPECIFICATION.txt` - Technical specifications
- `START_HERE.md` - Quick start guide

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-08  
**System Version**: THALOS PRIME v9.0
