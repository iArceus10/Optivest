# OptiVest

# Development Guide

**Document Version:** 1.0

**Project Version:** Version 1

**Repository Status:** Phase 5 Complete

**Current Test Status:** 117 Passing

**Target Audience:** Contributors and Maintainers

**Last Updated:** After Phase 5 Completion

---

# 1. Purpose

This document defines the development workflow, engineering standards,
coding conventions, testing philosophy, and contribution guidelines for
the OptiVest repository.

Unlike the Project Specification, which describes *what* the project
should accomplish, this document describes *how* development should be
performed.

Every contribution to the repository should follow the practices
described here.

---

# 2. Development Philosophy

OptiVest is developed as a production-quality software engineering
project rather than as an academic prototype.

Every feature is expected to satisfy the following objectives.

- Correctness
- Maintainability
- Readability
- Testability
- Extensibility
- Interview Defensibility

Implementation speed is never prioritized over software quality.

---

# 3. Repository Principles

Development follows several fundamental principles.

## Build Complete Features

Features are implemented vertically.

Every completed feature includes:

- Financial Engine
- Service
- Schemas
- API
- Tests
- Documentation

Partial implementations are not merged.

---

## Small Incremental Phases

The repository evolves through clearly defined phases.

Each phase introduces one major capability.

A phase is considered complete only after:

- Compilation succeeds
- Relevant tests pass
- Full test suite passes
- Documentation is updated

---

## Freeze Completed Modules

Once a Financial Engine has been validated and fully tested, it becomes
functionally frozen.

Future development should extend higher architectural layers rather than
modify established mathematical implementations.

Changes are permitted only when a correctness defect has been
demonstrated.

---

# 4. Development Workflow

Every new feature follows the same implementation sequence.

```text
Engineering Review

↓

Architecture Validation

↓

Financial Engine

↓

Financial Engine Tests

↓

Service

↓

Service Tests

↓

Schemas

↓

API

↓

API Tests

↓

Documentation

↓

Git Commit
```

Skipping steps is discouraged because it increases the likelihood of
regressions and architectural inconsistencies.

---

# 5. Engineering Review

Before writing code, the entire feature should be reviewed from an
architectural perspective.

Questions to answer include:

- Does the feature fit the existing architecture?
- Can existing components be reused?
- Is additional abstraction necessary?
- Does the implementation introduce duplication?
- Does the feature belong in the correct layer?

If improvements are required, they should be identified **before**
implementation begins.

---

# 6. Coding Standards

The repository follows a consistent coding style.

## General Guidelines

- Use descriptive identifiers.
- Prefer explicit code over clever code.
- Keep functions focused on a single responsibility.
- Avoid deeply nested logic.
- Minimize duplication.
- Use type hints throughout the codebase.

---

## Imports

Imports should be grouped as:

1. Standard library
2. Third-party packages
3. Local application imports

Unused imports should be removed.

Circular dependencies are prohibited.

---

## Documentation

Public classes and functions should contain concise docstrings.

Docstrings should explain:

- Purpose
- Parameters
- Return values
- Exceptions when appropriate

Comments should explain *why* rather than *what*.

---

# 7. Layer Responsibilities

Every architectural layer has a clearly defined responsibility.

## API Layer

Responsible for:

- Routing
- Request validation
- Response serialization
- HTTP exception handling

Must never contain:

- Financial calculations
- Business workflows
- Database queries

---

## Service Layer

Responsible for:

- Business orchestration
- Market data retrieval
- Validation of business rules
- Coordination of Financial Engines

Must never contain mathematical implementations.

---

## Financial Engine

Responsible for:

- Numerical computation
- Optimization algorithms
- Statistical calculations
- Validation of numerical inputs

Must remain framework independent.

---

## Database Layer

Responsible for:

- Persistence
- ORM models
- Sessions
- Migrations

Must not contain business logic.

---

# 8. Code Quality Checklist

Before any implementation is accepted, verify the following.

## Compilation

```bash
python -m compileall app
```

Compilation must complete without errors.

---

## Relevant Tests

Execute only the tests related to the modified module.

Example:

```bash
pytest tests/api/test_optimization_api.py -v
```

---

## Full Test Suite

Always execute the complete test suite before considering the feature
finished.

```bash
pytest
```

At the completion of Phase 5, the repository maintains:

```text
117 Passing Tests
0 Failing Tests
```

