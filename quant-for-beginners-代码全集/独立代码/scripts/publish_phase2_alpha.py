# -*- coding: utf-8 -*-
"""打包第二期内容到 quant-for-beginners-Alpha 发布目录。"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT.parent / "quant-for-beginners-Alpha"

NOTEBOOKS = [
    "01_理解波动率.ipynb",
    "02_夏普比率与Beta.ipynb",
    "03_最大回撤与仓位管理.ipynb",
    "04_多标的组合与相关性.ipynb",
]
IMAGES = [
    "Benoit Mandelbrot.jpg",
    "Harry Markowitz.jpg",
    "Robert Engle.jpg",
    "yibo quant.jpg",
]
HTML = [
    "daily-return-demo.html",
    "std-dev-demo.html",
    "population-variance-demo.html",
    "variance-formulas-demo.html",
    "sharpe-ratio-demo.html",
    "beta-demo.html",
    "README.md",
]

GITIGNORE = """# Python
__pycache__/
*.py[cod]
.venv/
venv/

# Jupyter
.ipynb_checkpoints/
.virtual_documents/

# IDE
.vscode/
.idea/
.cursor/

# OS
.DS_Store
Thumbs.db
"""

README = """# quant-for-beginners-Alpha · 第二期

《和Yibo零基础学习量化金融》**第二期**（第 5～8 章）：

| 章 | Notebook |
|----|----------|
| 5 | [01_理解波动率](notebooks/phase2_intro/01_理解波动率.ipynb) |
| 6 | [02_夏普比率与Beta](notebooks/phase2_intro/02_夏普比率与Beta.ipynb) |
| 7 | [03_最大回撤与仓位管理](notebooks/phase2_intro/03_最大回撤与仓位管理.ipynb) |
| 8 | [04_多标的组合与相关性](notebooks/phase2_intro/04_多标的组合与相关性.ipynb) |

## 快速开始

```bash
pip install -r requirements.txt
jupyter lab
```

交互演示见 [assets/interactive/README.md](assets/interactive/README.md)。

**推荐 Python 3.10+**
"""


def clear_notebook_outputs(path: Path) -> None:
    nb = json.loads(path.read_text(encoding="utf-8"))
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "code":
            cell["outputs"] = []
            cell["execution_count"] = None
    nb.get("metadata", {}).pop("widgets", None)
    path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")


def main() -> None:
    # 只更新内容，保留 .git / commit.py 等
    nb_dir = DEST / "notebooks" / "phase2_intro"
    html_dir = DEST / "assets" / "interactive"
    nb_dir.mkdir(parents=True, exist_ok=True)
    html_dir.mkdir(parents=True, exist_ok=True)

    src_nb = ROOT / "notebooks" / "phase2_intro"
    for name in NOTEBOOKS + IMAGES:
        shutil.copy2(src_nb / name, nb_dir / name)

    src_html = ROOT / "assets" / "interactive"
    for name in HTML:
        shutil.copy2(src_html / name, html_dir / name)

    shutil.copy2(ROOT / "requirements.txt", DEST / "requirements.txt")
    (DEST / ".gitignore").write_text(GITIGNORE, encoding="utf-8")
    (DEST / "README.md").write_text(README, encoding="utf-8")

    for path in nb_dir.glob("*.ipynb"):
        clear_notebook_outputs(path)
        print(f"cleared: {path.name}")

    print(f"\nDone -> {DEST}")


if __name__ == "__main__":
    main()
