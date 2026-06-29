---
date : '2026-06-29T10:00:00+08:00'
draft : false
title : 'OpenSpec的使用经验和最佳实践'
image : ""
categories : ["AI Coding"]
tags : ["OpenSpec", "Spec Coding"]
description: "在多个真实项目中沉淀下来的 OpenSpec 使用经验——从初始化到归档的六阶段最佳实践、常见踩坑与避坑指南，以及和 TDD、Claude Code 配合的进阶玩法。"
---

## 🧭 引言：从"会跑"到"跑得稳"

在上一篇《[OpenSpec 的概念与基本使用](../OpenSpec的概念与基本使用/index.zh-cn.md)》里，我们把 OpenSpec 的双文件夹模型、核心命令和最小流程跑通了一遍。但"能跑"和"跑得稳"之间，还隔着大量实战细节。

这一篇是经验复盘：把过去几个月在多个真实项目里踩过的坑、验证过的做法，整理成一份"避坑指南 + 最佳实践"合集。读完它，你应该能避免 80% 的常见返工。

整篇文章围绕 OpenSpec 生命周期的六个关键阶段展开：

| 阶段  | 关键词       | 核心目标                |
| --- | --------- | ------------------- |
| 初始化 | 选工具、选模式   | 搭建最少够用的工作环境          |
| 提案  | 输入质量、权重分配 | 把模糊意图压缩成可执行合同        |
| 实现  | 任务粒度、节奏控制 | 让 AI 严格按合同办事         |
| 验证  | 报告解读、自检   | 关闭变更前最后一道关           |
| 归档  | 留痕、活文档    | 让 `specs/` 反映系统真实状态   |
| 协作  | Git、Review | 多人多 Agent 共享同一份真相源 |

---

## 🎚️ Core vs Expanded 模式选择

OpenSpec 有两种工作模式（用 `openspec config profile` 切换）：

- **Core 模式**（默认）：`propose → apply → archive` 三个命令，够 80% 的项目用。
- **Expanded 模式**：额外解锁 `new`、`continue`、`ff`、`verify`、`bulk-archive`、`onboard`。

我的建议是：

> **默认 Core，复杂项目再 Expanded**。

理由很简单——命令越多，记忆负担越大，反而拖慢节奏。`verify` 和 `bulk-archive` 这两个命令看起来很香，但 `verify` 的输出经常和"直接跑测试"重复；`bulk-archive` 适合"一次性交付多个 feature"的场景，平时几乎用不上。

如果你一定要切到 Expanded，**至少先熟练 Core 一周再切**。一来就上 10 个命令的团队，几乎都会出现"忘了某个命令是干嘛的"的问题。

---

## 💬 前期沟通优先：先 explore 再动手

这是我踩过最多坑后学到的教训。在创建变更前，一定要先用 explore 和 AI 对齐需求边界。

```markdown
❌ 错误做法：
"/opsx/ff 给模型推理服务加个缓存"

✅ 正确做法：
"/opsx/explore 我想给模型推理服务加缓存，你帮我分析一下：
1. 缓存应该加在哪一层？
2. 用 Redis 还是本地 LRU？
3. 缓存 key 怎么设计？"
```

AI也会提出它认为还不够明确的地方，可以和AI进行多轮沟通，直到双方都充分理解需求并设计出具体的方案，再执行 /opsx:propose 或 /opsx:ff。

---

## 🎯 propose 阶段：把"模糊意图"压成"可执行合同"

`/opsx:propose` 是 OpenSpec 流程的"重头戏"——它决定后续 80% 的工作量。这一阶段的核心矛盾是：**人脑子里"大概想要的东西"** 和 **AI 需要的"可执行合同"** 之间，存在巨大的表达差。

### 📋 需求描述的"黄金模板"

我用得最多的需求描述模板（**五段式**）：

```text
1. 背景：为什么要做这个变更？（业务上下文）
2. 目标：完成什么之后可以认为"做完了"？（可衡量的成功标准）
3. 范围：包含什么 / 不包含什么？（边界）
4. 关键约束：性能、兼容性、API 风格、安全等硬性要求
5. 验收示例：给出 1~2 个具体的输入-输出对
```

