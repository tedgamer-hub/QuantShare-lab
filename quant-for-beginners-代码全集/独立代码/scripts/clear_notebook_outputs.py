# -*- coding: utf-8 -*-
"""
【仅在上传 GitHub 前手动使用】清除 Notebook 运行输出，减小体积、便于网页预览。

默认不会自动运行。必须加 --confirm 才会执行，避免误删本地结果：

    python scripts/clear_notebook_outputs.py --confirm
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NB_DIR = ROOT / "notebooks" / "phase1_intro"


def clear_notebook(path: Path) -> tuple[int, int, int]:
    before = path.stat().st_size
    nb = json.loads(path.read_text(encoding="utf-8"))
    cleared = 0
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        if cell.get("outputs") or cell.get("execution_count") is not None:
            cleared += 1
        cell["outputs"] = []
        cell["execution_count"] = None
    path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    after = path.stat().st_size
    return before, after, cleared


def main() -> None:
    parser = argparse.ArgumentParser(description="清除 Notebook 输出（需显式确认）")
    parser.add_argument(
        "--confirm",
        action="store_true",
        help="确认删除所有代码单元的 outputs（不可恢复，请先备份或已提交 git）",
    )
    args = parser.parse_args()
    if not args.confirm:
        print(
            "未执行：请加 --confirm 才会清除输出。\n"
            "示例：python scripts/clear_notebook_outputs.py --confirm\n"
            "本地学习请直接 Run All，不要运行本脚本。",
            file=sys.stderr,
        )
        sys.exit(1)

    paths = sorted(NB_DIR.glob("0*.ipynb"))
    if not paths:
        print("No notebooks found.", file=sys.stderr)
        sys.exit(1)
    for path in paths:
        before, after, n = clear_notebook(path)
        print(
            f"{path.name}: {before/1024:.0f} KB -> {after/1024:.0f} KB "
            f"(cleared {n} code cells)"
        )


if __name__ == "__main__":
    main()
