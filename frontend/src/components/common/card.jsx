function Card({
  children,
  title,
  subtitle,
  action,
  padding = "24px",
  minHeight,
  style,
}) {
  return (
    <section
      className="glass-panel"
      style={{
        padding,
        minHeight,
        ...style,
      }}
    >
      {(title || subtitle || action) && (
        <div
          style={{
            display: "flex",
            alignItems: "flex-start",
            justifyContent: "space-between",
            gap: 16,
            marginBottom: 20,
          }}
        >
          <div>
            {title ? (
              <h3
                style={{
                  margin: 0,
                  fontSize: "1.08rem",
                  fontWeight: 800,
                  letterSpacing: "-0.02em",
                }}
              >
                {title}
              </h3>
            ) : null}

            {subtitle ? (
              <p
                style={{
                  margin: "8px 0 0",
                  color: "var(--text-muted)",
                  lineHeight: 1.65,
                  fontSize: "0.95rem",
                }}
              >
                {subtitle}
              </p>
            ) : null}
          </div>

          {action ? <div>{action}</div> : null}
        </div>
      )}

      {children}
    </section>
  );
}

export default Card;