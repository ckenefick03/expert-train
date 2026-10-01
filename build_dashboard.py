#!/usr/bin/env python3
"""Regenerate dashboard.html from state.md (source of truth).

Usage: python3 build_dashboard.py
Reads the JSON block under "## DASHBOARD_DATA" in state.md, injects it into
dashboard.template.html, and writes a self-contained dashboard.html.
Never hand-edit dashboard.html; run this at the end of every cycle.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
state = (ROOT / "state.md").read_text(encoding="utf-8")
template = (ROOT / "dashboard.template.html").read_text(encoding="utf-8")

section = re.search(r"^## DASHBOARD_DATA\s*$(.*?)(?=^## )", state, re.S | re.M)
if not section:
    sys.exit("state.md: '## DASHBOARD_DATA' section not found")
block = re.search(r"```json\s*(.*?)```", section.group(1), re.S)
if not block:
    sys.exit("state.md: json block under DASHBOARD_DATA not found")

try:
    data = json.loads(block.group(1))
except json.JSONDecodeError as e:
    sys.exit(f"state.md: DASHBOARD_DATA is not valid JSON: {e}")

for key in ("account", "risk", "equity_history", "positions", "trades"):
    if key not in data:
        sys.exit(f"state.md: DASHBOARD_DATA missing '{key}'")

payload = json.dumps(data).replace("</", "<\\/")
if "/*__DATA__*/null" not in template:
    sys.exit("dashboard.template.html: data placeholder missing")
(ROOT / "dashboard.html").write_text(template.replace("/*__DATA__*/null", payload), encoding="utf-8")
print("dashboard.html regenerated from state.md")
