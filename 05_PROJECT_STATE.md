# 05_PROJECT_STATE.md

# OptiVest Project State

**Last Updated:** 29 June 2026

---

# Project Overview

OptiVest is a production-quality Portfolio Optimization & Risk Analytics platform built using FastAPI and React.

The project is intentionally engineered to demonstrate:

- Production-quality software engineering
- Quantitative finance
- Clean architecture
- Financial correctness
- Maintainability
- Interview readiness

The primary goal is to build an application suitable for:

- IIT campus placements
- Software Engineering interviews
- Quantitative Finance interviews
- FinTech roles

The backend follows a **Layered Modular Monolith Architecture**.

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

The project follows strict separation of concerns.

- APIs own HTTP.
- Services own business logic.
- Financial Engines own mathematics.
- Database owns persistence.

---

# Current Status

## Overall Progress

| Phase | Status |
|--------|--------|
| Phase 0 — Foundation | ✅ Complete |
| Phase 1 — Authentication | ✅ Complete |
| Phase 2 — Portfolio CRUD | ✅ Complete |
| Phase 3 — Market Data Foundation | ✅ Complete |
| Phase 4 — Portfolio Statistics Foundation | 🚧 In Progress |

---

# Phase 4 Progress

## Completed

### Financial Engine

- [x] Statistics package
- [x] Expected Returns Engine
- [x] Covariance Matrix Engine
- [x] Correlation Matrix Engine
- [x] Portfolio Volatility Engine
- [x] Statistics Validation Helpers

### Testing

- [x] Expected Returns tests
- [x] Covariance tests
- [x] Correlation tests
- [x] Portfolio Volatility tests

## Remaining

### Application Layer

- [ ] Statistics Service
- [ ] Statistics Schemas
- [ ] Statistics API
- [ ] Router registration

### Testing

- [ ] Statistics Service Tests
- [ ] Statistics API Tests

### Documentation

- [ ] Phase 4 completion update
- [ ] Git checkpoint

---

# Completed Phases

---

# Phase 0

## Project Foundation

Completed

- FastAPI application
- Environment configuration
- Configuration management
- Logging
- SQLAlchemy setup
- PostgreSQL integration
- Alembic migrations
- Root endpoint
- Health endpoint
- Swagger configuration

---

# Phase 1

## Authentication

Completed

- User model
- Password hashing
- JWT Authentication
- Registration
- Login
- Protected routes
- Authentication dependencies
- Authentication Service
- Security utilities

Testing

- Authentication API tests
- Security tests

---

# Phase 2

## Portfolio CRUD

Completed

- Portfolio model
- Portfolio schemas
- Portfolio Service
- Portfolio API
- Create portfolio
- Read portfolio
- Update portfolio
- Delete portfolio
- Ownership validation

Testing

- Portfolio API tests

---

# Phase 3

## Market Data Foundation

### Financial Engine

Completed

- Yahoo Finance integration
- Historical adjusted close retrieval
- Market data validation
- Daily returns calculation
- Annualization utilities

### Service Layer

Completed

- MarketDataService
- Business validation
- Ticker normalization
- Date validation

### API

Completed

- Historical prices endpoint
- Daily returns endpoint
- Response schemas
- DataFrame serialization
- HTTP error translation

### Testing

Completed

- Market Data Engine tests
- Returns tests
- Validation tests
- Annualization tests
- Service tests
- API tests

---

# Phase 4

## Portfolio Statistics Foundation

### Financial Engine

Completed

```
statistics/

__init__.py
validation.py
expected_returns.py
covariance.py
correlation.py
volatility.py
```

Implemented

- Expected annual returns
- Annualized covariance matrix
- Correlation matrix
- Portfolio volatility
- Shared return validation

### Mathematical Features

Implemented

- Mean daily returns
- Annualized expected returns
- Daily covariance matrix
- Annualized covariance matrix
- Pearson correlation matrix
- Portfolio volatility using

```
σ = √(wᵀΣw)
```

### Numerical Validation

Implemented

- Empty datasets
- Insufficient observations
- NaN handling
- Numeric validation
- Weight validation
- Matrix compatibility checks
- Numerical stability for floating-point precision

### Testing

Completed

- Expected Returns tests
- Covariance tests
- Correlation tests
- Portfolio Volatility tests

