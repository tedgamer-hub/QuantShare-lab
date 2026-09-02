# 【仅在上传 GitHub 前手动使用】清除 Notebook 运行输出，减小体积、便于网页预览。

该文件在原仓库中是一个完整的 Python 脚本，因此作为一个独立代码片段收录。

## 代码片段 01：【仅在上传 GitHub 前手动使用】清除 Notebook 运行输出，减小体积、便于网页预览。

- 原始位置：`scripts/clear_notebook_outputs.py`
- 所属小节：仓库维护与内容生成
- 用途：自动化生成、整理或发布仓库中的教学材料，减少手工维护 Notebook、图片和交互页面的工作量。
- 处理过程：导入本段所需的计算、数据处理或绘图库；封装可复用函数，减少后续单元中的重复计算；通过循环批量处理多个标的、参数或交易区间；打印关键数值，便于核验中间结果和最终指标。
- 运行结果：终端/单元格文字摘要、写入磁盘的文件。
- 代码特点：环境准备、函数封装、批量处理、结果展示
- 主要依赖：__future__、argparse、json、sys、pathlib

### 原始代码

```python
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
```

---
