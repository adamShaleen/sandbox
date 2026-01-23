- In all interactions and messages be extremely concise and sacrifice grammar for the sake of concision.

# Sandbox

This is a personal sandbox repository containing coding challenges, toy problems, and syntax examples.

## Project Structure

- `typescript/` - TypeScript solutions with inline Jest tests
- `javascript/` - JavaScript solutions (CodeWars, algorithm practice)
- `python/` - Python learning phases with inline pytest tests
  - `phase1_syntax.py` - Syntax bridge (JS → Python) ✓
  - `phase2_collections.py` - Collections & comprehensions (in progress)
  - Future: phase3_oop.py, phase4_functional.py, etc.
- `java/` - Java solutions (HackerRank)

## Languages

- TypeScript (primary)
- JavaScript
- Python
- Java

## Development

### Testing

Tests are written inline in the same files as the code.

```bash
# TypeScript/JavaScript (Jest)
npm test            # Run all tests
npm run test:watch  # Run tests in watch mode

# Python (pytest)
npm run test:py     # Run Python tests
```

### Linting & Formatting

```bash
# TypeScript/JavaScript
npm run lint        # Run ESLint
npm run lint:fix    # Auto-fix linting issues
npm run format      # Run Prettier

# Python
npm run format:py   # Run Black formatter
npm run lint:py     # Run flake8 linter
```

## Python Learning Plan

The user is learning Python coming from a JS/TS background. A phased curriculum is in progress.

### Progress
- [x] Phase 0: Environment Setup (pytest configured)
- [x] Phase 1: Syntax Bridge (`python/phase1_syntax.py`)
- [ ] Phase 2: Collections & Comprehensions (`python/phase2_collections.py`) ← CURRENT
- [ ] Phase 3: OOP & Classes
- [ ] Phase 4: Functional Patterns (decorators, lambdas)
- [ ] Phase 5: Iterators & Generators
- [ ] Phase 6: Error Handling & Context Managers
- [ ] Phase 7: Modules & Packaging
- [ ] Phase 8: Testing (pytest advanced)
- [ ] Phase 9: Type System Deep Dive
- [ ] Phase 10: Pythonic Idioms & Capstone

### How to Resume
1. Check the current phase file in `python/` for the last completed problem
2. Each problem has tests — run `npm run test:py` to verify
3. Add new toy problems with: function stub, tests, JS equivalent hint
4. After completing a problem: review code, add comments, provide feedback
5. Session style: 30-45 min, interactive coding with explanations

### Teaching Style
- Compare Python to JS/TS equivalents
- Provide hints without giving full answers
- After solution: review for style, performance, Pythonic patterns
- Add inline comments to explain concepts

Full plan details: `~/.claude/plans/parsed-zooming-wadler.md`

## Notes

- This is a learning/practice repository
- Code may be commented out or incomplete (work in progress)
- Solutions are from various platforms: CodeWars, HackerRank, LeetCode
- TypeScript tests use Jest `describe`/`it` blocks inline
- Python tests use pytest `test_` functions inline
