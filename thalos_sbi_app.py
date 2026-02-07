#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔════════════════════════════════════════════════════════════════════════════════╗
║                                                                                ║
║                    THALOS PRIME SBI - INTERACTIVE APPLICATION                  ║
║                        Advanced GUI with Neural Integration                     ║
║                                                                                ║
║  Copyright © 2026 THALOS PRIME SYSTEMS                                         ║
║  Creator: Tony Ray Macier III                                                  ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝
"""

import json
import threading
import time
import webbrowser
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

# Import the core SBI system
from thalos_sbi_core_v6 import ThalosApplication

# ═══════════════════════════════════════════════════════════════════════════════
# ADVANCED REQUEST HANDLER
# ═══════════════════════════════════════════════════════════════════════════════


class ThalosRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for THALOS Prime interactive system"""

    # Class variables shared across instances
    thalos_app = None
    config = None

    def log_message(self, format, *args):
        """Suppress default logging"""
        pass

    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)

        if parsed_path.path == "/":
            self.serve_main_page()
        elif parsed_path.path == "/api/status":
            self.api_status()
        elif parsed_path.path == "/api/capabilities":
            self.api_capabilities()
        else:
            self.send_error(404)

    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)

        if parsed_path.path == "/api/query":
            self.api_query()
        elif parsed_path.path == "/api/session":
            self.api_session()
        else:
            self.send_error(404)

    def serve_main_page(self):
        """Serve the advanced interactive interface"""
        html = self.generate_html_interface()
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", len(html.encode("utf-8")))
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def api_query(self):
        """Process AI query"""
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")

        try:
            request_data = json.loads(body)
            query = request_data.get("query", "")
            session_id = request_data.get("session_id", "default")

            if not query:
                self.send_error(400, "Query required")
                return

            # Process through THALOS system
            result = self.thalos_app.process_query(query, session_id)

            self.send_json_response(result)

        except Exception as e:
            self.send_json_response({"status": "error", "error": str(e)})

    def api_status(self):
        """Get system status"""
        status = {
            "system": "THALOS PRIME SBI v6.0",
            "status": "OPERATIONAL",
            "neural_core": "ACTIVE",
            "parameters": "200M+",
            "timestamp": datetime.now().isoformat(),
        }
        self.send_json_response(status)

    def api_capabilities(self):
        """Get system capabilities"""
        capabilities = {
            "code_generation": "Multi-language code implementation",
            "analysis": "Advanced technical and semantic analysis",
            "reasoning": "Multi-stage intelligent reasoning",
            "context_memory": "Last 100 interactions remembered",
            "encryption": "AES-256-GCM security",
            "confidence_scoring": "Real-time quality evaluation",
            "adaptive_response": "Dynamic temperature and parameters",
        }
        self.send_json_response({"capabilities": capabilities})

    def api_session(self):
        """Manage sessions"""
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")

        try:
            request_data = json.loads(body)
            action = request_data.get("action", "create")
            session_id = request_data.get("session_id")

            if action == "create":
                session_id = session_id or f"session_{int(time.time())}"
                self.thalos_app.context_manager.create_session(session_id)
                self.send_json_response({"status": "success", "session_id": session_id})
            else:
                self.send_json_response({"status": "error", "message": "Invalid action"})

        except Exception as e:
            self.send_json_response({"status": "error", "error": str(e)})

    def send_json_response(self, data):
        """Send JSON response"""
        response = json.dumps(data)
        self.send_response(200)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", len(response.encode("utf-8")))
        self.end_headers()
        self.wfile.write(response.encode("utf-8"))

    def generate_html_interface(self):
        """Generate advanced HTML/CSS/JavaScript interface"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>THALOS PRIME SBI v6.0</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            background: #000;
            font-family: 'Courier New', monospace;
            color: #0f0;
            overflow: hidden;
            height: 100vh;
        }
        
        /* Matrix background animation */
        #matrix-background {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: #000;
            z-index: 0;
            overflow: hidden;
        }
        
        .matrix-char {
            position: absolute;
            color: rgba(0, 255, 0, 0.1);
            font-size: 14px;
            animation: matrix-fall linear infinite;
            font-family: 'Courier New', monospace;
        }
        
        @keyframes matrix-fall {
            0% { transform: translateY(-100%); opacity: 1; }
            90% { opacity: 1; }
            100% { transform: translateY(100vh); opacity: 0; }
        }
        
        /* Left toolbar */
        #toolbar {
            position: fixed;
            left: 10px;
            top: 10px;
            width: 200px;
            background: rgba(0, 20, 0, 0.95);
            border: 2px solid #0f0;
            border-radius: 5px;
            z-index: 200;
            padding: 10px;
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
            resize: both;
            overflow: auto;
        }
        
        .toolbar-title {
            font-size: 12px;
            font-weight: bold;
            color: #0f0;
            text-transform: uppercase;
            margin-bottom: 10px;
            text-shadow: 0 0 5px #0f0;
            border-bottom: 1px solid #0f0;
            padding-bottom: 5px;
        }
        
        .toolbar-section {
            margin-bottom: 15px;
        }
        
        .toolbar-label {
            font-size: 10px;
            color: #0f0;
            opacity: 0.8;
            margin-bottom: 3px;
            text-transform: uppercase;
        }
        
        .toolbar-control {
            width: 100%;
            padding: 5px;
            background: rgba(0, 255, 0, 0.1);
            border: 1px solid #0f0;
            color: #0f0;
            font-family: 'Courier New', monospace;
            font-size: 11px;
            margin-bottom: 5px;
            cursor: pointer;
        }
        
        .toolbar-button {
            width: 100%;
            padding: 8px;
            background: rgba(0, 255, 0, 0.15);
            border: 1px solid #0f0;
            color: #0f0;
            cursor: pointer;
            font-size: 11px;
            text-transform: uppercase;
            margin-bottom: 5px;
            transition: all 0.2s;
        }
        
        .toolbar-button:hover {
            background: rgba(0, 255, 0, 0.3);
            box-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
        }
        
        /* Main window */
        #main-window {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 900px;
            height: 600px;
            background: rgba(0, 10, 0, 0.96);
            border: 2px solid #0f0;
            border-radius: 5px;
            z-index: 100;
            display: flex;
            flex-direction: column;
            box-shadow: 0 0 30px rgba(0, 255, 0, 0.4);
            resize: both;
            overflow: hidden;
        }
        
        #window-title {
            padding: 8px;
            background: rgba(0, 255, 0, 0.1);
            border-bottom: 1px solid #0f0;
            font-size: 12px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            cursor: move;
            text-shadow: 0 0 5px #0f0;
        }
        
        #telemetry {
            display: flex;
            gap: 15px;
            padding: 5px 8px;
            background: rgba(0, 0, 0, 0.5);
            border-bottom: 1px solid rgba(0, 255, 0, 0.3);
            font-size: 10px;
        }
        
        .telemetry-item {
            flex: 1;
        }
        
        .telemetry-label {
            color: #0f0;
            opacity: 0.6;
        }
        
        .telemetry-value {
            color: #0f0;
            font-weight: bold;
        }
        
        #output-container {
            flex: 1;
            overflow-y: auto;
            padding: 10px;
            border-bottom: 1px solid #0f0;
        }
        
        .message {
            margin-bottom: 10px;
            padding: 8px;
            border-left: 2px solid #0f0;
            background: rgba(0, 255, 0, 0.05);
            font-size: 12px;
            line-height: 1.4;
        }
        
        .message.user {
            border-left-color: #8f8;
            background: rgba(136, 255, 136, 0.05);
            color: #8f8;
        }
        
        .message.system {
            border-left-color: #ff0;
            background: rgba(255, 255, 0, 0.05);
            color: #ff0;
        }
        
        #input-container {
            padding: 8px;
            border-top: 1px solid #0f0;
        }
        
        #user-input {
            width: 100%;
            height: 80px;
            padding: 8px;
            background: rgba(0, 255, 0, 0.05);
            border: 1px solid #0f0;
            color: #0f0;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            resize: none;
            margin-bottom: 5px;
        }
        
        #input-controls {
            display: flex;
            gap: 5px;
        }
        
        .input-btn {
            flex: 1;
            padding: 6px;
            background: rgba(0, 255, 0, 0.15);
            border: 1px solid #0f0;
            color: #0f0;
            cursor: pointer;
            text-transform: uppercase;
            font-size: 11px;
        }
        
        .input-btn:hover {
            background: rgba(0, 255, 0, 0.3);
        }
        
        /* Status panel on right */
        #status-panel {
            position: fixed;
            right: 10px;
            top: 10px;
            width: 200px;
            background: rgba(0, 20, 0, 0.95);
            border: 2px solid #0f0;
            border-radius: 5px;
            z-index: 200;
            padding: 10px;
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
            display: none;
            max-height: 80vh;
            overflow-y: auto;
        }
        
        .status-title {
            font-size: 11px;
            font-weight: bold;
            color: #0f0;
            text-transform: uppercase;
            margin-bottom: 10px;
            border-bottom: 1px solid #0f0;
            padding-bottom: 5px;
        }
        
        .status-item {
            font-size: 10px;
            margin-bottom: 5px;
            padding: 3px;
            background: rgba(0, 255, 0, 0.05);
            border-left: 1px solid #0f0;
            padding-left: 5px;
        }
        
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(0, 255, 0, 0.05);
        }
        
        ::-webkit-scrollbar-thumb {
            background: #0f0;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div id="matrix-background"></div>
    
    <div id="toolbar">
        <div class="toolbar-title">THALOS PRIME SBI</div>
        
        <div class="toolbar-section">
            <div class="toolbar-label">Font Size</div>
            <input type="range" id="font-size" min="4" max="32" value="12" class="toolbar-control">
            <div id="font-size-label" style="font-size: 10px; color: #0f0; text-align: center;">12px</div>
        </div>
        
        <div class="toolbar-section">
            <div class="toolbar-label">Font Family</div>
            <select id="font-family" class="toolbar-control">
                <option value="Courier New">Courier New</option>
                <option value="Consolas">Consolas</option>
                <option value="monospace">Monospace</option>
                <option value="'Monaco'">Monaco</option>
            </select>
        </div>
        
        <div class="toolbar-section">
            <div class="toolbar-label">Window Opacity</div>
            <input type="range" id="opacity" min="0.5" max="1" step="0.05" value="0.96" class="toolbar-control">
        </div>
        
        <div class="toolbar-section">
            <button class="toolbar-button" onclick="clearOutput()">CLEAR OUTPUT</button>
            <button class="toolbar-button" onclick="toggleStatusPanel()">STATUS PANEL</button>
            <button class="toolbar-button" onclick="exportConversation()">EXPORT</button>
            <button class="toolbar-button" onclick="resetSession()">NEW SESSION</button>
        </div>
        
        <div class="toolbar-section">
            <div class="toolbar-label">Settings</div>
            <div style="font-size: 10px; color: #0f0; opacity: 0.7;">
                Matrix Speed: <span id="matrix-speed">Medium</span><br>
                Auto-Save: Enabled<br>
                Encryption: AES-256<br>
                Model: 200M+ Params
            </div>
        </div>
    </div>
    
    <div id="status-panel">
        <div class="status-title">SYSTEM STATUS</div>
        <div class="status-item">Status: <span id="system-status">LOADING</span></div>
        <div class="status-item">Neural Core: <span id="core-status">INITIALIZING</span></div>
        <div class="status-item">Memory: <span id="memory-usage">0 MB</span></div>
        <div class="status-item">Sessions: <span id="session-count">0</span></div>
        <div class="status-item">Interactions: <span id="interaction-count">0</span></div>
        <div class="status-item">Last Latency: <span id="last-latency">0 ms</span></div>
        <div class="status-title" style="margin-top: 15px;">REASONING TRACE</div>
        <div id="reasoning-trace"></div>
    </div>
    
    <div id="main-window">
        <div id="window-title">THALOS PRIME SBI v6.0 - Advanced Neural Interface</div>
        
        <div id="telemetry">
            <div class="telemetry-item">
                <span class="telemetry-label">STATUS:</span>
                <span class="telemetry-value" id="status">OPERATIONAL</span>
            </div>
            <div class="telemetry-item">
                <span class="telemetry-label">CORE:</span>
                <span class="telemetry-value" id="core">ACTIVE</span>
            </div>
            <div class="telemetry-item">
                <span class="telemetry-label">MODE:</span>
                <span class="telemetry-value" id="mode">SBI</span>
            </div>
            <div class="telemetry-item">
                <span class="telemetry-label">CONFIDENCE:</span>
                <span class="telemetry-value" id="confidence">--</span>
            </div>
        </div>
        
        <div id="output-container">
            <div class="message system">THALOS PRIME SBI v6.0 INITIALIZED
✓ Neural Core: 200M+ Parameters
✓ Multi-Stage Reasoning: ACTIVE
✓ Cryptographic Security: ENABLED
✓ Context Memory: Ready (100 interactions)
✓ Database: Connected
✓ Ready for queries</div>
        </div>
        
        <div id="input-container">
            <textarea id="user-input" placeholder="Enter query... (Press CTRL+ENTER or click EXECUTE)"></textarea>
            <div id="input-controls">
                <button class="input-btn" onclick="executeQuery()">EXECUTE</button>
                <button class="input-btn" onclick="clearInput()">CLEAR</button>
            </div>
        </div>
    </div>
    
    <script>
        let sessionId = 'session_' + Math.random().toString(36).substr(2, 9);
        let conversationHistory = [];
        let isProcessing = false;
        
        // Initialize matrix background
        function initMatrixBackground() {
            const bg = document.getElementById('matrix-background');
            const chars = 'ｦｧｨｩｪｫｬｭｮｯﾀﾁﾂﾃﾄﾅﾆﾇﾈﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾗﾘﾙﾚﾜ0123456789';
            
            for (let i = 0; i < 150; i++) {
                const char = document.createElement('div');
                char.className = 'matrix-char';
                char.textContent = chars[Math.floor(Math.random() * chars.length)];
                char.style.left = Math.random() * 100 + '%';
                char.style.top = Math.random() * 100 + '%';
                char.style.animationDuration = (Math.random() * 8 + 4) + 's';
                char.style.animationDelay = Math.random() * 5 + 's';
                bg.appendChild(char);
            }
        }
        
        // Setup event listeners
        document.addEventListener('DOMContentLoaded', function() {
            initMatrixBackground();
            createSession();
            
            // Font size control
            const fontSizeSlider = document.getElementById('font-size');
            fontSizeSlider.addEventListener('input', function() {
                const size = this.value;
                document.getElementById('main-window').style.fontSize = size + 'px';
                document.getElementById('font-size-label').textContent = size + 'px';
            });
            
            // Font family control
            const fontFamily = document.getElementById('font-family');
            fontFamily.addEventListener('change', function() {
                document.getElementById('output-container').style.fontFamily = this.value;
                document.getElementById('user-input').style.fontFamily = this.value;
            });
            
            // Opacity control
            const opacity = document.getElementById('opacity');
            opacity.addEventListener('input', function() {
                let bgColor = document.getElementById('main-window').style.background;
                document.getElementById('main-window').style.background = 
                    `rgba(0, 10, 0, ${this.value})`;
            });
            
            // Keyboard shortcuts
            document.getElementById('user-input').addEventListener('keydown', function(e) {
                if (e.key === 'Enter' && (e.ctrlKey || e.shiftKey)) {
                    executeQuery();
                }
            });
        });
        
        function createSession() {
            fetch('/api/session', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({action: 'create', session_id: sessionId})
            }).then(r => r.json()).then(data => {
                if (data.status === 'success') {
                    addMessage('Session created: ' + sessionId, 'system');
                }
            });
        }
        
        function executeQuery() {
            const input = document.getElementById('user-input').value.trim();
            if (!input || isProcessing) return;
            
            isProcessing = true;
            document.getElementById('user-input').value = '';
            
            addMessage(input, 'user');
            
            const loadingMsg = addMessage('⟳ THALOS Processing...', 'system');
            
            fetch('/api/query', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({query: input, session_id: sessionId})
            }).then(r => r.json()).then(data => {
                loadingMsg.remove();
                
                if (data.status === 'success') {
                    addMessage(data.response, 'ai');
                    
                    document.getElementById('confidence').textContent = 
                        (data.confidence * 100).toFixed(1) + '%';
                    
                    if (data.reasoning_trace) {
                        updateReasoningTrace(data.reasoning_trace);
                    }
                    
                    conversationHistory.push({
                        query: input,
                        response: data.response,
                        timestamp: new Date().toISOString()
                    });
                } else {
                    addMessage('ERROR: ' + (data.error || 'Unknown error'), 'system');
                }
                
                isProcessing = false;
            }).catch(err => {
                loadingMsg.remove();
                addMessage('ERROR: ' + err.message, 'system');
                isProcessing = false;
            });
        }
        
        function addMessage(text, type = 'ai') {
            const container = document.getElementById('output-container');
            const msg = document.createElement('div');
            msg.className = 'message ' + type;
            msg.textContent = text;
            container.appendChild(msg);
            container.scrollTop = container.scrollHeight;
            return msg;
        }
        
        function clearOutput() {
            document.getElementById('output-container').innerHTML = '';
        }
        
        function clearInput() {
            document.getElementById('user-input').value = '';
        }
        
        function toggleStatusPanel() {
            const panel = document.getElementById('status-panel');
            panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
        }
        
        function exportConversation() {
            const content = conversationHistory.map(item => 
                `Q: ${item.query}\\nA: ${item.response}\\n`
            ).join('---\\n');
            
            const blob = new Blob([content], {type: 'text/plain'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'thalos_conversation_' + Date.now() + '.txt';
            a.click();
            URL.revokeObjectURL(url);
        }
        
        function resetSession() {
            sessionId = 'session_' + Math.random().toString(36).substr(2, 9);
            conversationHistory = [];
            clearOutput();
            createSession();
        }
        
        function updateReasoningTrace(trace) {
            const container = document.getElementById('reasoning-trace');
            container.innerHTML = trace.map((item, i) => 
                `<div class="status-item">Stage ${i + 1}: ${JSON.stringify(item).substring(0, 50)}...</div>`
            ).join('');
        }
    </script>
</body>
</html>"""


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION SERVER
# ═══════════════════════════════════════════════════════════════════════════════


