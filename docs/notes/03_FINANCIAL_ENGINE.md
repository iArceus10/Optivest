# OptiVest – Financial Engine Documentation

Version: 1.0

Status: Active

---

# 1. Purpose

The Financial Engine is the computational core of OptiVest.

Its responsibilities are to:

* Retrieve and process market data.
* Compute portfolio statistics.
* Optimize asset allocation.
* Quantify investment risk.
* Generate deterministic portfolio insights.

The Financial Engine must remain completely independent of the web framework and database.

Given the same inputs, it should always produce identical outputs.

---

# 2. Financial Philosophy

OptiVest is designed around one fundamental principle:

> Investing is a trade-off between risk and return.

Every algorithm implemented in the project helps answer one or more of the following questions:

* What return can I reasonably expect?
* How much risk am I taking?
* Is this portfolio efficient?
* Can my allocation be improved?
* How bad could losses become?

---

# 3. Market Data

Source

Yahoo Finance (yfinance)

Data Retrieved

* Adjusted Close Prices
* Historical Daily Prices

Frequency

Daily

Reason

Daily prices provide sufficient historical resolution while keeping computations efficient.

---

# 4. Daily Returns

Definition

Percentage change in price between consecutive trading days.

Purpose

Returns—not prices—are the foundation of modern portfolio analysis because they normalize assets with different price levels.

Used By

* Expected Return
* Volatility
* Covariance Matrix
* Monte Carlo Simulation
* Portfolio Optimization

---

# 5. Expected Return

Definition

The annualized average return expected from the portfolio based on historical daily returns.

Purpose

Represents the reward component of investing.

Implementation

* Compute daily returns.
* Calculate mean daily return.
* Annualize using approximately 252 trading days.

Interview Talking Point

Expected return is an estimate derived from historical performance and should not be interpreted as a guaranteed future return.

---

# 6. Portfolio Volatility

Definition

Annualized standard deviation of portfolio returns.

Purpose

Measures uncertainty or dispersion in returns.

Higher volatility implies greater investment risk.

Implementation

* Compute covariance matrix.
* Apply portfolio variance equation.
* Take square root.

Used By

* Sharpe Ratio
* Efficient Frontier
* Monte Carlo Simulation
* Risk Analysis

---

# 7. Covariance Matrix

Definition

Measures how pairs of assets move relative to each other.

Why It Matters

Diversification is driven by covariance, not individual volatility.

Two highly volatile assets may still reduce overall portfolio risk if they are weakly correlated.

Interview Talking Point

Modern Portfolio Theory depends far more on covariance than on individual asset risk.

---

# 8. Correlation

Definition

Normalized covariance ranging from -1 to +1.

Interpretation

+1

Perfect positive relationship.

0

No linear relationship.

-1

Perfect inverse relationship.

Purpose

Used to visualize diversification opportunities.

---

# 9. Portfolio Optimization

Method

Modern Portfolio Theory (Harry Markowitz)

Goal

Determine portfolio weights that optimize the relationship between expected return and risk.

Constraints

* Sum of weights = 1
* Long-only positions
* No leverage

Optimization Library

CVXPY

Reason

Industry-standard convex optimization framework.

---

# 10. Efficient Frontier

Definition

The set of portfolios offering the highest expected return for each level of risk.

Purpose

Allows investors to compare efficient and inefficient portfolios.

Visualization

Displayed as a continuous frontier above randomly generated portfolios.

Interview Talking Point

Any portfolio below the Efficient Frontier is suboptimal because another portfolio exists with higher return for equal or lower risk.

---

# 11. Maximum Sharpe Portfolio

Objective

Maximize risk-adjusted return.

Interpretation

Provides the best reward per unit of risk.

Use Case

General-purpose portfolio recommendation.

---

# 12. Minimum Variance Portfolio

Objective

Minimize portfolio volatility.

Use Case

Conservative investors.

Characteristics

* Lower expected return
* Lower risk
* High diversification

---

# 13. Monte Carlo Portfolio Simulation

Purpose

Explore thousands of possible portfolios by randomly generating weight combinations.

Version 1

50,000 portfolios.

For each portfolio compute:

* Expected Return
* Volatility
* Sharpe Ratio

Output

Scatter plot with:

* Random portfolios
* Efficient Frontier
* Optimal portfolios

Reason

Provides intuitive visualization of the risk-return landscape.

---

# 14. Sharpe Ratio

Definition

Measures excess return earned per unit of total risk.

Interpretation

Higher values indicate better risk-adjusted performance.

Typical Guidelines

Below 1

Average

1–2

Good

Above 2

Excellent

Limitations

Assumes normally distributed returns and penalizes upside and downside volatility equally.

---

# 15. Maximum Drawdown

Definition

Largest percentage decline from a historical portfolio peak.

Purpose

Measures worst historical loss experienced by the portfolio.

Importance

Many investors understand drawdown more intuitively than volatility.

---

# 16. Historical Value at Risk (VaR)

Confidence Level

95%

Definition

Estimated maximum daily loss not expected to be exceeded on 95% of trading days.

Purpose

Downside risk estimation.

Limitations

Does not describe losses beyond the threshold.

---

# 17. Conditional Value at Risk (CVaR)

Definition

Average loss occurring beyond the VaR threshold.

Purpose

Captures tail risk ignored by VaR.

Importance

Preferred by many institutional risk managers.

---

# 18. Portfolio Health Score

Purpose

Provide a single interpretable metric summarizing overall portfolio quality.

Inputs

* Diversification
* Concentration
* Sharpe Ratio
* Volatility

Output

0–100 score.

Reason

Allows users to quickly evaluate portfolio quality without interpreting multiple statistics.

---

# 19. Numerical Stability

The Financial Engine must:

* Handle missing market data.
* Remove NaN values.
* Validate optimization constraints.
* Reject invalid portfolio weights.
* Avoid divide-by-zero errors.
* Detect singular covariance matrices where applicable.

---

# 20. Computational Complexity

Expected Return

O(n)

Covariance Matrix

O(n²)

Monte Carlo Simulation

O(P × A)

where:

P = number of portfolios

A = number of assets

Optimization

Depends on the convex optimization solver but remains tractable for Version 1 portfolio sizes.

---

# 21. Assumptions

The Financial Engine assumes:

* Historical prices are representative.
* Markets are sufficiently liquid.
* Trading costs are ignored.
* Taxes are ignored.
* Assets are infinitely divisible.
* Only long positions are allowed.

These assumptions simplify the optimization problem while remaining appropriate for educational and interview purposes.

---

# 22. Common Interview Questions

Q: Why use returns instead of prices?

A: Returns normalize assets with different price levels and enable meaningful statistical analysis.

---

Q: Why is covariance more important than volatility?

A: Portfolio risk depends on how assets move together, not just how risky each asset is individually.

---

Q: Why use Monte Carlo simulation?

A: It explores a broad space of feasible portfolios, helping visualize the risk-return trade-off and identify efficient allocations.

---

Q: Why use CVXPY?

A: Portfolio optimization is a convex optimization problem, and CVXPY provides reliable, well-tested solvers while keeping the implementation mathematically transparent.

---

Q: Why use CVaR in addition to VaR?

A: VaR identifies a loss threshold but ignores the magnitude of losses beyond it. CVaR captures the expected severity of those tail losses.
