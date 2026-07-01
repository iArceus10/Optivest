# OptiVest

# Software Architecture

**Document Version:** 1.0

**Project Version:** Version 1

**Repository Status:** Phase 5 Complete

**Current Test Status:** 117 Passing

**Architecture Style:** Layered Modular Monolith

**Last Updated:** After Phase 5 Completion

---

# 1. Purpose

This document defines the architectural principles governing the OptiVest
repository.

The architecture has been intentionally designed to demonstrate
production-quality backend engineering while remaining sufficiently simple
to understand, extend, and defend during technical interviews.

Every implementation within the repository must conform to the principles
described in this document.

The Software Architecture document is considered one of the primary
sources of truth for repository development.

---

# 2. Architectural Goals

The architecture has six primary goals.

## 2.1 Maintainability

Every module should have a clearly defined responsibility.

Changes made to one subsystem should require minimal modifications to
other parts of the repository.

---

## 2.2 Separation of Concerns

Application responsibilities are intentionally separated into
independent layers.

Examples include:

- HTTP handling
- Business orchestration
- Financial computation
- Database persistence
- External integrations

Each responsibility belongs to exactly one architectural layer.

---

## 2.3 Testability

Every architectural layer should be independently testable.

Examples include:

- Financial Engines without FastAPI
- Services without HTTP
- APIs without financial computation

Testing should isolate the layer under examination.

---

## 2.4 Extensibility

Future financial modules should integrate naturally without requiring
modifications to existing engines.

Examples include:

- Monte Carlo Simulation
- Risk Analytics
- Portfolio Health
- Black-Litterman Optimization

The architecture should support growth through extension rather than
modification.

---

## 2.5 Production Readiness

Although OptiVest is Version 1, every implemented component should
follow production-quality engineering practices.

Examples include:

- Strong typing
- Structured logging
- Centralized configuration
- Dependency injection
- Modular design
- Automated testing

---

## 2.6 Interview Defensibility

Every architectural decision should be explainable during software
engineering interviews.

No component should exist solely because it is considered fashionable or
enterprise-standard.

Each abstraction must provide measurable value.

---

# 3. Architectural Style

OptiVest follows a **Layered Modular Monolith** architecture.

The repository consists of logically separated modules that execute
within a single deployable application.

This approach combines the simplicity of a monolithic application with
the maintainability benefits of modular software design.

---

## Why a Modular Monolith?

The project intentionally avoids microservices.

Reasons include:

- Reduced operational complexity.
- Easier local development.
- Simpler testing.
- Lower deployment overhead.
- Better suitability for Version 1.

Microservices introduce challenges such as distributed transactions,
service discovery, network communication, and infrastructure management
that are unnecessary for the scope of this project.

---

# 4. High-Level Architecture

```text
                 Client Applications
                         │
                         ▼
                FastAPI REST API Layer
                         │
                         ▼
                 Application Services
                         │
                         ▼
                Financial Engine Layer
                 │                  │
                 ▼                  ▼
        Database Layer      External Market Data
```

Communication flows strictly downward.

Lower layers must never depend on higher layers.

---

# 5. Architectural Layers

The repository is divided into five primary layers.

## Layer 1 — API Layer

Directory:

```text
app/api/
```

Responsibilities:

- HTTP routing
- Request validation
- Response serialization
- Authentication
- Exception translation

The API layer **must never**:

- Perform portfolio optimization
- Execute financial calculations
- Query databases directly
- Implement business rules

Instead, it delegates all work to Services.

---

## Layer 2 — Service Layer

Directory:

```text
app/services/
```

Responsibilities:

- Business orchestration
- Workflow coordination
- Market data retrieval
- Validation of business rules
- Financial Engine coordination

Examples include:

- MarketDataService
- StatisticsService
- OptimizationService
- PortfolioService

Services are responsible for combining multiple components into complete
application workflows.

Services **must never** implement mathematical algorithms.

---

## Layer 3 — Financial Engine Layer

Directory:

```text
app/financial_engines/
```

This layer contains the mathematical core of the repository.

Characteristics:

- Framework independent
- Database independent
- FastAPI independent
- SQLAlchemy independent
- Pure Python numerical computation

Financial Engines receive numerical inputs and return deterministic
results.

Examples include:

### Market Data Engine

Responsible for:

- Return calculations
- Annualization
- Data validation

---

### Statistics Engine

Responsible for:

