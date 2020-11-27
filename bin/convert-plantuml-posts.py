from pathlib import Path
import re
import requests
from plantweb.render import render

PLANTUML_REGEX = re.compile(r"""```plantumlcode\n(?P<code>.+?)```""", re.DOTALL)
HEADER_REGEX = re.compile(r"""^#""", re.MULTILINE)

ROOT_PATH = Path(__file__).parent.parent / "docs"

INPUT_FILES = (ROOT_PATH / "_raw_posts").glob("*.md")
OUTPUT_DIR = ROOT_PATH / "_posts"
IMG_DIR = ROOT_PATH / "img" / "plantuml"
IMG_PATH = "/img/plantuml/"
PLANTUML_STYLE = Path(__file__).parent / "plantumlstyle"

SERVER_URL = "https://plantuml.server.d3f.me"


def render_plantuml(match):
    plantuml_text = PLANTUML_STYLE.read_text() + match.group("code")

    (output, format, engine, sha) = render(
        plantuml_text, engine="plantuml", format="svg", server=SERVER_URL
    )

    fname = sha + ".svg"

    (IMG_DIR / fname).write_bytes(output)

    return f'<img src="{IMG_PATH + fname}" class="svg">'


def replace_header(match):
    return match.group(0) + "#"


for image in IMG_DIR.glob("*.svg"):
    image.unlink()


for file in INPUT_FILES:
    print(file)
    output_path = OUTPUT_DIR / file.name
    text = file.read_text()
    text = HEADER_REGEX.sub(replace_header, text)
    text = PLANTUML_REGEX.sub(render_plantuml, text)
    output_path.write_text(text)
