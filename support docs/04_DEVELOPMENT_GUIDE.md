# 04_DEVELOPMENT_GUIDE.md

# OptiVest Development Guide

**Version:** 1.1

**Status:** Active

---

# 1. Development Philosophy

OptiVest is developed as if it were a production-grade fintech backend rather than a student project.

Every implementation should prioritize, in order:

* Correctness
* Financial correctness
* Readability
* Maintainability
* Extensibility
* Testability

Never trade long-term code quality for short-term speed.

---

# 2. Engineering Principles

Every implementation should satisfy:

* Single Responsibility Principle
* DRY
* KISS
* Strong Typing
* Explicit Dependencies
* Separation of Concerns
* Low Coupling
* High Cohesion

When in doubt, choose the simpler design that remains extensible.

---

# 3. Layer Responsibilities

The architecture is fixed.

```text
API
↓
Services
↓
Financial Engines
↓
Database / External APIs
```

## API Layer

Responsible for

* Request parsing
* Authentication
* Calling services
* Returning DTOs
* HTTP error translation

Never perform business logic.

---

## Service Layer

Responsible for

* Business validation
* Workflow orchestration
* Database interaction
* Calling Financial Engines

Never perform mathematical calculations.

---

## Financial Engines

Responsible for

* Mathematical algorithms
* Statistical calculations
* Optimization
* Numerical validation

Financial Engines must never import:

* FastAPI
* SQLAlchemy
* Database models
* Pydantic

They should behave as deterministic computational libraries.

---

# 4. Coding Standards

## Python

* Follow PEP 8.
* Use type hints everywhere.
* Prefer explicit code over clever code.
* Keep functions focused.
* Avoid duplicated logic.
* Use descriptive names.
* Never hardcode configuration.
* Raise meaningful exceptions.

---

## API Design

Routes should remain extremely thin.

Example flow

```text
Request

↓

Service

↓

Financial Engine

↓

Response DTO
```

---

## Services

Services should

* Validate business rules
* Coordinate workflow
* Return domain objects or DataFrames

Never return HTTP responses.

---

## Financial Engines

Should

* Accept primitive types, NumPy arrays or Pandas DataFrames
* Return deterministic outputs
* Validate numerical assumptions
* Raise Python exceptions

Never know anything about HTTP.

---

# 5. Internal Data Standards

Financial calculations use:

* Pandas DataFrames
* NumPy arrays

API responses use:

* Pydantic schemas

Serialization happens only inside the API layer.

---

# 6. Error Handling

### API

Translate

```text
ValueError

↓

HTTPException(400)
```

### Services

Raise Python exceptions.

### Financial Engines

Raise numerical validation errors.

Never expose framework-specific exceptions below the API layer.

---

# 7. Testing Policy

Every completed feature requires

## Runtime Validation

```bash
python -m compileall app
```

---

## Unit Tests

Financial Engines

* Mathematical correctness
* Numerical validation
* Edge cases

---

## Service Tests

* Business rules
* Validation
* Engine orchestration

---

## API Tests

* Request validation
* Serialization
* Status codes
* Error handling

---

## External Dependencies

Never call external APIs in tests.

Always mock

* Yahoo Finance
* Future optimization solvers
* Any third-party service

---

# 8. Development Workflow

Every feature follows exactly this sequence.

```text
Design

↓

Implement

↓

python -m compileall app

↓

Runtime Validation

↓

pytest

↓

Documentation Update

↓

Git Commit
```

A feature is not complete until every step succeeds.

---

# 9. Virtual Environment Policy

Always use the project virtual environment.

Verify

```bash
python -c "import sys; print(sys.executable)"
```

Use

```bash
python -m pip install ...
```

Never rely on

```bash
pip install ...
```

Reason

Using `python -m pip` guarantees packages are installed into the active interpreter, preventing environment mismatch issues encountered during Phase 3.

---

# 10. Documentation Policy

Every completed phase requires updating

* PROJECT_STATE.md
* DECISIONS.md
* Development Guide (if workflow changed)

Project documentation should always reflect the repository's current state.

---

# 11. Git Workflow

Commit after every meaningful feature.

Examples

```text
feat(auth): implement JWT authentication

feat(portfolio): add CRUD APIs

feat(market-data): complete market data foundation

feat(statistics): implement covariance matrix

docs: update project state

test: add statistics engine tests
```

Never commit failing tests.

---

# 12. Interview Readiness

Every feature should be explainable in terms of

* Problem
* Design decision
* Trade-offs
* Mathematical reasoning
* Time complexity
* Space complexity
* Future extensibility

If a feature cannot be defended during an interview, reconsider its implementation.

---

# 13. Version 1 Constraints

Do NOT introduce

* Repository Pattern
* Generic CRUD
* Unit of Work
* Interfaces
* Managers
* Factory Pattern
* Generic Service Layers

Follow the Rule of Three before introducing abstractions.

---

# 14. End-of-Phase Checklist

Before marking any phase complete

* Backend implementation complete
* Financial calculations validated
* Runtime compilation successful
* Unit tests written
* Integration tests written
* API tests written
* All tests passing
* Documentation updated
* PROJECT_STATE updated
* DECISIONS updated
* Git commit created

Only then is a phase considered complete.

---

Current Completed Phases

* Phase 0 — Foundation
* Phase 1 — Authentication
* Phase 2 — Portfolio CRUD
* Phase 3 — Market Data Foundation
* Phase 4 — Portfolio Statistics Foundation

Current Test Count

61 Passing Tests

Next Phase

Phase 5 — Portfolio Optimization
```
