"""Tiny SVG helpers for the hand-written course diagrams: the same 480x300
dark card and palette the lesson writer is asked to use."""

from __future__ import annotations

from html import escape

INK = "#e4f3fc"
MUTED = "#7c93a6"
BLUE = "#5fd3ff"
GREEN = "#8af5c8"
AMBER = "#ffb547"
RED = "#ff6b6b"
PURPLE = "#a78bfa"
COLOURS = {"ink": INK, "blue": BLUE, "green": GREEN, "amber": AMBER, "red": RED, "purple": PURPLE, "muted": MUTED}
FONT = 'font-family="sans-serif"'


def svg(*parts: str, w: int = 480, h: int = 300) -> str:
    markers = "".join(
        f'<marker id="m-{name}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M0 0 L10 5 L0 10 z" fill="{colour}"/></marker>'
        for name, colour in COLOURS.items()
    )
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><defs>{markers}</defs>'
            f'<rect width="{w}" height="{h}" rx="16" fill="#0b1620"/>' + "".join(parts) + "</svg>")


def text(x: float, y: float, s: str, size: int = 14, colour: str = INK, anchor: str = "middle", weight: str = "normal") -> str:
    return (f'<text x="{x}" y="{y}" fill="{colour}" font-size="{size}" {FONT} text-anchor="{anchor}" '
            f'font-weight="{weight}">{escape(s)}</text>')


def box(x: float, y: float, w: float, h: float, label: str = "", colour: str = INK, fill: str = "none", sub: str = "",
        size: int = 14, rx: int = 10) -> str:
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{colour}" stroke-width="2"/>'
    cy = y + h / 2 + (0 if sub else 5)
    if label:
        out += text(x + w / 2, cy - (4 if sub else 0), label, size, colour if fill == "none" else INK)
    if sub:
        out += text(x + w / 2, cy + 14, sub, 12, MUTED)
    return out


def line(x1: float, y1: float, x2: float, y2: float, colour: str = INK, width: float = 2, dash: str = "") -> str:
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{colour}" stroke-width="{width}"{d}/>'


def arrow(x1: float, y1: float, x2: float, y2: float, colour: str = BLUE, label: str = "", width: float = 2.5,
          dx: float = 0, dy: float = -8, size: int = 13) -> str:
    name = next((n for n, c in COLOURS.items() if c == colour), "blue")
    out = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{colour}" stroke-width="{width}" marker-end="url(#m-{name})"/>'
    if label:
        out += text((x1 + x2) / 2 + dx, (y1 + y2) / 2 + dy, label, size, colour)
    return out


def path(d: str, colour: str = INK, width: float = 2.5, fill: str = "none", dash: str = "") -> str:
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="{fill}" stroke="{colour}" stroke-width="{width}"{extra}/>'


def circle(cx: float, cy: float, r: float, colour: str = BLUE, fill: str = "none", label: str = "", size: int = 13) -> str:
    out = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{colour}" stroke-width="2"/>'
    if label:
        out += text(cx, cy + 5, label, size, colour if fill == "none" else INK)
    return out


def title(s: str) -> str:
    return text(240, 30, s, 15, INK, weight="bold")
