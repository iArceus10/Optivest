import { useEffect, useState } from "react";

import Button from "../common/button";
import Card from "../common/card";
import Input from "../common/input";

function getDefaultDates() {
  const today = new Date();
  const end = today.toISOString().slice(0, 10);

  const previousYear = new Date(today);
  previousYear.setFullYear(today.getFullYear() - 1);

  const start = previousYear.toISOString().slice(0, 10);

  return { start, end };
}

function normalizeTickers(rawTickers) {
  return rawTickers
    .split(",")
    .map((ticker) => ticker.trim().toUpperCase())
    .filter(Boolean);
}

function AnalysisControlsCard({
  initialTickers = "",
  onApplyAnalysisUniverse,
  isApplying = false,
}) {
  const defaultDates = getDefaultDates();

  const [formValues, setFormValues] = useState({
    tickers: initialTickers,
    start: defaultDates.start,
    end: defaultDates.end,
  });
  const [formErrors, setFormErrors] = useState({});

  useEffect(() => {
    setFormValues((previousValues) => ({
      ...previousValues,
      tickers: initialTickers,
    }));
  }, [initialTickers]);

  function updateField(field, value) {
    setFormValues((previousValues) => ({
      ...previousValues,
      [field]: value,
    }));

    setFormErrors((previousErrors) => ({
      ...previousErrors,
      [field]: "",
    }));
  }

  function handleSubmit(event) {
    event.preventDefault();

    const errors = {};
    const parsedTickers = normalizeTickers(formValues.tickers);

    if (parsedTickers.length === 0) {
      errors.tickers =
        "Enter at least one ticker. Example: AAPL, MSFT, NVDA";
    }

    if (!formValues.start) {
      errors.start = "Start date is required.";
    }

    if (!formValues.end) {
      errors.end = "End date is required.";
    }

    if (
      formValues.start &&
      formValues.end &&
      formValues.start >= formValues.end
    ) {
      errors.end = "End date must be later than start date.";
    }

    setFormErrors(errors);

    if (Object.keys(errors).length > 0) {
      return;
    }

    onApplyAnalysisUniverse({
      tickers: parsedTickers,
      start: formValues.start,
      end: formValues.end,
    });
  }

  return (
    <Card
      title="Analysis universe"
      subtitle="Configure the assets and date range for market data and statistics workflows on this portfolio page."
    >
      <form
        onSubmit={handleSubmit}
        style={{
          display: "grid",
          gap: 16,
        }}
      >
        <Input
          id="analysis-tickers"
          label="Tickers"
          placeholder="AAPL, MSFT, NVDA"
          value={formValues.tickers}
          onChange={(event) => updateField("tickers", event.target.value)}
          error={formErrors.tickers}
          hint="Comma-separated tickers. These will be used for market data and statistics requests."
          required
        />

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(2, minmax(0, 1fr))",
            gap: 16,
          }}
        >
          <div style={{ display: "grid", gap: 10 }}>
            <label
              htmlFor="analysis-start"
              style={{
                color: "var(--text-secondary)",
                fontWeight: 600,
                fontSize: "0.94rem",
              }}
            >
              Start date
            </label>

            <input
              id="analysis-start"
              type="date"
              value={formValues.start}
              onChange={(event) => updateField("start", event.target.value)}
              style={{
                width: "100%",
                minHeight: 50,
                padding: "0 16px",
                borderRadius: "var(--radius-sm)",
                border: `1px solid ${
                  formErrors.start
                    ? "rgba(239, 68, 68, 0.4)"
                    : "var(--border-subtle)"
                }`,
                background: "rgba(10, 16, 26, 0.84)",
                color: "var(--text-primary)",
              }}
            />

            {formErrors.start ? (
              <p
                style={{
                  margin: 0,
                  color: "var(--accent-red)",
                  fontSize: "0.88rem",
                }}
              >
                {formErrors.start}
              </p>
            ) : null}
          </div>

          <div style={{ display: "grid", gap: 10 }}>
            <label
              htmlFor="analysis-end"
              style={{
                color: "var(--text-secondary)",
                fontWeight: 600,
                fontSize: "0.94rem",
              }}
            >
              End date
            </label>

            <input
              id="analysis-end"
              type="date"
              value={formValues.end}
              onChange={(event) => updateField("end", event.target.value)}
              style={{
                width: "100%",
                minHeight: 50,
                padding: "0 16px",
                borderRadius: "var(--radius-sm)",
                border: `1px solid ${
                  formErrors.end
                    ? "rgba(239, 68, 68, 0.4)"
                    : "var(--border-subtle)"
                }`,
                background: "rgba(10, 16, 26, 0.84)",
                color: "var(--text-primary)",
              }}
            />

            {formErrors.end ? (
              <p
                style={{
                  margin: 0,
                  color: "var(--accent-red)",
                  fontSize: "0.88rem",
                }}
              >
                {formErrors.end}
              </p>
            ) : null}
          </div>
        </div>

        <Button type="submit" size="lg" isLoading={isApplying}>
          Apply analysis universe
        </Button>
      </form>
    </Card>
  );
}

export default AnalysisControlsCard;