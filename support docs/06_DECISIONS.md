# OptiVest

# Engineering Decisions

**Document Version:** 1.0

**Project Version:** Version 1

**Repository Status:** Phase 5 Complete

**Current Test Status:** 117 Passing

**Last Updated:** After Phase 5 Completion

---

# Purpose

This document records the architectural and engineering decisions that
govern the OptiVest repository.

Unlike the Project Specification, which defines *what* the project
should accomplish, or the Software Architecture document, which defines
*how* the repository is organized, this document explains **why**
important engineering decisions were made.

Each decision represents a deliberate design choice and should be
preserved unless a compelling technical reason exists to change it.

---

# Decision 001 — Layered Modular Monolith

The repository follows a Layered Modular Monolith architecture.

### Reason

Provides:

- Low operational complexity
- High maintainability
- Excellent testability
- Clear separation of concerns

without introducing unnecessary distributed-system complexity.

---

# Decision 002 — Financial Engines are Framework Independent

Financial Engines never depend on:

- FastAPI
- SQLAlchemy
- Pydantic
- JWT
- ORM Models

### Reason

Mathematical computation should remain reusable, deterministic and easily
testable.

---

# Decision 003 — Business Logic Belongs in Services

Application workflows belong exclusively to the Service layer.

### Reason

Services orchestrate application behaviour while Financial Engines
perform mathematical computation.

---

# Decision 004 — Thin REST APIs

REST endpoints perform only:

- request validation
- authentication
- serialization
- exception translation

### Reason

Keeps transport logic separate from business logic.

---

# Decision 005 — Financial Engines Own Mathematics

Every financial algorithm belongs inside Financial Engines.

Examples:

- Statistics
- Optimization
- Future Monte Carlo
- Future Risk Analytics

### Reason

Centralizes mathematical logic and prevents duplication.

---

# Decision 006 — Validation at Multiple Layers

Validation occurs where responsibility exists.

API

- Request validation

Service

- Business validation

Financial Engine

- Numerical validation

### Reason

Each architectural layer validates only what it owns.

---

# Decision 007 — Immutable Domain Models

Optimization results are represented using immutable domain models.

Examples:

- OptimizedPortfolio
- EfficientFrontierPoint

### Reason

Immutable objects reduce accidental modification and improve reasoning.

---

# Decision 008 — Deterministic Computation

Financial Engines must produce identical outputs for identical inputs.

Randomized algorithms must expose configurable seeds.

### Reason

Improves reproducibility and testing.

---

# Decision 009 — Production-Quality Testing

Every feature includes:

- Financial Engine tests
- Service tests
- API tests

### Reason

Different architectural layers require different validation strategies.

---

# Decision 010 — Documentation Driven Development

Repository documentation evolves together with implementation.

### Reason

Documentation should always describe the current repository rather than
historical development.

---

# Decision 011 — Version 1 Minimalism

Version 1 intentionally avoids unnecessary files.

Every file must directly implement repository functionality.

Placeholder modules are not permitted.

### Reason

Smaller repositories are easier to maintain and defend during technical
interviews.

---

# Decision 012 — Avoid Premature Abstraction

Enterprise abstractions are introduced only when justified.

Avoid:

- Repository Pattern
- Unit of Work
- Generic Managers
- Generic CRUD
- Service Factories

### Reason

Version 1 prioritizes simplicity over speculative extensibility.

---

# Decision 013 — Prefer Extending Existing Components

Before creating a new file, evaluate whether the functionality belongs
inside an existing module.

### Reason

Reduces repository growth and maintenance cost.

---

# Decision 014 — Strong Typing

Public interfaces use explicit type hints wherever practical.

### Reason

Improves readability, tooling support and maintainability.

---

# Decision 015 — Repository Growth is Controlled

Repository size should grow only through justified functionality.

No file should exist solely for future possibilities.

### Reason

Maintains a clean and understandable codebase.

---

# Decision 016 — Market Data Separation

Market data retrieval belongs in Services.

Financial Engines only process numerical datasets.