Every future phase must preserve this standard.

---

# 9. Testing Philosophy

Testing is considered an essential engineering activity rather than an
optional verification step.

The repository follows a layered testing strategy.

## Financial Engine Tests

Validate:

- Mathematical correctness
- Numerical stability
- Validation logic
- Edge cases

These tests do not involve FastAPI or databases.

---

## Service Tests

Validate:

- Workflow orchestration
- Business validation
- Integration between components

External dependencies should be mocked where appropriate.

---

## API Tests

Validate:

- HTTP routes
- Request validation
- Response serialization
- Error translation
- Status codes

API tests should mock Services rather than execute Financial Engines.

---

# 10. Error Handling

Errors are handled at the appropriate architectural layer.

Financial Engines raise Python exceptions.

Services propagate or translate business validation errors.

APIs convert exceptions into HTTP responses.

This separation preserves clean architecture and simplifies testing.

---

# 11. Git Workflow

OptiVest follows a simple, disciplined Git workflow designed to preserve
repository stability while keeping the commit history meaningful.

Development proceeds through incremental phases.

Each completed phase should correspond to one or more logically grouped
commits.

Large unrelated changes should never be combined into a single commit.

---

## Recommended Workflow

```text
Engineering Review

↓

Implementation

↓

Compile

↓

Relevant Tests

↓

Full Test Suite

↓

Documentation Update

↓

Git Commit

↓

Push
```

Every commit should leave the repository in a buildable state.

---

# 12. Commit Message Convention

Commit messages should clearly communicate the purpose of the change.

Preferred format:

```text
type(scope): summary
```

Examples:

```text
feat(optimization): add optimization REST API

feat(simulation): implement Monte Carlo engine

test(api): add optimization endpoint tests

refactor(service): simplify optimization orchestration

docs(project): update project state after Phase 6

fix(statistics): validate covariance dimensions
```

Meaningful commit messages improve repository history and simplify code
reviews.

---

# 13. Documentation Standards

Documentation evolves together with the codebase.

The following documents are considered repository documentation:

- Project Specification
- Software Architecture
- Financial Engine
- Development Guide
- Project State
- Decisions

Documentation should always describe the current repository state.

Historical notes, temporary plans, and outdated implementation details
should not accumulate inside these documents.

Instead, documentation should be periodically consolidated into clean,
authoritative versions.

---

# 14. Repository Maintenance

The repository should remain organized throughout development.

General maintenance guidelines include:

- Remove unused imports.
- Remove dead code.
- Delete obsolete files.
- Keep directory structures consistent.
- Maintain descriptive filenames.
- Keep module responsibilities focused.

Refactoring should improve clarity without changing observable
behaviour.

---

# 15. Dependency Management

Dependencies should be introduced only when they provide measurable
benefit.

Before adding a dependency, consider:

- Is an existing library already sufficient?
- Can the feature be implemented using the standard library?
- Does the dependency significantly increase complexity?
- Is the dependency actively maintained?

Version 1 intentionally minimizes unnecessary third-party libraries.

---

# 16. Refactoring Policy

Refactoring is encouraged when it improves:

- readability
- maintainability
- modularity
- testability

Refactoring should not alter business behaviour.

When behaviour changes are required, they should be introduced as
separate commits rather than mixed with structural refactoring.

---

# 17. Future Development Process

Every future phase should follow the same engineering discipline.

For each new feature:

1. Perform an engineering review.
2. Validate architectural placement.
3. Implement the Financial Engine.
4. Write Financial Engine tests.
5. Implement the Service.
6. Write Service tests.
7. Implement Schemas.
8. Implement REST APIs.
9. Write API tests.
10. Update documentation.
11. Run the full test suite.
12. Commit.

This repeatable workflow has been used successfully throughout the first
five development phases.

---

# 18. Phase Completion Checklist

A phase is considered complete only when all of the following conditions
are satisfied.

## Engineering

- Architecture remains consistent.
- No duplicated business logic.
- Layer responsibilities are preserved.
- Financial Engines remain framework independent.

---

## Quality

- Code compiles successfully.
- Static typing is maintained.
- Public interfaces are documented.
- Repository remains organized.

---

## Testing

- Relevant tests pass.
- Full test suite passes.
- No regressions are introduced.

---

## Documentation

- Project State updated.
- Decisions updated.
- New architecture documented if required.

