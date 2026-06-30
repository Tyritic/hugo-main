---
date : '2026-06-30T10:00:00+08:00'
draft : false
title : 'Superpowers的概念和基本使用'
image : ""
categories : ["AI Coding"]
tags : ["Spec Coding", "Superpowers"]
description: "Superpowers 是什么？它为什么强调纪律先于速度？八个核心 Skills 如何组成一条完整工程链？一份给新手的 Superpowers 入门笔记。"
---

## 🧠 写在前面：AI 编程为什么需要"流程纪律"

这两年 AI 编码助手的能力突飞猛进——几百行代码随手就能写出来。但只要真正把 Claude Code、Cursor、Codex 之类工具放进真实项目里，你大概率会撞上这几面墙：

- **需求漂移**：你说"做个登录功能"，AI 心领神会地写出一整套 OAuth；你要的其实只是手机号 + 验证码。
- **缺乏流程**：AI 不会主动问"为什么"，拿到需求就开干，写完也不知道它按什么逻辑写的。
- **质量不稳**：今天生成的好，明天生成的差；改一个 Bug 引入三个新 Bug。
- **不可追溯**：改了很多版，没人记得为什么改；后来人不敢动这段代码。

这些问题背后都有一个共同点：**AI 默认模式是"尽力完成当前指令"，而不是"遵循一套严谨的工程流程"**。

