# OptiVest – Software Architecture

Version: 1.0

Status: Active

---

# 1. Architecture Philosophy

OptiVest follows a **Layered Modular Monolith Architecture**.

The application is intentionally designed as a modular monolith instead of microservices because:

* Simpler deployment
* Easier debugging
* Lower operational complexity
* Better suited for a single-developer project
* Easy migration to microservices in future versions

The system emphasizes:

* Separation of Concerns
* Single Responsibility Principle
* Low Coupling
* High Cohesion
* Dependency Inversion
* Testability

---

# 2. High-Level Architecture

```
                    React Frontend
                           │
                    Axios HTTP Client
                           │
                    FastAPI REST API
                           │
────────────────────────────────────────────
            Application Service Layer
────────────────────────────────────────────
│
├── Authentication Service
├── Portfolio Service
├── Market Data Service
├── Optimization Service
├── Simulation Service
└── Risk Analytics Service
────────────────────────────────────────────
        Database + Financial Engines
────────────────────────────────────────────
│
├── PostgreSQL
├── SQLAlchemy ORM
├── NumPy
├── Pandas
├── SciPy
├── CVXPY
└── yfinance
```

---

# 3. Backend Directory Structure

```
backend/

app/

    api/
        auth.py
        portfolio.py
        optimization.py
        simulation.py
        risk.py

    services/
        auth_service.py
        portfolio_service.py
        market_service.py
        optimization_service.py
        simulation_service.py
        risk_service.py

    models/
        user.py
        portfolio.py
        holding.py

    schemas/
        auth.py
        portfolio.py
        optimization.py
        simulation.py
        risk.py

    database/
        base.py
        session.py

    core/
        config.py
        security.py
        logging.py

    utils/

    main.py
```

---

# 4. Layer Responsibilities

## API Layer

Responsibilities

* Receive HTTP requests
* Validate request bodies
* Authenticate users
* Call services
* Return HTTP responses

The API layer must never contain business logic.

---

## Service Layer

Responsibilities

* Business logic
* Portfolio calculations
* Validation
* Database interaction
* Calling financial engines

Every endpoint should delegate work to a service.

---

## Financial Engines

Responsibilities

Pure mathematical computations.

Examples

Optimization Engine

Monte Carlo Engine

Risk Engine

These modules should remain independent of FastAPI and SQLAlchemy.

Given the same inputs, they should always produce the same outputs.

---

## Database Layer

Responsibilities

* Persist user data
* Persist portfolios
* Manage relationships
* Execute queries

Business logic should never exist inside models.

---

# 5. Frontend Structure

```
frontend/

src/

    components/

        charts/

        cards/

        forms/

        layout/

    pages/

        Dashboard

        Portfolio

        Optimization

        Simulation

        Risk

    hooks/

    services/

    context/

    types/

    utils/
```

---

# 6. Frontend Responsibilities

## Pages

Responsible for

* Data fetching
* Layout
* Page composition

Should not contain reusable UI logic.

---

## Components

Reusable UI building blocks.

Examples

Portfolio Card

Metric Card

Navbar

Pie Chart

Scatter Plot

Allocation Table

---

## Services

Responsible for

HTTP communication only.

Uses Axios.

No UI logic.

---

## Hooks

Reusable React logic.

Example

usePortfolio()

useAuthentication()

---

# 7. Database Design

## Users

Stores authentication information.

Relationship

One User

↓

Many Portfolios

---

## Portfolios

Stores portfolio metadata.

Relationship

One Portfolio

↓

Many Holdings

---

## Holdings

Stores

Ticker

Weight

Quantity

Purchase Price

---

## Portfolio Snapshots

Stores

Historical portfolio metrics

Used for growth visualization.

---

# 8. Request Lifecycle

Example

Optimize Portfolio

```
Frontend

↓

POST /optimize

↓

API Layer

↓

Optimization Service

↓

Optimization Engine

↓

Response DTO

↓

Frontend Visualization
```

No mathematical logic should exist in the API layer.

---

# 9. Dependency Rules

Allowed

```
API

↓

Services

↓

Financial Engines

↓

Database
```

Forbidden

* Services importing API modules
* Database models calling services
* Financial engines importing FastAPI
* Frontend components making direct HTTP requests

---

# 10. Error Handling Strategy

Every layer has defined responsibilities.

API

* HTTP exceptions

Service

* Business exceptions

Financial Engine

* Numerical validation

Database

* Persistence errors

---

# 11. Validation Strategy

Input validation

Pydantic Schemas

Business validation

Service Layer

Mathematical validation

Financial Engine

Database validation

SQL Constraints

---

# 12. Security

Authentication

JWT

Passwords

bcrypt hashing

Secrets

Environment variables only

Never hardcode credentials.

---

# 13. Logging

Log

* Authentication attempts
* API requests
* Optimization failures
* Database errors

Never log

Passwords

JWT tokens

Secrets

---

# 14. Testing Strategy

Backend

* Unit Tests
* API Tests

Finance

* Numerical Tests

Frontend

* Component Tests

End-to-End

Critical user flows.

---

# 15. Engineering Principles

Every module should satisfy:

* Single Responsibility
* Open for Extension
* Closed for Modification
* Low Coupling
* High Cohesion
* Pure Functions wherever possible
* Type Safety
* Explicit Dependencies

---

# 16. Scalability

Future services can be added without modifying existing ones.

Examples

* Benchmark Service
* Stress Testing Service
* Rebalancing Service
* AI Insight Service

The architecture is intentionally designed to accommodate Version 2 and Version 3 features without significant refactoring.

---

# 17. Interview Talking Points

This architecture was selected because it:

* Separates business logic from transport logic.
* Keeps mathematical computations framework-independent.
* Encourages modularity and testability.
* Follows common production backend patterns.
* Supports future feature expansion with minimal coupling.
* Is appropriate for a production-grade application developed by a small engineering team.

When discussing the project, emphasize that the system is a **modular monolith**—a deliberate design choice balancing simplicity with extensibility, rather than an incomplete microservices architecture.