举例——同样是"加个用户头像上传功能"，两种描述差很多：

```text
❌ 差：帮我加个用户头像上传。
✅ 好：
   - 背景：用户反馈个人主页没有头像，转化率低。
   - 目标：用户可在个人设置页上传 ≤2MB 的 jpg/png，刷新后生效。
   - 范围：仅做单头像上传，不做多头像、裁剪、特效。
   - 关键约束：必须 CDN 加速；老用户无头像时显示默认占位图。
   - 验收示例：上传 3MB 文件 → 弹错误提示；上传 1MB jpg → 主页立即显示。
```

**输入质量决定产物质量**——这是 OpenSpec 的第一性原理。

### ⚖️ proposal/design/specs/tasks 的权重

很多人误以为"四份文档权重一样"。实战经验是**严重不均**的：

| 文档         | 重要度  | 阅读优先级 | 写不好的代价            |
| ---------- | ---- | ----- | ----------------- |
| `proposal` | ⭐⭐   | 低（一次） | 范围失控，AI 跑偏        |
| `design`   | ⭐⭐⭐  | 中（一次） | 方案返工，多走弯路         |
| `specs/`   | ⭐⭐⭐⭐⭐ | 高（持续） | AI 实现时反复偏离，业务不达标   |
| `tasks`    | ⭐⭐⭐⭐ | 高（持续） | 任务粒度失控，apply 阶段失控 |

> **关键判断**：**`specs/` 的 ROI 远高于其他三份**。一个反模式是把 proposal 写得很长、spec 写得很短。Spec 才是 AI 在 apply 阶段"读"得最多的文件，验收场景越具体，AI 跑偏的概率越低。

### 🔍 提案 review checklist

`/opsx:propose` 跑完后，**不要直接 `/opsx:apply`**。先用这张清单自检：

- [ ] `proposal.md` 的"为什么"是否清晰，团队成员能 30 秒内 get 到意图？
- [ ] `design.md` 的关键技术选型是否有 trade-off 记录？（不是只给一个方案）
- [ ] `specs/` 中每个 Requirement 是否都用 `SHALL` 写明确？
- [ ] 每个 Requirement 是否有 2 个以上 Scenario 覆盖正常/异常路径？
- [ ] `tasks.md` 的任务粒度是否在 30 分钟~2 小时可完成？（粗了失控，细了过度）
- [ ] 范围"边界"是否在 proposal 里写明（哪些明确不做）？

这张清单过一遍，archive 阶段的返工率能下降一半。

---

## 🔧 apply 阶段：让 AI 真正"按合同办事"

`/opsx:apply` 是把 Markdown 变成代码的阶段。这一阶段最大的坑是**让 AI 一次跑完整个 tasks.md**——表面上高效，实际上埋雷无数。

### 📐 任务粒度：再小一点也不为过

**经验法则**：一个任务如果不能在 30 分钟~2 小时内独立验证，**就应该再拆**。

我常用的拆解方式：

| 任务粒度      | 适合什么                  | 风险           |
| --------- | --------------------- | ------------ |
| 30 分钟以内   | 单文件、单函数、配置项            | 几乎没风险，适合激进 AI |
| 1~2 小时    | 单模块、单个 API 端点          | 风险低，主流粒度     |
| 半天以上      | 跨模块、跨服务                | 风险高，必须配合 review |
| 跨两天以上     | 不应该作为一个任务存在            | 一定要拆         |

举个例子，"实现用户登录"会被我拆成：

```text
1. 数据库 schema 调整（加 last_login_at 字段）
2. 登录 service 函数（含密码校验、失败次数）
3. 登录 API 路由（带 rate limit）
4. 错误响应统一封装
5. 日志埋点
6. 单元测试（覆盖 5 个边界 case）
7. 集成测试（从 HTTP 入口到 DB 落库）
```

7 个子任务，每个独立可验证。AI 在任何一个上跑偏，review 时都能快速定位。

### ✋ 中途打断：让 AI 慢下来

`/opsx:apply` 的本质是"AI 自动跑完整个 tasks.md"。听起来很爽，但实战中**必须主动打断**。

打断的三个黄金时机：

