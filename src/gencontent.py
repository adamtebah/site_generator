from pathlib import Path

from markdown_to_html import markdown_to_html_node


def extract_title(markdown: str) -> str:
    """Extract the h1 heading (line starting with a single #) from markdown. Raises if not found."""
    lines = markdown.strip().splitlines()
    for line in lines:
        stripped = line.strip()
        # Single # only: "# " then non-# (so "## " is not h1)
        if stripped.startswith("# ") and (len(stripped) == 2 or stripped[2] != "#"):
            return stripped[2:].strip()
    raise ValueError("Markdown must contain exactly one h1 header (a line starting with '# ')")


def generate_page(
    from_path: str, template_path: str, dest_path: str, basepath: str = "/"
) -> None:
    """Read markdown and template, convert markdown to HTML, fill template, write to dest_path."""
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown = Path(from_path).read_text(encoding="utf-8")
    template = Path(template_path).read_text(encoding="utf-8")

    html_node = markdown_to_html_node(markdown)
    content_html = html_node.to_html()
    title = extract_title(markdown)

    html_page = template.replace("{{ Title }}", title).replace("{{ Content }}", content_html)

    # Rewrite absolute paths so they work under a base path (e.g. GitHub Pages /repo/)
    if basepath != "/":
        html_page = html_page.replace('href="/', f'href="{basepath}')
        html_page = html_page.replace('src="/', f'src="{basepath}')

    dest = Path(dest_path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html_page, encoding="utf-8")
