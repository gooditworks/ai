#!/usr/bin/env python3
"""
Gather session data for reflection analysis.

Collects git activity, beads status, and file changes as structured JSON.
Claude analyzes this data to identify improvement patterns.

Usage:
    python scripts/gather_session.py [--commits N] [--json]

Output: JSON with raw session data for Claude to analyze.
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_command(cmd: list[str], cwd: str | None = None) -> tuple[bool, str]:
    """Run a command and return (success, output)."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=30,  # 30s timeout for slow git operations
        )
        return result.returncode == 0, result.stdout.strip()
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except FileNotFoundError:
        return False, f"Command not found: {cmd[0]}"


def get_git_data(num_commits: int = 20) -> dict:
    """Gather git activity data."""
    git_data = {
        "branch": "",
        "commits": [],
        "diff_stats": {},
        "status": [],
        "available": False,
    }

    # Check if in git repo
    success, _ = run_command(["git", "rev-parse", "--git-dir"])
    if not success:
        return git_data

    git_data["available"] = True

    # Current branch
    success, branch = run_command(["git", "branch", "--show-current"])
    if success:
        git_data["branch"] = branch

    # Recent commits with files changed
    success, log_output = run_command([
        "git", "log", f"-{num_commits}",
        "--pretty=format:%H|%s|%an|%ar",
        "--name-only"
    ])
    if success and log_output:
        commits = []
        current_commit = None
        for line in log_output.split("\n"):
            if "|" in line:
                parts = line.split("|")
                if len(parts) >= 4:
                    current_commit = {
                        "hash": parts[0][:8],
                        "message": parts[1],
                        "author": parts[2],
                        "when": parts[3],
                        "files": [],
                    }
                    commits.append(current_commit)
            elif line.strip() and current_commit:
                current_commit["files"].append(line.strip())
        git_data["commits"] = commits

    # Diff stats by file type
    success, diff_output = run_command([
        "git", "diff", "--stat", f"HEAD~{min(num_commits, 5)}..HEAD"
    ])
    if success and diff_output:
        stats = {"total_files": 0, "by_extension": {}}
        for line in diff_output.split("\n"):
            if "|" in line:
                filename = line.split("|")[0].strip()
                ext = Path(filename).suffix or "(no ext)"
                stats["by_extension"][ext] = stats["by_extension"].get(ext, 0) + 1
                stats["total_files"] += 1
        git_data["diff_stats"] = stats

    # Current status (modified/untracked files)
    success, status_output = run_command(["git", "status", "--porcelain"])
    if success and status_output:
        git_data["status"] = [
            {"state": line[:2].strip(), "file": line[3:]}
            for line in status_output.split("\n")
            if line.strip()
        ]

    return git_data


def get_beads_data() -> dict:
    """Gather beads issue tracker data."""
    beads_data = {
        "closed": [],
        "created": [],
        "in_progress": [],
        "available": False,
    }

    # Check if bd command exists
    success, _ = run_command(["which", "bd"])
    if not success:
        return beads_data

    # Check if .beads directory exists
    if not Path(".beads").exists():
        return beads_data

    beads_data["available"] = True

    # Get closed issues (recent)
    success, output = run_command(["bd", "list", "--status=closed", "--limit=10", "--json"])
    if success and output:
        try:
            beads_data["closed"] = json.loads(output)
        except json.JSONDecodeError:
            pass

    # Get in-progress issues
    success, output = run_command(["bd", "list", "--status=in_progress", "--json"])
    if success and output:
        try:
            beads_data["in_progress"] = json.loads(output)
        except json.JSONDecodeError:
            pass

    # Get open issues
    success, output = run_command(["bd", "list", "--status=open", "--limit=10", "--json"])
    if success and output:
        try:
            beads_data["created"] = json.loads(output)
        except json.JSONDecodeError:
            pass

    return beads_data


def get_files_edited() -> list[str]:
    """Get list of files modified in current session (from git status)."""
    success, output = run_command(["git", "status", "--porcelain"])
    if not success:
        return []

    files = []
    for line in output.split("\n"):
        if line.strip():
            # Extract filename (after status codes)
            filename = line[3:].strip()
            # Handle renames (old -> new)
            if " -> " in filename:
                filename = filename.split(" -> ")[1]
            files.append(filename)
    return files


def main():
    # Parse arguments
    num_commits = 20
    output_json = "--json" in sys.argv

    for i, arg in enumerate(sys.argv):
        if arg == "--commits" and i + 1 < len(sys.argv):
            try:
                num_commits = int(sys.argv[i + 1])
            except ValueError:
                pass

    # Gather all data
    session_data = {
        "timestamp": datetime.now().isoformat(),
        "git": get_git_data(num_commits),
        "beads": get_beads_data(),
        "files_edited": get_files_edited(),
    }

    # Output
    if output_json:
        print(json.dumps(session_data, indent=2))
    else:
        # Human-readable summary
        print("=" * 60)
        print("SESSION DATA SUMMARY")
        print("=" * 60)
        print(f"Timestamp: {session_data['timestamp']}")
        print()

        git = session_data["git"]
        if git["available"]:
            print(f"Git Branch: {git['branch']}")
            print(f"Recent Commits: {len(git['commits'])}")
            if git["commits"]:
                print("  Latest commits:")
                for c in git["commits"][:5]:
                    print(f"    - {c['hash']}: {c['message'][:50]}")
            print(f"Files in Status: {len(git['status'])}")
            if git["diff_stats"]:
                print(f"Files Changed (last 5 commits): {git['diff_stats'].get('total_files', 0)}")
        else:
            print("Git: Not available (not in a git repository)")
        print()

        beads = session_data["beads"]
        if beads["available"]:
            print(f"Beads Closed: {len(beads['closed'])}")
            print(f"Beads In Progress: {len(beads['in_progress'])}")
            print(f"Beads Open: {len(beads['created'])}")
        else:
            print("Beads: Not available (bd command or .beads/ not found)")
        print()

        print(f"Files Edited: {len(session_data['files_edited'])}")
        if session_data["files_edited"]:
            for f in session_data["files_edited"][:10]:
                print(f"  - {f}")
            if len(session_data["files_edited"]) > 10:
                print(f"  ... and {len(session_data['files_edited']) - 10} more")

        print()
        print("Run with --json for full structured output")


if __name__ == "__main__":
    main()
