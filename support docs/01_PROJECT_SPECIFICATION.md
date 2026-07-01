# OptiVest

# Project Specification

**Document Version:** 1.0

**Project Version:** Version 1

**Repository Status:** Phase 5 Complete

**Current Test Status:** 117 Passing

**Architecture:** Layered Modular Monolith

**Primary Language:** Python

**Backend Framework:** FastAPI

**Database:** PostgreSQL

**Last Updated:** After Phase 5 Completion

---

# 1. Executive Summary

OptiVest is a production-quality Portfolio Optimization and Risk Analytics platform designed to demonstrate modern backend software engineering, quantitative finance, clean architecture, and professional development practices.

The project has been developed with the objective of producing a repository suitable for software engineering internships, quantitative finance interviews, and FinTech roles while maintaining production-quality engineering standards throughout the development lifecycle.

Unlike many educational portfolio projects, OptiVest separates mathematical computation from application logic through dedicated Financial Engines. This separation enables deterministic numerical computation, reusable financial algorithms, comprehensive testing, and long-term maintainability.

The repository intentionally follows professional engineering practices including modular architecture, typed interfaces, comprehensive testing, immutable financial models, layered design, and documentation-driven development.

---

# 2. Project Vision

The vision of OptiVest is to provide a platform capable of performing advanced portfolio analysis using modern software engineering principles while remaining understandable, maintainable, and extensible.

Rather than focusing solely on implementing financial algorithms, the project demonstrates how quantitative finance software should be engineered in a production environment.

The long-term objectives include:

- Portfolio optimization
- Portfolio risk analytics
- Monte Carlo portfolio simulation
- Portfolio health assessment
- Modern REST API architecture
- Interactive frontend visualization
- Production deployment

Every feature is implemented using the same architectural philosophy regardless of complexity.

---

# 3. Problem Statement

Individual investors often lack access to transparent tools capable of explaining portfolio construction and risk analysis.

Most freely available tools provide portfolio recommendations without exposing the underlying methodology or allowing reproducibility.

Similarly, many educational implementations combine mathematical computation, HTTP APIs, persistence, and business logic into a single layer, resulting in tightly coupled software that is difficult to maintain and extend.

OptiVest addresses these problems by separating responsibilities into independent architectural layers.

Financial computation remains completely independent of FastAPI, SQLAlchemy, databases, and external frameworks.

Business orchestration remains independent of numerical implementation.

REST APIs remain responsible only for request validation and response serialization.

This separation improves maintainability, testing, correctness, and long-term extensibility.

---

# 4. Primary Objectives

The primary objectives of OptiVest are:

## Software Engineering

- Demonstrate production-quality backend engineering.
- Follow a layered modular architecture.
- Maintain strong separation of concerns.
- Produce highly testable software.
- Keep mathematical computation independent of infrastructure.
- Avoid unnecessary abstractions while maintaining extensibility.

## Quantitative Finance

- Implement modern portfolio theory.
- Compute portfolio statistics.
- Perform convex portfolio optimization.
- Support efficient frontier generation.
- Support Monte Carlo portfolio simulation.
- Provide portfolio risk metrics.
- Generate meaningful portfolio insights.

## Professional Development

The repository is intended to demonstrate competencies expected from software engineers and quantitative developers, including:

- API design
- Backend architecture
- Database integration
- Numerical programming
- Software testing
- Documentation
- Version control
- Clean coding practices

---

# 5. Intended Audience

OptiVest is designed for multiple audiences.

## Software Engineering Recruiters

The repository demonstrates:

- API architecture
- Service layer organization
- Modular software design
- Automated testing
- Production-quality Python
- Dependency management
- Clean code

---

## Quantitative Finance Recruiters

The repository demonstrates:

- Mean-Variance Optimization
- Efficient Frontier Generation
- Maximum Sharpe Optimization
- Covariance estimation
- Portfolio statistics
- Numerical optimization
- Financial modelling

---

## Students

Students can study:

- Portfolio optimization
- Financial mathematics
- Backend architecture
- REST API design
- Software testing
- Project organization

---

## Developers

Developers can use OptiVest as a reference implementation for:

- Layered backend architecture
- Financial engine organization
- FastAPI best practices
- Service-oriented backend design
- Numerical software engineering

---

# 6. Version 1 Scope

Version 1 focuses exclusively on implementing a production-quality backend before frontend visualization.

The backend is developed incrementally through clearly defined implementation phases.

Completed phases remain frozen unless a correctness bug is identified.

This policy minimizes regression risk and preserves repository stability.

---

# 7. Functional Requirements

## Authentication

The platform shall provide secure user authentication.

Features include:

- User registration
- User login
- Password hashing using bcrypt
- JWT authentication
- Protected endpoints
- Current user retrieval

---

## Portfolio Management

The platform shall allow authenticated users to manage investment portfolios.

Features include:

