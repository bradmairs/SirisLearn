import { Fragment, type ReactNode } from "react";

/**
 * A small Markdown renderer for lessons: headings, paragraphs, bulleted and
 * numbered lists, blockquotes, tables, code blocks, **bold**, *italic* and `code`.
 * It builds React elements (never raw HTML), so lesson text can't inject markup.
 */
export function Markdown({ text }: { text: string }) {
  return <div className="prose">{blocks(text)}</div>;
}

type Block =
  | { type: "h"; level: number; text: string }
  | { type: "p"; text: string }
  | { type: "quote"; text: string }
  | { type: "ul" | "ol"; items: string[] }
  | { type: "code"; text: string }
  | { type: "table"; head: string[]; rows: string[][] };

function cells(line: string): string[] {
  return line.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map((c) => c.trim());
}

export function parse(text: string): Block[] {
  const lines = text.replace(/\r\n/g, "\n").split("\n");
  const out: Block[] = [];
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    if (!line.trim()) {
      i++;
      continue;
    }
    if (line.trim().startsWith("```")) {
      const code: string[] = [];
      i++;
      while (i < lines.length && !lines[i].trim().startsWith("```")) code.push(lines[i++]);
      i++;
      out.push({ type: "code", text: code.join("\n") });
      continue;
    }
    if (line.trim().startsWith("|") && i + 1 < lines.length && /^\s*\|?\s*:?-{3,}/.test(lines[i + 1])) {
      const head = cells(line);
      i += 2;
      const rows: string[][] = [];
      while (i < lines.length && lines[i].trim().startsWith("|")) rows.push(cells(lines[i++]));
      out.push({ type: "table", head, rows });
      continue;
    }
    const heading = /^(#{1,4})\s+(.*)$/.exec(line);
    if (heading) {
      out.push({ type: "h", level: Math.min(4, heading[1].length + 1), text: heading[2] });
      i++;
      continue;
    }
    if (/^\s*>/.test(line)) {
      const quote: string[] = [];
      while (i < lines.length && /^\s*>/.test(lines[i])) quote.push(lines[i++].replace(/^\s*>\s?/, ""));
      out.push({ type: "quote", text: quote.join(" ") });
      continue;
    }
    const listKind = /^\s*[-*+]\s+/.test(line) ? "ul" : /^\s*\d+[.)]\s+/.test(line) ? "ol" : null;
    if (listKind) {
      const marker = listKind === "ul" ? /^\s*[-*+]\s+/ : /^\s*\d+[.)]\s+/;
      const items: string[] = [];
      while (i < lines.length && lines[i].trim()) {
        if (marker.test(lines[i])) items.push(lines[i].replace(marker, ""));
        else if (items.length && /^\s+/.test(lines[i])) items[items.length - 1] += ` ${lines[i].trim()}`;
        else break;
        i++;
      }
      out.push({ type: listKind, items });
      continue;
    }
    const para: string[] = [];
    while (i < lines.length && lines[i].trim() && !/^(#{1,4}\s|\s*>|\s*[-*+]\s|\s*\d+[.)]\s|\s*```|\s*\|)/.test(lines[i])) para.push(lines[i++].trim());
    out.push({ type: "p", text: para.join(" ") });
  }
  return out;
}

function blocks(text: string): ReactNode[] {
  return parse(text).map((b, key) => {
    switch (b.type) {
      case "h": {
        const Tag = `h${b.level}` as "h2" | "h3" | "h4";
        return <Tag key={key}>{inline(b.text)}</Tag>;
      }
      case "quote":
        return <blockquote key={key}>{inline(b.text)}</blockquote>;
      case "ul":
        return <ul key={key}>{b.items.map((item, i) => <li key={i}>{inline(item)}</li>)}</ul>;
      case "ol":
        return <ol key={key}>{b.items.map((item, i) => <li key={i}>{inline(item)}</li>)}</ol>;
      case "code":
        return <pre key={key}><code>{b.text}</code></pre>;
      case "table":
        return (
          <div key={key} className="table-wrap">
            <table>
              <thead><tr>{b.head.map((h, i) => <th key={i}>{inline(h)}</th>)}</tr></thead>
              <tbody>{b.rows.map((r, i) => <tr key={i}>{r.map((c, j) => <td key={j}>{inline(c)}</td>)}</tr>)}</tbody>
            </table>
          </div>
        );
      default:
        return <p key={key}>{inline(b.text)}</p>;
    }
  });
}

export function inline(text: string): ReactNode[] {
  const out: ReactNode[] = [];
  const pattern = /(`[^`]+`|\*\*[^*]+\*\*|__[^_]+__|\*[^*\s][^*]*\*|_[^_\s][^_]*_)/g;
  let last = 0;
  let match: RegExpExecArray | null;
  while ((match = pattern.exec(text))) {
    if (match.index > last) out.push(text.slice(last, match.index));
    const token = match[0];
    const key = out.length;
    if (token.startsWith("`")) out.push(<code key={key}>{token.slice(1, -1)}</code>);
    else if (token.startsWith("**") || token.startsWith("__")) out.push(<strong key={key}>{inline(token.slice(2, -2))}</strong>);
    else out.push(<em key={key}>{inline(token.slice(1, -1))}</em>);
    last = match.index + token.length;
  }
  if (last < text.length) out.push(text.slice(last));
  return out.map((node, i) => (typeof node === "string" ? <Fragment key={`t${i}`}>{node}</Fragment> : node));
}
