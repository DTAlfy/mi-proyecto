#!/usr/bin/env python3
"""Atajo: `python builder.py ...` desde la raíz. El código vive en 00_Sistema/scripts/builder.py"""

import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).resolve().parent / "00_Sistema" / "scripts" / "builder.py"), run_name="__main__")
