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

# Decision 033 — Monte Carlo Simulation Reuses Statistics Engine

The Monte Carlo Simulation Engine consumes expected annual returns and
annualized covariance matrices produced by the Statistics Engine.

The Simulation Engine does not recompute these statistical quantities.

### Reason

Expected returns and covariance estimation are reusable statistical
computations already owned by the Statistics Engine.

Reusing these outputs avoids duplicated financial calculations while
preserving clear separation between statistical estimation and portfolio
simulation.

---

# Decision 034 — Deterministic Monte Carlo Simulation

The Monte Carlo Simulation Engine exposes an optional random seed.

When a seed is supplied, identical numerical inputs produce identical
simulation outputs.

### Reason

Deterministic execution improves reproducibility, simplifies automated
testing, and enables consistent financial analysis.

---

# Decision 035 — Monte Carlo Domain Models

Monte Carlo simulation results are represented using immutable domain
models.

Examples include:

- MonteCarloPortfolio
- MonteCarloSimulationResult

### Reason

Immutable objects provide a stable interface between the Financial
Engine and higher architectural layers while preventing accidental
modification of simulation results.

---

# Decision 036 — Simulation Service Responsibilities

SimulationService performs:

- Market data retrieval
- Statistics Engine coordination
- Monte Carlo Financial Engine orchestration

SimulationService performs no financial calculations.

# Decision 037 — Risk Analytics Reuses Historical Returns

The Risk Analytics Financial Engine operates on historical portfolio
return series.

Historical market data retrieval remains the responsibility of the
Service layer.

### Reason

Separates business orchestration from deterministic financial
computation while keeping the Financial Engine framework-independent.

# Decision 038 — Unified Risk Analytics Interface

The Risk Analytics Financial Engine exposes a single public function that
returns all supported portfolio risk metrics through an immutable domain
model.

### Reason

Provides a stable Financial Engine interface while preventing Services
from orchestrating individual mathematical algorithms.

# Decision 039 — Immutable Risk Domain Model

Risk analytics results are represented using the immutable
RiskAnalyticsResult domain model.

### Reason

Immutable objects provide a stable interface between the Financial
Engine and higher architectural layers while preventing accidental
modification of computed risk metrics.

# Decision 040 — Risk Service Responsibilities

RiskAnalyticsService performs:

- market data retrieval
- portfolio return preparation
- Financial Engine orchestration

RiskAnalyticsService performs no financial calculations.

### Reason

Business orchestration belongs to Services while financial computation
remains isolated within Financial Engines.

# Decision 041 — Risk API Responsibilities

Risk Analytics endpoints perform only:

- request validation
- Service delegation
- response serialization
- exception translation

### Reason

REST APIs remain transport layers and contain no business or financial
logic.

# Decision 042 — Historical Risk Metrics

Version 1 implements historical risk metrics:

- Sharpe Ratio
- Sortino Ratio
- Maximum Drawdown
- Historical Value-at-Risk
- Historical Conditional Value-at-Risk

No parametric or Monte Carlo-based risk metrics are included.

### Reason

Historical metrics are deterministic, require fewer modelling
assumptions, and provide a solid production-quality foundation for
Version 1.

### Reason

Business orchestration belongs to Services while financial computation
remains isolated within Financial Engines, preserving the Layered
Modular Monolith architecture.

# Decision 043 — Portfolio Health Reuses Existing Financial Engines

The Portfolio Health module is an aggregation layer built on top of
existing repository capabilities.

Portfolio health analysis reuses:

- Statistics outputs
- Risk Analytics outputs
- Monte Carlo Simulation outputs

The Portfolio Health Financial Engine does not fetch market data and does
not independently recompute portfolio risk analytics or simulation
results.

### Reason

Portfolio health is a higher-level diagnostic built from existing
portfolio return, risk, and simulation signals.

Reusing established Financial Engines avoids duplicated financial logic,
preserves deterministic behaviour, and keeps ownership of mathematical
responsibilities in the modules that already define them.

