# Publishing to GitHub

## 上传前检查

在仓库根目录运行：

```bash
python scripts/validate_skill.py skills/learn-by-evidence
python scripts/validate_cases.py tests/cases.json
python -m unittest discover -s tests -p "test_*.py"
```

确认以下内容符合预期：

- `plugin.json` 的版本号正确；
- `CHANGELOG.md` 已记录本次变化；
- 没有真实学习记录、账号、密钥或私人对话；
- 根目录 `LICENSE` 为标准 MIT License，版权名和年份正确；
- `tests/cases.json` 覆盖本次行为变化。

## 方法一：GitHub 网页上传

1. 在 GitHub 创建空仓库，建议命名为 `learn-by-evidence`。
2. 不要让 GitHub 自动添加 README、许可证或 `.gitignore`，以免与项目已有文件冲突。
3. 解压交付包。
4. 将 `learn-by-evidence/` 目录内的所有文件上传到仓库根目录。
5. 提交后确认 GitHub Actions 的 `Validate skill` 工作流通过。

## 方法二：命令行上传

在解压后的项目根目录执行：

```bash
git init
git add .
git commit -m "Initial release: learn-by-evidence v1.0.0"
git branch -M main
git remote add origin https://github.com/<your-account>/learn-by-evidence.git
git push -u origin main
```

将 `<your-account>` 替换成你的 GitHub 用户名或组织名。执行前先在 GitHub 创建同名空仓库。

## 建议的仓库信息

- Repository name：`learn-by-evidence`
- Description：`Evidence-based cross-domain learning coach for ChatGPT, Codex, and Agent Skills compatible runtimes.`
- Topics：`agent-skills`、`codex`、`chatgpt`、`ai-tutor`、`adaptive-learning`、`education`
- 默认分支：`main`

## 首个 Release

校验通过后可创建 `v1.0.0` 标签和 GitHub Release：

```bash
git tag -a v1.0.0 -m "Learn by Evidence v1.0.0"
git push origin v1.0.0
```

Release 说明可直接摘取 `CHANGELOG.md` 的 `1.0.0` 小节。

## 许可证状态

项目采用 MIT License，标准文本位于仓库根目录的 `LICENSE`。发布前不要删改其中的版权与许可声明；若未来更换许可证，应先确认既有版本、外部贡献和第三方内容是否允许变更，并同步更新 README 与 Release 说明。
