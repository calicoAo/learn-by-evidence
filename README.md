# Learn by Evidence

一个以“可观察能力证据”为核心的通用学习 Skill。它不会把“看过、讲过、答对一次”直接等同于掌握，而是通过能力地图、小步教学、单题练习、针对性补漏、迁移验证和复习记录形成闭环。

> 当前版本：`1.0.0`  
> 主要语言：中文  
> 适用范围：ChatGPT、Codex、支持 Agent Skills 的兼容环境

## 它解决什么问题

普通 AI 学习对话很容易变成：

```text
问一个大问题 → 得到一篇长教程 → 当时看懂 → 很快忘掉
```

Learn by Evidence 改成：

```text
确定目标和起点
→ 建立能力地图
→ 学一个最小知识块
→ 用户先尝试
→ 根据证据诊断
→ 只补当前缺口
→ 换一个情境再验证
→ 更新能力与复习状态
```

核心判断不是“已经讲了多少”，而是“用户现在能独立完成什么”。

## 核心能力

- 用可观察能力而不是章节名构建学习路线
- 支持完整课程、单次陪练、诊断、复习和速查表
- 默认一次只留一个待答任务，避免认知过载
- 区分用户自述、提示下完成、独立完成和迁移能力
- 答错时只修复实际缺口，并使用新任务重新检验
- 尊重“只要地图”“直接告诉我答案”“批量出题”“今天停止”等明确要求
- 适配编程、数学、概念、考试、语言、创作和实操技能
- 生成可复制的学习 checkpoint（检查点）与复习队列
- 防止虚假掌握、答案泄露、伪造保存和旧资料当作现行规则

## 项目结构

```text
learn-by-evidence/
├── plugin.json                       # 便携式插件清单
├── skills/
│   └── learn-by-evidence/            # 可独立使用的 Skill
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       ├── assets/icon.svg
│       └── references/
│           ├── domain-adaptation.md
│           └── state-and-review.md
├── docs/
│   ├── ARCHITECTURE.md
│   ├── PUBLISHING.md
│   └── TESTING.md
├── examples/
│   ├── prompts.md
│   └── checkpoint.yaml
├── scripts/
│   ├── validate_skill.py
│   └── validate_cases.py
├── tests/
│   ├── cases.json
│   └── test_validator.py
└── .github/workflows/validate.yml
```

仓库级说明、测试和 CI 位于 Skill 目录之外，避免它们在 Skill 触发后占用模型上下文。

## 安装与使用

### 作为 Skill 使用

将 [`skills/learn-by-evidence`](skills/learn-by-evidence) 整个目录放入宿主支持的 Skills 位置，或让宿主从 `skills/` 目录发现 Skill。目录内的 `SKILL.md` 是必需入口，`references/`、`assets/` 和 `agents/` 应一并保留。

OpenAI 官方文档说明：每个 Skill 都应位于独立目录并包含 `SKILL.md`，详细背景资料放在 `references/`，可复用资源放在 `assets/`，确定性执行代码放在 `scripts/`。具体导入方式以当前宿主为准：

- [Build skills — OpenAI Developers](https://developers.openai.com/plugins/build/skills)
- [Skills — OpenAI API](https://developers.openai.com/api/docs/guides/tools-skills)

### 作为便携式插件使用

仓库根目录包含 `plugin.json`，Skill 位于标准的 `skills/` 目录。支持 Agent Plugin 格式的宿主可从仓库根目录读取该插件。

### 显式调用

```text
使用 $learn-by-evidence 带我学习 Agent Memory。
先根据我的目标建立能力地图，不要立即开始讲课。
```

Skill 也允许隐式触发，例如：

```text
继续昨天的 Retrieval 学习，从我的薄弱点开始，一次问一道题。
```

## 常用场景

```text
# 建立路线
我想用两个月系统学习 SQL。先给学习地图和过关标准。

# 单题陪练
考我 JavaScript 闭包，一次只问一道题。

# 概念诊断
我总分不清 eventTime、validTime 和 recency，帮我定位问题。

# 项目型学习
带我做一个小型 RAG 项目，但第一版代码让我自己写。

# 续学
读取这份 checkpoint，从尚未验证的能力开始。

# 停止与交接
今天先到这里，不要再出题，帮我留下下次恢复点。
```

更多示例见 [examples/prompts.md](examples/prompts.md)。

## 本地验证

项目只使用 Python 标准库，无需安装依赖：

```bash
python scripts/validate_skill.py skills/learn-by-evidence
python scripts/validate_cases.py tests/cases.json
python -m unittest discover -s tests -p "test_*.py"
```

验证内容包括：

- Skill frontmatter 与名称格式
- 支持文件引用完整性
- UI 元数据与默认调用提示
- TODO/占位内容残留
- 测试用例结构与 ID 唯一性
- 校验器自身的正反例单元测试

完整测试策略和当前结果见 [docs/TESTING.md](docs/TESTING.md)。

准备创建 GitHub 仓库时，按 [docs/PUBLISHING.md](docs/PUBLISHING.md) 操作。

## 设计边界

- “循证”指能力判断必须有用户表现作为证据，不宣称该 Skill 已通过教育学临床实验验证。
- Skill 可以建议复习时间，但没有成功创建自动化任务时，不会声称已经设置提醒。
- 没有持久化能力时，只返回可复制 checkpoint，不会声称能够跨会话自动记住。
- 医学、法律、金融等主题中的学习练习不等于个体化专业建议。
- Skill 不强制把所有一次性问答改造成课程。

## 贡献

提交修改前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)，并运行全部验证命令。行为修改应同时增加或更新 `tests/cases.json` 中的回归用例。

## 许可

本项目采用 [MIT License](LICENSE)。你可以使用、修改、分发和商业化本项目，但必须保留版权与许可声明。软件按“原样”提供，不附带任何担保。
