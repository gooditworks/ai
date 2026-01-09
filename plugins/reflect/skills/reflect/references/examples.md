# Real Reflection Examples

Examples from actual development sessions showing good reflection practices.

## Contents

- [Good Reflection Structure](#good-reflection-structure)
- [Pattern Discovery Example](#pattern-discovery-example)
- [Permission Gap Discovery](#permission-gap-discovery)
- [Documentation Gap Example](#documentation-gap-example)
- [Cross-Session Theme Escalation](#cross-session-theme-escalation)
- [Anti-Pattern to Avoid](#anti-pattern-to-avoid)

---

## Good Reflection Structure

A well-structured reflection captures actionable insights without excessive detail.

**Example: Server/Client Boundary Discovery**

```markdown
# Reflection: 2026-01-09 - Code Deduplication Cleanup

## Session Summary
Large-scale code deduplication across the monorepo, consolidating duplicated
utilities, types, and UI components into shared packages.

## Discoveries
- **Server/Client boundary violation**: Consolidating server-only code
  (`next/headers`) into a barrel file that Client Components import causes
  build failures. Solution: separate export paths (`./mutations` vs
  `./mutations/server`)
- **Re-export anti-pattern**: Files that just re-export from `@jupid/ui`
  add indirection without value—always import from source directly

## Improvements Made
- [x] Added "Server/Client Export Boundaries" section to AGENTS.md
- [x] Added "Avoid Re-export Files" guidance to AGENTS.md

## Patterns to Watch
- New shared utilities should be added to appropriate packages, not app-local
- When moving server code to packages, always consider client import paths
```

**Why it's good:**
- Concise summary (1-2 sentences)
- Discoveries are specific and actionable
- Improvements are concrete (what file, what change)
- Patterns to watch help future sessions

---

## Pattern Discovery Example

When you discover an undocumented pattern during work.

**Session observation:**
```
Tried to import `getUserId` from `@jupid/supabase/mutations`
Build failed: "Module not found: next/headers"
Realized: server-only code can't be in client-accessible barrel
```

**Reflection output:**
```markdown
## Discoveries
- **Server/Client Export Boundaries**: Server-only code using `next/headers`
  must NOT be exported from barrel files that Client Components import.
  - Create separate paths: `./mutations` (client-safe) vs `./mutations/server`
  - Build error "Module not found: next/headers" indicates this violation

## Improvements Made
- [x] Added section to AGENTS.md under "Package Architecture"
```

**Why this matters:** Future sessions won't spend time debugging the same build error.

---

## Permission Gap Discovery

Identifying commands that should be pre-approved.

**Session observation:**
```
[Permission request] bun test packages/agi
[Approved]
[Permission request] bun test packages/types --watch
[Approved]
[Permission request] bun test
[Approved]
```

**Reflection output:**
```markdown
## Friction Points
- Approved `bun test` variations 3+ times

## Improvements Made
- [x] Added `Bash(bun test:*)` to .claude/settings.json permissions

## Validation
- Next session: `bun test` commands should execute without approval prompt
```

**Pattern:** Same command approved 3+ times = add to permissions.

---

## Documentation Gap Example

Finding information that should be obvious but wasn't.

**Session observation:**
```
Searched for: "inngest function runs"
Searched for: "inngest production logs"
Searched for: "how to check inngest"
Eventually found: Use Inngest MCP to query runs
```

**Reflection output:**
```markdown
## Friction Points
- Searched 3 different terms trying to find how to check Inngest runs
- Solution wasn't in AGENTS.md or skill descriptions

## Improvements Made
- [x] Created `/inngest` skill with subcommands: send, runs, cancel, docs
- [x] Added Inngest section to AGENTS.md Quick Reference

## Priority
P1 - Implemented in session (new skill creation)
```

**Pattern:** Searched for same concept 3+ times = documentation gap.

---

## Cross-Session Theme Escalation

When `/reflect deep` identifies recurring issues.

**History analysis:**
```
From gather_history.py:
Recurring themes:
- "worktree": 5 mentions across 3 sessions
- "cleanup": 4 mentions across 2 sessions
- "node_modules": 5 mentions across 2 sessions
```

**Reflection output:**
```markdown
## Cross-Session Patterns (from /reflect deep)

### Recurring: Worktree Cleanup
- Mentioned in: 2026-01-07, 2026-01-08, 2026-01-09
- Pattern: Manual worktree cleanup steps repeated each session
- Escalation: P3 → P1 (mentioned 3+ times)

### Action Taken
- Created beads issue: "Automate git worktree cleanup in /start-work"
- Priority 1 (escalated from 3 due to recurrence)

### Issue Created
```bash
bd create "Automate worktree cleanup in start-work skill" \
  -t feature -p 1 \
  --description "Recurring friction: worktree cleanup mentioned 5+ times"
```
```

**Pattern:** Issue mentioned 2+ times across sessions = escalate priority.

---

## Anti-Pattern to Avoid

What NOT to do in reflections.

**Bad reflection example:**
```markdown
## Session Summary
Did a lot of stuff today. Fixed some bugs. Made some changes.

## Discoveries
- Learned things
- Found some patterns

## Improvements Made
- Made it better
- Fixed stuff
```

**Why it's bad:**
- Vague summary (what bugs? what changes?)
- Non-specific discoveries (what patterns?)
- Unmeasurable improvements (what specifically?)
- No file references or commands
- Can't be validated or reproduced

**Better version:**
```markdown
## Session Summary
Fixed authentication redirect loop in dashboard login flow.

## Discoveries
- **Auth redirect loop cause**: `useRouter().push()` doesn't preserve
  query params by default. Must use `router.push(url, { scroll: false })`.

## Improvements Made
- [x] Added "Auth Redirect Patterns" to AGENTS.md Code Patterns section
- [x] Fixed redirect in `apps/dashboard/src/app/auth/callback/route.ts:42`
```

**Key differences:**
- Specific problem identified
- Exact solution documented with code pattern
- File path included for reference
- Improvement is concrete and verifiable

---

## Quick Reference: Good vs Bad

| Aspect | Bad | Good |
|--------|-----|------|
| Summary | "Fixed bugs" | "Fixed auth redirect loop in login" |
| Discovery | "Learned patterns" | "useRouter().push() doesn't preserve query params" |
| Improvement | "Made it better" | "Added section to AGENTS.md:L142" |
| Issue | "Create issue for thing" | `bd create "..." -t bug -p 2` |
| Validation | (none) | "Next login should redirect correctly" |
