# quant-for-beginners 代码全集与逐段讲解

本目录从原仓库自动提取全部教学代码单元、维护脚本、交互式 HTML、Markdown 围栏示例和关键配置。每个片段都有独立文件，同时在“讲解版”中附有用途、处理过程、输出、特点与依赖说明。

## 收录统计

| 类别 | 数量 | 说明 |
|---|---:|---|
| Notebook 代码单元 | 76 | 61 个非空代码单元，15 个原仓库空练习单元 |
| Notebook Markdown 内嵌示例 | 11 | 说明文字单元中的围栏代码、命令或伪代码 |
| Python 脚本 | 13 | `scripts/` 下的完整脚本 |
| 交互式 HTML | 7 | HTML、CSS、JavaScript 按完整文件保留 |
| Markdown 文档围栏示例 | 10 | README 文档中的命令和结构示例 |
| 项目配置 | 3 | requirements 与 Git 配置 |
| **总计** | **120** | 包含空练习单元占位 |

## 目录说明

- `讲解版/`：按原仓库章节和文件排列，每个代码片段单独成节并附中文讲解。
- `独立代码/`：每个片段都是可单独复制的原始文件；Notebook 内容按 `片段_序号_类型` 排列。
- `manifest.json`：记录每个片段的来源、位置、输出文件和 SHA-256，用于防遗漏核对。
- `校验报告.md`：统计数量并检查独立代码与原始内容是否一致。

> 说明：Notebook 单元常常依赖前面单元创建的变量，单独复制时需按章节顺序运行。二进制图片、Notebook 运行输出、普通说明文字和 `.gitkeep` 不属于代码片段，因此未重复复制。

## 讲解版索引

### Notebook 教学章节

- [01_什么是量化金融](讲解版/notebooks/phase1_intro/01_什么是量化金融.md)
- [02_你的第一个量化实验](讲解版/notebooks/phase1_intro/02_你的第一个量化实验.md)
- [03_移动平均线策略](讲解版/notebooks/phase1_intro/03_移动平均线策略.md)
- [04_策略回测](讲解版/notebooks/phase1_intro/04_策略回测.md)
- [01_理解波动率](讲解版/notebooks/phase2_intro/01_理解波动率.md)
- [02_夏普比率与Beta](讲解版/notebooks/phase2_intro/02_夏普比率与Beta.md)
- [03_最大回撤与仓位管理](讲解版/notebooks/phase2_intro/03_最大回撤与仓位管理.md)
- [04_多标的组合与相关性](讲解版/notebooks/phase2_intro/04_多标的组合与相关性.md)

### 仓库维护与生成脚本

- [为 phase1 四个 Notebook 的代码单元添加逐行中文注释。](讲解版/scripts/apply_notebook_comments.md)
- [生成 Beta 动态演示 HTML（数据来自 AkShare 美股日线）。](讲解版/scripts/build_beta_demo.md)
- [Build notebooks/phase2_intro/01_理解波动率.ipynb — full chapter content.](讲解版/scripts/build_ch05_volatility.md)
- [生成总体方差动态演示 HTML。](讲解版/scripts/build_population_variance_demo.md)
- [生成夏普比率动态演示 HTML（数据来自 AkShare 美股日线）。](讲解版/scripts/build_sharpe_demo.md)
- [生成方差修正四种公式合一的动态演示 HTML。](讲解版/scripts/build_variance_formulas_demo.md)
- [【仅在上传 GitHub 前手动使用】清除 Notebook 运行输出，减小体积、便于网页预览。](讲解版/scripts/clear_notebook_outputs.md)
- [第 2～4 章 Notebook 带注释源码。](讲解版/scripts/comment_data_ch2_4.md)
- [为 phase1_intro 下所有 notebook 的代码行补充中文行尾注释。](讲解版/scripts/comment_phase1_notebooks.md)
- [Generate Phase 2 notebook skeletons for notebooks/phase2_intro/.](讲解版/scripts/generate_phase2_notebooks.md)
- [Generate README showcase images (run from repo root).](讲解版/scripts/generate_showcase_images.md)
- [仅整理 Notebook 的版式（封面宽度、HTML），便于 GitHub 渲染。](讲解版/scripts/prepare_github_notebooks.md)
- [打包第二期内容到 quant-for-beginners-Alpha 发布目录。](讲解版/scripts/publish_phase2_alpha.md)

### 交互式 HTML 演示

- [Beta 动态演示 · Quant for Beginners](讲解版/assets/interactive/beta-demo.md)
- [布朗运动与随机游走 · 交互可视化](讲解版/assets/interactive/brownian-random-walk.md)
- [日收益率动态演示 · Quant for Beginners](讲解版/assets/interactive/daily-return-demo.md)
- [总体方差动态演示 · Quant for Beginners](讲解版/assets/interactive/population-variance-demo.md)
- [夏普比率动态演示 · Quant for Beginners](讲解版/assets/interactive/sharpe-ratio-demo.md)
- [样本标准差动态演示 · Quant for Beginners](讲解版/assets/interactive/std-dev-demo.md)
- [方差修正四种公式 · 动态演示](讲解版/assets/interactive/variance-formulas-demo.md)

### Markdown 文档中的代码示例

- [README.md 文档示例](讲解版/markdown_examples/README.md)
- [assets/interactive/README.md 文档示例](讲解版/markdown_examples/assets/interactive/README.md)

### 其他

- [项目配置](讲解版/项目配置.md)

## 建议阅读顺序

先阅读 `讲解版/notebooks/phase1_intro/`，再阅读 `phase2_intro/`；需要了解课程资料如何生成时再看 `讲解版/scripts/`，交互网页则可直接打开 `独立代码/assets/interactive/*.html`。

生成时间：2026-09-01 11:29:37 CST
