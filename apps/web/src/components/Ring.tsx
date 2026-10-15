/** A progress ring (0..1) with a label in the middle. */
export function Ring({ value, size = 92, stroke = 7, color = "var(--accent)", children, label }: {
  value: number; size?: number; stroke?: number; color?: string; children?: React.ReactNode; label: string;
}) {
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;
  const shown = Math.max(0, Math.min(1, value));
  return (
    <div className="ring" style={{ width: size, height: size }} role="img" aria-label={label}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} aria-hidden="true">
        <circle cx={size / 2} cy={size / 2} r={r} className="ring__track" strokeWidth={stroke} />
        {shown > 0 && (
          <circle cx={size / 2} cy={size / 2} r={r} className="ring__value" strokeWidth={stroke} stroke={color}
            strokeDasharray={`${c * shown} ${c}`} />
        )}
      </svg>
      <div className="ring__inner">{children}</div>
    </div>
  );
}
