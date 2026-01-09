# Good IT Works - AI Plugin Marketplace

A curated collection of AI-powered development tools and skills for Claude Code.

## Installation

Add this marketplace to Claude Code:

```
/plugin marketplace add gooditworks/ai
```

Then install individual plugins:

```
/plugin install reflect@gooditworks/ai
```

## Available Plugins

### reflect

**Category:** Productivity
**Version:** 1.0.0

Meta-improvement skill that analyzes development sessions to enhance your toolkit.

**Features:**
- Identifies permission gaps (commands approved repeatedly)
- Discovers documentation gaps (patterns searched multiple times)
- Suggests skill improvements and new skill candidates
- Detects automation opportunities
- Provides structured reflection workflow

**Invocation:**
```bash
/reflect                    # Full reflection on current session
/reflect quick              # Quick wins only (permissions, small doc fixes)
/reflect deep               # Deep analysis with cross-session patterns
```

**Includes:**
- 1 skill with 5-phase workflow
- 3 Python data-gathering scripts
- Reference documentation and templates

## Contributing

1. Fork this repository
2. Create a new plugin in `plugins/your-plugin/`
3. Add plugin.json and skill files
4. Update marketplace.json
5. Submit a pull request

## License

Apache-2.0