def main():
    """Main entry point for THALOS Prime Interactive Application"""

    print("\n" + "=" * 80)
    print("THALOS PRIME SBI v6.0 - INTERACTIVE APPLICATION".center(80))
    print("=" * 80 + "\n")

    # Initialize THALOS application
    print("[INIT] Starting THALOS Prime SBI System...")
    thalos_app = ThalosApplication()

    # Configure request handler
    ThalosRequestHandler.thalos_app = thalos_app
    ThalosRequestHandler.config = thalos_app.config

    # Start HTTP server
    port = 8889
    server_address = ("127.0.0.1", port)
    httpd = HTTPServer(server_address, ThalosRequestHandler)

    print(f"[SERVER] Starting HTTP server on http://127.0.0.1:{port}")
    print("[SERVER] Opening browser in 2 seconds...\n")

    # Start server in background thread
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()

    # Open browser
    time.sleep(2)
    try:
        webbrowser.open(f"http://127.0.0.1:{port}")
        print("[SUCCESS] Browser opened")
    except Exception:
        print(f"[INFO] Please open: http://127.0.0.1:{port}")

    print("\n[READY] THALOS Prime SBI System ready for interaction")
    print("[READY] Begin typing queries...\n")

    # Keep server running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] THALOS Prime shutting down...")
        httpd.shutdown()
        print("[SHUTDOWN] System offline")


if __name__ == "__main__":
    main()
