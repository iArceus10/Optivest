# OptiVest

# Financial Engine

**Document Version:** 1.0

**Project Version:** Version 1

**Repository Status:** Phase 5 Complete

**Current Test Status:** 117 Passing

**Last Updated:** After Phase 5 Completion

---

# 1. Purpose

This document defines the design, implementation philosophy, and
mathematical responsibilities of the Financial Engine layer within
OptiVest.

The Financial Engine represents the quantitative core of the repository.

Unlike the API and Service layers, Financial Engines contain **only**
deterministic mathematical computation.

Every financial algorithm implemented within OptiVest belongs to this
layer.

---

# 2. Design Philosophy

Financial Engines are intentionally designed as pure computational
modules.

They receive validated numerical inputs, perform deterministic
calculations, and return immutable domain objects.

Financial Engines never:

- communicate with databases
- perform HTTP operations
- access authentication information
- serialize API responses
- read environment variables
- call external REST APIs

This isolation ensures correctness, reusability, and testability.

---

# 3. Engineering Principles

Every Financial Engine follows the same engineering principles.

## Framework Independence

Financial Engines must never depend on:

- FastAPI
- SQLAlchemy
- Pydantic
- JWT
- ORM Models

The only permitted dependencies are numerical and scientific computing
libraries.

Examples include:

- NumPy
- Pandas
- CVXPY

---

## Deterministic Behaviour

Identical numerical inputs must always produce identical outputs.

Financial Engines should never introduce randomness unless explicitly
requested.

Algorithms using randomness (such as Monte Carlo Simulation) must expose
a configurable random seed to ensure reproducibility.

---

## Stateless Computation

Financial Engines contain no mutable application state.

Every function behaves as a pure transformation.

```text
Input

↓

Mathematical Computation

↓

Output
```

No side effects are permitted.

---

## Strong Validation

Every engine validates numerical inputs before computation.

Validation prevents:

- empty datasets
- incompatible dimensions
- missing values
- invalid covariance matrices
- inconsistent asset labels

Validation occurs before any optimization or statistical calculation.

---

## Immutable Outputs

Whenever practical, Financial Engines return immutable domain models.

Examples include:

- EfficientFrontierPoint
- OptimizedPortfolio

Immutable outputs reduce accidental modification and improve
predictability.

---

# 4. Financial Engine Architecture

The Financial Engine layer consists of independent computational modules.

```text
Financial Engines

├── Market Data

├── Statistics

├── Optimization

├── Simulation (Planned)

└── Risk Analytics (Planned)
```

Each module has a clearly defined responsibility.

Modules communicate through typed numerical data rather than framework
objects.

---

# 5. Market Data Engine

The Market Data Engine transforms historical price data into numerical
datasets suitable for downstream financial analysis.

Responsibilities include:

- Daily return computation
- Return validation
- Annualization support
- Data preparation

The engine does **not** download market data.

External data retrieval is handled by MarketDataService.

This separation allows the computational logic to remain independent of
the chosen data provider.

---

## Inputs

Typical inputs include:

- Historical adjusted close prices
- Trading dates
- Asset tickers

---

## Outputs

The engine produces:

- Daily return matrices
- Annualized returns
- Clean numerical datasets

These outputs become inputs for the Statistics Engine.

---

# 6. Statistics Engine

The Statistics Engine derives statistical properties from historical
asset returns.

Its responsibilities include estimating expected performance and
quantifying relationships between assets.

---

## Implemented Components

### Expected Annual Returns

Computes annualized expected returns using daily historical returns.

Output:

```text
pd.Series
```

indexed by asset ticker.

---

### Annualized Covariance Matrix

Computes the covariance structure of asset returns.

Output:

```text
pd.DataFrame
```

representing the covariance matrix.

---

### Correlation Matrix

Measures pairwise linear relationships between assets.

Output:

```text
pd.DataFrame
```

representing the correlation matrix.

---

### Portfolio Volatility

Computes annualized portfolio volatility using

- portfolio weights
- covariance matrix

Output:

```text
float
```

representing annualized standard deviation.

---

## Validation

The Statistics Engine validates:

- sufficient observations
- missing values
- matrix dimensions
- numerical consistency

Only validated statistics are forwarded to higher layers.

---

# 7. Optimization Engine

The Optimization Engine implements Modern Portfolio Theory using convex
optimization.

