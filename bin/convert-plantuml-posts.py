from pathlib import Path
import re
import requests
from plantweb.render import render

PLANTUML_REGEX = re.compile(r"""```plantumlcode\n(?P<code>.+?)```""", re.DOTALL)

ROOT_PATH = Path(__file__).parent.parent / "docs"

INPUT_FILES = (ROOT_PATH / "_raw_posts").glob("*.md")
OUTPUT_DIR = ROOT_PATH / "_posts"
PLANTUML_STYLE = Path(__file__).parent / "plantumlstyle"

SERVER_URL = "https://plantuml.server.d3f.me"


def render_plantuml(match):
    plantuml_text = PLANTUML_STYLE.read_text() + match.group("code")
    
    (output, format, engine, sha) = render(
        plantuml_text, engine="plantuml", format="svg", server=SERVER_URL
    )

    svg = output.decode('utf-8')
    html = svg.replace('<?xml version="1.0" encoding="UTF-8" standalone="no"?>', '')
    return html


for file in INPUT_FILES:
    print(file)
    output_path = OUTPUT_DIR / file.name

    output_path.write_text(PLANTUML_REGEX.sub(render_plantuml, file.read_text()))
