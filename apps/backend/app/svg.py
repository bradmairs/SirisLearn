"""Sanitises the SVG diagrams the model draws for lessons and image questions.

The browser shows them as <img src="data:image/svg+xml,...">, where scripts
never run, but they're cleaned here too: only drawing elements survive, no
event handlers, no external references, no embedded HTML.
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET

MAX_BYTES = 80_000
SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"

ALLOWED = {
    "svg", "g", "defs", "title", "desc", "path", "rect", "circle", "ellipse", "line", "polyline", "polygon",
    "text", "tspan", "textPath", "marker", "linearGradient", "radialGradient", "stop", "pattern", "clipPath",
    "mask", "symbol", "use",
}
URL_REF = re.compile(r"url\(\s*['\"]?(?!#)", re.I)

ET.register_namespace("", SVG_NS)
ET.register_namespace("xlink", XLINK_NS)


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def sanitize(markup: str | None) -> str:
    """A clean SVG string, or "" when there's nothing usable."""
    markup = (markup or "").strip()
    if not markup or len(markup.encode()) > MAX_BYTES or "<!DOCTYPE" in markup.upper() or "<!ENTITY" in markup.upper():
        return ""
    start = markup.find("<svg")
    if start < 0:
        return ""
    try:
        root = ET.fromstring(markup[start:])
    except ET.ParseError:
        return ""
    if _local(root.tag) != "svg":
        return ""
    _clean(root)
    if root.tag == "svg":  # no namespace in the source: add it, or <img> won't render it
        root.set("xmlns", SVG_NS)
    if not root.get("viewBox") and root.get("width") and root.get("height"):
        root.set("viewBox", f"0 0 {_num(root.get('width'))} {_num(root.get('height'))}")
    for size in ("width", "height"):
        root.attrib.pop(size, None)  # scale with the card, keep the viewBox
    return ET.tostring(root, encoding="unicode")


def _num(value: str | None) -> str:
    match = re.match(r"[\d.]+", value or "")
    return match.group(0) if match else "100"


def _clean(element: ET.Element) -> None:
    for child in list(element):
        if not isinstance(child.tag, str) or _local(child.tag) not in ALLOWED:
            element.remove(child)
            continue
        _clean(child)
    for name in list(element.attrib):
        local = _local(name).lower()
        value = element.attrib[name]
        lowered = value.lower()
        if (
            local.startswith("on")
            or (local == "href" and not value.startswith("#"))
            or URL_REF.search(value)
            or "javascript:" in lowered
            or "expression(" in lowered
        ):
            del element.attrib[name]
