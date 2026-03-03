- In all interactions and messages be extremely concise and sacrifice grammar for the sake of concision.

# Sandbox

This is a personal sandbox repository containing coding challenges, toy problems, and syntax examples.

## Project Structure

- `typescript/` - TypeScript solutions with inline Jest tests
- `javascript/` - JavaScript solutions (CodeWars, algorithm practice)
- `python/` - Python learning phases with inline pytest tests
  - `phase1/` - Syntax bridge (JS → Python) ✓
    - `lessons.py` - Core concepts and examples
    - `problems.py` - Practice problems
  - `phase2/` - Collections & comprehensions ✓
    - `lessons.py` - Core concepts and examples
    - `problems.py` - 12 practice problems
  - `phase3/` - OOP & Classes ✓
    - `lessons.py` - Core concepts and examples
    - `problems.py` - 10 practice problems
  - `phase4/` - Functional Patterns ✓
    - `lessons.py` - Core concepts and examples
    - `problems.py` - 8 practice problems
  - `phase5/` - Iterators & Generators ✓
    - `lessons.py` - Core concepts and examples
    - `problems.py` - 12 practice problems
  - `phase6/` - Error Handling & Context Managers ✓
    - `lessons.py` - Core concepts and examples
    - `problems.py` - 12 practice problems
  - `phase7/` - Modules & Packaging ✓
    - `lessons.py` - Core concepts and examples
    - `problems.py` - 12 practice problems
  - `phase8/` - Testing (pytest advanced) ✓
  - `phase9/` - Type System Deep Dive ✓
    - `lessons.py` - Core concepts and examples
    - `problems.py` - 8 practice problems
  - `phase10/` - Pythonic Idioms & Capstone ✓
    - `lessons.py` - Core concepts and examples
    - `problems.py` - 6 problems + capstone
  - `phase11/` - Async Python & HTTP ✓
    - `lessons.py` - Core concepts and examples
    - `problems.py` - 7 problems
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
npm run test:py                              # Run all Python tests
npm run test:py:match <test_name>            # Run test by name (e.g., test_file_lines)
npm run test:py:file <path>                  # Run specific file (e.g., python/phase5/problems.py)
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
- [x] Phase 1: Syntax Bridge (`python/phase1/`)
- [x] Phase 2: Collections & Comprehensions (`python/phase2/`) - 12 problems
- [x] Phase 3: OOP & Classes (`python/phase3/`) - 10 problems
- [x] Phase 4: Functional Patterns (`python/phase4/`) - 8 problems
- [x] Phase 5: Iterators & Generators (`python/phase5/`) - 12 problems
- [x] Phase 6: Error Handling & Context Managers (`python/phase6/`) - 12 problems
- [x] Phase 7: Modules & Packaging (`python/phase7/`) - 12 problems
- [x] Phase 8: Testing (pytest advanced) (`python/phase8/`) - 10 problems
- [x] Phase 9: Type System Deep Dive (`python/phase9/`) - 8 problems
- [x] Phase 10: Pythonic Idioms & Capstone (`python/phase10/`) - 6 problems + capstone
- [x] Phase 11: Async Python & HTTP (`python/phase11/`) - 7 problems

### How to Resume

1. Check the current phase folder in `python/phaseN/problems.py` for the last completed problem
2. Each problem has tests — run `npm run test:py` to verify
3. Add new toy problems to `problems.py` with: function stub, tests, JS equivalent hint
4. After completing a problem: review code, add comments, provide feedback
5. Session style: 30-45 min, interactive coding with explanations

### File Structure

Each phase has three files:

- `__init__.py` - Empty file, required for pytest module resolution
- `lessons.py` - Reference material: concept explanations, syntax comparisons, demo tests
- `problems.py` - Practice problems with hints, solutions, and tests

**Important:** New phase folders MUST include an empty `__init__.py` file or pytest will fail with module import errors.

### Teaching Style

- Compare Python to JS/TS equivalents
- **NEVER give complete solutions unless user explicitly asks for the answer**
- Explain concepts, show small illustrative snippets, but let user write the actual solution
- After user completes solution: review for style, performance, Pythonic patterns
- Add inline comments to explain concepts
- **ONE concept/problem at a time** — add the next lesson concept or problem only after the user signals they're ready to move on

### lessons.py Code Style

- Each `demo_` function must be immediately followed by its paired `test_` function
- Two blank lines between every top-level function (standard PEP 8)
- Pattern: `demo_foo` → `test_foo` → `demo_bar` → `test_bar` (never group all demos then all tests)

### problems.py Workflow

- Start with only Problem 1 in the file
- Add the next problem only after the user completes the current one

Full plan details: `~/.claude/plans/parsed-zooming-wadler.md`

## Notes

- This is a learning/practice repository
- Code may be commented out or incomplete (work in progress)
- Solutions are from various platforms: CodeWars, HackerRank, LeetCode
- TypeScript tests use Jest `describe`/`it` blocks inline
- Python tests use pytest `test_` functions inline
