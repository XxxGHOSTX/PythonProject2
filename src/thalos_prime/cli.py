"""CLI entrypoint that bridges to the legacy root launcher."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path


def main() -> int:
    """Run the legacy launcher from the project root."""
    project_root = Path(__file__).resolve().parents[2]
    main_path = project_root / "main.py"

    if not main_path.is_file():
        print("Error: main.py not found in project root.")
        return 1

    sys.path.insert(0, str(project_root))
    runpy.run_path(str(main_path), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
