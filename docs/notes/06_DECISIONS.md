# OptiVest – Engineering Decisions

Version: 1.0

---

## Decision 001

### Title

Modular Monolith Architecture

### Decision

Use a layered modular monolith instead of microservices.

### Reason

* Simpler deployment
* Easier debugging
* Appropriate project scale
* Clear separation of concerns
* Easy future migration if required

---

## Decision 002

### Title

FastAPI

### Decision

Backend framework is FastAPI.

### Reason

* Automatic OpenAPI documentation
* Strong typing
* High performance
* Excellent developer experience

---

## Decision 003

### Title

React + TypeScript

### Reason

* Type safety
* Component reusability
* Industry adoption

---

## Decision 004

### Title

PostgreSQL

### Reason

* Relational data model
* ACID compliance
* Excellent SQL support
* Suitable for portfolio data

---

## Decision 005

### Title

CVXPY

### Reason

Portfolio optimization is a convex optimization problem.

CVXPY provides reliable optimization solvers while remaining mathematically transparent.

---

## Decision 006

### Title

Monte Carlo Portfolio Count

### Decision

50,000 portfolios

### Reason

* Fast execution
* Good visualization
* Statistically sufficient
* Easy to scale later

---

## Decision 007

### Title

Financial Data Source

### Decision

Yahoo Finance via yfinance

### Reason

* Free
* Reliable for educational purposes
* Historical data available
* Simple integration

---

# Future Decisions

Every major architectural, financial, or engineering choice should be appended here with:

* Decision
* Reason
* Alternatives Considered
* Trade-offs
