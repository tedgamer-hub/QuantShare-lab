# -*- coding: utf-8 -*-
"""
仅整理 Notebook 的版式（封面宽度、HTML），便于 GitHub 渲染。

重要：本脚本不会删除任何 cell 的运行输出（outputs）。
若需上传 GitHub 前去掉输出，请手动运行：
    python scripts/clear_notebook_outputs.py --confirm
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NB_DIR = ROOT / "notebooks" / "phase1_intro"
OLD_BANNER = "yibo quant.jpg"
NEW_BANNER = "yibo-quant.jpg"


def normalize_banner(source: list[str]) -> list[str]:
    text = "".join(source)
    if "yibo quant.jpg" in text or "yibo-quant.jpg" in text:
        return [
            '<p align="center">\n',
            f'  <img src="./{NEW_BANNER}" alt="课程封面" width="720"/>\n',
            "</p>\n",
        ]
    return source


def sanitize_markdown_html(source: list[str]) -> list[str]:
    text = "".join(source)
    text = re.sub(
        r'<div style="display:\s*flex[^"]*"[^>]*>\s*',
        "",
        text,
        flags=re.IGNORECASE,
    )
    text = text.replace("</div>", "")
    text = re.sub(r'width\s*=\s*["\']?\d{4,}["\']?', 'width="720"', text)
    return [line + ("\n" if not line.endswith("\n") else "") for line in text.splitlines(True)]


def prepare_notebook(path: Path) -> None:
    nb = json.loads(path.read_text(encoding="utf-8"))
    nb["nbformat"] = 4
    nb["nbformat_minor"] = 4
    nb.setdefault("metadata", {})
    nb["metadata"].pop("widgets", None)

    for cell in nb.get("cells", []):
        # 不修改 outputs / execution_count，保留你本地运行结果
        if cell.get("cell_type") == "markdown":
            src = cell.get("source", [])
            if src and ("yibo quant" in "".join(src) or "yibo-quant" in "".join(src)):
                cell["source"] = normalize_banner(src)
            elif "<div" in "".join(src) or 'width="3000"' in "".join(src):
                cell["source"] = sanitize_markdown_html(src)

    text = json.dumps(nb, ensure_ascii=False, indent=1)
    text = text.replace(OLD_BANNER, NEW_BANNER)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    old = NB_DIR / OLD_BANNER
    new = NB_DIR / NEW_BANNER
    if old.exists() and not new.exists():
        new.write_bytes(old.read_bytes())
    for path in sorted(NB_DIR.glob("0*.ipynb")):
        prepare_notebook(path)
        outs = sum(len(c.get("outputs", [])) for c in json.loads(path.read_text(encoding="utf-8"))["cells"])
        print(f"prepared {path.name} ({path.stat().st_size // 1024} KB, outputs kept: {outs} items)")


if __name__ == "__main__":
    main()
