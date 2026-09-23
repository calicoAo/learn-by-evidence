# Contributing

感谢你改进 Learn by Evidence。

## 修改原则

1. 保持 `SKILL.md` 聚焦可执行流程，不把仓库说明、测试报告或长篇背景塞入 Skill。
2. 把领域差异和状态协议放入 `references/`，并从 `SKILL.md` 明确说明何时读取。
3. 尊重用户明确指令。Skill 的默认节奏不能覆盖“直接回答、批量出题、停止”等请求。
4. 任何能力升级都必须能追溯到用户作答、作品或行为证据。
5. 不把助手示范、已展示答案、自述或同题复述计为独立掌握。

## 提交流程

1. 为行为变更增加或更新 `tests/cases.json`。
2. 运行：

   ```bash
   python scripts/validate_skill.py skills/learn-by-evidence
   python scripts/validate_cases.py tests/cases.json
   python -m unittest discover -s tests -p "test_*.py"
   ```

3. 在 Pull Request 中说明：

   - 修改解决了什么学习问题；
   - 哪些输入应该或不应该触发 Skill；
   - 对能力判断、提示强度或状态更新有什么影响；
   - 新增了哪些回归用例。

## 前向测试

涉及教学节奏、诊断或掌握门槛的修改，应在干净上下文中测试。只向被测模型提供 Skill 和真实用户请求，不提前透露预期答案或怀疑的缺陷。

保存原始输入与输出，并按 [docs/TESTING.md](docs/TESTING.md) 的评分规则判断。不要只检查“回答看起来不错”，还要检查是否保留用户思考机会、是否虚报掌握、是否遵守停止条件。

## 许可提示

本项目采用 MIT License。提交贡献即表示你有权提供相关内容，并同意该贡献按本仓库的 MIT License 分发。
