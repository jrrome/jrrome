#!/usr/bin/env python3
"""Generate the self-contained terminal images used by the profile README."""

from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

PALETTES = {
    "dark": {
        "background": "#101214",
        "foreground": "#d0d4d5",
        "muted": "#8a9499",
        "border": "#292d30",
        "prompt": "#a5bf8b",
        "link": "#8faec4",
    },
    "light": {
        "background": "#f5f5f3",
        "foreground": "#303739",
        "muted": "#626c70",
        "border": "#d9dedc",
        "prompt": "#426641",
        "link": "#3d6284",
    },
}


def element(parent, tag, **attrs):
    return ET.SubElement(parent, f"{{{NS}}}{tag}", {k: str(v) for k, v in attrs.items()})


def render(theme, mobile=False):
    colors = PALETTES[theme]
    width, height = (360, 504) if mobile else (800, 408)
    left = 22 if mobile else 30
    svg = ET.Element(f"{{{NS}}}svg", {
        "width": str(width), "height": str(height),
        "viewBox": f"0 0 {width} {height}",
        "role": "img", "aria-labelledby": "title description",
    })
    element(svg, "title", id="title").text = "jrrome — terminal profile"
    element(svg, "desc", id="description").text = (
        "Jaime Romero Martínez. Santiago de Compostela. "
        "Computer Engineering, University of Santiago de Compostela, final year. "
        "Website: jaime-romero.com. Email: jromeromartinez@icloud.com."
    )
    element(svg, "rect", x="0.5", y="0.5", width=width - 1, height=height - 1,
            rx=6, fill=colors["background"], stroke=colors["border"])
    element(svg, "path", d=f"M1 38.5H{width - 1}", stroke=colors["border"])
    body = element(svg, "g", fill=colors["foreground"], **{
        "font-family": "'SFMono-Regular', Menlo, Consolas, 'Liberation Mono', monospace",
        "font-size": "14", "font-weight": "400",
    })

    def text(value, x, y, color="foreground", size=None, anchor=None):
        attrs = {"x": x, "y": y, "fill": colors[color]}
        if size is not None:
            attrs["font-size"] = size
        if anchor:
            attrs["text-anchor"] = anchor
        node = element(body, "text", **attrs)
        node.text = value
        return node

    def command(value, y):
        line = text("", left, y)
        # Explicit character positions keep the prompt consistent across renderers.
        element(line, "tspan", x=left, fill=colors["prompt"]).text = "jrrome"
        element(line, "tspan", x=left + 6 * 8.4, fill=colors["muted"]).text = "@github"
        element(line, "tspan", x=left + 14 * 8.4, fill=colors["link"]).text = "~"
        element(line, "tspan", x=left + 16 * 8.4, fill=colors["prompt"]).text = "$"
        if value:
            element(line, "tspan", x=left + 18 * 8.4).text = value

    text("zsh", 20, 24, "muted", size=11)
    text("jrrome — ~", width / 2, 24, "muted", size=11, anchor="middle")

    command("whoami", 72)
    text("Jaime Romero Martínez", left, 98)
    text("Santiago de Compostela", left, 122, "muted")

    command("cat education", 166)
    if mobile:
        text("degree", left, 192, "muted")
        text("Computer Engineering", left, 216)
        text("university", left, 242, "muted")
        text("University of Santiago", left, 266)
        text("de Compostela", left, 290)
        text("status", left, 316, "muted")
        text("Final year", left, 340)
        contact_y, end_y = 384, 478
    else:
        for y, key, value in (
            (192, "degree", "Computer Engineering"),
            (216, "university", "University of Santiago de Compostela"),
            (240, "status", "Final year"),
        ):
            text(key, left, y, "muted")
            text(value, left + 104, y)
        contact_y, end_y = 284, 378

    command("cat contact", contact_y)
    for offset, key, value in (
        (26, "web", "jaime-romero.com"),
        (50, "email", "jromeromartinez@icloud.com"),
    ):
        text(key, left, contact_y + offset, "muted")
        text(value, left + 64, contact_y + offset, "link")

    command("", end_y)
    element(body, "rect", x=left + 18 * 8.4, y=end_y - 12,
            width=8, height=15, fill=colors["foreground"])

    suffix = f"mobile-{theme}" if mobile else theme
    ET.indent(svg, space="  ")
    output = ASSETS / f"terminal-{suffix}.svg"
    output.write_text(ET.tostring(svg, encoding="unicode") + "\n", encoding="utf-8")
    print(output.relative_to(ROOT))


if __name__ == "__main__":
    ASSETS.mkdir(parents=True, exist_ok=True)
    for theme in PALETTES:
        render(theme)
        render(theme, mobile=True)
