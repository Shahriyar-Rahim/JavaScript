#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
import subprocess

repo_root = Path(__file__).resolve().parents[2]
readme_path = repo_root / "README.md"


def get_git_branch():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=str(repo_root),
            text=True,
        ).strip() or "main"
    except Exception:
        return "main"


def count_repo_files():
    try:
        return sum(
            1
            for p in repo_root.rglob("*")
            if p.is_file() and ".git" not in p.parts
        )
    except Exception:
        return 0


def list_top_level_entries():
    try:
        return ", ".join(
            sorted(p.name for p in repo_root.iterdir() if p.name != ".git")
        )
    except Exception:
        return "repository"

branch = get_git_branch()
last_update = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
file_count = count_repo_files()
entries = list_top_level_entries()

readme = readme_path.read_text(encoding="utf-8")
start_marker = "<!-- AUTO-README:START -->"
end_marker = "<!-- AUTO-README:END -->"

replacement = f"""{start_marker}
## 🧾 Repository Snapshot

- Repository: JavaScript
- Branch: {branch}
- Last auto-update: {last_update}
- Learning status: active
- Files tracked: {file_count}
- Top-level content: {entries}

{end_marker}"""

if start_marker in readme and end_marker in readme:
    before, _ = readme.split(start_marker)
    _, after = readme.split(end_marker)
    updated = before + replacement + after
else:
    updated = readme + "\n\n" + replacement + "\n"

readme_path.write_text(updated, encoding="utf-8")
print(f"README refreshed on branch {branch} at {last_update}")