- Portfolio creation
- Portfolio updates
- Portfolio deletion
- Ownership validation
- Portfolio retrieval

---

## Market Data

The platform shall retrieve historical financial market data.

Capabilities include:

- Historical adjusted close prices
- Daily returns
- Business validation
- Market data normalization

---

## Portfolio Statistics

The platform shall compute statistical characteristics of historical returns.

Statistics include:

- Annualized expected returns
- Annualized covariance matrix
- Correlation matrix
- Portfolio volatility

---

## Portfolio Optimization

The optimization engine shall provide deterministic portfolio optimization algorithms.

Implemented algorithms include:

- Mean-Variance Optimization
- Minimum Variance Portfolio
- Maximum Sharpe Portfolio
- Efficient Frontier Generation

Each optimization algorithm shall:

- operate independently of FastAPI
- operate independently of SQLAlchemy
- remain deterministic
- validate numerical inputs
- produce normalized portfolio allocations

---

# 8. Planned Functional Requirements

The following functionality is planned for future implementation.

## Monte Carlo Simulation

- Random portfolio generation
- Portfolio return estimation
- Portfolio volatility estimation
- Sharpe ratio computation
- Efficient frontier comparison

---

## Risk Analytics

- Sharpe Ratio
- Sortino Ratio
- Maximum Drawdown
- Historical Value-at-Risk
- Conditional Value-at-Risk

---

## Portfolio Health

- Diversification analysis
- Concentration analysis
- Portfolio health score
- Automated recommendations

---

## Frontend

A React-based frontend will provide:

- Authentication
- Dashboard
- Portfolio management
- Optimization visualization
- Monte Carlo visualization
- Risk analytics dashboard

---

## Deployment

Version 1 will conclude with production deployment including:

- Docker
- Docker Compose
- GitHub Actions
- Environment configuration
- Documentation
- Deployment guide

---

# 9. Non-Functional Requirements

The repository follows several non-functional engineering requirements.

## Maintainability

Code shall remain modular and readable.

Business logic shall remain independent of transport logic.

Mathematical computation shall remain independent of infrastructure.

---

## Testability

Every implemented feature shall include automated tests.

Financial engines shall be tested independently.

Services shall be tested independently.

REST APIs shall be tested independently.

Regression shall be minimized through comprehensive automated testing.

---

## Determinism

Financial engines shall produce deterministic outputs for identical numerical inputs.

Randomized algorithms shall support deterministic execution through configurable seeds where appropriate.

---

## Performance

Version 1 prioritizes correctness, readability, maintainability, and interview quality over premature optimization.

Performance improvements shall not compromise architectural clarity.

---

# 10. Technology Stack

OptiVest has been designed using technologies that are widely adopted in
modern backend software engineering and quantitative finance.

The technology choices prioritize readability, maintainability,
ecosystem maturity, and interview relevance.

---

## Backend

| Technology | Purpose |
|------------|---------|
| Python 3.12+ | Primary programming language |
| FastAPI | REST API framework |
| Pydantic v2 | Data validation and serialization |
| SQLAlchemy 2.x | ORM |
| PostgreSQL | Relational database |
| Alembic | Database migrations |
| Uvicorn | ASGI server |

---

## Financial Computing

| Technology | Purpose |
|------------|---------|
| NumPy | Numerical computation |
| Pandas | Financial time-series processing |
| CVXPY | Convex portfolio optimization |

---

## Security

| Technology | Purpose |
|------------|---------|
| python-jose | JWT Authentication |
| Passlib | Password hashing |
| bcrypt | Secure password hashing |

---

## Testing

| Technology | Purpose |
|------------|---------|
| pytest | Unit and integration testing |
| FastAPI TestClient | API testing |
| unittest.mock | Service mocking |

---

## Frontend (Planned)

Version 1 concludes with a React frontend.

Planned technologies include:

- React
- TypeScript
- Tailwind CSS
- Axios
- React Router
- Recharts

---

## Deployment (Planned)

Version 1 deployment includes:

- Docker
- Docker Compose
- GitHub Actions
- Environment configuration
- Production documentation

---

# 11. Software Architecture Summary

OptiVest follows a **Layered Modular Monolith** architecture.

Business logic, mathematical computation, persistence,
and transport responsibilities are intentionally isolated.

The architecture is designed to maximize:

- Maintainability
- Testability
- Extensibility
- Separation of Concerns

without introducing unnecessary enterprise abstractions.

The dependency direction is strictly controlled.

```text
Client

↓

FastAPI API Layer

↓

Service Layer

↓

Financial Engines

↓

Infrastructure
(Database / External APIs)
```

Each layer has clearly defined responsibilities.

---

## API Layer

Responsibilities include:

- HTTP request handling
- Request validation
- Response serialization
- Authentication
- Exception translation

The API layer **never performs business logic or financial calculations**.

---

## Service Layer

