# China Quant Research Skill

面向 A 股、ETF 与中国公募基金的 Codex 量化基本面研究 Skill。它接收用户提供的行情、净值、财务或持仓数据，在原有数据质量与量化分析工作流中加入市场预期、Thesis、反方研究、Fundamental/Quant 冲突处理、情景分析和 Thesis Break，并输出可复核的结构化报告。

本 Skill 不包含行情数据，不绑定单一数据商，也不执行交易。它可以直接分析用户上传的数据，并在客户端已经连接 FTShare 等数据工具时按需补充数据。

## 核心能力

- 保持固定七步流程：识别任务、检查输入、判断数据充分性、共通分析、资产分支、风险检查、报告输出。
- 允许给出明确但有条件的研究倾向，同时主动寻找最强反方证据。
- 用市场预期、Edge–Risk–Odds、Bull/Base/Bear 和 Thesis Break 组织判断；没有数据时不硬填概率或目标价。
- 独立比较基本面与量化证据，解释冲突而不是机械平均评分。
- 保留 No Edge / 需要更多数据作为有效结论，不为了回答而制造买卖建议。

完整英文单文件草案见 `china-quant-research-English-Version.md`。

## 安装

将整个 `QuantShare-lab` 目录放入 Codex Skills 目录：

```bash
git clone https://github.com/tedgamer-hub/QuantShare-lab.git
cp -R QuantShare-lab ~/.codex/skills/
```

重新启动 Codex 或新建任务后即可使用。

## 使用示例

显式调用：

```text
使用 $china-quant-research 分析我上传的 3 只 ETF 日线数据，
比较近一年收益、最大回撤、波动、流动性和跟踪质量，
运行风险检查并输出研究报告。
```

```text
使用 $china-quant-research 研究 600519.SH。
我提供了日线行情和最近八个季度财务数据；请检查复权和披露时点，
与合适基准比较，建立 Thesis、寻找最强反方证据并写明 Thesis Break，
只对数据能够支持的结论负责。
```

```text
使用 $china-quant-research 比较这些公募基金的净值表现。
处理 A/C 份额差异、基金经理任期和持仓披露滞后，
识别可持续优势或明确 No Edge，不要给买卖指令。
```

自动调用保持开启，因此用户也可以直接提出 A 股、ETF 或公募基金研究请求，由支持 Skills 的 Codex 环境自动选择本 Skill。

## 建议输入

可以上传 CSV、Excel、JSON 或直接粘贴表格。尽量包含标的代码、日期、字段单位、币种、数据频率、复权方式或净值口径；资料不齐时，Skill 会继续完成可支持的部分，并明确列出缺口。

## 可选数据工具

- **FTShare MCP**：适合由 Agent 按需查询 A 股、ETF、公募基金、指数、财务、宏观、公告和新闻等结构化数据，可直接参与自然语言研究工作流。
- **AkShare**：适合 Python 研究、公开数据批量采集和本地数据管线。AkShare 本身不是 MCP；如需让 Agent 直接调用，需要本地代码执行能力或另行连接相应 MCP 封装。
- **Yahoo Finance**：适合补充美股、海外 ETF、全球指数、外汇、期货与商品代理标的等数据，也可以为国内资产研究提供海外基准。可以使用用户导出的 CSV、Python 第三方 `yfinance` 库，或用户自行连接的 Yahoo Finance MCP/API 服务。使用时需核对交易所后缀、币种、时区、报价延迟、分红拆股和复权口径，并遵守数据许可及使用条款。
- **用户自有数据库或文件**：适合可复现研究、批量回测和长期数据治理。

任何外部数据工具都不是安装本 Skill 的强制依赖。

Yahoo Finance 对 A 股和中国公募基金的覆盖不应被假定为优于本地数据源；本 Skill 优先将其用于海外基准、跨市场比较和交叉验证。更完整的选择与风险说明见 `references/data-tools.md`。

## 发布前检查

- 为仓库选择并添加合适的开源许可证；未添加许可证不代表他人可以自由再分发。
- 将 README 中的仓库地址占位符替换为真实地址。
- 不要提交 API Key、账户信息、付费数据或无权分发的数据样本。
- 使用官方校验脚本检查 `SKILL.md` 与元数据。

## 免责声明

此 Skill 用于研究流程和信息整理，不提供收益保证，不构成个性化投资建议，也不执行下单或资金操作。数据质量、授权和最终投资决策由使用者负责。

## Contributors

- [xtraid](https://github.com/xtraid)
- [alibizho](https://github.com/alibizho)
