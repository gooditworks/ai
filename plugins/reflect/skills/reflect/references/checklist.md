# Reflection Checklist

Detailed checklist for analyzing a development session. Work through relevant sections based on session type.

## Contents

- [Session Analysis Questions](#session-analysis-questions) - What to reflect on
  - Context & Discovery
  - Friction Points
  - Anti-Patterns Introduced
  - Tool Gaps
- [Improvement Identification](#improvement-identification) - Where to improve
  - Permission Gaps
  - Documentation Gaps
  - Skill Gaps
  - Hook Opportunities
- [Output Decision Matrix](#output-decision-matrix) - How to prioritize
- [Cross-Session Analysis](#cross-session-analysis-for-reflect-deep) - For `/reflect deep`
- [Final Checks](#final-checks) - Before completing

**Script Support:**
- `[AUTO]` = Data available from `gather_session.py`
- `[HIST]` = Data available from `gather_history.py`
- `[PERM]` = Data available from `gather_permissions.py`

## Session Analysis Questions

### Context & Discovery

- [ ] What files/patterns did I search for multiple times? `[AUTO: check git diff_stats]`
- [ ] What architectural decisions did I discover during work?
- [ ] What conventions exist that weren't documented?
- [ ] What gotchas or edge cases did I encounter?
- [ ] What integration quirks needed workarounds?

### Friction Points

- [ ] Which bash commands required approval repeatedly? `[PERM: compare against allowed]`
- [ ] What information was hard to find?
- [ ] Which skills were used but had gaps?
- [ ] Which skills should have triggered but didn't?
- [ ] What multi-step processes were done manually? `[AUTO: check repeated file edits]`

### Anti-Patterns Introduced

- [ ] Any `as any` type assertions added?
- [ ] Any error handling skipped?
- [ ] Any tests skipped or marked todo?
- [ ] Any "temporary" workarounds that need proper fixes?
- [ ] Any TODO/FIXME/HACK comments added?

### Tool Gaps

- [ ] Would Playwright MCP have helped for UI verification?
- [ ] Would Supabase MCP have made DB queries easier?
- [ ] Would a custom MCP have helped?
- [ ] Were there repeated operations that should be scripted?

---

## Improvement Identification

### Permission Gaps (.claude/settings.json)

Check if these commands were approved during session:

```
Common candidates:
- bun test:*
- bun run <script>:*
- turbo <command>:*
- supabase <command>:*
- linear <command>:*
- bd <command>:*
- Custom project scripts
```

For each approved command, ask:
1. Will this be used again? → Add to permissions
2. Is it project-specific? → Add to project settings
3. Is it global? → Add to ~/.claude/settings.json

### Documentation Gaps (AGENTS.md)

| Section | What to Add |
|---------|-------------|
| Quick Reference | New commonly-used commands |
| Code Patterns | Discovered conventions |
| Database | Schema patterns, RLS rules |
| Package Architecture | Dependency rules discovered |
| TypeScript Rules | New constraints found |
| Naming Conventions | Patterns not listed |
| Testing | Test patterns/approaches |

Questions to surface gaps:
- "What did I have to figure out that should be obvious?"
- "What would a new contributor need to know?"
- "What broke my assumptions about the codebase?"

### Skill Gaps

**Existing Skills to Improve:**

| Skill | Potential Improvements |
|-------|----------------------|
| start-work | Missing workflow steps, edge cases |
| requirements-spec | Missing spec categories |
| frontend-design | Missing component patterns |
| skill-creator | Process improvements |

**New Skills to Consider:**

| Workflow | Skill Name | Trigger |
|----------|------------|---------|
| Database migrations | /migrate | "create migration", "update schema" |
| PR review | /review-pr | "review this PR", PR URL |
| Debug session | /debug | "help me debug", error traces |
| Refactoring | /refactor | "refactor this", "clean up" |
| Testing | /test | "add tests", "test coverage" |
| Deploy | /deploy | "deploy to", environment names |

### Hook Opportunities

**PostToolUse Hooks:**

| Tool Pattern | Action | Benefit |
|--------------|--------|---------|
| Edit *.ts | Remind typecheck | Catch errors early |
| Edit *.test.ts | Suggest run test | Verify test works |
| Write migration | Remind generate types | Keep types in sync |
| Bash git commit | Remind bd sync | Keep beads synced |

**PreToolUse Hooks:**

| Tool Pattern | Action | Benefit |
|--------------|--------|---------|
| Edit (large file) | Read file first | Ensure context |
| Bash rm | Confirm destructive | Prevent accidents |

**SessionStart Hooks:**

| Condition | Action | Benefit |
|-----------|--------|---------|
| .beads/ exists | bd prime | Load beads context |
| spec/ exists | Remind check spec | Ensure compliance |
| Dirty git state | Show git status | Awareness |

---

## Output Decision Matrix

For each improvement identified:

```
Is it a quick fix (< 5 min)?
├─ Yes → Implement now (P0)
└─ No
   └─ Is it high impact?
      ├─ Yes → Implement if time allows (P1) or create P1-2 beads issue
      └─ No → Create P3-4 beads issue (backlog)
```

---

## Cross-Session Analysis (for /reflect deep)

**Run first:** `python scripts/gather_history.py --json`

When reviewing `history/reflections/`:

1. **Recurring Themes** `[HIST: check recurring_themes]`
   - Same type of friction appearing?
   - Same documentation gaps noted?
   - Pattern of similar issues?

2. **Escalation Triggers** `[HIST: keywords appearing 2+ times]`
   - Issue noted 2+ times → Increase priority
   - Workaround used 3+ times → Must fix
   - Same question answered 3+ times → Must document

3. **Consolidation Opportunities**
   - Related issues that should be one
   - Similar skills that could merge
   - Documentation scattered across files

---

## Final Checks

Before completing reflection:

- [ ] All P0 improvements implemented
- [ ] P1 improvements implemented or tracked
- [ ] P2/P3 improvements have beads issues
- [ ] Anti-patterns have fix issues (not just documented)
- [ ] Session summary saved to history/reflections/
- [ ] Improvements committed (or ready to commit)
