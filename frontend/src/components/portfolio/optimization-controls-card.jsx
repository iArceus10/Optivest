import Button from "../common/button";
import Card from "../common/card";

function OptimizationControlsCard({
  title,
  description,
  fields = [],
  values,
  onChange,
  actionLabel,
  onAction,
  isLoading = false,
}) {
  return (
    <Card title={title} subtitle={description}>
      <div
        style={{
          display: "grid",
          gap: 18,
        }}
      >
        {fields.length ? (
          <div
            style={{
              display: "grid",
              gap: 16,
              gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
            }}
          >
            {fields.map((field) => (
              <label
                key={field.key}
                style={{
                  display: "grid",
                  gap: 8,
                }}
              >
                <span
                  style={{
                    fontSize: "0.9rem",
                    fontWeight: 600,
                    color: "var(--text-secondary)",
                  }}
                >
                  {field.label}
                </span>

                <input
                  type={field.type || "number"}
                  value={values[field.key]}
                  onChange={(event) =>
                    onChange(field.key, event.target.value)
                  }
                  min={field.min}
                  step={field.step}
                  placeholder={field.placeholder}
                  style={{
                    minHeight: 46,
                    borderRadius: "var(--radius-sm)",
                    border: "1px solid var(--border-subtle)",
                    background: "rgba(255, 255, 255, 0.03)",
                    color: "var(--text-primary)",
                    padding: "0 14px",
                    outline: "none",
                  }}
                />
              </label>
            ))}
          </div>
        ) : null}

        <div
          style={{
            display: "flex",
            justifyContent: "flex-end",
          }}
        >
          <Button
            variant="primary"
            size="md"
            onClick={onAction}
            isLoading={isLoading}
          >
            {actionLabel}
          </Button>
        </div>
      </div>
    </Card>
  );
}

export default OptimizationControlsCard;