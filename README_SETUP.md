Windows setup (PowerShell or CMD)

1) From project root (recommended):

    cd "C:\Users\LT\Desktop\THALOS PRIME\PythonProject2"

2) Create and activate a virtual environment (CMD):

    python -m venv .venv
    .venv\Scripts\activate

   Or PowerShell (if ExecutionPolicy allows):

    python -m venv .venv
    .\.venv\Scripts\Activate.ps1

3) Upgrade pip and install requirements:

    python -m pip install --upgrade pip
    pip install -r requirements.txt

4) Run the application (example):

    python thalos_sbi_app.py

Troubleshooting

- If you ran `pip install -r requirements.txt` from `C:\Windows\System32` (as in your error), pip couldn't find the file because you were in the wrong working directory. Change to the project directory before running the command.

- If Python isn't found, install Python 3.10+ and ensure it's on PATH.

- If tkinter GUI modules are required, ensure the OS-level tkinter is installed (Windows Python installer includes it by default).

- To remove and recreate the venv, delete the `.venv` folder and rerun `setup_env.bat`.


Notes

- Current minimal dependency: numpy. If you later add features that rely on external packages (requests, pillow, cryptography, torch, tensorflow, etc.) add them to `requirements.txt`.

## Automated deployment and launch (Windows)

Two helper `.bat` scripts were added to automate environment setup and launching:

- `setup_env.bat` — creates a virtual environment and installs dependencies (`requirements.txt`). Run this first if you want just environment setup.
- `deploy_auto.bat` — creates/activates the venv, installs deps, and launches the general deployment server.
- `deploy_coding_agent.bat` — same setup flow but opens only the Coding Agent UI (`thalos_coding_agent.html`) on a free port.
- `run_thalos.bat coding` — activate venv and launch Coding Agent via the unified launcher.

Examples (PowerShell/CMD):

    cd "C:\Users\LT\Desktop\THALOS PRIME\PythonProject2"
    .\deploy_coding_agent.bat

or to start the full deploy server:

    .\deploy_auto.bat