1. **跨任务粒度切换时**——比如从"数据库层"切到"API 层"时，要求 AI 先暂停，汇报当前进展。
2. **遇到模糊点时**——AI 主动提问"这里用 try-catch 还是 Result 类型"时，**不要让它自己选**。
3. **发现 spec 有歧义时**——立即停下来，先改 spec，再继续 apply。

打断话术参考：

```text
"先停一下。回顾一下当前 tasks 1~3 的完成情况，列出已经修改的文件和未覆盖的边界 case，
我们 review 完再继续 4~7。"
```

这一招在长任务链里特别管用——AI 不会"闷头走到黑"，人在环路里始终能纠偏。

### 🧪 与 TDD 工具的配合

OpenSpec 管"做什么"，TDD 管"做得对不对"——两者缺一不可。

推荐组合：

```text
OpenSpec /opsx:apply  →  按 tasks 推进
   ↓ 每个子任务完成后
Superpowers test-driven-development  →  强制走 红-绿-重构
   ↓
下一个子任务
```

在 Claude Code 里的具体操作：

```text
# 1. OpenSpec 提出 tasks
/opsx:apply
# 2. 切到 TDD 模式（强制红绿循环）
/superpowers:test-driven-development
# 3. AI 会先写失败测试，再写最小实现
```

实战中这个组合能把"AI 自己写完然后发现测试挂了"的情况消灭掉。**AI 写测试 → AI 改实现 → 测试通过**，是一个稳定的反馈环。

---

## ✅ verify 与 archive 阶段：把好最后一道关

很多团队栽在"看起来对就 archive"这一步。**verify + archive 才是 OpenSpec 真正产生价值的地方**。

### 📊 如何读懂 verify 报告

`/opsx:verify` 会输出 CRITICAL / WARNING / SUGGESTION 三级问题。我的处理策略：

| 级别        | 含义        | 处理方式                |
| --------- | --------- | ------------------- |
| CRITICAL  | spec 强制约束被违反 | **必须修复**，否则不进 archive |
| WARNING   | 实现偏离但未触底  | 评估偏离原因，必要时回滚或调整 spec |
| SUGGESTION | 风格/可读性建议   | 记录到 backlog，不阻塞 archive |

实战经验：

- **CRITICAL 数量 ≠ 实现质量**——一个变更 0 CRITICAL 不代表完美，可能只是 spec 写得太松。
- **WARNING 集中在同一模块时**，往往是设计本身有问题，应该改 `design.md` 而不是改代码。
- **SUGGESTION 数量特别多时**，说明这个项目的 spec 风格没沉淀下来，应该在归档后顺手补一个 `AGENTS.md` 模板。

### 🛡️ 双保险验证机制

强烈建议：新开一个 Agent 窗口专门执行 verify 指令。原因很简单——让写代码的 AI 和检查代码的 AI 是"两个人"，避免"自己查自己"的盲区。
### 📦 archive 前的最终自检

archive 之前我会跑一张"四问清单"：

```text
1. 测过没有？  → 跑一遍测试套件，看是否有新增失败。
2. 看过没有？  → 把 changes/xxx/ 下的 proposal/design/specs/tasks 全部 review 一遍。
3. 退路有没有？ → Git 上有 commit/tag 能回滚到 archive 前的状态吗？
4. 文档同步没？ → 如果有 README、CHANGELOG，archive 之前一并更新。
```

四个问题都"Yes"了，再 `/opsx:archive <name>`，否则就是埋雷。

archive 的副作用要清楚——**整个 changes/xxx/ 目录会被移到 changes/archive/，不再可编辑**。所以"还有想改的地方"就千万别 archive，要么补 spec 重新走，要么先不开 archive 命令。

---

## 🤝 团队协作：让 OpenSpec 真正"飞起来"

个人项目里 OpenSpec 是"自我约束"，团队项目里它是"协作协议"。两者用法差别很大。

### 🌿 Git 工作流配合

团队里推荐的工作流：

```text
openspec/changes/xxx/  → 随 feature branch 一起提交
        ↓
PR review 阶段：重点 review changes/xxx/ 下的四份文档
        ↓
merge 到 main 后：跑 /opsx:archive
        ↓
changes/archive/ 目录也提交到 Git，作为变更历史
```

