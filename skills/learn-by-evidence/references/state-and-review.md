# 学习状态与复习协议

## 存放与读取

不同主题用独立记录；文件名可用 learning/<topic>/state.md，实际位置服从宿主文件规则。关联资料与速查表，不复制无关对话或私人信息。

恢复时读取最新可用记录，优先用户当前修正。字段缺失标未知；记录陈旧、冲突或证据不足时只复核受影响能力，避免全部重学。没记录时说明缺口并问一个恢复问题。

写入前读取当前版本，保留既有证据与其它主题，按宿主版本机制更新。发生冲突先读最新版本并合并增量，不用陈旧记录整体覆盖。

## 最小记录模板

这是字段约定，不是必须采用的数据库或严格 JSON schema。小主题可用 Markdown。

```yaml
schema_version: 1
topic_id: topic-slug
record_version: 1
updated_at: null  # 真实保存时间；无法取得不编造
learning_goal: null
constraints: {session_minutes: null, deadline: null, language: zh}
current_level: {self_report: null, observed: null}
current_unit: null
phase: assess  # assess/plan/teach/practice/repair/check/paused
materials: []  # 来源、版本/日期、核验状态
capability_map: []
# 每项：id, observable_goal, exposure, level, verification,
#       evidence_ids, limitations, retention
# exposure: unseen/introduced/practiced
# level: null/理解/可在提示下完成/可独立完成/可解释与迁移
# verification: unverified/provisional/verified/needs_recheck
# retention: untested/retained/needs_review
mastery_gates: []
# 每项：unit_id, criteria, required_evidence, evidence_ids,
#       status(pending/passed/not_yet_met/skipped)
known_weaknesses: []
mistake_patterns: []  # 模式及依据；一次失误先作候选
completed_exercises: []
# 每项：id, capability_ids, task_summary, user_answer_summary,
#       rubric, result, support(none/hint/scaffold/worked_example),
#       answer_exposed, context, observed_at
review_queue: []
# 每项：capability_id, reason, suggested_when, status
cheat_sheets: []
resource_shortlist: []
pending_task: null  # 待答题原文，提示/答案是否已展示
next_action: null
```

只填真实获得的信息。level: null 加 exposure: introduced 表达“讲过，尚未验证理解”。有反证时保留历史，标 needs_recheck，再据新证据调整。

## 更新证据

1. 先记答题条件：新题还是看过答案、无提示还是有帮助。
2. 记录可审计的答案摘要与判定理由，不只留分数。
3. 只更新真正检验过的能力；题目挂了多个标签不等于每项都得到可评分证据。
4. 用独立证据判断晋级，不用同题多次复述凑次数。
5. 讲解、助手示范、自述和阅读不等于独立作答。
6. 资料版本变化时复核证据适用性，保留旧版本下结论。

## 复习选择

按当前单元关键前置缺口 → 到期或久未验证能力 → 高频易混项 → 新知识排序；选本次时间允许的一项开始。

可提议次日、约一周后再复习，明确为可调整建议，不是遗忘概率预测，也不是已创建提醒。

延迟复习用无提示且有变化的题。通过记保持证据；失败定位缺口、短补漏、换题再检验。疲劳、题意歧义、输入错误可能影响结果，不凭一次失败抹掉全部历史能力。

## 结束与交接

最小交接：目标、材料版本、已验证能力与证据摘要、未验证/薄弱点、待答题及答案是否暴露、下一步。用户要求停止时不追加新题。

保存失败时说明，并给可复制记录，不说“下次自动记得”。
