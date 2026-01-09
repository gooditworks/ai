#!/usr/bin/env python3
"""
Gather current Claude Code permission state.

Reads .claude/settings.json to extract current permissions for comparison
against session activity.

Usage:
    python scripts/gather_permissions.py [settings_path] [--json]

Output: JSON with current permissions and patterns.
"""

import json
import re
import sys
from pathlib import Path


def parse_permission_pattern(permission: str) -> dict:
    """Parse a permission string into structured data."""
    # Common permission patterns:
    # "Bash(command:*)" - bash command with wildcard
    # "Bash(command arg:*)" - bash with args
    # "Read(*)" - file read
    # "Edit(*)" - file edit
    # "mcp__server__tool" - MCP tool

    result = {
        "raw": permission,
        "type": "unknown",
        "tool": "",
        "pattern": "",
        "has_wildcard": "*" in permission,
    }

    # MCP tool pattern
    if permission.startswith("mcp__"):
        result["type"] = "mcp"
        parts = permission.split("__")
        if len(parts) >= 3:
            result["tool"] = f"{parts[1]}/{parts[2]}"
        return result

    # Tool with pattern: Tool(pattern)
    match = re.match(r"(\w+)\((.+)\)", permission)
    if match:
        result["type"] = "tool"
        result["tool"] = match.group(1)
        result["pattern"] = match.group(2)
        return result

    # Simple tool name
    if permission.isalnum() or permission.replace("_", "").isalnum():
        result["type"] = "tool"
        result["tool"] = permission
        return result

    return result


def load_settings(settings_path: Path) -> dict | None:
    """Load and parse Claude settings file."""
    if not settings_path.exists():
        return None

    try:
        content = settings_path.read_text()
        return json.loads(content)
    except (json.JSONDecodeError, Exception):
        return None


def gather_permissions(settings_path: Path) -> dict:
    """Gather all permission-related data from settings."""
    output = {
        "settings_path": str(settings_path),
        "exists": settings_path.exists(),
        "current_permissions": [],
        "permission_patterns": [],
        "denied_patterns": [],
        "by_tool": {},
        "mcp_permissions": [],
        "bash_patterns": [],
    }

    settings = load_settings(settings_path)
    if not settings:
        return output

    # Extract permissions from settings
    permissions = settings.get("permissions", {})
    allow_list = permissions.get("allow", [])
    deny_list = permissions.get("deny", [])

    output["current_permissions"] = allow_list
    output["denied_patterns"] = deny_list

    # Parse each permission
    for perm in allow_list:
        parsed = parse_permission_pattern(perm)
        output["permission_patterns"].append(parsed)

        # Group by tool
        tool = parsed.get("tool", "unknown")
        if tool not in output["by_tool"]:
            output["by_tool"][tool] = []
        output["by_tool"][tool].append(perm)

        # Special handling for common types
        if parsed["type"] == "mcp":
            output["mcp_permissions"].append(perm)
        elif parsed["tool"] == "Bash":
            output["bash_patterns"].append(parsed["pattern"])

    return output


def main():
    # Parse arguments
    output_json = "--json" in sys.argv

    # Default settings path
    settings_path = Path(".claude/settings.json")

    # Check for path argument
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            settings_path = Path(arg)
            break

    # Also check home directory settings
    home_settings = Path.home() / ".claude" / "settings.json"

    # Gather from both locations
    project_perms = gather_permissions(settings_path)
    home_perms = gather_permissions(home_settings)

    output = {
        "project_settings": project_perms,
        "home_settings": home_perms,
        "combined_permissions": list(set(
            project_perms["current_permissions"] +
            home_perms["current_permissions"]
        )),
        "combined_bash_patterns": list(set(
            project_perms["bash_patterns"] +
            home_perms["bash_patterns"]
        )),
    }

    if output_json:
        print(json.dumps(output, indent=2))
    else:
        # Human-readable summary
        print("=" * 60)
        print("CLAUDE CODE PERMISSIONS SUMMARY")
        print("=" * 60)

        print(f"\nProject Settings: {settings_path}")
        print(f"  Exists: {project_perms['exists']}")
        if project_perms["exists"]:
            print(f"  Permissions: {len(project_perms['current_permissions'])}")
            for perm in project_perms["current_permissions"][:10]:
                print(f"    - {perm}")
            if len(project_perms["current_permissions"]) > 10:
                print(f"    ... and {len(project_perms['current_permissions']) - 10} more")

        print(f"\nHome Settings: {home_settings}")
        print(f"  Exists: {home_perms['exists']}")
        if home_perms["exists"]:
            print(f"  Permissions: {len(home_perms['current_permissions'])}")
            for perm in home_perms["current_permissions"][:10]:
                print(f"    - {perm}")
            if len(home_perms["current_permissions"]) > 10:
                print(f"    ... and {len(home_perms['current_permissions']) - 10} more")

        print("\nBash Command Patterns:")
        all_bash = set(project_perms["bash_patterns"] + home_perms["bash_patterns"])
        for pattern in sorted(all_bash)[:15]:
            print(f"  - {pattern}")

        print("\nMCP Tool Permissions:")
        all_mcp = set(project_perms["mcp_permissions"] + home_perms["mcp_permissions"])
        for perm in sorted(all_mcp)[:10]:
            print(f"  - {perm}")

        print()
        print("Run with --json for full structured output")


if __name__ == "__main__":
    main()
