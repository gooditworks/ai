# Output Templates

Templates for generating improvements from reflection.

## Contents

- [Permission Addition](#permission-addition) - Add approved commands
- [AGENTS.md Updates](#agentsmd-updates) - Document discoveries
- [Skill Updates](#skill-updates) - Fix or enhance skills
- [New Skill Template](#new-skill-template) - Create new skills
- [Beads Issue Templates](#beads-issue-templates) - Track larger work
- [Hook Templates](#hook-templates) - Automate workflows
- [Session Summary Template](#session-summary-template) - Persist learnings
- [MCP Gap Analysis Template](#mcp-gap-analysis-template) - Track tool needs

---

## Permission Addition

**When to use:** Command approved 3+ times in session

**Input (observation):**
```
Approved: bun test packages/agi
Approved: bun test packages/types
Approved: bun test --watch
```

**Output (improvement):**
```json
// Add to .claude/settings.json
{
  "permissions": {
    "allow": [
      "Bash(bun test:*)"
    ]
  }
}
```

**Common patterns:**
```
Bash(bun test:*)           # All bun test invocations
Bash(bun run build:*)      # Build commands
Bash(turbo <cmd>:*)        # Turbo commands
Bash(supabase *:*)         # Supabase CLI
Bash(linear *:*)           # Linear CLI
Bash(bd *:*)               # Beads CLI
Bash(gh pr *:*)            # GitHub PR commands
```

**Validation:** After adding, command should not require approval.

---

## AGENTS.md Updates

**When to use:** Discovered convention, pattern, or gotcha that future sessions would benefit from

**Input (observation):**
```
Searched "how to run migrations" 3 times
Eventually found: bun run supabase migration new <name>
Also need to run generate:db after to update types
```

**Output (improvement):**
```markdown
// Add to AGENTS.md under Database section
### Creating Migrations
1. Run `bun run supabase migration new <name>`
2. Edit the SQL file in `packages/supabase/supabase/migrations/`
3. Run `bun run supabase migration up` to apply
4. Run `bun run generate:db` to regenerate TypeScript types
```

### New Section Template

```markdown
## Section Name

Brief description of what this section covers.

### Subsection

- **Term/Pattern**: Explanation
- **Convention**: How to do X

### Quick Reference

| Item | Value/Pattern |
|------|---------------|
| X    | Y             |
```

### Adding to Existing Section

Look for the appropriate section and add:

```markdown
- **New Item**: Description of the pattern/convention/gotcha
```

For gotchas/warnings:
```markdown
- **Warning**: Description of what to avoid and why
```

**Validation:** Future sessions should find this info via grep/search.

---

## Skill Updates

### Fixing Skill Description

Update frontmatter `description` to include missing triggers:

```yaml
description: |
  [Current description]. Also use when: (N) [new trigger scenario],
  (N+1) [another trigger scenario].
```

### Adding Skill Section

```markdown
## New Section Name

Brief explanation of when this applies.

### Steps/Process

1. Step one
2. Step two

### Examples

```bash
# Example command or code
```
```

---

## New Skill Template

Minimal skill structure:

```markdown
---
name: skill-name
description: |
  One-line description of what the skill does. Use when: (1) trigger scenario,
  (2) another trigger, (3) user says "keyword".
---

# Skill Name

Brief overview of the skill's purpose.

## Workflow

### Phase 1: Name

Steps for this phase.

### Phase 2: Name

Steps for this phase.

## Quick Reference

| Action | Command/Approach |
|--------|------------------|
| X      | Y                |
```

---

## Beads Issue Templates

### New Skill Issue

```bash
bd create "Create /skill-name skill for [workflow]" \
  -t feature \
  -p 2 \
  --description "$(cat <<'EOF'
## Context
[Why this skill is needed]

## Trigger Scenarios
- User says "X"
- When doing Y
- After Z happens

## Proposed Workflow
1. Step one
2. Step two

## Resources Needed
- scripts/: [if any]
- references/: [if any]
- assets/: [if any]
EOF
)"
```

### Documentation Issue

```bash
bd create "Document [topic] in [target file]" \
  -t task \
  -p 3 \
  --description "$(cat <<'EOF'
## Gap Identified
[What's missing and how it was discovered]

## Proposed Content
[Outline of what to add]

## Location
[Which file and section]
EOF
)"
```

### Tooling/Automation Issue

```bash
bd create "Add [automation/script] for [purpose]" \
  -t feature \
  -p 3 \
  --description "$(cat <<'EOF'
## Current Friction
[What manual process this replaces]

## Proposed Solution
[What the automation would do]

## Implementation Notes
[Technical approach]
EOF
)"
```

### Anti-Pattern Fix Issue

```bash
bd create "Fix: [anti-pattern description]" \
  -t bug \
  -p 2 \
  --description "$(cat <<'EOF'
## Anti-Pattern
[What was done as a workaround]

## Proper Fix
[What should be done instead]

## Location
[Files affected]

## Risk if Not Fixed
[Why this matters]
EOF
)"
```

---

## Hook Templates

### PostToolUse Hook

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "ToolName",
      "hooks": [{
        "type": "command",
        "command": "echo 'Reminder: action to take'"
      }]
    }]
  }
}
```

With file pattern matching:
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit",
      "filePattern": "**/*.test.ts",
      "hooks": [{
        "type": "command",
        "command": "echo 'Consider running: bun test'"
      }]
    }]
  }
}
```

### SessionStart Hook

```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "if [ -d .beads ]; then bd prime 2>/dev/null; fi"
      }]
    }]
  }
}
```

---

## Session Summary Template

Save to `history/reflections/YYYY-MM-DD-topic.md`:

```markdown
# Reflection: [Date] - [Brief Topic]

## Session Summary
[1-2 sentences describing what was accomplished]

## Key Discoveries

### Patterns/Conventions
- [Pattern discovered]

### Gotchas/Edge Cases
- [Gotcha encountered]

### Architecture Insights
- [Architectural learning]

## Improvements Made

### Implemented
- [x] [Improvement 1] - [target file]
- [x] [Improvement 2] - [target file]

### Issues Created
- [ ] bd-XXX: [Issue title]
- [ ] bd-YYY: [Issue title]

## Anti-Patterns Noted
- [Anti-pattern] → Issue: bd-ZZZ

## Open Questions
- [Question that remains unclear]

## Recommendations for Future Sessions
- [Advice for next time this area is touched]
```

---

## MCP Gap Analysis Template

When noting MCP that would have helped:

```bash
bd create "Evaluate [MCP name] integration" \
  -t task \
  -p 3 \
  --description "$(cat <<'EOF'
## Use Case
[What task would have been easier]

## Current Approach
[How it was done without MCP]

## MCP Benefits
- [Benefit 1]
- [Benefit 2]

## Setup Requirements
[What's needed to add the MCP]
EOF
)"
```
