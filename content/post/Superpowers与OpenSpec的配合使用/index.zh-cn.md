---
date : '2026-06-25T23:33:15+08:00'
draft : false
title : 'Superpowers与OpenSpec的配合使用'
image : 
categories : ["Vibe Coding"]
tags : ["Vibe Coding","Superpowers","OpenSpec","AI编程","Claude Code"]
description: "把 OpenSpec 的规范驱动与 Superpowers 的工程工作流结合起来，让 AI 编程从'自由发挥'走向'先立规矩、再干活'。"
---


## 🧠 写在前面：AI 编程为什么需要"两件套"

2024 年到 2026 年，AI 编程助手的能力突飞猛进——几百行代码随手就能写出来。但只要真正把 Claude Code、Cursor、Copilot 之类工具放进真实项目里，你大概率会撞上这几面墙：

- **需求漂移**：你说"做个登录功能"，AI 心领神会地写出一整套 OAuth；你要的其实只是手机号 + 验证码。
- **缺乏流程**：AI 不会主动问"为什么"，拿到需求就开干，写完也不知道它按什么逻辑写的。
- **质量不稳**：今天生成的好，明天生成的差；改一个 Bug 引入三个新 Bug。
- **不可追溯**：改了很多版，没人记得为什么改；后来人不敢动这段代码。

这些问题的本质是：**AI 默认模式是"尽力完成当前指令"，而不是"遵循一套严谨的工程流程"**。

社区给出的答案是两个相互补位的工具：

- **OpenSpec**：管"做什么"——把需求变成可审查、可追溯的规范文档。
- **Superpowers**：管"怎么做"——强制 AI 走完"需求分析 → 制定计划 → TDD → 代码审查 → 验证"的工程流程。

一个管契约，一个管纪律。这两件套组合起来，被不少开发者称为 AI 编程的"黄金搭档"。

---

## 🧩 OpenSpec：给 AI 立一份"需求契约"

### 1.1 它是什么

