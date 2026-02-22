"""Documentation API — serves C³-Brain F1-F12 markdown files."""

from pathlib import Path

from fastapi import APIRouter, HTTPException, Query

from config import BRAIN_DOCS_DIR

router = APIRouter()


def _build_tree(root: Path, base: Path = None) -> dict:
    """Recursively build directory tree for the docs browser."""
    if base is None:
        base = root
    result = {
        "name": root.name,
        "type": "directory",
        "path": str(root.relative_to(base)),
        "children": [],
    }
    for item in sorted(root.iterdir()):
        if item.name.startswith("."):
            continue
        if item.is_dir():
            result["children"].append(_build_tree(item, base))
        elif item.suffix == ".md":
            result["children"].append({
                "name": item.name,
                "type": "file",
                "path": str(item.relative_to(base)),
            })
    return result


@router.get("/tree")
async def docs_tree():
    """Get the full directory tree of C³-Brain documentation."""
    if not BRAIN_DOCS_DIR.exists():
        raise HTTPException(status_code=404, detail="Documentation directory not found")
    return _build_tree(BRAIN_DOCS_DIR)


@router.get("/content")
async def docs_content(path: str = Query(..., description="Relative path within C³-Brain")):
    """Get markdown content of a specific document."""
    full_path = BRAIN_DOCS_DIR / path
    # Security: ensure path stays within docs dir
    try:
        full_path.resolve().relative_to(BRAIN_DOCS_DIR.resolve())
    except ValueError:
        raise HTTPException(status_code=403, detail="Path traversal not allowed")
    if not full_path.exists() or not full_path.is_file():
        raise HTTPException(status_code=404, detail=f"Document not found: {path}")
    return {"content": full_path.read_text(encoding="utf-8"), "path": path}
