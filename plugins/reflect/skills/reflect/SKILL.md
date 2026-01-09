---
name: reflect
description: |
  Analyze development sessions to improve the toolkit: AGENTS.md, skills, configuration, hooks,
  and automation. Use when: (1) Ending a significant work session, (2) User says "reflect",
  "what did we learn", "improve the toolkit", "session review", or "capture learnings",
  (3) After completing a complex task to document discoveries, (4) When encountering repeated
  friction, manual steps, or permission denials, (5) Before starting a new major feature to
  review previous patterns. Outputs direct improvements to files and beads issues for larger work.
allowed-tools: Read, Grep, Glob, Bash, LS
metadata:
  version: "1.0.0"
  author: "Jupid"
  tags: ["meta", "improvement", "toolkit", "documentation", "automation"]
---

# Reflect

Meta-improvement skill that analyzes development sessions to enhance the toolkit itself.

## Quick Start

1. **Gather data** (optional): `python scripts/gather_session.py`
2. **Review** the 4 retroactive questions in Phase 1 below
3. **Identify patterns** using the Quick Checks table in Phase 2
4. **Apply P0 improvements** immediately, create beads issues for P2+
5. **Save summary** to `history/reflections/YYYY-MM-DD-topic.md`

**Variants:**
- `/reflect` — Full 5-phase workflow
- `/reflect quick` — Skip to Phase 3, only P0 quick wins
- `/reflect deep` — Include cross-session analysis from `history/reflections/`

## Invocation

```bash
/reflect                    # Full reflection on current session
/reflect quick              # Quick wins only (permissions, small doc fixes)
/reflect deep               # Deep analysis with cross-session patterns
```

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  Phase 1: Session Analysis (gather what happened)               │
├─────────────────────────────────────────────────────────────────┤
│  Phase 2: Pattern Recognition (identify improvements)           │
├─────────────────────────────────────────────────────────────────┤
│  Phase 3: Categorize & Prioritize (sort by impact/effort)       │
├─────────────────────────────────────────────────────────────────┤
│  Phase 4: Generate Improvements (create outputs)                │
├─────────────────────────────────────────────────────────────────┤
│  Phase 5: Persist Learnings (save for future sessions)          │
└─────────────────────────────────────────────────────────────────┘
```

## Phase 1: Session Analysis

### Retroactive Investigation

Ask yourself (don't ask user unless needed):

1. **What would have helped at session start?**
   - Missing context about the codebase
   - Patterns that had to be discovered
   - Configuration that wasn't obvious

2. **What manual steps were repeated?**
   - Commands run multiple times
   - Information looked up repeatedly
   - Approvals requested for same actions

3. **What problems were encountered?**
   - Errors and how they were resolved
   - Dead ends and pivots
   - Unexpected behaviors

4. **What was discovered?**
   - Architectural patterns
   - Code conventions
   - Integration quirks
   - Gotchas and edge cases

### Data Sources to Review

```bash
# Check recent git activity
git log --oneline -20
git diff --stat HEAD~5..HEAD

# Check beads activity
bd list --status=closed --limit=10
bd list --status=open