几个工程上的小技巧：

- **把 `openspec/` 整体加入 Git**——它是真相源，必须进版本控制。
- **PR 模板里加一行**："关联的 OpenSpec 变更：`changes/xxx/`"——让 review 重点对齐。
- **`.gitignore` 不要忽略 `openspec/changes/archive/`**——归档历史是审计资产。
- **敏感场景**：用 `.openspec.yaml` 里的 `schema` 字段限制该变更允许的 spec 范围。

### 👀 Code Review 节奏

OpenSpec 改变了 Code Review 的"看什么"：

| 阶段      | Review 重点                  | Reviewer       |
| ------- | -------------------------- | -------------- |
| `propose` 后 | `proposal.md` 范围、`specs/` 验收场景 | 业务方 / PM       |
| `apply` 中  | 关键任务的实现 + 测试              | 同组工程师         |
| `archive` 前 | verify 报告 + 边界 case         | 资深工程师 / Tech Lead |

**别让 PM 看代码、让工程师看 proposal**——OpenSpec 最大的好处就是让两类人用"各自的语言"协作。

### 🐙 多 Agent 协作

OpenSpec 最大的隐藏价值：**它是一份跨 Agent 的真相源**。

我经常这样用：

- **Claude Code**：负责 propose 阶段（写文档它最稳）。
- **Cursor**：负责 apply 阶段（diff 视角最直观）。
- **Codex**：负责测试和 verify（命令行友好）。

由于 `specs/` 是文件系统级的 Markdown，**新开会话、新开 IDE、换工具，行为标准完全一致**。这是 OpenSpec 比"AI 工具原生规则"强的根本原因——**你的规范不绑定任何 AI 工具**。

> 一句话：**OpenSpec 是 AI 工具之间的"通用语"**。换 Cursor 到 Claude Code，规范不动；换 Claude Code 到 Codex，规范不动。

---

## ⚠️ 真实踩坑实录：那些我犯过的错

经验如果不带血泪教训，就是空话。下面是我（和身边团队）真实踩过的坑，几乎每个 OpenSpec 新手都会撞上。

### 🐘 需求膨胀：spec 越改越长

**症状**：一个本应 2 天的变更，3 周还没 archive，spec 已经从 200 行膨胀到 1500 行。

**根因**：propose 阶段没有锁边界。AI 在 `/opsx:apply` 过程中，遇到"顺手能做的"就做掉了。

**避坑**：

- `proposal.md` 里写死"不在本次范围内"的清单。
- 任务粒度拆到 2 小时内，超出 scope 的立刻打回。
- 养成习惯——**"下个变更做"比"这次顺手做"健康得多**。

### 📜 spec 变成伪代码

**症状**：`specs/capability/spec.md` 写成了"半代码半文档"，Requirement 里全是 `if/else/function`。

**根因**：把"实现"误当"规范"。

**避坑**：

- Spec 只描述**外部可观察行为**，不写实现细节。
- Scenario 用"输入-输出"对，不用代码片段。
- 验收点用 `SHALL` 不用 `def`——这是"AI 看的合同"，不是"AI 抄的模板"。

### 💥 多变更并行冲突

**症状**：两个 feature branch 同时改 `specs/auth/spec.md`，merge 时冲突无法解决。

**根因**：把 `specs/` 当作"多人编辑的共享文件"，但 archive 是单向的。

**避坑**：

- **同一能力下只允许一个活跃变更**——在 `.openspec.yaml` 显式记录依赖。
- 跨能力的变更完全独立（因为 `specs/auth/` 和 `specs/billing/` 不冲突）。
- 实在有重叠，**先 archive 一个，再开第二个**。

### 🪤 归档前漏掉 verify

**症状**：直接 `/opsx:archive`，一周后线上出问题，回查才发现某个 Scenario 从来没实现过。

**根因**：把 archive 当作"提交代码"，而不是"完成变更"。

**避坑**：

- archive 命令前置 verify——在团队 wiki 里把它写死成"两步走"。
- 严肃项目里，archive 之前必须跑一遍测试套件，截图贴到 PR 描述里。
- 实在赶进度，**宁可只 archive 一部分能力**（用 `partial-archive` 子命令），也别整体放过。

