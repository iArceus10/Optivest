import { useMemo, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";

import { useAuth } from "../../context/auth-context";
import { AUTH_PAGE_COPY } from "../../utils/constants";
import Button from "../common/button";
import Input from "../common/input";

function getInitialFormState(mode) {
  if (mode === "register") {
    return {
      fullName: "",
      email: "",
      password: "",
    };
  }

  return {
    email: "",
    password: "",
  };
}

function validateLoginForm(values) {
  const errors = {};

  if (!values.email.trim()) {
    errors.email = "Email is required.";
  }

  if (!values.password.trim()) {
    errors.password = "Password is required.";
  }

  return errors;
}

function validateRegisterForm(values) {
  const errors = {};

  if (!values.fullName.trim()) {
    errors.fullName = "Full name is required.";
  }

  if (!values.email.trim()) {
    errors.email = "Email is required.";
  }

  if (!values.password.trim()) {
    errors.password = "Password is required.";
  } else if (values.password.length < 8) {
    errors.password = "Password must be at least 8 characters long.";
  }

  return errors;
}

function AuthForm({ mode = "login" }) {
  const navigate = useNavigate();
  const location = useLocation();
  const { login, register } = useAuth();

  const [formValues, setFormValues] = useState(() => getInitialFormState(mode));
  const [formErrors, setFormErrors] = useState({});
  const [submitError, setSubmitError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const copy = AUTH_PAGE_COPY[mode];
  const isRegisterMode = mode === "register";

  const redirectPath = useMemo(() => {
    if (location.state?.from && typeof location.state.from === "string") {
      return location.state.from;
    }

    return "/dashboard";
  }, [location.state]);

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

    const validationErrors = isRegisterMode
      ? validateRegisterForm(formValues)
      : validateLoginForm(formValues);

    setFormErrors(validationErrors);

    if (Object.keys(validationErrors).length > 0) {
      return;
    }

    setIsSubmitting(true);
    setSubmitError("");

    try {
      if (isRegisterMode) {
        await register(formValues);
        await login({
          email: formValues.email,
          password: formValues.password,
        });
      } else {
        await login({
          email: formValues.email,
          password: formValues.password,
        });
      }

      navigate(redirectPath, { replace: true });
    } catch (error) {
      setSubmitError(error.message || "Unable to complete authentication.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      style={{
        display: "grid",
        gap: 18,
      }}
    >
      <div style={{ marginBottom: 8 }}>
        <h2
          style={{
            margin: 0,
            fontSize: "1.9rem",
            fontWeight: 800,
            letterSpacing: "-0.03em",
          }}
        >
          {copy.title}
        </h2>

        <p
          style={{
            margin: "12px 0 0",
            color: "var(--text-muted)",
            lineHeight: 1.7,
            fontSize: "0.98rem",
          }}
        >
          {copy.subtitle}
        </p>
      </div>

      {isRegisterMode ? (
        <Input
          id="fullName"
          label="Full name"
          placeholder="Harshit Kulshrestha"
          value={formValues.fullName}
          onChange={(event) => updateField("fullName", event.target.value)}
          error={formErrors.fullName}
          autoComplete="name"
          required
        />
      ) : null}

      <Input
        id="email"
        label="Email address"
        type="email"
        placeholder="you@example.com"
        value={formValues.email}
        onChange={(event) => updateField("email", event.target.value)}
        error={formErrors.email}
        autoComplete="email"
        required
      />

      <Input
        id="password"
        label="Password"
        type="password"
        placeholder={isRegisterMode ? "At least 8 characters" : "Enter your password"}
        value={formValues.password}
        onChange={(event) => updateField("password", event.target.value)}
        error={formErrors.password}
        autoComplete={isRegisterMode ? "new-password" : "current-password"}
        required
      />

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
        {copy.submitLabel}
      </Button>

      <p
        style={{
          margin: 0,
          color: "var(--text-muted)",
          textAlign: "center",
          fontSize: "0.94rem",
        }}
      >
        {copy.alternateLabel}{" "}
        <Link
          to={copy.alternateHref}
          style={{
            color: "var(--accent-cyan)",
            fontWeight: 700,
          }}
        >
          {copy.alternateAction}
        </Link>
      </p>
    </form>
  );
}

export default AuthForm;