[OpenSpec](https://github.com/Fission-AI/OpenSpec) 是由 [Fission-AI](https://openspec.dev/) 开源的 **Spec-Driven Development（SDD）框架 + CLI 工具**，核心口号是 **"Align before code"（先对齐规格，再写代码）**。

它的形态很轻量：

- 一组本地 Markdown 文档（`openspec/specs/`、`openspec/changes/`）
- 一组斜杠命令（`/opsx:propose`、`/opsx:apply`、`/opsx:archive`）
- 一个 npm 包：`@fission-ai/openspec`

支持 25+ AI 工具，包括 Claude Code、Cursor、Codex、GitHub Copilot、Windsurf、Gemini CLI、Cline、Trae 等。

### 1.2 核心设计：双文件夹模型

OpenSpec 在项目根目录的 `openspec/` 下维护两套内容：

```text
openspec/
├── specs/    # 系统当前生效的规范（Source of Truth，事实来源）
└── changes/  # 正在进行的变更提案（每个功能一个子目录）
```

每次新功能都在 `changes/<name>/` 下开一个独立目录，里面包含：

| 文件 | 作用 |
|---|---|
| `proposal.md` | 为什么要做、改动范围 |
| `design.md` | 技术方案、关键决策 |
| `specs/` | 需求与场景的 delta（差异清单） |
| `tasks.md` | 实施任务的 checkbox 清单 |

`/opsx:archive` 完成后，规范会自动合并到 `specs/`，作为活文档继续维护。

### 1.3 三步走的核心命令（Core 模式）

安装完默认进入 Core 模式，命令精简到三个：

```text
/opsx:propose  →  /opsx:apply  →  /opsx:archive
```

- **`/opsx:propose <name>`**：一键生成 `proposal.md` + `design.md` + `specs/` + `tasks.md`
- **`/opsx:apply`**：按 `tasks.md` 逐项实现
- **`/opsx:archive`**：归档完成的变更

需求不清时还有 `/opsx:explore` 兜底——不产生产物，只梳理思路。

---

## 🛠️ Superpowers：给 AI 装一个"工程化大脑"

### 2.1 它是什么

[Superpowers](https://github.com/obra/superpowers) 是 GitHub 用户 [`obra`](https://github.com/obra) 开源的一个 **Claude Skill 框架 + 软件开发方法论**。它由一组 Markdown 格式的 `SKILL.md` 文件组成，被 Claude Code / Codex / Cursor / Gemini CLI 等工具读取并执行。

它的设计哲学是：

> **不是让 AI 多会写代码，而是尽量让它少在错误的时机写代码。**

### 2.2 八个核心技能（Skills）

Superpowers 把开发流程拆成 8 个可触发的技能，每个对应一个环节：

| 技能 | 触发时机 | 白话解释 |
|---|---|---|
| `brainstorming` | 写代码前 | 像产品经理一样追问，把模糊需求变清晰 |
| `using-git-worktrees` | 设计批准后 | 在新分支建隔离工作区 |
| `writing-plans` | 设计通过后 | 把大任务拆成 2~5 分钟的小步骤 |
| `subagent-driven-development` | 计划完成后 | 派多个子代理并行干活、互相审查 |
| `test-driven-development` | 实现过程中 | 强制红-绿-重构循环 |
| `systematic-debugging` | 调试阶段 | 4 步根因诊断法 |
| `requesting-code-review` | 任务之间 | 写完代码自动找人审查 |
| `verification-before-completion` | 收尾阶段 | 交活前全部跑一遍 |

这套技能的最大特点是 **按上下文自动触发**——你不需要手动敲命令，AI 看到合适的时机就会自己调用。

### 2.3 安装（以 Claude Code 为例）

```bash
# 注册市场
/plugin marketplace add obra/superpowers-marketplace

# 安装插件
/plugin install superpowers@superpowers-marketplace
```

装完后开一个新会话，说一句"帮我做一个登录功能"，Superpowers 就会自动激活 `brainstorming` 技能开始追问。

---

## 🔄 两者的协同关系：契约 + 纪律

把两个工具叠在一起看，它们的边界其实非常清楚：

<div align="center">
  <img src="workflow.png" alt="OpenSpec 与 Superpowers 协同关系图" width="82%">
</div>

| 维度 | Superpowers | OpenSpec |
|---|---|---|
| 定位 | AI 的执行纪律（怎么做） | 项目的规格说明书（做什么） |
| 解决问题 | 防止跳过设计、保证编码质量 | 防止需求遗忘、保证规范可追溯 |
| 核心产物 | 对话决策、实施计划、代码 | proposal.md、specs/、tasks.md |
| 工作流 | 单任务高质量闭环 | 长期增量变更管理 |
| 状态持久 | 依赖对话历史 | 基于文件系统，跨会话持久 |
| 擅长场景 | 执行阶段 | 设计阶段 |

**一句话总结：OpenSpec 让 AI 写代码前先签"合同"，锁定设计（做什么），Superpowers 让 AI 写代码时按"工艺"，保障执行（怎么做）**。两者合起来，AI 才真正像个能交付的高级工程师，而不是"按行计费"的代码打字机。

- 单独 OpenSpec：有规范但执行可能跳步，缺少 TDD 纪律。
- 单独 Superpowers：有纪律但设计共识仅存于对话，无法持久化。

组合价值：OpenSpec 将设计固化为文件资产，Superpowers 在执行中强制 TDD、调试、审查等纪律。

## 方案一:superpowers-openspec-team-skills
superpowers-openspec-team-skills 是 github上的一个解决方案，用于管理 OpenSpec 和 Superpowers 项目的开发流程。官方仓库地址：[superpowers-openspec-team-skills](https://github.com/SYZ-Coder/superpowers-openspec-team-skills)

### 具体使用

1）安装
```bash
npm install -g superpowers-openspec-team
```

2）项目初始化
```bash
sot init /path/to/your/project
```
3）工作流
选择具体的工作流
- superpowers-openspec-superpowers：先用 Superpowers 把问题想透，再用 OpenSpec 把事实锁准，最后回到 Superpowers 把实现、验证和归档做稳
- openspec-superpowers：先完成 OpenSpec 变更产物，再交给 Superpowers 继续实现、验证和归档
- superpowers-feature：只使用 Superpowers 的设计、计划、TDD、验证纪律(等价于单独使用superpowers)
- superpowers-learning：不是主交付流程，而是其他 workflow 完成后的增强收尾层，用来更新项目记忆、沉淀经验，并让下一次会话可以直接接上当前成果
- openspec-feature：先完成 OpenSpec proposal、design、specs、tasks，再进入实现(等价于单独使用Superpowers)

这些 workflow 只应在以下情况启用：

- 用户明确点名某个 workflow
- 用户明确要求按这种 workflow 风格执行
- 仓库策略明确要求使用该 workflow

它们不应该成为 AI 工具的默认后台流程。

示例：

```text
请使用 $superpowers-openspec-superpowers-workflow 处理这个功能。
```

4）预计产物
1.  docs/superpowers/specs/ 下的 Superpowers 设计草稿
2.  openspec/changes/<change-name>/ 下的 proposal、design、specs、tasks
3.  docs/superpowers/plans/ 下的实现计划
4.  已验证的代码变更
5.  完成后的 OpenSpec change 归档

### 工作流

#### 工作流的选取逻辑
- 想先用 Superpowers 做探索、再用 OpenSpec 锁定、最后回到 Superpowers 执行，用 `superpowers-openspec-superpowers`
- 想先从 OpenSpec 产物起步，再交给 Superpowers 继续交付，用 `openspec-superpowers`
- 只想要 Superpowers 工程纪律，不需要 OpenSpec change 产物，用 `superpowers-feature`
- 工作已经做完，想把这次经验、状态和可复用知识沉淀下来，并让下一次会话直接接上，用 `superpowers-learning`
- 只想先补齐 OpenSpec 变更文档，用 `openspec-feature`

其中 `superpowers-learning` 需要特别注意：它更像其他 workflow 的“增强收尾层”，不是一条替代开发流程的主入口。通常是在 `superpowers-feature`、`superpowers-openspec-superpowers`、`openspec-superpowers` 这类交付型 workflow 完成之后，再用它把本次会话里真正值得长期保留的内容写回 `.superpowers-memory/`，包括稳定项目事实、当前状态、简短会话记录，以及后续可沉淀成 skill、checklist 或知识库条目的经验。

对持续协作的项目，推荐这样串联：

1. 先运行一个交付型 workflow
2. 完成实现与验证
3. 再运行 `superpowers-learning`，把这次工作的稳定事实、当前状态、会话记录和可复用经验写回项目记忆




## 🚀 标准 SOP：六阶段配合流程

下面给出一套经过社区验证的"六阶段标准操作流程"（SOP），把两个工具的指令串成一条完整的链路。

<div align="center">
  <img src="sop-flow.png" alt="六阶段 SOP 流程" width="88%">
</div>

### 阶段 1：创建分支

```bash
git checkout -b feature/user-registration
```

保持 `main` 分支干净，所有变更在独立分支进行。

### 阶段 2：提案定义（OpenSpec 主导）

```text
/opsx:propose user-registration-with-verification
```

AI 会在 `openspec/changes/user-registration-with-verification/` 下生成完整文档结构：

```text
openspec/changes/user-registration-with-verification/
├── proposal.md   ← 变更动机与范围
├── design.md     ← 技术方案
├── specs/        ← 需求与场景
└── tasks.md      ← 实施任务清单
```

**人工必做**：仔细 review `proposal.md`，确认需求方向正确后再继续。

### 阶段 3：深度设计（Superpowers 主导）

```text
/superpowers:brainstorming "用户注册功能的具体设计"
```

Superpowers 不会直接动代码，而是启动苏格拉底式追问，把 OpenSpec proposal 里没写清楚的边界条件、异常分支、验收标准再问一通，并产出设计问答记录。

### 阶段 4：计划拆分（Superpowers 主导）

```text
/superpowers:writing-plans
```

把设计拆成 2~5 分钟就能完成的小任务，每个任务写明：

- 精确的文件路径
- 完整的代码片段
- 验证步骤（如何知道这一步做对了）

输出物是一份**给"热情但无判断力的初级工程师"也能照着做**的计划文档。

### 阶段 5：TDD 执行（Superpowers + OpenSpec 共同主导）

```text
/superpowers:subagent-driven-development
# 或
/opsx:apply
```

两种用法可选：

- **想用子代理并行**：`/superpowers:subagent-driven-development`，Superpowers 会为每个任务派一个全新子代理，并通过两阶段审查（规范符合性 + 代码质量）。
- **想沿用 OpenSpec 节奏**：`/opsx:apply`，AI 按 `tasks.md` 逐项打勾实现。

无论哪种，**TDD 都不能跳过**——先写测试，看着它失败；再写最小代码让它通过；再重构。Superpowers 的 `test-driven-development` 技能会强制执行这条纪律。

### 阶段 6：归档收尾

```text
/opsx:archive user-registration-with-verification
```

实现完成后，OpenSpec 会把 `changes/` 下的产物归档，并把规范 delta 合并到 `openspec/specs/` 中。这步会留下完整的审计轨迹，方便后续人员回看"这个功能当时是怎么设计的"。

---

## 🧪 实操示例：用户注册功能

下面用一个最小例子把整套流程跑通。

### Step 1：初始化项目

```bash
mkdir demo-app && cd demo-app
npm init -y
openspec init --tools claude
```

按提示选择 Claude Code，确认后 `openspec/` 与 `.claude/` 目录会一并生成。

### Step 2：提案

在 Claude Code 对话框输入：

```text
/opsx:propose user-registration-with-email-verification
```

需求描述示例：

> 添加用户注册功能：邮箱 + 密码，注册成功后发送验证邮件，72 小时内未验证则账号失效。

OpenSpec 会输出 4 个文档，其中 `tasks.md` 大致长这样：

```markdown
## 1. 数据模型
- [ ] 1.1 创建 User 模型（email、passwordHash、status、emailVerifiedAt）
- [ ] 1.2 添加数据库迁移脚本

## 2. 接口实现
- [ ] 2.1 POST /api/register 入参校验
- [ ] 2.2 密码哈希存储（bcrypt）
- [ ] 2.3 发送验证邮件（含 72h 过期 token）

## 3. 测试
- [ ] 3.1 单元测试：邮箱格式校验
- [ ] 3.2 集成测试：注册 → 验证 → 登录完整流程
```

### Step 3：触发 Superpowers 设计追问

```text
/superpowers:brainstorming "用户注册中的边界条件：邮箱重复怎么办？验证邮件链接重复点击怎么办？"
```

Superpowers 会把"重复注册""邮件链接过期""重发验证邮件"这些边界条件逐条澄清，并写入设计文档。

### Step 4：拆任务并 TDD 执行

```text
/superpowers:writing-plans
/superpowers:test-driven-development
```

接下来 AI 会严格按红-绿-重构循环逐项推进。`tasks.md` 里的 checkbox 会一项项被勾掉。

### Step 5：归档

```text
/opsx:archive user-registration-with-email-verification
```

归档成功后 `openspec/specs/user/spec.md` 就会出现新的 Requirement / Scenario，整套变更历史可追溯。

---

## ⚠️ 注意事项与最佳实践

### 命令类型别搞混

- **CLI 命令**（`openspec init`、`git checkout -b`）：在终端里直接跑。
- **Skill 命令**（`/opsx:propose`、`/superpowers:brainstorming`）：在 AI 对话框里输入，由 AI 自动执行对应流程。

### 选对工作模式

OpenSpec 默认是 **Core 模式**（4 个命令够用）。如果项目复杂、需要更细的粒度，可以切换到 Expanded 模式：

```bash
openspec config profile   # 勾选 new/continue/ff/verify/bulk-archive/onboard
openspec update           # 让 AI 识别这些新命令
```

### 模型选型有讲究

OpenSpec 的 `propose` 与 Superpowers 的 `brainstorming` 都很吃推理能力，建议使用 Opus、GPT-5、Claude Sonnet 4.5 这一档；执行阶段（`apply`、TDD）可以用更便宜的模型，**因为有规范文档兜底，弱模型也能稳住**。

### 上下文要保持干净

OpenSpec 的精髓是"规范是上下文"。在 `/opsx:apply` 之前，建议新开一个干净的对话窗口，让 AI 只能从 `specs/` 与 `tasks.md` 里读上下文，**避免旧对话污染判断**。

### 变更结束立刻归档

完成一个变更就 `/opsx:archive`，不要堆十几个 `changes/` 不归档，否则规范库会越积越乱。

### 两种工具的"分工"再强调

| 阶段 | 谁主导 | 为什么 |
|---|---|---|
| 需求对齐 | OpenSpec | 需要结构化文档作为契约 |
| 设计澄清 | Superpowers | 需要反复追问，文档很难替代对话 |
| 计划拆分 | Superpowers | 需要按"工程师可执行"粒度拆 |
| 代码实现 | 两者皆可 | 看团队习惯 |
| 质量审查 | Superpowers | 强制 TDD 与 code-review 闭环 |
| 变更归档 | OpenSpec | 需要把 delta 合并到活文档 |

---

## 📝 总结

Superpowers 与 OpenSpec 不是一个二选一的问题，而是 **"上规矩 + 下工艺"** 的互补关系：

- **OpenSpec** 把"想做什么"变成可审查、可追溯的规范文档，解决"AI 跑偏"的问题。
- **Superpowers** 把"应该怎么写"变成强制的工程工作流，解决"AI 偷工减料"的问题。

两者配合后，AI 不再是一个"需要时刻盯着的实习生"，而是一个**按规范交付、按流程实施、按纪律收尾** 的工程师。比起单打独斗，组合使用至少带来三方面收益：

1. **可审计**：每个变更都有 `proposal.md`、`specs/`、`tasks.md` 留痕。
2. **可复用**：规范合并到 `specs/` 后是活文档，新成员 onboarding 直接读 spec 即可。
3. **可规模化**：多人/多 Agent 协作时，规则在文档里、纪律在 Skill 里，AI 行为是一致的。


---

### 参考资料

- OpenSpec 官方仓库：<https://github.com/Fission-AI/OpenSpec>
- Superpowers 官方仓库：<https://github.com/obra/superpowers>