- Expected returns
- Covariance matrices
- Correlation matrices
- Portfolio volatility

---

### Optimization Engine

Responsible for:

- Mean-Variance Optimization
- Minimum Variance Optimization
- Maximum Sharpe Optimization
- Efficient Frontier Generation

Future engines will include:

- Monte Carlo Simulation
- Risk Analytics

---

## Layer 4 — Infrastructure Layer

Infrastructure includes:

```text
Database

Configuration

Logging

Authentication

External APIs
```

Infrastructure provides services required by the application but contains
no business logic.

Examples:

- SQLAlchemy
- PostgreSQL
- JWT
- Yahoo Finance
- Logging configuration

---

## Layer 5 — Persistence Layer

Directory:

```text
app/database/
```

Responsibilities include:

- Database sessions
- ORM models
- Migrations
- Persistence

Persistence is isolated from Financial Engines.

Financial Engines never communicate directly with databases.

---

# 6. Dependency Rules

The dependency direction is strictly enforced.

```text
API
 │
 ▼
Services
 │
 ▼
Financial Engines
 │
 ▼
Infrastructure
```

Allowed dependencies:

```text
API
    ↓
Services

Services
    ↓
Financial Engines

Services
    ↓
Infrastructure

Infrastructure
    ↓
Database
```

Forbidden dependencies:

```text
Financial Engine
        ↑
FastAPI

Financial Engine
        ↑
SQLAlchemy

Financial Engine
        ↑
Pydantic

API
    ↓
Database

Database
    ↑
Services
```

Violating these dependency rules creates tight coupling and reduces
maintainability.

---

# 7. Request Lifecycle

A typical request follows the sequence below.

```text
HTTP Request

↓

API Endpoint

↓

Request Validation

↓

Service

↓

Financial Engine

↓

Service

↓

Response Serialization

↓

HTTP Response
```

Every request follows the same lifecycle regardless of functionality.

This consistency improves readability and reduces architectural drift.

---

# 8. Domain Model Philosophy

The repository distinguishes between three categories of models.

## ORM Models

Represent persistent database entities.

Examples:

- User
- Portfolio

These models belong exclusively to the persistence layer.

---

## API Schemas

Represent transport objects exchanged through REST APIs.

Examples:

- Requests
- Responses

API Schemas never contain business logic.

---

## Domain Models

Represent immutable business concepts independent of frameworks.

Examples:

- EfficientFrontierPoint
- OptimizedPortfolio

These models are produced by Financial Engines and consumed by higher
layers without introducing framework dependencies.

---

# 9. Repository Structure

The repository follows a feature-oriented organization while preserving
clear separation between architectural layers.

```text
backend/
│
├── app/
│   ├── api/
│   │   └── v1/
│   │
│   ├── core/
│   │
│   ├── database/
│   │
│   ├── financial_engines/
│   │   ├── market_data/
│   │   ├── statistics/
│   │   ├── optimization/
│   │   ├── simulation/          (Planned)
│   │   └── risk/                (Planned)
│   │
│   ├── models/
│   │
│   ├── schemas/
│   │
│   └── services/
│
├── tests/
│
├── docs/
│
└── scripts/
```

Each directory exists for a single architectural purpose.

No directory should contain logic belonging to another layer.

---

# 10. Module Responsibilities

## API Modules

API modules expose REST endpoints.

Responsibilities include:

- Routing
- Request validation
- Authentication
- Response serialization
- HTTP exception handling

They delegate all application work to Services.

---

## Service Modules

Services orchestrate complete business workflows.

Typical workflow:

```text
Validate request

↓

Retrieve market data

↓

Prepare Financial Engine inputs

↓

Execute Financial Engine

↓

Return domain result
```

Services coordinate components but never implement mathematical
algorithms.

---

## Financial Engines

Financial Engines implement reusable quantitative algorithms.

Characteristics:

- Stateless
- Deterministic
- Framework independent
- Unit-testable

Every Financial Engine accepts numerical inputs and returns domain
objects.

No engine may import:

- FastAPI
- SQLAlchemy
- Pydantic
- ORM models
- API schemas

---

## Database Modules

Responsible for:

- ORM models
- Sessions
- Metadata
- Persistence

Business logic must never be implemented inside ORM models.

---

## Schema Modules

Schemas define contracts between the API and external clients.

They are responsible for:

- Validation
- Serialization
- Documentation

Schemas never contain business rules.

---

# 11. Error Handling Strategy