社区给出的答案之一，就是 [Superpowers](https://github.com/obra/superpowers)——一个**专门给 AI 编码助手装上"工程化大脑"** 的 Skills 框架。本文聚焦 Superpowers 本身：它是什么、它如何重塑 AI 的工作流、如何独立使用它，以及和同类工具的差异。**和 OpenSpec 的配合使用** 会在另一篇专门讲。

***

## 📖 Superpowers 是什么

[Superpowers](https://github.com/obra/superpowers) 是由 [Jesse Vincent](https://blog.fsck.com) 在 [Prime Radiant](https://primeradiant.com) 开源的一个 **AI 编码助手 Skills 框架 + 软件开发方法论**。它的官方定义是：

> **A complete software development workflow for your coding agents, built on top of a set of composable "skills" and some initial instructions that make sure your agent uses them.**

翻译过来就是：**一套为 AI 编码助手量身打造的完整软件开发工作流，建立在一组可组合的"技能（Skills）"之上，并通过初始指令确保你的 agent 真正用上它们**。

它的形态非常"软"——和 OpenSpec 那套结构化文档不同，Superpowers 几乎**全部由 Markdown 格式的** **`SKILL.md`** **文件组成**。这些文件被 Claude Code、Cursor、Codex 等 AI 工具加载后，会在合适的时机**自动触发**，强制 AI 走完"需求分析 → 制定计划 → TDD → 代码审查 → 验证"的工程流程。

一句话总结：**它不做"加什么功能"，它专门管"AI 应该在什么时候、用什么方式写代码"**。

***

## 🧭 设计哲学：纪律先于速度

Superpowers 反复强调的设计哲学，可以浓缩为一句话：

> **Not "make AI write more code", but "make AI write less code at the wrong time".**
> （不是让 AI 多写代码，而是尽量让它少在错误的时机写代码。）

围绕这句话，它把四条原则刻进了每个 Skill 的设计里：

| 原则                          | 含义                                       |
| :-------------------------- | :--------------------------------------- |
| **Test-Driven Development** | 永远先写测试；TDD 不是建议，是纪律。                     |
| **Systematic over ad-hoc**  | 系统化流程优先于临场发挥；过程比灵感重要。                    |
| **Complexity reduction**    | 简单是首要目标；YAGNI（You Aren't Gonna Need It）。 |
| **Evidence over claims**    | 证据优先于声明；验证完成前不宣布成功。                      |

这四条原则对应到 AI 工作流里，就变成了几条"硬约束"：

- 写代码前必须 `brainstorming`，把模糊需求问透。
- 设计批准后才能 `using-git-worktrees` 建工作区。
- 计划必须细到 2-5 分钟一个任务，每步都有"如何知道做对了"的验证步骤。
- 实现过程中强制 `test-driven-development`：先写失败测试，再写最小代码让它通过，再重构。
- 任务之间必须 `requesting-code-review`。
- 收尾必须 `verification-before-completion`。

**写代码不再是一蹴而就的事情，而是一连串必须走完的关卡**。

***

## 🏗️ 核心机制：可组合的 Skills

### 🪜 核心Skill

下面这张表汇总了 Superpowers 的 所有Skills，及其触发方式与典型适用场景。

| 技能                               | 触发方式                                          | 核心动作                                       |
| :------------------------------- | :-------------------------------------------- | :----------------------------------------- |
| `brainstorming`                  | `/superpowers:brainstorming`                  | 苏格拉底式追问，写代码前进行需求澄清、方案比较、设计确认和设计文档沉淀。       |
| `using-git-worktrees`            | `/superpowers:using-git-worktrees`            | 创建隔离的开发环境，在执行实现前建立或识别隔离工作区                 |
| `writing-plans`                  | `/superpowers:writing-plans`                  | 将需求转化为详细的实现计划，把大任务拆成 2-5 分钟的小步骤，每步含完整代码与验证 |
| `executing-plans`                | `/superpowers:executing-plans`                | 执行已有实现计划，无法或不适合用子代理时，按计划在当前会话内执行。          |
| `subagent-driven-development`    | `/superpowers:subagent-driven-development`    | 执行已有实现计划，用子代理按任务实现、评审、修复和记录进度。             |
| `test-driven-development`        | `/superpowers:test-driven-development`        | TDD 开发流程，强制 RED-GREEN-REFACTOR；先写失败测试再写实现  |
| `systematic-debugging`           | `/superpowers:systematic-debugging`           | 系统化调试问题，4 步根因诊断法，杜绝"猜一猜"式调试                |
| `requesting-code-review`         | `/superpowers:requesting-code-review`         | 完成任务或合并前请求代码评审。                            |
| `receiving-code-review`          | `/superpowers:receiving-code-review`          | 接收评审反馈时先理解、验证、评估，再修改。                      |
| `verification-before-completion` | `/superpowers:verification-before-completion` | 完工前进行验证                                    |
| `dispatching-parallel-agents`    | `/superpowers:dispatching-parallel-agents`    | 多个独立问题并行分派给子代理。                            |
| `finishing-a-development-branch` | `/superpowers:finishing-a-development-branch` | 验证、识别 worktree 状态、给出 merge/PR/保留/丢弃选项。     |
| `writing-skills`                 | `/superpowers:writing-skills`                 | 创建和验证新技能，把技能写作也按 TDD 思路处理。                 |

在 Claude Code 中触发技能非常简单：

- 方法1：直接命令触发
  - 例如：`/superpowers:brainstorming`
- 方法2：通过上下文自动触发
  - Superpowers 会**根据上下文自动调用**对应 Skill。你不需要每次都手动敲命令，agent 会自己判断。

### 🧩 架构设计

所有的 skill 可以分为以下几类：

#### 🏛️ 工作流骨架 Skills

- **using-superpowers**：这是整个系统的引导层，它在每次会话开始时激活，建立 skill 发现和调用机制，要求 agent 在任何回应（包括澄清性问题）之前都先检查是否有适用的 skill。
- **brainstorming**：在写任何代码之前激活。通过提问逐步提炼粗糙的想法，探索替代方案，将设计以短小可读的段落呈现供用户验证，最终保存设计文档。最新版本还增加了可视化伴侣（在浏览器侧窗口展示 mockup 和图表），以及对超大型项目的拆分评估机制。
- **using-git-worktrees**：在设计获批后激活。在新分支上创建隔离的工作区，运行项目初始化，验证干净的测试基线。这样多个特性可以并行开发而不互相污染。
- **writing-plans**：使用已批准的设计，生成实施计划。目标读者是"一个对代码库一无所知、品味有限、不擅长测试设计的热心初级工程师"——每个任务包含精确的文件路径、完整代码、验证步骤，粒度为 2-5 分钟一个任务。
- **subagent-driven-development / executing-plans**：有了计划之后激活。为每个任务派发独立的子 agent，进行两阶段代码审查（先检查是否符合规格，再检查代码质量）；或以批次执行并设置人工检查点。
- **finishing-a-development-branch**：所有任务完成时激活。验证测试，向用户提供选项（merge/PR/保留/丢弃），清理 worktree。

#### 🧪 测试与实现 Skills

- **test-driven-development**：在实现阶段激活，强制执行 RED-GREEN-REFACTOR 循环：先写会失败的测试，看着它失败，再写最少的代码让它通过，提交。框架中还内置了一份 anti-patterns 参考，防止 agent 走捷径。
- **async-testing-patterns**：当测试中存在竞态条件、时序依赖，或测试结果不稳定时触发。专门处理异步代码的测试问题，替代用 setTimeout/sleep 敷衍了事的做法。
- **verification-before-completion**：在声称工作完成之前强制触发，确认修复或实现真正生效，防止"看起来好了"的假完成。

#### 🔍 调试 Skills

- **systematic-debugging**：核心原则：在尝试任何修复之前，必须找到根本原因。症状修复即失败。强制完成 Phase 1（证据收集、错误分析、数据流追踪）后才能提出修复方案。如果连续三次修复失败，必须停下来质疑架构设计。该 skill 内置三个子技术：
  - **root-cause-tracing**：沿调用栈向后追踪 bug，定位触发问题的源头。
  - **condition-based-waiting**：用条件轮询替代任意超时。
  - **defense-in-depth**：找到根因后，在多个层次添加校验。

#### ⚙️ Meta Skills

- **writing-skills**：用于创建新 skill，本身也遵循 TDD 方法论——先写测试场景，用子 agent 验证当前行为失败，再写 skill 文档，最后验证 agent 能正确遵从。
- **dispatching-parallel-agents**：管理并发子 agent 的分配策略，适用于多个独立任务可以同时推进的场景。
- **remembering-conversations**：将对话内容向量化存入 SQLite 数据库，使用 Claude Haiku 生成摘要，并提供命令行搜索工具。为避免无效搜索污染上下文，该 skill 使用子 agent 做搜索。
- **requesting-code-review**：提供代码审查前的预检清单，并以严重程度分级的方式报告问题。

***

## 🔄 常见工作流

### 🎯 基础工作流：八步闭环

Superpowers 的核心工作流可以浓缩为八步。下面用一张图展示全貌：

```text
[1]  🔍 brainstorming
        │  产出：设计文档（design.md）
        ▼
[2]  🌳 using-git-worktrees
        │  产出：独立分支 + 工作区
        ▼
[3]  📝 writing-plans
        │  产出：实现计划（plan.md），2-5 分钟/任务
        ▼
[4]  🤖 subagent-driven-development
        │       or
        │  ⚙️ executing-plans
        │  产出：每任务含两阶段审查（规范符合 + 代码质量）
        ▼
[5]  🧪 test-driven-development
        │  每步循环：写失败测试 → 写最小实现 → 重构
        ▼
[6]  🔎 requesting-code-review
        │  每任务结束：按严重程度分级报告
        ▼
[7]  ✅ verification-before-completion
        │  产出：代码审查报告（review.md）
        ▼
[8]  🏁 finishing-a-development-branch
        │  产出：测试全绿 + merge/PR/keep/discard 决策
```

***

### 🐛 Bug 修复工作流

```text
[1]  🔍 发现 Bug
        │  
        ▼
[2]  🐛 systematic-debugging（系统化调试）
        │  
        ▼
[3]  📝 writing-plans（修复计划）
        │  
        ▼
[4]  ⚙️ executing-plans（执行修复）
        │  
        ▼
[5]  🧪 verification-before-completion（验证修复）
        │  
        ▼
[6]  🏁 finishing-a-development-branch
        │  产出：测试全绿 + merge/PR/keep/discard 决策
```

***

### 🔧 重构工作流

```text
[1]  🔍 发现代码问题
        │  
        ▼
[2]  💡 brainstorming（重构方案）
        │  
        ▼
[3]  🧪 test-driven-development（TDD 重构）
        │  
        ▼
[4]  ✨ code-simplifier（代码优化）
        │  
        ▼
[5]  🎯 verification-before-completion（验证重构）
        │  
        ▼
[6]  🏁 finishing-a-development-branch
        │  产出：测试全绿 + merge/PR/keep/discard 决策
```

***

## ⚠️ 适用场景与局限

### 👍 适合用 Superpowers 的场景

- **长期维护的项目**：Skills 强制每步走流程，避免技术债务堆积。
- **多人协作的团队**：所有 AI 行为规则统一存在 Skills 里，新人 onboarding 只需读 SKILL.md。
- **质量要求高的代码**：TDD + code review + verification 是一道硬关卡。
- **复杂功能开发**：需要多任务并行、子代理协作的场景，`subagent-driven-development` 非常合适。

### ❌ 不适合用 Superpowers 的场景

- **一次性脚本或小修小补**：强制走完 brainstorm + plan + TDD 流程成本太高。
- **探索性 PoC**：需求还没定型时，brainstorming 会问太多问题拖慢节奏。
- **不支持多 agent 的平台**：`subagent-driven-development` 在某些平台上不可用，需要回退到 `executing-plans` 的人工检查点模式。
- **追求"零摩擦"的小项目**：Skills 的纪律反而是负担。

### ❗ 常见误区

| 误区                       | 真相                                                          |
| :----------------------- | :---------------------------------------------------------- |
| "装了 Superpowers AI 就变强了" | Superpowers 只管"流程纪律"，不管"模型能力"。弱模型 + Superpowers 仍可能产出低质量代码。 |
| "Skills 越多越好"            | Skills 越多，agent 切换上下文越频繁，反而拖慢节奏。**只装用得到的**。                 |
| "TDD 是浪费时间"              | TDD 在需求清晰时极快，在需求模糊时确实慢。先 `brainstorming` 把需求问透，TDD 就不慢。     |
| "自动触发就是全自动"              | 关键决策点（设计批准、Critical 修复）**仍然需要人在环路**。                        |

***

## 📝 总结

Superpowers 不是一个"AI 增强插件"，它是一种 **"AI 工程化方法论"**。它把"高级工程师应该怎么做"提炼成一组可组合的 Skills，再用强制流程保证 AI 真的照做。

它的核心价值是：

1. **纪律先于速度**：强制 TDD、强制 review、强制 verify。
2. **流程可组合**：8 个核心 Skill 串成一条完整链路。
3. **平台无关**：同一套 Skills 在 Claude Code / Cursor / Codex 等多平台通用。
4. **人仍在环路**：关键决策点（设计批准、Critical 修复）必须人工确认。

如果和 OpenSpec 配合使用（详见[《Superpowers与OpenSpec的配合使用》](../Superpowers与OpenSpec的配合使用/index.zh-cn.md)），还可以叠加一层"规范可追溯"的能力——**Superpowers 管纪律，OpenSpec 管契约**。

> 一句话记忆：**OpenSpec 让 AI 先签合同再干活，Superpowers 让 AI 按工艺把活干完**。

***

### 🔗 参考资料

- Superpowers 官方仓库：<https://github.com/obra/superpowers>
- Jesse Vincent 的博客：<https://blog.fsck.com/2025/10/09/superpowers/>
- Prime Radiant：<https://primeradiant.com/>
- Claude Code 插件市场：<https://claude.com/plugins/superpowers>
- Superpowers Discord 社区：<https://discord.gg/35wsABTejz>
- OpenSpec 官方仓库：<https://github.com/Fission-AI/OpenSpec>
- 配套阅读：[《Superpowers与OpenSpec的配合使用》](../Superpowers与OpenSpec的配合使用/index.zh-cn.md)