---

# Decision 044 — Portfolio Health Financial Engine Owns Only Health Scoring Logic

The Portfolio Health Financial Engine owns only the deterministic logic
required to convert prepared portfolio analytics inputs into health
diagnostics.

Its responsibilities include:

- validation of health engine inputs
- return scoring
- risk scoring
- diversification scoring
- concentration scoring
- optimization efficiency scoring
- summary generation
- recommendation generation

It does not perform market data retrieval, portfolio return estimation,
risk metric computation, or Monte Carlo simulation.

### Reason

Portfolio Health is a composite analytics layer rather than a new source
of base financial calculations.

Keeping the engine focused on health scoring preserves clean
responsibility boundaries and avoids mathematical duplication across
Financial Engines.

---

# Decision 045 — Portfolio Health Service Orchestrates Cross-Engine Inputs

PortfolioHealthService is responsible for orchestrating the inputs
required by the Portfolio Health Financial Engine.

It coordinates:

- StatisticsService for portfolio expected return and volatility
- RiskAnalyticsService for risk metrics
- SimulationService for best simulated Sharpe ratio

PortfolioHealthService performs orchestration and business validation but
does not implement portfolio health mathematics directly.

### Reason

Portfolio Health depends on multiple previously completed application
capabilities.

The Service layer is the correct place to coordinate cross-engine
workflows while preserving the framework independence of the Financial
Engine.

---

# Decision 046 — Portfolio Health Optimization Efficiency Uses Monte Carlo Best Sharpe

Portfolio Health evaluates optimization efficiency by comparing the
current portfolio Sharpe ratio against the best Sharpe ratio discovered
during Monte Carlo simulation over the same asset universe and date
range.

This metric is exposed as `optimization_efficiency_score`.

### Reason

A portfolio health layer should evaluate not only raw return and risk,
but also how efficiently the current allocation uses the opportunity set
available within the analyzed assets.

Using the best simulated Sharpe ratio creates a deterministic,
interview-defensible benchmark while reusing the Monte Carlo Simulation
Engine already present in the repository.

---

# Decision 047 — Portfolio Health Uses a Unified Domain Result

Portfolio health analysis returns a single immutable domain model,
`PortfolioHealthResult`, that contains all health diagnostics exposed by
the module.

The model includes:

- overall health score
- return score
- risk score
- diversification score
- concentration score
- optimization efficiency score
- summary
- recommendations

### Reason

A unified immutable result provides a stable contract between the
Financial Engine, Service layer, and API layer.

It also prevents callers from orchestrating health subcomponents
manually and keeps the public interface concise.

---

# Decision 048 — StatisticsService Owns Portfolio Expected Return Aggregation

Portfolio expected return aggregation is exposed through
`StatisticsService.get_portfolio_expected_return(...)`.

PortfolioHealthService reuses this StatisticsService method rather than
performing expected-return dot-product aggregation itself.

### Reason

Portfolio expected return is a statistics concern.

Keeping this aggregation inside the Statistics application layer
preserves module ownership, avoids service-level duplication, and keeps
PortfolioHealthService focused on orchestration rather than portfolio
statistics computation.

---

# Decision 049 — Portfolio Health API Responsibilities

Portfolio Health endpoints perform only:

- request validation
- Service delegation
- response serialization
- exception translation

The API layer does not compute portfolio health metrics.

### Reason

Portfolio Health follows the same thin-API discipline used throughout
the repository.

This preserves the Layered Modular Monolith architecture and keeps
transport logic separate from business and financial logic.

# Future Decisions

# Future Decisions

Future phases will extend this document with additional decisions for:

- React Frontend
- Production Deployment

New decisions should be appended rather than modifying historical
entries unless a previous decision has become technically incorrect.

.....

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

**Repository Status:** Phase 8 Complete

**Current Test Status:** 253 Passing

**Engineering Decisions:** 49

**Next Planned Phase:** Phase 9 – Frontend and Productization