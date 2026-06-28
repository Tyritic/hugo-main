---
date : '2026-06-27T20:00:00+08:00'
draft : false
title : 'Spec Coding 的定义'
image : ""
categories : ["AI Coding"]
tags : ["Spec Coding"]
description: "把规格当作单一事实来源，让 AI 编程从'凭感觉'走向'按图纸施工'——一份关于 Spec-Driven Development 理念、工作流与落地的实战笔记。"
---

## 🧠 写在前面：AI 编程缺的不是模型，是图纸

2024 年到 2026 年这两年，我用 Claude Code、Cursor、Copilot 写过的代码比过去十年加起来都多。但越用越清楚地意识到一件事：

> **AI 不缺写代码的能力，缺的是一张'图纸'。**

Vibe Coding 的爽感我们都体会过——敲一句"做个登录页"，五秒钟出 HTML。Demo 截图发到群里人人点赞。但只要把这段代码接进真实项目，问题就接踵而至：

- **上下文漂移**：改了一个文件，三处不相关的代码跟着坏。
- **需求漂移**：你说"登录支持手机号"，AI 默认走了 OAuth 流程。
- **知识孤岛**：昨天为什么这么设计，没人记得——AI 不记得，你自己也不记得。
- **质量不稳**：同样的需求，时好时坏，全看模型心情。
- **协作断点**：同事接手时只能对着代码反推意图，最后的结论往往是"别动这段"。

这些痛点指向同一个结论：**AI 编程的下一个瓶颈不是模型能力，而是"人机协作的工程方法论"**。