---

## 🚀 进阶技巧：让 OpenSpec 价值翻倍

最后分享几个"用了就回不去"的进阶技巧。

### 🔗 维护 Artifact 一致性

这是 SDD 的铁律：永远先改文档，再改代码。如果你在实现过程中发现 design.md 的方案需要调整，不要直接改代码，而是：
- 先更新 design.md
- 再更新 tasks.md、/specs等相关文档
（1和2都可使用AI修改）
- 最后让 AI 按新的方案重新 apply

这样才能保证文档和代码的一致性，也方便后续回溯。

### 🌍 善用全局上下文

在 config.yaml 中把你的技术栈、编码规范、领域知识都写清楚。这些信息会在每次创建变更时自动注入，形成复利效应。

### 🧬 定制 AGENTS.md

`openspec init` 会生成一份默认的 `AGENTS.md`，但**默认那版太短**。实战中我建议至少加这些内容：

```markdown
# AGENTS.md（项目级 AI 协作规约）

## 工作流
所有变更必须走 OpenSpec：propose → apply → archive。

## 命名规范
- changes/ 下的目录名用动词开头：add-xxx、refactor-xxx、fix-xxx
- 不允许使用 personal-xxx、test-xxx 这种含糊命名

## Spec 风格
- 每个 Requirement 必须有 SHALL 关键字
- Scenario 至少覆盖正常 + 异常两条路径
- Spec 不写实现细节，只写外部可观察行为

## 必跑命令
- 提交前：npm test
- 归档前：openspec verify
- 归档后：git tag archive/<变更名>-<日期>
```

**`AGENTS.md` 是项目的"AI 宪法"**——花一下午写好它，后面所有 Agent 的行为都会更一致。

### 🧩 自定义工作流
Custom schema 是 OpenSpec 中对 workflow 的自定义描述。它定义一次 change 从创建到实施、sync、archive 的 artifact 结构和依赖关系。通过 custom schema，团队可以把不同研发场景拆成多种 workflow，而不是强制所有 change 都走同一条路径。

OpenSpec 的命令文件位于 `~/.claude/commands/opsx/`（以 Claude Code 为例）。你可以**自己加命令**：

```markdown
<!-- ~/.claude/commands/opsx/review.md -->
# /opsx:review

读取当前 changes/ 下的所有 proposal/specs/design/tasks，
对照"四问清单"做一次自检，输出 PASS/FAIL 清单。

**不修改任何文件**，只输出报告。
```
这样你就有了一个 `/opsx:review`——专属于你们团队的自定义工作流命令。

---

## 📝 总结：六字心诀

把整篇文章浓缩成六个字的 OpenSpec 心法：

> **先慢后快、严进宽出**。

- **先慢后快**：propose 阶段宁愿多花 1 小时，apply 阶段就能省 1 天。
- **严进宽出**：spec 写得严（SHALL、Scenario），archive 之后才能宽（活文档复用）。

OpenSpec 的本质不是"AI 写代码"，而是"**人用规范约束 AI、AI 用规范对齐人**"的双向协议。它和传统 SDD 最大的区别是：**文件是 AI 真正在读的，而不是写给人看的**。

所以最后一条建议是：

> **永远把 spec 写给 AI 读，不是写给人看**。人是兜底，AI 才是第一消费者。

如果你也想开始用 OpenSpec，从下一篇"加个小功能"开始，按本文的 checklist 走一遍，30 分钟就能体会"spec 驱动"的爽感。

---

### 📖 参考资料

- OpenSpec 官方仓库：<https://github.com/Fission-AI/OpenSpec>
- OpenSpec 官网：<https://openspec.dev/>
- 上一篇：[OpenSpec 的概念与基本使用](../OpenSpec的概念与基本使用/index.zh-cn.md)
- Spec Coding 系列：[Spec Coding 的踩坑实录](../Spec%20Coding的踩坑实录/index.zh-cn.md)
- 配合 Superpowers 使用：[Superpowers 与 OpenSpec 的配合使用](../Superpowers与OpenSpec的配合使用/index.zh-cn.md)
