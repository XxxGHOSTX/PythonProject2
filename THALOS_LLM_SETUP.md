# THALOS PRIME - Local LLM Setup (Ollama)

This guide wires a local LLM to THALOS PRIME using Ollama.

## Requirements

- Ollama installed and running locally.
- A model pulled in Ollama.

## Quick Start

1) Install Ollama (if not already installed).
2) Pull a model:

```
ollama pull llama3.1:8b
```

3) Start the unified server:

```
python hyper_nextus_server.py
```

## Configure Model/Host

Set environment variables before launch:

- `THALOS_OLLAMA_URL` (default `http://localhost:11434`)
- `THALOS_OLLAMA_MODEL` (default `llama3.1:8b`)

Example (PowerShell):

```
$env:THALOS_OLLAMA_MODEL = "llama3.1:8b"
$env:THALOS_OLLAMA_URL = "http://localhost:11434"
python hyper_nextus_server.py
```

## Endpoints

- `POST /api/llm/query`
  - Body:

```
{
  "query": "Hello from THALOS",
  "system": "You are THALOS PRIME.",
  "options": {"temperature": 0.7}
}
```

- `POST /api/llm/stream`
  - Same body as `/api/llm/query`, returns a streaming response.

- `POST /api/llm/agent`
  - Same body as `/api/llm/query`, enables tool orchestration.

- `GET /api/llm/health`

## UI Commands (thalos_prime.html)

- `/agent on|off`
- `/stream on|off`
- `/read path`
- `/write path :: content`
- `/fetch url`

## Notes

- If Ollama is not running, the server will report local LLM as unavailable.
- The unified server falls back to existing SBI patterns for other endpoints.
