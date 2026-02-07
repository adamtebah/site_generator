import logging
import shutil
from pathlib import Path


def copy_directory(src: str, dst: str) -> None:
    """
    Recursively copy all files and subdirectories from src to dst.
    Creates destination directories as needed. Logs each file copied.
    """
    src_path = Path(src).resolve()
    dst_path = Path(dst).resolve()

    if not src_path.is_dir():
        raise FileNotFoundError(f"Source is not a directory: {src_path}")

    dst_path.mkdir(parents=True, exist_ok=True)

    for item in src_path.iterdir():
        dest_item = dst_path / item.name
        if item.is_file():
            shutil.copy2(item, dest_item)
            logging.info("Copied: %s -> %s", item, dest_item)
        elif item.is_dir():
            copy_directory(str(item), str(dest_item))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    project_root = Path(__file__).resolve().parent.parent
    copy_directory(str(project_root / "static"), str(project_root / "public"))
