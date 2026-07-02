import { useState } from "react";

import Button from "../common/button";
import Card from "../common/card";
import Input from "../common/input";

function CreatePortfolioForm({ onCreatePortfolio, isSubmitting }) {
  const [formValues, setFormValues] = useState({
    name: "",
    description: "",
  });
  const [formErrors, setFormErrors] = useState({});
  const [submitError, setSubmitError] = useState("");

  function updateField(field, value) {
    setFormValues((previousValues) => ({
      ...previousValues,
      [field]: value,
    }));

    setFormErrors((previousErrors) => ({
      ...previousErrors,
      [field]: "",
    }));

    if (submitError) {
      setSubmitError("");
    }
  }

  async function handleSubmit(event) {
    event.preventDefault();

    const errors = {};

    if (!formValues.name.trim()) {
      errors.name = "Portfolio name is required.";
    }

    setFormErrors(errors);

    if (Object.keys(errors).length > 0) {
      return;
    }

    try {
      setSubmitError("");

      await onCreatePortfolio({
        name: formValues.name.trim(),
        description: formValues.description.trim(),
      });

      setFormValues({
        name: "",
        description: "",
      });
    } catch (error) {
      setSubmitError(
        error.message || "Unable to create portfolio right now."
      );
    }
  }

  return (
    <Card
      title="Create portfolio"
      subtitle="Create a new portfolio container. In the current OptiVest version, portfolio creation captures portfolio metadata first, while analytics workflows will be performed inside the portfolio workspace."
    >
      <form
        onSubmit={handleSubmit}
        style={{
          display: "grid",
          gap: 16,
        }}
      >
        <Input
          id="portfolio-name"
          label="Portfolio name"
          placeholder="High Growth Tech Basket"
          value={formValues.name}
          onChange={(event) => updateField("name", event.target.value)}
          error={formErrors.name}
          required
        />

        <div style={{ display: "grid", gap: 10 }}>
          <label
            htmlFor="portfolio-description"
            style={{
              color: "var(--text-secondary)",
              fontWeight: 600,
              fontSize: "0.94rem",
            }}
          >
            Description
          </label>

          <textarea
            id="portfolio-description"
            rows={4}
            placeholder="Optional note about the investment thesis, benchmark, or strategy."
            value={formValues.description}
            onChange={(event) =>
              updateField("description", event.target.value)
            }
            style={{
              width: "100%",
              padding: "14px 16px",
              borderRadius: "var(--radius-sm)",
              border: "1px solid var(--border-subtle)",
              background: "rgba(10, 16, 26, 0.84)",
              color: "var(--text-primary)",
              resize: "vertical",
              minHeight: 120,
            }}
          />
        </div>

        {submitError ? (
          <div
            style={{
              padding: "14px 16px",
              borderRadius: "var(--radius-sm)",
              border: "1px solid rgba(239, 68, 68, 0.24)",
              background: "rgba(127, 29, 29, 0.16)",
              color: "#fecaca",
              fontSize: "0.92rem",
              lineHeight: 1.6,
            }}
          >
            {submitError}
          </div>
        ) : null}

        <Button type="submit" size="lg" isLoading={isSubmitting}>
          Create portfolio
        </Button>
      </form>
    </Card>
  );
}

export default CreatePortfolioForm;