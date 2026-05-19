# AI Agent Context

This document provides context and conventions for AI coding agents working in this repository.

## Agent Guidelines

### Before Making Changes

1. Read relevant documentation in `agent-docs/`
2. Check [plans/roadmap.md](../05-plans/roadmap.md) for current priorities
3. Review [personas/](../13-personas/) to understand users
4. Check [changelog/](../09-changelog/) for recent decisions

### While Working

1. Follow conventions in existing code
2. Write tests for new functionality
3. Update relevant documentation
4. Use semantic commit messages

### After Completing Changes

1. Run linting and tests
2. Update [changelog/](../09-changelog/index.md) if user-facing changes
3. Note any new dependencies or environment requirements

## Available Tools

| Tool | Purpose |
|------|---------|
| `npm run dev` | Start development server |
| `npm test` | Run tests |
| `npm run lint` | Lint code |
| `npm run build` | Build for production |

## Code Conventions

- Language: JavaScript/TypeScript
- Style: ESLint + Prettier
- Testing: [Test framework]
- Branch naming: `feature/`, `fix/`, `docs/`

## Constraints

- Do not commit secrets or credentials
- Do not disable security features
- Maintain backward compatibility unless specified
