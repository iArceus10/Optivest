# 05_PROJECT_STATE.md

# OptiVest Project State

**Version:** 1.0

**Project:** OptiVest – Portfolio Optimization & Risk Analytics Platform

**Current Phase:** Phase 2 – Portfolio Domain Foundation (Ready to Begin)

**Last Completed Phase:** Phase 1 – Authentication

**Status:** Stable

---

# 1. Executive Summary

OptiVest is a production-quality fintech platform being developed for IIT campus placements.

Primary goals:

* Production-quality software engineering
* Quantitative finance implementation
* Interview-defensible architecture
* Clean layered modular monolith
* High code quality
* Maintainability
* Extensibility

The project intentionally avoids unnecessary abstractions during Version 1 while maintaining production engineering practices.

---

# 2. Overall Roadmap

## Phase 0 – Foundation

Status

✅ Complete

Completed

* Repository Foundation
* FastAPI Initialization
* Configuration Management
* Structured Logging
* API Routing
* SQLAlchemy Integration
* Alembic Configuration
* Database Session Management

---

## Phase 1 – Authentication

Status

✅ Complete

Completed

* User ORM
* User Migration
* Registration
* Login
* Password Hashing (bcrypt)
* JWT Authentication
* OAuth2PasswordBearer
* Current User Dependency
* Protected Endpoint (/auth/me)
* Security Tests
* API Integration Tests
* Shared Test Infrastructure

---

## Phase 2 – Portfolio Management

Status

⏳ Ready to Begin

---

## Future Phases

⏳ Market Data

⏳ Portfolio Analytics

⏳ Optimization Engine

⏳ Risk Analytics

⏳ Monte Carlo Simulation

⏳ Reporting

⏳ Frontend

---

# 3. Repository Status

backend/

app/

api/

dependencies/

✔ auth.py

v1/

✔ auth.py

✔ health.py

✔ root.py

core/

✔ config.py

✔ logging.py

✔ security.py

database/

✔ base.py

✔ session.py

models/

✔ user.py

⬜ portfolio.py

schemas/

✔ auth.py

⬜ portfolio.py

services/

✔ auth_service.py

⬜ portfolio_service.py

financial_engines/

⬜ Empty

tests/

✔ conftest.py

✔ test_security.py

✔ test_auth_api.py

---

# 4. Authentication Module

Status

✅ Production Ready

Features

* Password hashing using bcrypt
* Password verification
* JWT Access Tokens
* JWT Validation
* Email normalization
* Transaction rollback
* OAuth2 Bearer Authentication
* Protected Routes

Authentication Flow

Register

↓

Hash Password

↓

Store User

↓

Login

↓

Verify Password

↓

Generate JWT

↓

Bearer Token

↓

Protected API

---

# 5. API Inventory

Health

GET /health

Status

✅

Root

GET /

Status

✅

Authentication

POST /api/v1/auth/register

Status

✅

POST /api/v1/auth/login

Status

✅

GET /api/v1/auth/me

Status

✅

Portfolio

Not Started

---

# 6. Database Status

Current Tables

users

Fields

* id
* email
* full_name
* hashed_password
* is_active
* created_at
* updated_at

Pending Tables

portfolio

portfolio_holdings

assets

transactions

market_prices

---

# 7. Testing Status

Infrastructure

✔ pytest configured

✔ conftest.py

✔ isolated SQLite test database

✔ dependency overrides

Security Tests

✔ Password Hash

✔ Password Verify

✔ JWT Create

✔ JWT Decode

Result

5 / 5 Passing

Authentication Tests

✔ Register

✔ Duplicate Register

✔ Login

✔ Wrong Password

✔ Protected Route

✔ Invalid Token

Result

6 / 6 Passing

Current Total

11 Passing Tests

---

# 8. Engineering Decisions

Decision 1

Layered Modular Monolith

Status

Accepted

Decision 2

No Repository Pattern

Status

Accepted

Decision 3

Business Logic inside Services

Status

Accepted

Decision 4

JWT stores immutable User UUID

Status

Accepted

Decision 5

Authentication dependency implemented using OAuth2PasswordBearer

Status

Accepted

Decision 6

Shared pytest fixtures via conftest.py

Status

Accepted

Decision 7

SQLite isolated test database for API tests

Status

Accepted

---

# 9. Known Limitations

Not Implemented

* Refresh Tokens
* Role-Based Authorization
* Password Reset
* Email Verification
* Multi-Factor Authentication

Reason

Deferred to Version 2.

---

# 10. Current Code Quality

Architecture

★★★★★

Readability

★★★★★

Testing

★★★★★

Maintainability

★★★★★

Interview Readiness

★★★★★

---

# 11. Next Phase

Phase 2

Portfolio Domain Foundation

To Implement

* Portfolio ORM
* Portfolio Schemas
* Portfolio Service
* Portfolio CRUD APIs
* Alembic Migration
* Portfolio Tests

No optimization logic.

No financial calculations.

No market data.

No analytics.

Only Portfolio CRUD.

---

# 12. Development Checklist

Completed

✅ Foundation

✅ Authentication

Pending

⬜ Portfolio CRUD

⬜ Asset Model

⬜ Holdings

⬜ Portfolio Analytics

⬜ Efficient Frontier

⬜ Risk Metrics

⬜ Monte Carlo

⬜ Reporting

⬜ Frontend

---

END OF STATE
