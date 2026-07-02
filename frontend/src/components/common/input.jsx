function Input({
  id,
  label,
  type = "text",
  placeholder,
  value,
  onChange,
  error,
  hint,
  autoComplete,
  disabled = false,
  required = false,
}) {
  return (
    <div style={{ display: "grid", gap: 10 }}>
      {label ? (
        <label
          htmlFor={id}
          style={{
            color: "var(--text-secondary)",
            fontWeight: 600,
            fontSize: "0.94rem",
          }}
        >
          {label}
        </label>
      ) : null}

      <input
        id={id}
        type={type}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        autoComplete={autoComplete}
        disabled={disabled}
        required={required}
        style={{
          width: "100%",
          minHeight: 50,
          padding: "0 16px",
          borderRadius: "var(--radius-sm)",
          border: `1px solid ${error ? "rgba(239, 68, 68, 0.4)" : "var(--border-subtle)"}`,
          background: "rgba(10, 16, 26, 0.84)",
          color: "var(--text-primary)",
          transition: "border-color var(--transition-base), box-shadow var(--transition-base)",
          boxShadow: error ? "0 0 0 4px rgba(239, 68, 68, 0.08)" : "none",
        }}
      />

      {error ? (
        <p
          style={{
            margin: 0,
            color: "var(--accent-red)",
            fontSize: "0.88rem",
            lineHeight: 1.5,
          }}
        >
          {error}
        </p>
      ) : hint ? (
        <p
          style={{
            margin: 0,
            color: "var(--text-faint)",
            fontSize: "0.86rem",
            lineHeight: 1.5,
          }}
        >
          {hint}
        </p>
      ) : null}
    </div>
  );
}

export default Input;