# CLAUDE.md - AI Assistant Guide for DIO-v3

## Project Overview

**DIO-v3** (Defense Input Output Model v3) is an open-source project licensed under MIT.

- **Repository owner:** kelaxten
- **License:** MIT
- **Current state:** Early-stage / newly initialized

## Repository Structure

```
DIO-v3/
├── LICENSE          # MIT License
├── README.md        # Project description
└── CLAUDE.md        # This file - AI assistant guide
```

## Development Conventions

### Git Workflow

- **Main branch:** `main`
- **Feature branches:** Use descriptive branch names prefixed by purpose (e.g., `feature/`, `fix/`, `docs/`)
- **Commit messages:** Use clear, imperative-tense messages describing the "why" not just the "what"
- Keep commits atomic - one logical change per commit

### Code Style (to be established)

As the project grows, adhere to the following principles:
- Prefer simplicity and readability over cleverness
- Follow the conventions already established in the codebase
- Do not over-engineer solutions - implement only what is needed
- Avoid introducing unnecessary dependencies

### Security Considerations

- Never commit secrets, API keys, or credentials
- Validate all external inputs at system boundaries
- Follow OWASP top-10 best practices
- Review dependencies for known vulnerabilities before adding them

## AI Assistant Guidelines

### Before Making Changes

1. Read and understand existing code before modifying it
2. Check the current branch and repository state with `git status`
3. Understand the purpose of the change being requested

### When Implementing Changes

1. Make minimal, focused changes that address the request
2. Do not refactor or "improve" code beyond what is asked
3. Do not add unnecessary comments, docstrings, or type annotations to unchanged code
4. Avoid adding features or configurability that wasn't requested
5. Test changes when a test framework is available

### When Committing

1. Stage only the relevant files (avoid `git add -A` blindly)
2. Write concise commit messages that explain the purpose
3. Never force-push to `main`
4. Never commit files containing secrets or credentials

### What to Avoid

- Do not create documentation files unless explicitly requested
- Do not add error handling for impossible scenarios
- Do not create abstractions for one-time operations
- Do not add backwards-compatibility shims when direct changes suffice
- Do not guess at project requirements - ask when uncertain

## Build & Development

No build system or development tooling is currently configured. As infrastructure is added, this section should be updated with:
- How to install dependencies
- How to run the development server
- How to build for production
- How to run tests
- How to lint/format code

## Testing

No testing framework is currently configured. When tests are added, document:
- Test runner and framework used
- How to run the full test suite
- How to run individual tests
- Testing conventions and patterns used

## Dependencies

No package manager or dependency manifest is currently configured. When dependencies are added:
- Document the package manager used
- Keep dependencies minimal and justified
- Audit new dependencies for security issues and maintenance status
