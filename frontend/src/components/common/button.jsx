function Button({
  type = "button",
  variant = "primary",
  size = "md",
  isLoading = false,
  disabled = false,
  children,
  style,
  ...rest
}) {
  const isDisabled = disabled || isLoading;

  const variantStyles = {
    primary: {
      background: "var(--gradient-brand)",
      color: "#04120a",
      border: "1px solid transparent",
      boxShadow: "var(--shadow-glow-green)",
    },
    secondary: {
      background: "rgba(15, 23, 36, 0.82)",
      color: "var(--text-primary)",
      border: "1px solid var(--border-subtle)",
    },
    ghost: {
      background: "transparent",
      color: "var(--text-secondary)",
      border: "1px solid transparent",
    },
  };

  const sizeStyles = {
    sm: {
      minHeight: 40,
      padding: "0 14px",
      fontSize: "0.92rem",
    },
    md: {
      minHeight: 48,
      padding: "0 18px",
      fontSize: "0.96rem",
    },
    lg: {
      minHeight: 54,
      padding: "0 22px",
      fontSize: "1rem",
    },
  };

  return (
    <button
      type={type}
      disabled={isDisabled}
      style={{
        width: "100%",
        display: "inline-flex",
        alignItems: "center",
        justifyContent: "center",
        gap: 10,
        borderRadius: "var(--radius-sm)",
        fontWeight: 700,
        letterSpacing: "-0.01em",
        transition: "transform var(--transition-base), opacity var(--transition-base), border-color var(--transition-base), background var(--transition-base)",
        opacity: isDisabled ? 0.72 : 1,
        cursor: isDisabled ? "not-allowed" : "pointer",
        ...variantStyles[variant],
        ...sizeStyles[size],
        ...style,
      }}
      {...rest}
    >
      {isLoading ? "Please wait..." : children}
    </button>
  );
}

export default Button;