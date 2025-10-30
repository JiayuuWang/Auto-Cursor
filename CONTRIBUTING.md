# Contributing to Auto-Cursor · Auto-Cursor 贡献指南

Thank you for helping us build a resilient GUI-native agent. 谢谢你愿意参与构建这个稳健的 GUI 原生智能体。

---

## Ground Rules · 基本原则
- **Open collaboration 开放协作**：欢迎任何新想法，优先讨论问题而非个人。
- **User trust 用户信任**：所有改动都应提升系统稳定性、透明度或可维护性。
- **Accessibility 可达性**：文档、界面与交互应兼顾多操作系统与不同分辨率的用户。
- **Security first 安全优先**：请避免引入泄露密钥、越权操作等潜在安全风险。

---

## Getting Started · 快速上手
1. **Fork & Clone 仓库复制**
   ```bash
   git clone https://github.com/<your-username>/Auto-Cursor.git
   cd Auto-Cursor
   ```
2. **Create Virtual Environment 创建虚拟环境**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate # macOS / Linux
   ```
3. **Install Dependencies 安装依赖**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure Secrets 配置密钥**
   - Copy `.env.example` (if provided) or create `.env` manually.
   - Set at least one LLM provider key (`OPENAI_API_KEY`, `OPENROUTER_API_KEY`, `GEMINI_API_KEY`).
5. **Adjust Regions 配置屏幕区域**
   - Duplicate `config.yaml` to a safe copy.
   - Follow the README guide to measure `timestamp_region`, `terminal_region`, and `cursor_region`.

---

## Development Workflow · 开发流程
- **Issue First 先开 Issue**：为每个功能或缺陷创建 Issue，描述动机、风险与测试计划。
- **Feature Branch 特性分支**：`git checkout -b feature/<slug>` 或 `fix/<slug>`。
- **Tests & Logs 测试与日志**：
  - 请确保自动化脚本在你的屏幕配置下运行正常。
  - 为新增的自动化步骤添加必要的日志，便于排查。
- **Pull Request 提交 PR**：
  - 关联 Issue，概述改动、动机与测试结果。
  - 截图/录屏展示 GUI 自动化行为是强烈推荐的。

---

## Coding Guidelines · 代码规范
- **Python Style**：遵循 PEP 8，保持函数短小、单一职责。
- **Type Hints 类型标注**：对外部接口、核心模块补充类型注解与 docstring。
- **Logging 日志**：使用标准库 `logging`，避免 `print`。
- **Configuration 配置管理**：不要硬编码坐标；使用 `config.yaml` 或新增配置项。
- **Safety Checks 安全检查**：自动化动作需考虑异常场景（窗口失焦、截图失败等）。

---

## Pull Request Checklist · PR 自检清单
- [ ] Tests: 本地验证自动化脚本至少 1 次。
- [ ] Docs: 更新 README / docstrings / 注释。
- [ ] Screens: 提供必要的截图或录屏说明 GUI 行为。
- [ ] Security: 未泄露任何密钥或敏感路径。
- [ ] Lint: 通过基本语法检查，无明显静态扫描警告。

---

## Communication · 沟通方式
- 使用 GitHub Discussions / Issues 交流需求、愿景与实现细节。
- 若涉及安全问题，请参考 `SECURITY.md` 进行私下反馈。

---

## Recognition · 致谢
我们遵循贡献者公约（Contributor Covenant），期待与每位贡献者共建健康的开源生态。感谢你的时间与智慧！

