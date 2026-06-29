# 06_DECISIONS.md

# OptiVest Engineering Decisions

**Version:** 1.1

**Last Updated:** 29 June 2026

---

# Purpose

This document records the architectural and engineering decisions accepted throughout the development of OptiVest.

These decisions are considered part of the project's architecture and should not be changed unless a compelling engineering reason exists.

---

# Decision 001

## Architecture

**Accepted**

OptiVest follows a **Layered Modular Monolith Architecture**.

```
FastAPI

↓

API Layer

↓

Service Layer

↓

Financial Engines

↓

Database / External APIs
```

### Reason

- Simple deployment
- Low operational complexity
- High maintainability
- Easy debugging
- Future migration to microservices remains possible

---

# Decision 002

## Business Logic Placement

Business logic belongs exclusively inside the **Service Layer**.

Services own

- workflow
- orchestration
- validation
- business rules
- database interaction

Business logic must never exist inside API routes.

---

# Decision 003

## Mathematical Logic Placement

All quantitative finance and statistical algorithms belong exclusively inside **Financial Engines**.

Financial Engines must never depend on

- FastAPI
- SQLAlchemy
- Pydantic
- Database Models

Financial Engines remain deterministic computational libraries.

---

# Decision 004

## Framework Independence

Financial Engines depend only upon

- Python
- NumPy
- Pandas

They must remain reusable in

- CLI tools
- notebooks
- batch jobs
- future services

---

# Decision 005

## API Responsibilities

API routes are responsible only for

- request parsing
- authentication
- calling services
- serialization
- HTTP exception translation

APIs never contain business logic or mathematical calculations.

---

# Decision 006

## Service Responsibilities

Services coordinate

- workflow
- validation
- database interaction
- Financial Engine invocation

Services never perform financial mathematics.

---

# Decision 007

## Version 1 Simplicity

Version 1 intentionally excludes

- Repository Pattern
- Unit of Work
- Interfaces
- Managers
- Generic CRUD
- Generic Services
- Factory Pattern

The project follows the **Rule of Three** before introducing abstractions.

---

# Decision 008

## Internal Financial Representation

Financial Engines communicate using

- Pandas DataFrames
- Pandas Series
- NumPy arrays

These remain internal implementation details.

API responses never expose them directly.

---

# Decision 009

## Serialization

Serialization from

```
DataFrame / Series

↓

JSON
```

occurs only inside the API layer.

This preserves framework independence of lower layers.

---

# Decision 010

## Market Data Provider

Version 1 uses

Yahoo Finance (`yfinance`)

Reason

- free
- reliable
- educational
- widely adopted

Future providers should be replaceable without changing Services or Financial Engines.

---

# Decision 011

## Historical Prices

Adjusted Close prices are used for all return calculations.

Reason

Adjusted Close correctly incorporates

- stock splits
- dividends
- corporate actions

---

# Decision 012

## Multi-Asset API

Market Data endpoints accept multiple ticker symbols.

Example

```
AAPL,MSFT,NVDA
```

Reason

Portfolio analytics naturally operate on multiple assets simultaneously.

---

# Decision 013

## Validation Strategy

Validation responsibilities are separated.

Financial Engines

- numerical validation
- mathematical assumptions

Services

- business validation
- dates
- ticker normalization

API

- request validation
- HTTP responses

---

# Decision 014

## Error Handling

Financial Engines

Raise Python exceptions.

Services

Raise Python exceptions.

API

Translates exceptions into HTTP responses.

Framework-specific exceptions never propagate into lower layers.

---

# Decision 015

## Testing Philosophy

Each architectural layer is tested independently.

Financial Engines

- mathematical correctness

Services

- orchestration
- validation

API

- HTTP behavior
- serialization
- status codes

---

# Decision 016

## External Dependencies

External APIs are always mocked during testing.

Automated tests never perform network requests.

---

# Decision 017

## Development Workflow

Every feature follows