The implementation is based on CVXPY and supports long-only,
fully-invested portfolios.

The engine is entirely independent of FastAPI, SQLAlchemy, and external
services.

---

## Shared Utilities

The optimization package contains shared utilities that eliminate
duplication across optimization algorithms.

Examples include:

- optimization variable creation
- constraint construction
- convex solver execution
- common validation

Shared utilities improve maintainability while preserving mathematical
clarity.

---

## Numerical Validation

Before solving any optimization problem, inputs are validated.

Validation includes:

- expected return vector
- covariance matrix
- asset label consistency
- positive semidefinite covariance matrices

Invalid numerical inputs immediately produce descriptive exceptions.

---

## Mean-Variance Optimization

Objective:

Maximize expected return while penalizing portfolio variance.

Optimization problem:

```text
maximize

μᵀw − λ wᵀΣw
```

Subject to:

```text
Σ w = 1

w ≥ 0
```

where:

- μ = expected returns
- Σ = covariance matrix
- λ = risk aversion coefficient

Output:

```text
pd.Series
```

containing normalized portfolio weights.

---

## Minimum Variance Portfolio

Objective:

Construct the portfolio with the smallest possible variance while
remaining fully invested.

Optimization problem:

```text
minimize

wᵀΣw
```

Subject to:

```text
Σ w = 1

w ≥ 0
```

The resulting portfolio minimizes risk regardless of expected return.

---

## Maximum Sharpe Portfolio

Objective:

Maximize the Sharpe Ratio.

The optimization uses a convex reformulation suitable for numerical
optimization.

Inputs include:

- expected returns
- covariance matrix
- risk-free rate

Output:

Normalized portfolio allocations maximizing risk-adjusted performance.

---

## Efficient Frontier

The Efficient Frontier represents portfolios offering the maximum
expected return for a given level of risk.

Implementation characteristics:

- multiple target returns
- repeated convex optimization
- deterministic ordering
- immutable domain outputs

Each point on the frontier is represented by an
`EfficientFrontierPoint` domain model.

---

# 8. Domain Models

The Financial Engine exposes immutable domain models to represent the
results of quantitative computations.

Domain models are independent of:

- FastAPI
- SQLAlchemy
- Pydantic
- ORM entities
- REST APIs

They provide a stable interface between the Financial Engine and the
Service Layer.

---

## OptimizedPortfolio

The `OptimizedPortfolio` model represents the result of an optimization
algorithm.

It contains:

- Expected annual return
- Annualized portfolio volatility
- Portfolio allocation weights

This model provides a complete mathematical description of an optimized
portfolio.

---

## EfficientFrontierPoint

The `EfficientFrontierPoint` model represents a single portfolio on the
Efficient Frontier.

Each instance contains:

- Expected return
- Portfolio volatility
- Portfolio allocation weights

A sequence of `EfficientFrontierPoint` objects forms the complete
Efficient Frontier.

Using immutable domain models prevents accidental modification of
optimization results while improving clarity throughout the repository.

---

# 9. Numerical Stability

Financial software must produce reliable numerical results.

The Financial Engine therefore applies several safeguards before and
after numerical computation.

Examples include:

- Covariance matrix symmetry validation
- Positive semidefinite covariance validation
- Removal of insignificant floating-point noise
- Validation of optimization solver status
- Verification of solver output

Very small floating-point values are rounded to zero when they represent
numerical artifacts rather than meaningful portfolio allocations.

These safeguards improve reproducibility and make API responses easier
to interpret.

---

# 10. Validation Philosophy

Validation is considered an essential part of every Financial Engine.

Rather than allowing numerical libraries to fail with obscure error
messages, OptiVest validates inputs before computation begins.

Validation responsibilities include:

## Market Data

- Empty datasets
- Missing values
- Invalid trading history

---

## Statistics

- Empty return matrices
- Missing observations
- Dimension consistency

---

## Optimization

- Expected return vector validation
- Covariance matrix validation
- Asset label consistency
- Positive semidefinite covariance matrices
- Minimum asset count

Validation failures produce descriptive exceptions that can be translated
into meaningful API responses by higher architectural layers.

---

# 11. Error Handling Strategy

Financial Engines communicate failures through standard Python
exceptions.

Typical examples include:

```python
raise ValueError("Expected returns cannot be empty.")
```