OptiVest follows a layered error-handling approach.

## Financial Engines

Financial Engines raise standard Python exceptions.

Example:

```python
raise ValueError("Optimization failed.")
```

They are unaware of HTTP or FastAPI.

---

## Services

Services propagate Financial Engine exceptions or convert business
validation failures into descriptive Python exceptions.

Services never raise HTTP-specific exceptions.

---

## API Layer

The API layer converts Python exceptions into HTTP responses.

Example:

```text
ValueError

↓

HTTP 400 Bad Request
```

This preserves separation between transport logic and business logic.

---

# 12. Validation Strategy

Validation occurs at multiple architectural layers.

## API Validation

Handled by Pydantic.

Examples:

- Required fields
- Date parsing
- Numeric ranges
- Input types

---

## Business Validation

Handled by Services.

Examples:

- Empty ticker lists
- Portfolio ownership
- User permissions

---

## Numerical Validation

Handled by Financial Engines.

Examples:

- Matrix dimensions
- Positive definiteness
- Missing values
- Invalid covariance matrices

Each layer validates only what it owns.

---

# 13. Configuration Architecture

Application configuration is centralized.

Responsibilities include:

- Environment variables
- Database URLs
- JWT configuration
- Secret management
- Application metadata

Configuration is accessed through a single settings object.

This avoids scattered configuration throughout the repository.

---

# 14. Logging Architecture

Logging is configured once during application startup.

Principles:

- Centralized configuration
- Structured logging
- Module-specific loggers
- Consistent formatting

Logging is intended for operational visibility rather than debugging.

Business logic should not depend on logging behavior.

---

# 15. Security Architecture

Authentication follows JWT-based stateless authentication.

Components include:

- Password hashing
- Password verification
- JWT generation
- JWT validation
- Protected endpoints

Security responsibilities are isolated within dedicated modules.

No Financial Engine or Service performs authentication directly.

---

# 16. Testing Architecture

Testing mirrors the repository architecture.

```text
Financial Engine Tests

↓

Service Tests

↓

API Tests
```

---

## Financial Engine Tests

Validate:

- Mathematical correctness
- Numerical stability
- Edge cases
- Deterministic behavior

These tests contain no FastAPI or database dependencies.

---

## Service Tests

Validate:

- Workflow orchestration
- Business validation
- Interaction between components

External dependencies are mocked where appropriate.

---

## API Tests

Validate:

- Routing
- Request validation
- Response serialization
- HTTP status codes
- Error translation

API tests mock Services rather than executing Financial Engines.

---

# 17. Extension Strategy

Future functionality should be added by extending the existing
architecture rather than modifying completed modules.

Example:

```text
Phase 6

Financial Engine

↓

Service

↓

Schemas

↓

API

↓

Tests
```

The same development sequence applies to all future features.

Completed Financial Engines remain frozen unless a correctness bug is
identified.

---

# 18. Architectural Principles

The following principles govern all development.

- Single Responsibility Principle
- Separation of Concerns
- Deterministic Financial Computation
- Explicit Dependencies
- Strong Typing
- Documentation-Driven Development
- Comprehensive Automated Testing
- Production-Quality Code

These principles take precedence over convenience or premature
optimization.

---

# 19. Architectural Constraints

The repository intentionally avoids unnecessary enterprise abstractions.

The following patterns are excluded from Version 1 unless justified by
future requirements:

- Repository Pattern
- Generic CRUD Services
- Unit of Work
- Service Factories
- Generic Managers
- Abstract Service Layers

This keeps the architecture simple, readable, and interview-defensible.

---

# 20. Summary

The Layered Modular Monolith architecture enables OptiVest to maintain a
clear separation between application concerns while remaining compact and
easy to understand.

By isolating REST APIs, Services, Financial Engines, and Infrastructure,
the repository achieves:

- High maintainability
- Excellent testability
- Deterministic financial computation
- Strong architectural consistency
- Low coupling
- High cohesion

This architecture forms the foundation for all remaining development
phases, including Monte Carlo Simulation, Risk Analytics, Portfolio
Health, React Frontend, and Production Deployment.

---

**End of Document**

**Document:** 02_SOFTWARE_ARCHITECTURE.md

**Version:** 1.0

**Architecture:** Layered Modular Monolith

**Repository Status:** Phase 5 Complete

**Current Test Status:** 117 Passing

**Next Planned Phase:** Phase 6 – Monte Carlo Simulation

