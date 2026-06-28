# OptiVest – Development Guide

Version: 1.0

Status: Active

---

# 1. Development Philosophy

OptiVest is developed as if it were a production fintech product rather than a student assignment.

Every implementation should prioritize:

* Correctness
* Readability
* Maintainability
* Extensibility
* Testability

Avoid shortcuts that reduce code quality.

---

# 2. Coding Standards

## General

* Prefer explicit code over clever code.
* Write self-documenting code.
* Keep functions small and focused.
* Avoid duplicated logic.
* Use descriptive variable names.
* Never hardcode secrets or configuration.

---

## Python

* Follow PEP 8.
* Use type hints.
* Use Pydantic for validation.
* Business logic belongs in Services.
* Mathematical logic belongs in Financial Engines.
* API routes should remain thin.

---

## TypeScript

* Avoid `any`.
* Define interfaces and types.
* Keep components reusable.
* Prefer composition over inheritance.
* Avoid duplicated UI logic.

---

# 3. Git Workflow

Commit after every meaningful feature.

Examples

```text
feat(auth): implement JWT authentication

feat(portfolio): add CRUD APIs

feat(optimization): implement efficient frontier

feat(risk): add VaR and CVaR calculations

docs: update project state

test: add optimization engine tests
```

Never commit broken code.

---

# 4. Testing Policy

Every feature should include:

Backend

* Unit Tests
* API Tests

Finance

* Numerical validation
* Edge cases

Frontend

* Component rendering
* API integration

---

# 5. Error Handling

Every error should:

* Be logged
* Be understandable
* Return meaningful messages
* Never expose internal details

---

# 6. Security Guidelines

* JWT Authentication
* bcrypt password hashing
* Environment variables
* SQLAlchemy ORM (avoid SQL injection)
* Validate all user inputs

Never expose secrets.

---

# 7. Documentation Policy

Every completed feature must include:

* Code comments where appropriate
* README updates
* API documentation
* PROJECT_STATE update

---

# 8. Interview Readiness

Every implemented feature should be explainable in terms of:

* Problem
* Design decision
* Trade-offs
* Complexity
* Limitations
* Future improvements

If a feature cannot be defended in an interview, reconsider its implementation.

---

# 9. End-of-Phase Checklist

Before marking a phase complete:

* Backend complete
* Frontend complete
* Validation complete
* Tests written
* Documentation updated
* Git commit created
* PROJECT_STATE updated
* Technical debt reviewed

Only then is a phase considered complete.