# Review any test failures encountered
# Review any typecheck issues fixed
```

## Phase 2: Pattern Recognition

Use checklist in [references/checklist.md](references/checklist.md) for detailed analysis.

### Quick Checks

| Pattern | Signal | Improvement Target |
|---------|--------|-------------------|
| Same bash command approved 3+ times | Permission gap | `.claude/settings.json` |
| Searched for same pattern multiple times | Documentation gap | `AGENTS.md` |
| Skill triggered but had missing info | Skill gap | `.claude/skills/*/SKILL.md` |
| Skill should have triggered but didn't | Description gap | Skill frontmatter |
| Multi-step workflow repeated | Automation candidate | New skill or hook |
| Had to explain same thing to Claude | Context gap | `CLAUDE.md` or `AGENTS.md` |
| Workaround used instead of proper fix | Anti-pattern | Beads issue |

### Anti-Pattern Detection

Flag these for proper fixes (not toolkit improvements):

- Temporary workarounds that should be permanent fixes
- Type assertions (`as any`) added during session
- Error handling skipped "for now"
- Tests marked as skip/todo
- Comments like "TODO", "FIXME", "HACK"

Create beads issues for anti-patterns, not documentation.

## Phase 3: Categorize & Prioritize

### Improvement Categories

| Category | Target | Effort | Examples |
|----------|--------|--------|----------|
| **Permissions** | `.claude/settings.json` | Low | Add approved bash commands |
| **Quick Docs** | `AGENTS.md` | Low | Add gotcha, convention, pattern |
| **Skill Fix** | Existing skill | Medium | Update description, add section |
| **New Skill** | `.claude/skills/` | High | New workflow automation |
| **Hook** | `.claude/settings.json` | Medium | Pre/post command automation |
| **Tooling** | Scripts, MCP | High | New automation scripts |

### Priority Matrix

```
         High Impact
              │
   ┌──────────┼──────────┐
   │ DO NOW   │ SCHEDULE │
   │ (P1)     │ (P2)     │
Low ──────────┼────────── High Effort
   │ QUICK    │ BACKLOG  │
   │ WINS(P0) │ (P3)     │
   └──────────┼──────────┘
              │
         Low Impact
```

- **P0 Quick Wins**: Implement immediately (permissions, small doc fixes)
- **P1 Do Now**: Implement in this session if time allows
- **P2 Schedule**: Create beads issue with priority 1-2
- **P3 Backlog**: Create beads issue with priority 3-4

## Phase 4: Generate Improvements

### Output Templates

See [references/output-templates.md](references/output-templates.md) for templates.

### Direct Edits (with user approval)

For P0/P1 improvements, propose edits:

1. **Permission additions** → Edit `.claude/settings.json`
2. **AGENTS.md updates** → Add to appropriate section
3. **Skill fixes** → Edit existing skill files
4. **Hook additions** → Add to settings

### Beads Issues

For P2/P3 improvements, create beads issues:

```bash
# New skill needed
bd create "Create /skill-name skill for [workflow]" -t feature -p 2

# Larger documentation update
bd create "Document [pattern] in AGENTS.md" -t task -p 3

# Tooling improvement
bd create "Add [automation] script" -t feature -p 3
```

## Phase 5: Persist Learnings

### Session Summary

Create reflection summary in `history/reflections/`:

```bash
mkdir -p history/reflections
```

Filename: `YYYY-MM-DD-brief-topic.md`

Template:
```markdown
# Reflection: [Date] - [Brief Topic]

## Session Summary
[1-2 sentences on what was done]

## Discoveries
- [Pattern/convention discovered]
- [Gotcha encountered]

## Improvements Made
- [x] Added X to AGENTS.md
- [x] Updated Y skill
- [ ] Created issue for Z

## Open Questions
- [Things still unclear]

## Patterns to Watch
- [Things that might recur]
```

### Cross-Session Patterns

When running `/reflect deep`, also:

1. Read recent files in `history/reflections/`
2. Identify recurring themes
3. Escalate repeated issues (increase priority)
4. Consolidate related improvements

## Quick Reference

### Commands Cheatsheet

```bash
# Permission audit - find commands that needed approval
# (Review session mentally, no command available)

# Check what skills exist
ls .claude/skills/

# Check current permissions
cat .claude/settings.json

# Create improvement issue
bd create "Improve: [description]" -t task -p 2
```

### Common Improvements

| Friction | Solution |
|----------|----------|
| "I keep having to approve `bun test`" | Add `Bash(bun test:*)` to permissions |
| "I had to search for the auth pattern 3 times" | Add Auth section to AGENTS.md |
| "The /start-work skill didn't know about X" | Update skill with X info |
| "I wish there was a skill for Y" | Create new skill for Y |
| "Every session I have to explain Z" | Add Z to CLAUDE.md |

### Don't Reflect On

- One-off issues (not recurring)
- User-specific preferences (unless they ask)
- External tool bugs (report upstream instead)
- Things already documented (unless outdated)

## MCP/Plugin Gap Analysis

Note when these would have helped:

- **Playwright MCP**: UI testing/verification needed but not used
- **Supabase MCP**: Database queries done via bash instead
- **GitHub MCP**: PR/issue operations that could be faster
- **Context7 MCP**: Documentation lookups that were manual

Create issues for MCP integrations that would add value.

## Hooks Recommendations

Suggest hooks when you notice patterns like:

```
"You always run typecheck after editing .ts files"
→ Suggest: PostToolUse hook for Edit on .ts files

"You always check git status before committing"
→ Already should be doing this, but could be a reminder hook

"You always run tests after changing test files"
→ Suggest: PostToolUse hook for Edit on .test.ts files
```

Hook template:
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit",
      "hooks": [{
        "type": "command",
        "command": "echo 'Consider running typecheck'"
      }]
    }]
  }
}
```

## Examples

### Example 1: Permission Gap Discovery

**Session observation:** Approved `bun test` command 5 times during session

**Analysis:** Same command repeatedly approved = permission gap

**Improvement:**
```json
// Add to .claude/settings.json permissions.allow
"Bash(bun test:*)"
```

**Priority:** P0 (quick win, implement immediately)

---

### Example 2: Documentation Gap

**Session observation:** Searched for "how to add a database migration" 3 times, eventually found the pattern in an old PR

**Analysis:** Information exists but not discoverable = documentation gap

**Improvement:**
```markdown
// Add to AGENTS.md under Database section
### Creating Migrations
1. Run `bun run supabase migration new <name>`
2. Edit the generated SQL file in `packages/supabase/supabase/migrations/`
3. Run `bun run supabase migration up` to apply
4. Run `bun run generate:db` to regenerate TypeScript types
```

**Priority:** P1 (implement in session)

---

### Example 3: Skill Trigger Gap

**Session observation:** When user said "let's review what we built today", the reflect skill didn't trigger

**Analysis:** Trigger phrase not in description = skill description gap

**Improvement:**
```yaml
# Add to reflect skill description triggers
"review what we built", "end of session"
```

**Priority:** P0 (quick win)

---

### Example 4: New Skill Candidate

**Session observation:** Performed the same 5-step PR review process manually 3 times

**Analysis:** Repeated multi-step workflow = new skill candidate

**Improvement:**
```bash
bd create "Create /review-pr skill for PR reviews" -t feature -p 2 \
  --description "Automate the PR review workflow: fetch PR, analyze changes, check tests, suggest improvements"
```

**Priority:** P2 (create beads issue)

## Progress Checklist

Copy this checklist to track your reflection progress:

```
Reflection Progress:
- [ ] Phase 1: Gathered session data (git log, beads, mental review)
- [ ] Phase 2: Identified patterns using Quick Checks table
- [ ] Phase 3: Categorized improvements by priority (P0-P3)
- [ ] Phase 4a: Implemented all P0 quick wins
- [ ] Phase 4b: Implemented P1 improvements (if time)
- [ ] Phase 4c: Created beads issues for P2/P3
- [ ] Phase 5: Saved reflection to history/reflections/
```