The Service Layer orchestrates application workflows.

Responsibilities include:

- Business validation
- Market data retrieval
- Financial Engine coordination
- Result aggregation

Services do **not** implement financial mathematics.

---

## Financial Engines

Financial Engines contain all mathematical computation.

Characteristics:

- Framework independent
- Database independent
- FastAPI independent
- Deterministic
- Fully testable

Each engine accepts strongly typed numerical inputs
and returns deterministic outputs.

---

## Infrastructure Layer

Infrastructure components include:

- Database
- External Market Data Providers
- Authentication
- Logging
- Configuration

Infrastructure never depends on Financial Engines.

---

# 12. Repository Structure

The repository is organized into independent modules.

```text
backend/

app/

api/

services/

financial_engines/

database/

schemas/

models/

core/

tests/

docs/
```

Each package has a single responsibility.

This organization minimizes coupling and encourages
incremental development.

---

# 13. Development Philosophy

The following engineering principles guide every implementation.

## Production First

Every feature is developed as if it were intended for
production deployment.

Placeholder implementations are not accepted.

---

## Layer Separation

Business logic belongs inside Services.

Financial computation belongs inside Financial Engines.

HTTP concerns belong inside API routes.

Persistence belongs inside Infrastructure.

---

## Deterministic Computation

Financial Engines produce deterministic results.

The same numerical inputs must always produce
the same outputs.

---

## Documentation Driven

Major architectural decisions are documented.

Documentation evolves together with the repository.

---

## Testing Driven Quality

Every completed feature includes:

- Financial Engine tests
- Service tests
- API tests

The repository maintains a passing test suite
before advancing to the next phase.

---

# 14. Version 1 Constraints

Version 1 intentionally avoids unnecessary complexity.

The following patterns are **not** introduced unless
they provide measurable value.

- Repository Pattern
- Generic CRUD abstractions
- Unit of Work
- Generic Managers
- Factory hierarchies
- Enterprise dependency injection frameworks

The objective is to maintain production-quality code
without over-engineering.

---

# 15. Development Roadmap

The project is implemented incrementally.

## Completed

### Phase 0

Repository Foundation

### Phase 1

Authentication

### Phase 2

Portfolio CRUD

### Phase 3

Market Data

### Phase 4

Portfolio Statistics

### Phase 5

Portfolio Optimization

- Financial Engine
- Optimization Service
- Schemas
- REST API
- API Tests

Current Status

```text
117 Passing Tests
```

---

## Upcoming

### Phase 6

Monte Carlo Simulation

### Phase 7

Risk Analytics

### Phase 8

Portfolio Health

### Phase 9

React Frontend

### Phase 10

Deployment and Productionization

---

# 16. Success Criteria

Version 1 will be considered complete when the repository provides:

- Secure authentication
- Portfolio management
- Historical market data
- Portfolio statistics
- Portfolio optimization
- Monte Carlo simulation
- Risk analytics
- Portfolio health assessment
- Interactive frontend
- Production deployment
- Comprehensive documentation
- Automated testing

---

# 17. Interview Discussion Topics

The repository is intentionally designed to support
technical interview discussions.

Software Engineering topics include:

- Layered architecture
- REST API design
- Clean code
- Dependency management
- Testing strategy
- Database integration
- Authentication
- Documentation

Quantitative Finance topics include:

- Modern Portfolio Theory
- Expected Returns
- Covariance Estimation
- Efficient Frontier
- Mean-Variance Optimization
- Maximum Sharpe Portfolio
- Monte Carlo Simulation
- Risk Metrics

Backend Engineering topics include:

- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL
- Service orchestration
- Financial engine isolation
- API serialization

---

# 18. Future Enhancements

Future versions of OptiVest may include:

- Factor models
- Black-Litterman optimization
- Portfolio rebalancing
- Transaction cost modelling
- Tax-aware optimization
- Multi-currency portfolios
- ESG scoring
- Alternative asset support
- Live market streaming
- Real-time portfolio monitoring

These enhancements are outside the scope of Version 1
but the current architecture has been designed to
support future expansion.

---

# 19. Conclusion

OptiVest is intended to demonstrate that quantitative finance software
can be developed using the same engineering discipline expected from
production backend systems.

The project emphasizes correctness, maintainability,
architectural consistency, and software quality rather than
maximizing the number of implemented features.

By separating Financial Engines from Services and REST APIs,
the repository remains modular, testable, and extensible.

Version 1 establishes a robust foundation for future work in
portfolio simulation, risk analytics, and interactive financial
visualization while serving as a strong demonstration of backend
software engineering and quantitative development skills.

---

**End of Document**

**Document:** 01_PROJECT_SPECIFICATION.md

**Version:** 1.0

**Repository Status:** Phase 5 Complete

**Current Test Status:** 117 Passing

**Next Planned Phase:** Phase 6 – Monte Carlo Simulation