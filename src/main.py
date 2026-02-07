import os
import shutil
import sys
from pathlib import Path

from copy_static import copy_directory
from gencontent import generate_page

dir_path_static = "./static"
dir_path_docs = "./docs"
dir_path_content = "./content"
template_path = "./template.html"


def generate_pages_recursive(
    dir_path_content: str,
    template_path: str,
    dest_dir_path: str,
    basepath: str,
) -> None:
    """Crawl the content directory; for each markdown file, generate an .html file using the template and write it to the destination directory in the same directory structure."""
    content_path = Path(dir_path_content)
    dest_path = Path(dest_dir_path)
    for md_file in content_path.rglob("*.md"):
        rel = md_file.relative_to(content_path)
        html_rel = rel.with_suffix(".html")
        generate_page(
            str(md_file),
            template_path,
            str(dest_path / html_rel),
            basepath,
        )


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    print("Deleting docs directory...")
    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)

    print("Copying static files to docs directory...")
    copy_directory(dir_path_static, dir_path_docs)

    print("Generating pages...")
    generate_pages_recursive(
        dir_path_content, template_path, dir_path_docs, basepath
    )


if __name__ == "__main__":
    main()
