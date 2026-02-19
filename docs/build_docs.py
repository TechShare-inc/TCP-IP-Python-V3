"""Generate API markdown and build the VitePress site.

Usage:
    python docs/build_docs.py --api-only
    python docs/build_docs.py --site-only
    python docs/build_docs.py
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


def run_command(command: list[str], cwd: Path) -> None:
    """Run a shell command and fail fast on error."""
    subprocess.run(command, cwd=str(cwd), check=True)


def sync_markdown(api_source_dir: Path, api_target_dir: Path) -> None:
    """Copy generated markdown files into the VitePress reference folder."""
    api_target_dir.mkdir(parents=True, exist_ok=True)

    for markdown_file in api_target_dir.glob("*.md"):
        markdown_file.unlink()

    for markdown_file in api_source_dir.glob("*.md"):
        shutil.copy2(markdown_file, api_target_dir / markdown_file.name)


def build_api_docs(project_root: Path) -> None:
    """Generate markdown files from Sphinx sources."""
    sphinx_source_dir = project_root / "docs" / "sphinx"
    api_output_dir = project_root / "docs" / "_autogen"
    api_target_dir = project_root / "docs" / "reference" / "api"

    run_command(
        [
            "sphinx-build",
            "-b",
            "markdown",
            str(sphinx_source_dir),
            str(api_output_dir),
        ],
        cwd=project_root,
    )

    sync_markdown(api_output_dir, api_target_dir)


def build_site(project_root: Path) -> None:
    """Build VitePress static site."""
    docs_dir = project_root / "docs"
    run_command(["npm", "run", "docs:build"], cwd=docs_dir)


def parse_args() -> argparse.Namespace:
    """Parse CLI options."""
    parser = argparse.ArgumentParser(description="Build docs pipeline")
    parser.add_argument(
        "--api-only", action="store_true", help="Build API markdown only"
    )
    parser.add_argument(
        "--site-only", action="store_true", help="Build VitePress site only"
    )
    return parser.parse_args()


def main() -> None:
    """Entrypoint for docs build script."""
    args = parse_args()
    project_root = Path(__file__).resolve().parents[1]

    if args.api_only and args.site_only:
        raise ValueError("--api-only and --site-only cannot be used together")

    if args.site_only:
        build_site(project_root)
        return

    build_api_docs(project_root)
    if not args.api_only:
        build_site(project_root)


if __name__ == "__main__":
    main()