---

# Current Backend Structure

```
backend/

app/

├── api/
│   ├── dependencies/
│   └── v1/
│       ├── auth.py
│       ├── health.py
│       ├── market_data.py
│       ├── portfolio.py
│       ├── root.py
│       └── router.py
│
├── core/
│   ├── config.py
│   ├── logging.py
│   └── security.py
│
├── database/
│   ├── base.py
│   └── session.py
│
├── financial_engines/
│   ├── market_data/
│   │   ├── annualization.py
│   │   ├── market_data_engine.py
│   │   ├── returns.py
│   │   └── validation.py
│   │
│   └── statistics/
│       ├── __init__.py
│       ├── correlation.py
│       ├── covariance.py
│       ├── expected_returns.py
│       ├── validation.py
│       └── volatility.py
│
├── models/
│   ├── portfolio.py
│   └── user.py
│
├── schemas/
│   ├── auth.py
│   ├── market_data.py
│   └── portfolio.py
│
├── services/
│   ├── auth_service.py
│   ├── market_data_service.py
│   └── portfolio_service.py
│
└── main.py

tests/

├── financial_engines/
│   ├── market_data/
│   └── statistics/
│       ├── test_expected_returns.py
│       ├── test_covariance.py
│       ├── test_correlation.py
│       └── test_volatility.py
│
├── conftest.py
├── test_auth_api.py
├── test_market_data_api.py
├── test_portfolio_api.py
└── test_security.py
```

---

# Architecture Status

## API Layer

Completed

- Authentication
- Portfolio
- Market Data

Pending

- Statistics
- Optimization
- Simulation
- Risk

---

## Service Layer

Completed

- AuthService
- PortfolioService
- MarketDataService

Pending

- StatisticsService
- OptimizationService
- SimulationService
- RiskAnalyticsService

---

## Financial Engines

Completed

### Market Data

- Historical prices
- Daily returns
- Annualization
- Validation

### Statistics

- Expected returns
- Covariance
- Correlation
- Portfolio volatility

Pending

- Optimization
- Monte Carlo
- Risk Analytics
- Backtesting

---

# Testing Status

Current Passing Tests

```
50 Passed
0 Failed
```

Coverage includes

- Authentication
- Security
- Portfolio CRUD
- Market Data Engine
- Statistics Engine
- Market Data API
- Annualization
- Validation
- Returns

---

# Accepted Engineering Decisions

Current repository follows

- Layered Modular Monolith
- Framework-independent Financial Engines
- Services own business logic
- APIs remain thin
- DataFrames are internal financial representations
- API layer performs serialization
- External APIs mocked during testing
- Mathematical engines remain deterministic

---

# Version 1 Constraints

The following are intentionally NOT implemented

- Repository Pattern
- Unit of Work
- Interfaces
- Managers
- Generic CRUD
- Generic Services
- Factory Pattern

The project follows the Rule of Three before introducing abstractions.

---

# Current Development Workflow

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

No feature is considered complete until every step succeeds.

---

# Git Checkpoint

Current recommended commit

```
feat(statistics): implement portfolio statistics financial engine
```

---

# Immediate Next Objective

Complete the remaining Phase 4 application layer.

Implement

- StatisticsService
- Statistics response schemas
- Statistics API
- Statistics router registration
- Service tests
- API tests

Target

```
60+ Passing Tests
```

---

# Future Roadmap

## Phase 5

Portfolio Optimization

- Mean-Variance Optimization
- Efficient Frontier
- Maximum Sharpe Portfolio
- Minimum Variance Portfolio

---

## Phase 6

Monte Carlo Simulation

- Random portfolio generation
- Portfolio visualization
- Efficient Frontier comparison

---

## Phase 7

Risk Analytics

- Sharpe Ratio
- Sortino Ratio
- Maximum Drawdown
- Historical VaR
- Historical CVaR

---

## Phase 8

Backtesting

- Portfolio performance
- Benchmark comparison
- Rolling statistics

---

# Long-Term Vision

Phase 4 establishes the complete statistical foundation required for:

- Portfolio Optimization
- Efficient Frontier
- Monte Carlo Simulation
- Risk Analytics

No refactoring of the Financial Engine should be required in future phases.