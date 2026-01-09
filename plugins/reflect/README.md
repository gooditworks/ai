# Reflect Plugin

Meta-improvement skill that analyzes development sessions to enhance your toolkit.

## Installation

```
/plugin install reflect@gooditworks/ai
```

## Usage

```bash
/reflect                    # Full reflection on current session
/reflect quick              # Quick wins only (permissions, small doc fixes)
/reflect deep               # Deep analysis with cross-session patterns
```

## What It Does

The reflect skill helps you improve your development environment by:

1. **Permission Gaps** - Identifies commands you approve repeatedly that should be pre-approved
2. **Documentation Gaps** - Finds patterns you search for repeatedly that should be documented
3. **Skill Gaps** - Discovers skills that need improvement or new skills that should be created
4. **Automation Candidates** - Spots manual workflows that could be automated with hooks

## Workflow

```
Phase 1: Session Analysis (gather what happened)
Phase 2: Pattern Recognition (identify improvements)
Phase 3: Categorize & Prioritize (sort by impact/effort)
Phase 4: Generate Improvements (create outputs)
Phase 5: Persist Learnings (save for future sessions)
```

## Scripts

The plugin includes Python scripts for data gathering:

- `gather_session.py` - Collects git activity, beads status, file changes
- `gather_history.py` - Parses reflection history for cross-session patterns
- `gather_permissions.py` - Reads current permission state

## License

Apache-2.0
