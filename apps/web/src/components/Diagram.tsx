/**
 * A diagram drawn by the model, already sanitised by the server. Shown as an
 * <img> from a data URL so nothing inside it can run.
 */
export function Diagram({ svg, alt, caption }: { svg: string; alt: string; caption?: string }) {
  if (!svg) return null;
  const src = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`;
  return (
    <figure className="diagram">
      <img src={src} alt={alt} loading="lazy" />
      {caption && <figcaption>{caption}</figcaption>}
    </figure>
  );
}