### Reason

Separates infrastructure from computation.

---

# Decision 017 — Statistics Engine Separation

Statistics calculations remain independent of Optimization.

### Reason

Statistics are reusable by multiple future Financial Engines.

---

# Decision 018 — Shared Optimization Utilities

Common optimization logic is centralized into shared helper modules.

### Reason

Avoids duplicated CVXPY code while preserving readability.

---

# Decision 019 — Optimization Models

Optimization domain models reside in a dedicated `models.py` module.

### Reason

Separates reusable domain objects from optimization algorithms.

---

# Decision 020 — Efficient Frontier Domain Model

Each frontier portfolio is represented by an immutable
`EfficientFrontierPoint`.

### Reason

Provides a stable interface between Financial Engines and Services.

---

# Decision 021 — Optimization Service Responsibilities

OptimizationService performs:

- Market data retrieval
- Input preparation
- Financial Engine orchestration

It performs no mathematical optimization.

### Reason

Preserves clean separation of concerns.

---

# Decision 022 — Optimization API Responsibilities

Optimization endpoints perform only:

- Request validation
- Service delegation
- Response serialization
- Exception translation

### Reason

REST APIs should remain transport layers.

---

# Decision 023 — Optimization Serialization

Optimization responses intentionally expose only portfolio allocations.

The API does not compute additional financial metrics.

### Reason

Services currently return optimized weights only.

The API must never invent financial calculations.

---

# Decision 024 — Efficient Frontier Serialization

Efficient Frontier responses are serialized from immutable domain models.

### Reason

Separates domain representation from transport representation.

---

# Decision 025 — API Testing Strategy

API tests mock Services.

They do not execute Financial Engines.

### Reason

API tests validate HTTP behaviour rather than mathematical correctness.

---

# Decision 026 — Service Testing Strategy

Service tests verify orchestration.

External dependencies should be mocked.

### Reason

Business workflow testing should remain isolated from infrastructure.

---

# Decision 027 — Financial Engine Testing Strategy

Financial Engine tests verify:

- Mathematical correctness
- Numerical stability
- Validation
- Edge cases

### Reason

Mathematical correctness belongs exclusively to Financial Engine tests.

---

# Decision 028 — Frozen Financial Engines

Completed Financial Engines are considered stable.

Changes require:

- correctness bug
- numerical stability issue
- verified implementation defect

### Reason

Protects validated mathematical implementations.

---

# Decision 029 — Phase Completion Policy

A phase is complete only after:

- compile succeeds
- relevant tests pass
- full test suite passes
- documentation updated

### Reason

Prevents incomplete feature delivery.

---

# Decision 030 — Documentation Consolidation

Repository documentation should be periodically rewritten rather than
continuously appended.

### Reason

Prevents duplicated history and outdated implementation notes.

---

# Decision 031 — Repository Quality over Feature Count

Engineering quality is prioritized over the number of implemented
features.

### Reason

Maintainability and correctness provide greater long-term value than
rapid feature expansion.

---

# Decision 032 — Interview Defensibility

Every architectural decision should be explainable during technical
interviews.

### Reason

The repository is intended to demonstrate engineering judgement in
addition to implementation ability.

---

# Future Decisions

Future phases will extend this document with additional decisions for:

- Monte Carlo Simulation
- Risk Analytics
- Portfolio Health
- React Frontend
- Production Deployment

New decisions should be appended rather than modifying historical
entries unless a previous decision has become technically incorrect.

---

# Summary

The decisions recorded in this document define the engineering identity
of OptiVest.

They ensure that future development remains consistent with the
repository's architectural principles, coding philosophy, and quality
standards.

Any significant deviation from these decisions should be documented and
justified before implementation.

---

**End of Document**

**Document:** 06_DECISIONS.md

**Version:** 1.0

**Repository Status:** Phase 5 Complete

**Current Test Status:** 117 Passing

**Engineering Decisions:** 32

**Next Planned Phase:** Phase 6 – Monte Carlo Simulation