or

```python
raise ValueError("Covariance matrix must be positive semidefinite.")
```

The Financial Engine never raises HTTP-specific exceptions.

This ensures complete independence from the transport layer.

Error translation occurs exclusively within the API layer.

---

# 12. Service Integration

Financial Engines are not called directly by REST endpoints.

Instead, every request follows the same execution path.

```text
HTTP Request

↓

API Endpoint

↓

Application Service

↓

Financial Engine

↓

Application Service

↓

HTTP Response
```

This separation provides several advantages:

- Cleaner APIs
- Better testing
- Easier maintenance
- Reusable mathematical code
- Framework independence

The Service Layer is responsible for:

- Preparing Financial Engine inputs
- Calling Financial Engines
- Combining multiple computations
- Returning domain results

---

# 13. Planned Monte Carlo Simulation Engine

Phase 6 introduces the Monte Carlo Simulation Engine.

Responsibilities include:

- Random portfolio generation
- Weight normalization
- Portfolio return computation
- Portfolio volatility computation
- Sharpe ratio computation
- Best Sharpe portfolio identification
- Minimum volatility portfolio identification

The Monte Carlo Engine will consume:

- Expected annual returns
- Annualized covariance matrices

provided by the Statistics Engine.

Randomness will be deterministic when a fixed seed is supplied,
ensuring reproducible simulations during testing.

---

# 14. Planned Risk Analytics Engine

Phase 7 introduces advanced portfolio risk analysis.

Planned metrics include:

- Sharpe Ratio
- Sortino Ratio
- Maximum Drawdown
- Historical Value-at-Risk (VaR)
- Conditional Value-at-Risk (CVaR)

Each metric will be implemented as an independent computational
function.

Risk metrics will consume numerical outputs from the Statistics Engine
and remain completely independent of FastAPI and database components.

---

# 15. Testing Strategy

Financial Engines receive the highest level of testing within the
repository.

Each engine is tested independently from Services and REST APIs.

Testing focuses on:

- Mathematical correctness
- Numerical stability
- Validation logic
- Edge cases
- Deterministic outputs
- Error handling

Optimization algorithms additionally verify:

- Weight normalization
- Constraint satisfaction
- Solver correctness
- Portfolio feasibility

Service and API tests do **not** duplicate Financial Engine tests.

Instead, they verify orchestration and transport behavior.

This separation minimizes duplicated test logic while maintaining high
confidence in correctness.

---

# 16. Design Decisions

The following decisions define the Financial Engine architecture.

### Framework Independence

Financial computation must remain reusable outside FastAPI.

---

### Deterministic Algorithms

Repeated execution with identical inputs must produce identical outputs.

---

### Immutable Results

Optimization outputs are represented using immutable domain models.

---

### Validation Before Computation

Invalid numerical inputs are rejected before optimization or statistical
calculation begins.

---

### Shared Utilities

Common optimization logic is centralized into shared helper modules to
eliminate duplication while preserving readability.

---

### Frozen Financial Engines

Once a Financial Engine has been validated and fully tested, it becomes
functionally frozen.

Subsequent repository development should extend higher architectural
layers rather than modifying established mathematical implementations.

Changes to a frozen Financial Engine should occur only when a verified
correctness defect is identified.

This policy minimizes regression risk and preserves confidence in
previously validated algorithms.

---

# 17. Summary

The Financial Engine is the quantitative foundation of OptiVest.

Its strict separation from application infrastructure ensures that
financial computation remains deterministic, reusable, maintainable, and
fully testable.

By organizing Market Data, Statistics, Optimization, and future
Simulation and Risk Analytics modules into independent computational
packages, the repository achieves a clean separation between software
engineering concerns and financial mathematics.

This architecture enables the repository to evolve through future phases
without compromising correctness or introducing unnecessary coupling,
providing a robust foundation for advanced portfolio analytics.

---

**End of Document**

**Document:** 03_FINANCIAL_ENGINE.md

**Version:** 1.0

**Repository Status:** Phase 5 Complete

**Financial Engines Implemented:**
- Market Data
- Statistics
- Portfolio Optimization

**Financial Engines Planned:**
- Monte Carlo Simulation
- Risk Analytics

**Current Test Status:** 117 Passing

**Next Planned Phase:** Phase 6 – Monte Carlo Simulation