[GitHub](https://github.blog/) 在 2025 年正式把这套方法论命名为 **Spec-Driven Development（SDD）**，社区里更口语化的叫法是 **Spec Coding**——用规格驱动编码。

这篇文章是我对 Spec Coding 的一份系统化实践笔记，重点不在某一个具体工具，而在**它作为一种开发范式，到底解决了什么、要怎么落地、有什么坑**。

---

## ⚖️ 什么是 Spec Coding

### 📖 定义与定位

**Spec Coding**（或 SDD, Spec-Driven Development）是一种**把"可执行的规格"置于软件开发生命周期中心**的工程实践。它借鉴了传统软件工程中"契约优先"（Contract-First）的思想，但做了关键升级：

- **规格不再是静态文档**，而是与代码一同演进、版本化、可被 AI 直接消费的活工件。
- **代码不再是 Source of Truth**，而是规格的"最后一公里输出"。
- **AI 不是替代者**，而是被规格约束的"高级实现者"。

一句话概括：

> **过去是先写代码再补文档；现在反过来——先写规格，代码只是规格的编译产物。**

### 🔍 Spec Coding vs Vibe Coding

| 维度 | Vibe Coding | Spec Coding |
|------|-------------|-------------|
| **核心信念** | "AI 心领神会" | "规格是契约" |
| **输入形态** | 自然语言提示 | 结构化规格文档 |
| **上下文管理** | 靠对话历史 | 靠版本化的文件 |
| **决策可追溯** | 不可追溯 | 每个决策都有据可查 |
| **变更成本** | 改一处牵全身 | 改规格 → 重新生成 |
| **适合场景** | Demo、探索、PoC | 真实项目、长期维护、协作 |
| **典型代表** | Cursor 自由对话 | Spec Kit / Kiro / OpenSpec |

**它们不是对立关系，是不同阶段的工具**：

- 想快速验证一个想法 → Vibe Coding 更轻。
- 想把想法变成可交付、可维护的产品 → Spec Coding 更稳。

社区里越来越多人把 Spec Coding 视为 Vibe Coding 的"工业化升级版"。

---

## 🔄 核心工作流：Specify → Plan → Tasks → Implement

主流 SDD 框架（GitHub Spec Kit、AWS Kiro、OpenSpec）虽然在命令名上略有差异，但底层都收敛到了同一个四阶段工作流：

```text
Specify  →  Plan  →  Tasks  →  Implement
（定目标）  （定方案）  （拆任务）  （按规格实现）
```

每一个阶段都遵循**人在环路（Human-in-the-Loop）**原则：必须由人审阅、批准，才进入下一阶段。

### 🛠️ 阶段一：Specify（定目标）

**回答的问题**：我们要解决什么问题？给谁用？成功的标准是什么？

这一阶段**不涉及任何技术选型**，只关注：

- 用户故事（User Story）
- 业务目标（Goal）
- 验收标准（Acceptance Criteria）
- 边界条件与异常场景

输出通常是一份 `spec.md`，语言要"无歧义、可测试"。AWS Kiro 在这一步使用 [EARS](https://alistairmavin.com/ears/)（Easy Approach to Requirements Syntax）格式，能让 AI 自动生成覆盖边角情况的验收条件。

```markdown
## Feature: 用户注册

### US-1 注册新账号
- WHEN 用户提交合法的邮箱与密码
- THEN 系统创建账号并发送验证邮件
- AND 5 秒内返回 201

### 边界情况
- WHEN 邮箱已被注册
- THEN 返回 409 Conflict
- AND 提示"该邮箱已注册"
```

### 🧩 阶段二：Plan（定方案）

**回答的问题**：在已知的约束下，怎么实现？

这一阶段把"业务目标"翻译成"技术决策"：

- 技术栈（语言、框架、数据库）
- 架构风格（单体 / 微服务 / Serverless）
- 关键依赖（第三方服务、合规要求）
- 性能与安全目标
- 风险点与备选方案

输出通常是 `plan.md`，可以**并列多个方案**让 AI 比较。比如："用 Postgres 全文检索 vs. 用 ElasticSearch"——AI 会根据 Spec 给出权衡分析。

```markdown
## 技术方案
- 框架：Go 1.22 + Gin
- 数据库：PostgreSQL 16
- 缓存：Redis
- 部署：Docker + Kubernetes
- 鉴权：JWT + Refresh Token
- 关键风险：邮件发送失败的重试策略
```

### ⚙️ 阶段三：Tasks（拆任务）

**回答的问题**：怎么把方案变成可执行、可验收的小步骤？

这一阶段**不写代码**，只生成任务清单。Spec Kit / Kiro 在这一步生成的 `tasks.md` 通常长这样：

```markdown
- [ ] T001 创建数据库表 `users`（含唯一索引）
- [ ] T002 实现 `POST /api/v1/register` 路由
- [ ] T003 集成邮件服务（带重试）
- [ ] T004 写单元测试（密码强度校验）
- [ ] T005 写集成测试（注册 → 验证 → 登录）
- [ ] T006 在 staging 环境跑一遍 e2e
```

**关键纪律**：

- 每个任务 2~5 分钟可以完成
- 任务之间有清晰依赖
- 每个任务有明确"完成"的定义（DoD）
- **不写代码**——代码是下一阶段的事

### 🚀 阶段四：Implement（按规格实现）

**回答的问题**：让 AI 在规格约束下，把任务逐个变成代码。

这一阶段 AI 才真正开始写代码，但它会**严格对照前面的 Spec/Plan/Tasks**。如果发现实现与规格冲突，应该回头改规格，而不是偷偷改逻辑。

> 一个常见的纪律：**任何偏离 Spec 的实现，都必须先回退到 Spec 修改并重新走批准流程**。

实践上还可以叠加 TDD、子代理并行、Code Review 等纪律——这部分可以参考 [Superpowers 与 OpenSpec 的配合使用](../Superpowers与OpenSpec的配合使用/index.zh-cn.md) 一文。

---

## 🧪 实践示例：做一个 CLI Todo 应用

把上面四阶段跑一遍。需求是"做一个命令行 Todo 工具，支持增删改查与本地持久化"。

### 💡 Step 1：明确业务目标

先用一句话把目标写清楚：

> 给我做一个 CLI 工具，名字叫 `todo`，支持添加、列出、完成、删除 Todo，数据存本地 JSON 文件。

然后让 AI 协助扩成结构化的 `spec.md`：

```markdown
## 功能需求

### US-1 添加 Todo
- WHEN 用户运行 `todo add "买牛奶"`
- THEN 在 todos.json 中追加一条 `{id, content, done=false, created_at}`
- AND 输出 "已添加 #1: 买牛奶"

### US-2 列出 Todo
- WHEN 用户运行 `todo list`
- THEN 按 id 升序列出所有未完成 Todo
- AND 每行格式 `[#id] [ ] content`

### US-3 标记完成
- WHEN 用户运行 `todo done 1`
- THEN 把 id=1 的 Todo 标记为 done
- AND 输出 "已完成 #1: 买牛奶"

### 边界情况
- 当 todos.json 不存在时，自动创建
- 当 id 不存在时，提示 "未找到该 Todo"
- 当 JSON 损坏时，备份原文件并重新创建
```

### 🔹 Step 2：编写规格

`plan.md`（技术方案）：

```markdown
- 语言：Go 1.22
- 第三方依赖：仅 `spf13/cobra`
- 存储：本地 JSON 文件，路径 `~/.todo/todos.json`
- 并发：单进程，不需要锁
- 测试：表格驱动 + golden file
```

### 📐 Step 3：拆解任务

`tasks.md`（任务清单）：

```markdown
- [ ] T001 初始化 Go module 与 cobra 骨架
- [ ] T002 实现 `add` 子命令
- [ ] T003 实现 `list` 子命令
- [ ] T004 实现 `done` 子命令
- [ ] T005 实现 `del` 子命令
- [ ] T006 实现 storage 层（load/save/append）
- [ ] T007 写单测覆盖所有命令
- [ ] T008 跑 go vet / go test / go build
```

### ✅ Step 4：交付与验证

把四份文档喂给 Claude Code，让它按 `tasks.md` 逐项实现，每个任务完成后自动跑测试：

```bash
# 提示词示例（使用 Claude Code + Spec Kit）
$spec-kit implement
```

AI 写完一个任务，会自检：

- 是不是严格按 `spec.md` 实现？
- 单测是否覆盖了所有验收条件？
- 是否触犯了 `plan.md` 中的"约束清单"？

如果发现规格本身漏了边界情况（比如"删除已完成的 Todo 要二次确认"），就**回头改 Spec**，让规格成为唯一真相。

最终交付物：

- 4 份 Markdown 文档（spec / plan / tasks / constitution）
- 一个可用的二进制 `todo`
- 一份与 Spec 一一对应的测试报告

---

## 💻 工具链速览

SDD 在 2025-2026 年迎来了一波工具爆发。这里按定位简单梳理：

### 🎯 GitHub Spec Kit

**当前最主流的开源 SDD 框架**。Python CLI 工具，原生支持 GitHub Copilot，兼容 Claude Code、Gemini CLI、Amazon Q 等 30+ AI 编码代理。

四阶段流程：**Specify → Plan → Tasks → Implement**。

最独特的设计是 **Constitution（宪法）**——一份放在项目根目录的长效文档，定义架构原则、编码规范、安全要求。AI 每次开发都必须遵守。

```bash
# 初始化
uv tool install spec-kit
specify init my-project
```

适合：想入门 SDD 的团队，已有 IDE 体系，不想切换工具链。

### 🤝 AWS Kiro

**最"原生"的规格驱动 AI IDE**。基于 Code OSS（VS Code 同源）构建，但要求开发者先正式定义需求，再进入开发。

三阶段流程：**Requirements → Design → Tasks**，每阶段用 EARS 格式描述，自动生成用户故事、验收条件、边界场景。

独有 **Agent Hooks**——事件驱动的自动化系统，保存文件后自动跑测试、刷新 README、执行安全扫描。

适合：企业级团队，需要正式 SDD 流程，多人协作的复杂项目。

### 🏗️ BMAD-METHOD

**最"团队化"的多 Agent 开发框架**。MIT 开源，内部编排 12+ AI 角色（产品经理、架构师、UX、Developer、QA、Scrum Master），Agent 之间通过文件"交接棒"完成交付。

```text
需求 → 设计 → 开发 → 测试 → 交付
```

适合：大型团队，多角色协作，需要严格流程的组织。

### 📚 其他值得关注的工具

| 工具 | 定位 | 一句话总结 |
|------|------|-----------|
| **OpenSpec** | 变更管理专家 | 提案式流程，`ADDED/MODIFIED/REMOVED` 增量标记 |
| **Augment Code** | 大规模代码上下文 | Context Engine 维护 40 万+ 文件级架构理解 |
| **TaskFlow** | 任务编排 | 把 Spec 拆成 DAG，让多个 AI Worker 并行执行 |
| **Claude Code Spec Mode** | 轻量级 Spec | 内置于 Claude Code，适合个人开发者 |

> 工具只是手段，不是目的。**先想清楚你的 Spec 应该长什么样，再选工具**。

---

## ⚠️ 常见陷阱与最佳实践

Spec Coding 不是银弹。方法论选错了，文档反而比代码更难维护。

### ❌ 陷阱一：把 Spec 写成"伪代码"

最常见的失败模式是——Spec 写得太细，直接写 SQL、建表语句、函数签名。

```markdown
# 错误示例
function register(email, password) {
  const hash = bcrypt(password, 10);
  return db.query(`INSERT INTO users ...`, [email, hash]);
}
```

**为什么有问题**：

- Spec 变成了"另一种代码"，AI 写代码时直接照抄，失去意义。
- 改业务逻辑要改两份（Spec + 实现），维护成本反而更高。
- 评审 Spec 等于评审代码，门槛变高，参与人变少。

**正确做法**：Spec 关注**意图与验收条件**，不关注实现细节。

```markdown
# 正确示例
WHEN 用户提交合法邮箱与密码
THEN 系统创建账号并发送验证邮件
AND 5 秒内返回 201
```

### 🔁 陷阱二：跳过 Plan 直接写代码

很多人写完 Spec 就急着让 AI 写代码，跳过 Plan 阶段。结果：AI 自由发挥，技术栈与项目现状脱节。

**正确做法**：Plan 阶段是"防 AI 跑偏"的最后一道闸。再小的项目，也要回答三个问题：

- 技术栈是什么？
- 有没有不能用的依赖？
- 性能/安全底线是什么？

### 💎 最佳实践总结

最后是几条在真实项目里验证过的经验：

1. **Spec 写在版本控制里**：与代码同仓库，PR 时一起 Review。
2. **Constitution 是项目宪法**：定义"AI 永远不能违反的规则"，比如"不允许用 `any`"、"不允许直接 `rm -rf`"。
3. **任务粒度 2~5 分钟**：太大的任务 AI 容易跑偏；太小又失去意义。
4. **规格变了，先 PR Spec**：实现跟着 Spec 走，不要反过来。
5. **Spec 也是产品文档**：业务方、PM、QA 都能看懂同一份 Spec。
6. **不要追求"完整 Spec"**：80% 的清晰度已经能换来 80% 的可靠性，最后 20% 让实现阶段补。
7. **Vibe Coding 与 Spec Coding 混用**：探索阶段用 Vibe，确定方案后切到 Spec。

---

## 📝 总结

回到开头那句话：**AI 编程缺的不是模型，是图纸**。

Spec Coding 不是要取代 Vibe Coding，而是给"自由探索"配上一条"工业化产线"。当你有了：

- 一份清晰的 Spec（业务目标）
- 一份严谨的 Plan（技术方案）
- 一份可验证的 Tasks（任务清单）
- 一份长效的 Constitution（项目宪法）

AI 就不再是"凭感觉的代码打字机"，而是一个**严格按图纸施工的工程师**。

未来一两年，随着模型能力的进一步提升，**瓶颈会更集中在 Spec 的质量上**。会写 Spec 的开发者，会比会写代码的开发者更稀缺。

如果你还没试过，可以从一个小工具开始：

1. 找一个本周要做的小功能
2. 花 20 分钟写一份 Spec
3. 让 Claude Code 按 Spec 实现
4. 体会一下"几乎一次跑通"的感觉

你会发现，**写 Spec 的过程本身，就是一次深度思考**。

---

> 延伸阅读：
>
> - [Superpowers 与 OpenSpec 的配合使用](../Superpowers与OpenSpec的配合使用/index.zh-cn.md)
> - [Claude Code 最佳实践](../Claude Code最佳实践/index.zh-cn.md)
> - [GitHub Spec Kit 官方仓库](https://github.com/github/spec-kit)
> - [AWS Kiro 官方介绍](https://kiro.dev/)
> - [EARS 需求描述规范](https://alistairmavin.com/ears/)