```
Design

↓

Implementation

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

---

# Decision 018

## Dependency Installation

Always install packages using

```
python -m pip install ...
```

Never rely on

```
pip install ...
```

to avoid virtual environment ambiguity.

---

# Decision 019

## Project Philosophy

Production quality takes priority over development speed.

The repository should be suitable for

- IIT placements
- Software Engineering interviews
- Quantitative Finance interviews
- long-term maintainability

---

# Decision 020

## Statistics Package

A dedicated

```
financial_engines/statistics/
```

package has been introduced.

Implemented modules

- expected_returns.py
- covariance.py
- correlation.py
- volatility.py
- validation.py

Reason

Separates statistical algorithms from market data retrieval and prepares the mathematical foundation for portfolio optimization.

---

# Decision 021

## Shared Statistics Validation

Return matrix validation has been centralized into

```
statistics/validation.py
```

Reason

Validation logic appeared in three statistical engines.

The abstraction was introduced only after satisfying the Rule of Three.

---

# Decision 022

## Expected Returns

Expected return is computed as

```
Mean Daily Return × 252
```

Reason

This follows the standard historical annualization approach used in portfolio analytics.

The engine returns a **Series**, not a scalar, allowing direct use in optimization algorithms.

---

# Decision 023

## Covariance Matrix

The covariance engine provides

- daily covariance
- annualized covariance

Reason

Portfolio optimization operates directly on the covariance matrix.

Annualization occurs inside the Financial Engine to avoid duplication elsewhere.

---

# Decision 024

## Correlation Matrix

Correlation is implemented independently from covariance.

Reason

Although optimization depends on covariance, correlation is essential for

- diversification analysis
- visualization
- portfolio diagnostics

---

# Decision 025

## Portfolio Volatility

Portfolio volatility is calculated using

```
σ = √(wᵀΣw)
```

where

- w = portfolio weights
- Σ = annualized covariance matrix

Reason

This is the standard Modern Portfolio Theory formulation.

---

# Decision 026

## Numerical Stability

Portfolio variance is clamped to zero when extremely small negative values arise from floating-point precision.

Example

```
-2e-16
```

↓

```
0
```

Reason

Prevents invalid square-root operations while still rejecting genuinely invalid covariance matrices.

---

# Decision 027

## Weight Validation

Portfolio weight validation currently remains inside

```
volatility.py
```

Reason

Only one engine currently requires this validation.

A shared helper will not be introduced until the Rule of Three is satisfied during the optimization phase.

---

# Decision 028

## Statistics Engine Output Types

The Statistics Engine returns

Expected Returns

→ Pandas Series

Covariance

→ Pandas DataFrame

Correlation

→ Pandas DataFrame

Volatility

→ float

Reason

Each output naturally matches its mathematical representation while remaining easy for the Service Layer to consume.

---

# Decision 029

## Financial Engine Completion Order

Financial Engines are implemented before Services.

Services before APIs.

APIs before integration tests.

Reason

This minimizes debugging complexity and ensures higher layers depend on stable lower layers.

---

Decision 030
Statistics Service

StatisticsService is responsible only for orchestration.

Responsibilities

Retrieve daily returns
Invoke Statistics Financial Engine
Perform business validation

StatisticsService never performs mathematical calculations.

Reason

Maintains strict separation between orchestration and quantitative finance algorithms.

Decision 031
Statistics Serialization

Statistics Financial Engines communicate internally using

Pandas DataFrames
Pandas Series

Serialization into JSON occurs exclusively inside the API layer using dedicated response schemas.

Reason

Preserves framework independence of Financial Engines while exposing stable API contracts.

Decision 032
Portfolio Volatility Engine Interface

The Portfolio Volatility engine accepts

Daily Returns

rather than a covariance matrix.

The engine internally computes the annualized covariance matrix before calculating volatility.

Reason

Encapsulates covariance computation.
Avoids duplication across services.
Provides a simpler and more cohesive public API for future Optimization and Monte Carlo modules.

# Current Accepted Architecture

```
FastAPI

↓

API Layer

↓

Service Layer

↓

Financial Engines

↓

Database / External APIs
```

No accepted decision currently violates this architecture.

---

# Future Reserved Decisions

The following phases will introduce additional engineering decisions.

Phase 5

- Optimization Engine
- Efficient Frontier
- CVXPY integration

Phase 6

- Monte Carlo Simulation
- Random Portfolio Generation

Phase 7

- Sharpe Ratio
- Sortino Ratio
- VaR
- CVaR
- Maximum Drawdown

Phase 8

- Backtesting
- Benchmark Comparison

Future decisions should extend this document without modifying previously accepted architecture unless absolutely necessary.

## 06_DECISIONS.md

# Phase 5 Decisions

## Optimization Package Introduced

A dedicated optimization package was introduced under the Financial Engine.

```
financial_engines/
    optimization/
```

This isolates portfolio optimization from market data and statistics while preserving framework independence.

---

## Shared Optimization Infrastructure

A private `_base.py` module centralizes:

* CVXPY variable creation
* Constraint creation
* Optimization solving
* Numerical cleanup

This avoids duplicated optimization code across multiple optimizers.

---

## Constraint Composition

Constraints are now composed rather than hardcoded.

Separate helpers exist for:

* Fully Invested
* Long Only

This allows different optimizers to reuse only the constraints they require.

---

## Framework Independence

Optimization engines remain completely independent of:

* FastAPI
* SQLAlchemy
* Pydantic

They operate purely on NumPy, Pandas, and CVXPY objects.

---

## Maximum Sharpe Formulation

Maximum Sharpe is implemented using a convex reformulation rather than direct fractional optimization.

Reasons:

* DCP compliant
* Numerically stable
* Industry standard
* Compatible with CVXPY

---

## Efficient Frontier Domain Model

Efficient Frontier returns immutable domain objects:

```
EfficientFrontierPoint
```

instead of dictionaries.

Reasons:

* Strong typing
* Better readability
* Easier future extension
* Cleaner service layer

---

## Efficient Frontier Implementation

Efficient Frontier generation uses:

* Internal helper for a single frontier point
* Configurable frontier size
* Numerical safeguards
* Non-decreasing target returns

---

## Solver Selection

Solver selection is delegated to CVXPY.

The project intentionally uses:

```python
problem.solve()
```

instead of forcing a specific solver.

Reason:

The optimization package now contains both:

* Quadratic Programs (QP)
* Quadratically Constrained Programs (QCQP)

Automatic solver selection correctly dispatches to an appropriate solver.

---

## Testing Philosophy

Optimization tests validate mathematical invariants rather than exact numerical solutions.

Tests verify:

* Asset ordering
* Long-only constraints
* Fully invested portfolios
* Deterministic behaviour
* Numerical validity

This avoids brittle solver-specific tests while ensuring mathematical correctness.

---

## Current Architecture

The layered architecture remains unchanged.

```
API

↓

Services

↓

Financial Engines

↓

Database
```

Financial Engines continue to contain all quantitative finance logic.

Services remain orchestration and business logic only.

APIs remain HTTP-only.

This separation will continue through the remaining phases.
