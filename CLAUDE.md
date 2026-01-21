- In all interactions and messages be extremely concise and sacrifice grammar for the sake of concision.

# Sandbox

This is a personal sandbox repository containing coding challenges, toy problems, and syntax examples.

## Project Structure

- `sandbox.ts` - TypeScript solutions with inline Jest tests
- `sandbox.js` - JavaScript solutions (CodeWars, algorithm practice)
- `sandbox.py` - Python solutions and syntax examples
- `sandbox.java` - Java solutions (HackerRank)

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

## Notes

- This is a learning/practice repository
- Code may be commented out or incomplete (work in progress)
- Solutions are from various platforms: CodeWars, HackerRank, LeetCode
- TypeScript tests use Jest `describe`/`it` blocks inline
- Python tests use pytest `test_` functions inline
