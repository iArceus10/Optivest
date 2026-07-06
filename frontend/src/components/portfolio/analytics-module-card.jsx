import Button from "../common/button";
import Card from "../common/card";

function AnalyticsModuleCard({
  title,
  description,
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
        <p
          style={{
            margin: 0,
            color: "var(--text-muted)",
            lineHeight: 1.75,
          }}
        >
          Use the configured analysis universe to run this backend workflow
          against the selected portfolio context.
        </p>

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

export default AnalyticsModuleCard;