Only after completing all items should the next development phase begin.

---

# 19. Interview Readiness Checklist

OptiVest is intended to support technical interviews.

Before considering a feature complete, ensure it can be explained from
both software engineering and financial perspectives.

Questions contributors should be able to answer include:

Software Engineering:

- Why does this feature belong in its current layer?
- Why is the chosen architecture appropriate?
- How is duplication avoided?
- How is the feature tested?
- How would the implementation scale?

Financial Engineering:

- What financial problem does the algorithm solve?
- What assumptions are made?
- How are numerical inputs validated?
- Why is the chosen optimization method appropriate?

A feature that cannot be confidently explained should be revisited before
being merged.

---

# 20. Common Anti-Patterns

The following practices should be avoided.

## Architectural Violations

- Financial calculations inside API routes.
- Business logic inside ORM models.
- Database access from Financial Engines.
- Direct API-to-database communication.

---

## Code Quality Issues

- Duplicate logic.
- Placeholder implementations.
- Excessive abstraction.
- Long functions with multiple responsibilities.
- Unused code.
- Hidden side effects.

---

## Testing Issues

- Untested features.
- Tests depending on external services.
- API tests executing financial algorithms directly.
- Flaky or nondeterministic tests.

Avoiding these anti-patterns helps preserve repository quality over the
entire development lifecycle.

---

# 21. Repository Metrics

At the completion of Phase 5, the repository status is:

| Metric | Status |
|--------|--------|
| Architecture | Layered Modular Monolith |
| Current Phase | Phase 5 Complete |
| Passing Tests | 117 |
| Failing Tests | 0 |
| Optimization Engine | Complete |
| Optimization API | Complete |
| Optimization Tests | Complete |
| Next Milestone | Phase 6 – Monte Carlo Simulation |

These metrics should be updated whenever a major development phase is
completed.

---

# 22. Conclusion

The Development Guide establishes a consistent engineering workflow for
the OptiVest repository.

By combining disciplined implementation, layered architecture,
comprehensive testing, and documentation-driven development, the project
maintains production-quality standards while remaining approachable and
interview-defensible.

Every future contribution should follow the practices described in this
guide to ensure that the repository continues to evolve in a consistent,
maintainable, and high-quality manner.

---

**End of Document**

**Document:** 04_DEVELOPMENT_GUIDE.md

**Version:** 1.0

**Repository Status:** Phase 5 Complete

**Current Test Status:** 117 Passing

**Next Planned Phase:** Phase 6 – Monte Carlo Simulation

## Version 1 Minimalism

OptiVest Version 1 intentionally prioritizes engineering quality over
feature quantity.

The repository should contain only components that directly contribute
to implemented functionality.

Avoid creating files solely to satisfy architectural patterns or future
possibilities.

Examples of files that should not be introduced without immediate need
include:

- Placeholder modules
- Empty packages
- Generic utility layers
- Repository abstractions
- Service managers
- Factory hierarchies
- Generic CRUD implementations
- Interfaces with a single implementation

Every new file must have a clear, immediate responsibility within the
current repository.

Future expansion should occur incrementally rather than through
premature scaffolding.

## Avoid Premature Abstraction

Architectural abstractions should be introduced only when justified by
existing complexity.

The repository intentionally avoids enterprise design patterns that do
not provide measurable value for Version 1.

Examples include:

- Repository Pattern
- Unit of Work
- Generic Service Layers
- Abstract Managers
- Dependency Injection Frameworks

These patterns may be considered in future versions if repository scale
demands them.

Until then, simplicity is preferred over theoretical extensibility.

## Prefer Extending Existing Components

Before creating a new module, evaluate whether the required functionality
naturally belongs within an existing component.

Creating new files increases repository complexity and maintenance cost.

A new file should be introduced only when:

- it represents a distinct responsibility,
- it improves modularity,
- or it significantly improves readability.

Small extensions to existing modules are preferred over unnecessary file
creation.

## Financial Engine Stability

Financial Engines represent validated mathematical implementations.

Once an engine has been completed and tested, it is considered stable.

Future phases should build upon existing engines rather than modifying
them.

Changes to completed Financial Engines are permitted only when:

- a mathematical correctness issue exists,
- a numerical stability issue is identified,
- or a verified bug requires correction.

Architectural refactoring alone is not sufficient justification for
modifying a completed Financial Engine.