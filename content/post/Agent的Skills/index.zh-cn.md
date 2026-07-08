---
date : '2026-03-27T10:20:00+08:00'
draft : false
title : 'Agent的Skills'
image : ""
categories : ["Agent"]
tags : ["智能体"]
description : "深入理解Agent Skills的概念、原理，以及它与Prompt、MCP、Function Calling的本质区别"
---

## 🎯 Skills是什么？

随着 AI 应用从简单的"单轮问答"走向复杂的"自动化工作流"，Skills 已经成为大模型应用架构中绕不开的工程概念。

更合理的工程做法，是把每一项**专项能力**分别写成独立的 `SKILL.md`：

- 代码审查标准
- 慢查询排查流程
- 报告生成规范

元数据常驻上下文，正文按需加载。新人能读懂，换项目能复用，Agent 按需激活执行，互不干扰。

### 🧠 核心定义

**Skill 是一个用自然语言定义的、具有特定领域上下文的逻辑指令集，本质上是通过延迟加载优化 Token 消耗的 sub-agent。**

在团队协作中，很多"隐性知识"都在老员工脑子里，比如代码规范、排查流程、Review 标准。

Skills 的核心价值在于：**把这些隐性规则变成显性的文档（SOP），让 AI 能够自主阅读、理解并执行。**

---

与传统的硬编码逻辑不同，Skill 不强制规定每一步的代码逻辑，而是用自然语言将决策权下放给模型。

模型通过 `load_skill()` 动态加载 `SKILL.md` 后，将其中定义的规则、流程和约束实时注入到推理上下文中，指导后续的工具调用和决策。这既保留了 Agent 处理不确定性的优势，又避免了纯代码编排的僵化。

---

### 🔧 关键机制

**延迟加载（Lazy Loading）**

- 元数据保持简短，常驻上下文
- 正文仅在触发时动态注入，避免挤占 Token

**动态上下文注入**

- 不同于静态文档的"阅读"，Skills 是将规则实时注入推理上下文
- 直接影响模型决策，而非仅作为参考

当你或 Claude 调用一个 skill 时，呈现的 `SKILL.md` 内容作为单个消息进入对话，并在会话的其余部分保持在那里。Claude Code 不会在后续轮次重新读取 skill 文件，因此将应该在整个任务中应用的指导写成常设说明，而不是一次性步骤。

[自动压缩](https://code.claude.com/docs/zh-CN/how-claude-code-works#when-context-fills-up) 在令牌预算内转发调用的 skills。当对话被总结以释放上下文时，Claude Code 在总结后重新附加每个 skill 的最新调用，保留前 5,000 个token。重新附加的 skills 共享 25,000 个token的组合预算。Claude Code 从最近调用的 skill 开始填充此预算，因此如果你在一个会话中调用了许多 skills，较旧的 skills 可能会在压缩后完全删除。

如果一个 skill 似乎在第一个响应后停止影响行为，内容通常仍然存在，模型正在选择其他工具或方法。加强 skill 的 `description` 和说明，以便模型继续偏好它，或使用 [hooks](https://code.claude.com/docs/zh-CN/hooks) 来确定性地强制行为。如果 skill 很大或你在它之后调用了其他几个，在压缩后重新调用它以恢复完整内容。

---

### 🚫 为什么不是"基于 Function Calling 封装"？

这个表述容易让人误以为 Skill 是某种 Function Calling 的语法糖。实际上，Skill 的核心机制是**上下文注入**——Agent 读取 Markdown 文档，把其中的规则和流程纳入推理上下文。

Function Calling 只是 Agent 执行某些动作时可能用到的底层手段，不是 Skills 本身的定义层。

> 注意：`load_skill()` 是对"Agent 读取并激活 SKILL.md"这一过程的概念性描述，不同工具的实际触发方式会有差异。

---

## 🔍 Skills与相关概念的区别

### 📝 Skills vs Prompt

| 维度 | Prompt | Skills |
|------|--------|--------|
| **本质** | 单次对话的文本指令 | 可持久化、可发现的能力单元 |
| **复用性** | 随对话上下文丢失，难以维护 | 标准化封装，跨项目、多场景复用 |
| **加载机制** | 全量载入（挤占 Token） | 延迟加载（按需读取正文） |

提示词工程更像是“这一次对话里，我把要求写清楚”。Skill更像是“把这套要求、流程、模板，甚至脚本，打包成一个可复用的能力”。
- 复用性不一样
    - 提示词工程通常是一次性的，或者用户得反复复制粘贴同一套 prompt。
    - Skill 是可复用的，后面再遇到类似任务，可以直接按这套固定方法做
- 封装的内容不一样
    - 普通 prompt 主要是文字指令。
    - Skill 除了指令，还可以带参数、条件、循环等复杂逻辑。
    **一句话总结**：Prompt 是用户即时表达意图的载体；Skills 是包含元数据（何时使用）+ 正文（如何执行）的完整方案，通过 `load_skill()` 机制按需加载到上下文。

---

### 🌐 Skills vs MCP

这是最容易产生误解的地方。

| 维度 | MCP (Model Context Protocol) | Skills |
|------|------------------------------|--------|
| **核心思路** | 标准化连接：通过 JSON-RPC 统一数据格式 | 逻辑编排：用自然语言描述复杂执行路径 |
| **定义方式** | 在 Server 端用代码（TS/Python）写死逻辑 | 在 `SKILL.md` 中用自然语言引导模型决策 |
| **环境依赖** | 需要运行一个 MCP Server 进程 | 依赖可执行环境（如本地 Shell 或沙箱） |
| **哲学** | 以协议为中心：一次编写，所有 AI 通用 | 以模型为中心：利用模型推理能力处理不确定性 |

- **MCP 解决的是连通性**：它像 USB-C，让 AI 能以统一格式读文件、查数据库。

- **Skills 解决的是编排逻辑**：它像一份说明书，告诉 AI 如何执行复杂任务流。这些任务完全可以包括调用多个 MCP 工具。

**两者关系**：它们不是竞争关系，而是解决不同层面的问题。MCP 负责把外部系统接入，Skills 负责决定什么时候用、怎么组合这些能力。一个高级 Skill 的底层往往调用多个 MCP 工具。

- 当你的问题核心是“这一类任务每次都要按同一套方法做”。比如固定格式周报、PRD 摘要模板。这类场景重点是流程复用、输出一致、少重复解释，更适合 Skill。Skills 适合可重复任务、团队规范、模板/checklist、多步骤工作流
- 当你的问题核心是“模型需要访问某个外部系统，不连上就做不了”。比如要查 Notion、日历、数据库、GitHub、Figma、内部工具，或者要调用搜索、执行器、业务 API。这类场景重点是连接能力和工具能力，更适合 MCP。MCP 官方定义里明确把它定位成连接外部数据源、工具和工作流的标准接口。

---

### ⚡ Function Calling vs Skills

| 维度 | Function Calling | Skills |
|------|-----------------|--------|
| **层级** | 底层机制 | 上层应用 |
| **粒度** | 原子操作（单次工具调用） | 复合流程（多步骤决策 + 工具组合） |

Skills 没有创造新能力，而是通过自然语言文档将能力组织成更易用的形式。

Agent 读取 `SKILL.md`，将规则和流程注入推理上下文。根据上下文指导，Agent 可能通过 Function Calling 执行脚本、读取资源或调用 MCP 工具。

---

### 🎨 四层关系总结

| 组件 | 一句话定义 | 形象类比 |
|------|-----------|---------|
| **Prompt** | 即时意图表达的载体 | 用户说的话 |
| **Function Calling** | LLM 输出结构化调用的能力 | 神经信号，一切的基础 |
| **MCP** | 标准化的工具接入协议 | USB-C 接口 |
| **Skills** | 用自然语言定义的 sub-agent | 任务说明书 |

**层级关系**：Function Calling 是地基 → Prompt 表达意图 → MCP 负责连通外部系统 → Skills 负责编排复杂任务流。

> 一句话总结：**Prompt 承载意图，Function Calling 实现交互，MCP 负责连通外部系统，Skills 负责编排复杂任务流——从"说什么"到"怎么做"再到"聪明地做"。**

---

## 🧪 Skills示例

### 📂 Skill的目录结构

从结构上看，Skill 核心就是一个 `SKILL.md` 文件，包含元数据（描述什么时候用）和正文（具体的执行 SOP）。

设计亮点是**渐进式披露**：元数据常驻上下文，AI 知道有哪些技能可用；正文按需加载，只有触发时才读取。

复杂点的 Skill 还会有附加的资源目录、脚本和参考文档：

```text
skill-name/
├── SKILL.md              # 必需：元数据（何时使用）+ 正文（指令、流程、示例）
├── scripts/              # 可选：可执行脚本（Python/Bash），按需调用
├── references/           # 可选：参考文档，按需读取
└── assets/               # 可选：模板、图片等资源
```



Skills 可以在其目录中包含多个文件。这使 `SKILL.md` 专注于要点，同时让 Claude 仅在需要时访问详细的参考资料。大型参考文档、API 规范或示例集合不需要在每次 skill 运行时加载到上下文中。

```text
my-skill/
├── SKILL.md (required - overview and navigation)
├── reference.md (detailed API docs - loaded when needed)
├── examples.md (usage examples - loaded when needed)
└── scripts/
    └── helper.py (utility script - executed, not loaded)
```

从 `SKILL.md` 中引用支持文件，以便 Claude 知道每个文件包含什么以及何时加载它：

```markdown
## Additional resources

- For complete API details, see [reference.md](reference.md)
- For usage examples, see [examples.md](examples.md)
```

将 `SKILL.md` 保持在 500 行以下。将详细的参考资料移到单独的文件中。

---

### 📄 SKILL.md示例结构

```markdown
# code-review-expert

## Meta
- name: code-review-expert
- description: 资深工程师视角的结构化代码审查
- triggers: 当需要审查代码质量时激活

## Capabilities
1. 架构设计审查
2. SOLID 原则合规性检查
3. 安全性风险扫描
4. 性能问题识别
5. 错误处理完整性
6. 边界条件覆盖

## Review Framework
1. 接收代码片段或文件路径
2. 逐维度分析（见 Capabilities）
3. 输出结构化审查报告
4. 针对每项问题提供修复建议

## Output Format
- 问题编号与严重程度
- 问题描述与代码位置
- 修复建议与参考规范
```

---

### 💼 项目实战场景

在工程实践中，Skills 主要用于固化工程标准：

| Skill 名称 | 用途 |
|-----------|------|
| `code-reviewer` | 审查代码规范，从架构合理性、异常处理、日志规范、安全风险等多维度进行结构化审查 |
| `api-endpoint-generator` | 按项目统一响应结构与异常模型生成标准化接口代码 |
| `database-access-review` | 审查数据库访问逻辑，关注索引使用与慢查询风险 |
| `refactor-analysis` | 先评估影响范围与依赖关系，再输出分步骤重构方案 |
| `security-audit` | 扫描 SQL 拼接、XSS、权限绕过等常见安全风险 |

---

使用 Skills 的好处：**AI 在执行任务时，不再是"随缘发挥"，而是严格执行团队标准，保持质量一致性。**

---

### 📚 推荐Skills资源

- [skills.sh](https://skills.sh/)：查找热门和所需的 Skills
- [Superpowers](https://github.com/obra/superpowers)：内置多种开箱即用的开发 Skills
- [Claude Code 内置 Skills](https://docs.anthropic.com/en/docs/claude-code)：包括 `/simplify`（审查修复）、`/batch`（批量修改）、`/debug`（排查问题）等

---

## 🛠️ 如何开发一个Skill

### 📑 Skill 内容的类型

Skill 文件可以包含任何说明，但思考用户想如何调用它们有助于指导要包含的内容：

**参考内容** 添加 Claude 应用于当前工作的知识。约定、模式、风格指南、领域知识。此内容内联运行，以便 Claude 可以将其与对话上下文一起使用。

```yaml
---
name: api-conventions
description: API design patterns for this codebase
---

When writing API endpoints:
- Use RESTful naming conventions
- Return consistent error formats
- Include request validation
```

**任务内容** 为 Claude 提供特定操作的分步说明，如部署、提交或代码生成。这些通常是想使用 `/skill-name` 直接调用的操作，而不是让 Claude 决定何时运行它们。添加 `disable-model-invocation: true` 以防止 Claude 自动触发它。

```yaml
---
name: deploy
description: Deploy the application to production
context: fork
disable-model-invocation: true
---

Deploy the application:
1. Run the test suite
2. Build the application
3. Push to the deployment target
```

 `SKILL.md` 可以包含任何内容，但思考用户想如何调用该 skill（由你、由 Claude 或两者）以及你想在哪里运行它（内联或在 subagent 中）有助于指导要包含的内容。对于复杂的 skills，你也可以 [添加支持文件](#add-supporting-files) 以保持主 skill 的专注。

保持主体本身简洁。一旦 skill 加载，其内容**在整个会话中保持在上下文中**，因此每一行都是一个重复的令牌成本。说明要做什么而不是叙述如何或为什么，并应用与 [CLAUDE.md 内容](https://code.claude.com/docs/zh-CN/best-practices#write-an-effective-claude-md) 相同的简洁性测试。

### ⚙️ Skill的相关配置

除了 markdown 内容外，可以使用 `SKILL.md` 文件顶部 `---` 标记之间的 YAML frontmatter 字段来配置 skill 行为：

```yaml
---
name: my-skill
description: What this skill does
disable-model-invocation: true
allowed-tools: Read Grep
---

Your skill instructions here...
```

所有字段都是可选的。建议使用 `description` ，以便 Claude 知道何时使用该 skill。

| 字段                       | 必需 | 描述                                                         |
| -------------------------- | ---- | ------------------------------------------------------------ |
| `name`                     | 否   | Skill 列表中显示的显示名称。默认为目录名称。请参阅 [Skill 如何获得其命令名称](#how-a-skill-gets-its-command-name) 以了解这与你输入的名称在 `/` 后的调用方式有何不同。 |
| `description`              | 推荐 | Skill 的功能以及何时使用它。Claude 使用它来决定何时应用该 skill。如果省略，使用 markdown 内容的第一段。将关键用例放在前面：组合的 `description` 和 `when_to_use` 文本在 skill 列表中被截断为 1,536 个字符以减少上下文使用。 |
| `when_to_use`              | 否   | 关于 Claude 何时应该调用该 skill 的额外上下文，例如触发短语或示例请求。附加到 skill 列表中的 `description` ，并计入 1,536 个字符的上限。 |
| `argument-hint`            | 否   | 自动完成期间显示的提示，指示预期的参数。示例： `[issue-number]` 或 `[filename] [format]` 。 |
| `arguments`                | 否   | 用于 skill 内容中 [`$name` 替换](#available-string-substitutions) 的命名位置参数。接受空格分隔的字符串或 YAML 列表。名称按顺序映射到参数位置。 |
| `disable-model-invocation` | 否   | 设置为 `true` 以防止 Claude 自动加载此 skill。用于你想使用 `/name` 手动触发的工作流。也防止该 skill 被 [预加载到 subagents](https://code.claude.com/docs/zh-CN/sub-agents#preload-skills-into-subagents) 中。从 v2.1.196 开始，也防止该 skill 在 [计划任务](https://code.claude.com/docs/zh-CN/scheduled-tasks) 使用该 skill 作为其提示时运行。默认值： `false` 。 |
| `user-invocable`           | 否   | 设置为 `false` 以从 `/` 菜单中隐藏。用于用户不应直接调用的背景知识。默认值： `true` 。 |
| `allowed-tools`            | 否   | 当此 skill 处于活动状态时，Claude 可以使用而无需请求权限的工具。接受空格分隔的字符串或 YAML 列表。 |
| `disallowed-tools`         | 否   | 当此 skill 处于活动状态时从 Claude 的可用工具池中移除的工具。用于不应该调用某些工具的自主 skills，例如用于后台循环的 `AskUserQuestion` 。接受空格分隔的字符串或 YAML 列表。当你发送下一条消息时，限制会清除。 |
| `model`                    | 否   | 当此 skill 处于活动状态时要使用的模型。覆盖适用于当前轮的其余部分，不保存到设置；会话模型在你的下一个提示时恢复。接受与 [`/model`](https://code.claude.com/docs/zh-CN/model-config) 相同的值，或 `inherit` 以保持活动模型。被你的组织的 [`availableModels`](https://code.claude.com/docs/zh-CN/model-config#restrict-model-selection) 允许列表排除的值不会被使用，会话保持其当前模型。 |
| `effort`                   | 否   | 当此 skill 处于活动状态时的 [工作量级别](https://code.claude.com/docs/zh-CN/model-config#adjust-effort-level) 。覆盖会话工作量级别。默认值：继承自会话。选项： `low` 、 `medium` 、 `high` 、 `xhigh` 、 `max` ；可用级别取决于模型。 |
| `context`                  | 否   | 设置为 `fork` 以在分叉的 subagent 上下文中运行。             |
| `agent`                    | 否   | 当设置 `context: fork` 时要使用的 subagent 类型。            |
| `hooks`                    | 否   | 限定于此 skill 生命周期的 hooks。有关配置格式，请参阅 [Skills 和代理中的 Hooks](https://code.claude.com/docs/zh-CN/hooks#hooks-in-skills-and-agents) 。 |
| `paths`                    | 否   | Glob 模式，限制何时激活此 skill。接受逗号分隔的字符串或 YAML 列表。设置后，Claude 仅在处理与模式匹配的文件时自动加载该 skill。使用与 [路径特定规则](https://code.claude.com/docs/zh-CN/memory#path-specific-rules) 相同的格式。 |
| `shell`                    | 否   | 用于此 skill 中 `` !`command` `` 和 ` ```! ` 块的 shell。接受 `bash` （默认）或 `powershell` 。设置 `powershell` 在 Windows 上通过 PowerShell 运行内联 shell 命令。需要 `CLAUDE_CODE_USE_POWERSHELL_TOOL=1` 。 |



#### 🔤 可用的字符串替换

Skills 支持 skill 内容中动态值的字符串替换：

| 变量                    | 描述                                                         |
| ----------------------- | ------------------------------------------------------------ |
| `$ARGUMENTS`            | 调用 skill 时传递的所有参数。如果内容中不存在 `$ARGUMENTS` ，参数将作为 `ARGUMENTS: <value>` 追加。 |
| `$ARGUMENTS[N]`         | 按 0 基索引访问特定参数，如 `$ARGUMENTS[0]` 表示第一个参数。 |
| `$N`                    | `$ARGUMENTS[N]` 的简写，如 `$0` 表示第一个参数或 `$1` 表示第二个参数。 |
| `$name`                 | 在 [`arguments`](#frontmatter-reference) frontmatter 列表中声明的命名参数。名称按顺序映射到位置，因此使用 `arguments: [issue, branch]` 时，占位符 `$issue` 扩展为第一个参数， `$branch` 扩展为第二个参数。 |
| `${CLAUDE_SESSION_ID}`  | 当前会话 ID。适用于日志记录、创建会话特定文件或将 skill 输出与会话关联。 |
| `${CLAUDE_EFFORT}`      | 当前工作量级别： `low` 、 `medium` 、 `high` 、 `xhigh` 或 `max` 。Ultracode 不是一个不同的级别，报告为 `xhigh` 。使用此来根据活动工作量设置调整 skill 说明。 |
| `${CLAUDE_SKILL_DIR}`   | 包含 skill 的 `SKILL.md` 文件的目录。对于插件 skills，这是插件内 skill 的子目录，而不是插件根目录。在 bash 注入命令中使用它来引用与 skill 捆绑的脚本或文件，无论当前工作目录如何。 |
| `${CLAUDE_PROJECT_DIR}` | 项目根目录。这是与 [hooks](https://code.claude.com/docs/zh-CN/hooks#reference-scripts-by-path) 和 MCP 服务器相同的路径，作为 `CLAUDE_PROJECT_DIR` 接收。使用此来引用项目本地脚本或文件，例如 `${CLAUDE_PROJECT_DIR}/.claude/hooks/helper.sh` ，独立于 skill 的安装位置。 |

`${CLAUDE_PROJECT_DIR}` 替换需要 Claude Code v2.1.196 或更高版本。它适用于 skill 主体和 [`allowed-tools`](#frontmatter-reference) frontmatter，因此权限规则如 `Bash(${CLAUDE_PROJECT_DIR}/scripts/lint.sh *)` 解析为 skill 主体使用的相同路径。

索引参数使用 shell 风格的引用，因此用引号包装多词值以将其作为单个参数传递。例如， `/my-skill "hello world" second` 使 `$0` 扩展为 `hello world` ， `$1` 扩展为 `second` 。 `$ARGUMENTS` 占位符始终扩展为完整的参数字符串，如输入的那样。

要包含文字 `$` 在数字、 `ARGUMENTS` 或声明的参数名称之前，例如散文中的 `$1.00` ，用反斜杠转义它： `\$1.00` 。反斜杠在任何其他 `$` 之前保持不变。只有直接在令牌之前的单个反斜杠才能转义它。双反斜杠（如 `\\$1` ）保留两个反斜杠， `$1` 仍然扩展为参数值。

**使用替换的示例：**

```yaml
---
name: session-logger
description: Log activity for this session
---

Log the following to logs/${CLAUDE_SESSION_ID}.log:

$ARGUMENTS
```



#### 👥 配置skill的调用方

默认情况下，用户和 Claude 都可以调用任何 skill。你可以输入 `/skill-name` 直接调用它，Claude 可以在与你的对话相关时自动加载它。两个 frontmatter 字段让你限制这一点：

- **`disable-model-invocation: true`** ：只有你可以调用该 skill。用于有副作用的工作流或你想控制时间的工作流，如 `/commit` 、 `/deploy` 或 `/send-slack-message` 。你不希望 Claude 因为你的代码看起来准备好了就决定部署。
- **`user-invocable: false`** ：只有 Claude 可以调用该 skill。用于不可作为命令操作的背景知识。 `legacy-system-context` skill 解释了旧系统的工作原理。Claude 在相关时应该知道这一点，但 `/legacy-system-context` 对用户来说不是一个有意义的操作。

此示例创建一个只有你可以触发的部署 skill。 `disable-model-invocation: true` 字段防止 Claude 自动运行它：

```yaml
---
name: deploy
description: Deploy the application to production
disable-model-invocation: true
---

Deploy $ARGUMENTS to production:

1. Run the test suite
2. Build the application
3. Push to the deployment target
4. Verify the deployment succeeded
```

以下是两个字段如何影响调用和上下文加载：

| Frontmatter                      | 你可以调用 | Claude 可以调用 | 何时加载到上下文中                       |
| -------------------------------- | ---------- | --------------- | ---------------------------------------- |
| （默认）                         | 是         | 是              | 描述始终在上下文中，调用时加载完整 skill |
| `disable-model-invocation: true` | 是         | 否              | 描述不在上下文中，你调用时加载完整 skill |
| `user-invocable: false`          | 否         | 是              | 描述始终在上下文中，调用时加载完整 skill |

在常规会话中，skill 描述被加载到上下文中，以便 Claude 知道什么可用，但完整 skill 内容仅在调用时加载。 [预加载 skills 的 Subagents](https://code.claude.com/docs/zh-CN/sub-agents#preload-skills-into-subagents) 的工作方式不同：完整 skill 内容在启动时注入。



#### 🔐 配置 skill 的工具集

`allowed-tools` 字段在 skill 处于活动状态时授予对列出的工具的权限，因此 Claude 可以使用它们而无需提示你获得批准。它不限制哪些工具可用：每个工具仍然可调用，你的 [权限设置](https://code.claude.com/docs/zh-CN/permissions) 仍然管理不在列表中的工具。

对于检入项目的 `.claude/skills/` 目录的 skills， `allowed-tools` 在你接受该文件夹的工作区信任对话后生效，与 `.claude/settings.json` 中的权限规则相同。在信任存储库之前查看项目 skills，因为 skill 可以授予自己广泛的工具访问权限。

此 skill 让 Claude 在你调用它时运行 git 命令而无需每次使用批准：

```yaml
---
name: commit
description: Stage and commit the current changes
disable-model-invocation: true
allowed-tools: Bash(git add *) Bash(git commit *) Bash(git status *)
---
```

要在 skill 处于活动状态时从 Claude 的可用工具池中移除某些工具，请在 skill 的 frontmatter 中的 `disallowed-tools` 中列出它们。当你发送下一条消息时，限制会清除。要在所有 skills 和提示中阻止工具，请在你的 [权限设置](https://code.claude.com/docs/zh-CN/permissions) 中添加拒绝规则。

### 📨 将参数传递给 skills

用户和 Claude 都可以在调用 skill 时传递参数。参数可通过 `$ARGUMENTS` 占位符获得。

此 skill 按编号修复 GitHub 问题。 `$ARGUMENTS` 占位符被替换为 skill 名称后面的任何内容：

```yaml
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---

Fix GitHub issue $ARGUMENTS following our coding standards.

1. Read the issue description
2. Understand the requirements
3. Implement the fix
4. Write tests
5. Create a commit
```

当用户运行 `/fix-issue 123` 时，Claude 收到”Fix GitHub issue 123 following our coding standards…”

如果用户使用参数调用 skill 但 skill 不包含 `$ARGUMENTS` ，Claude Code 会将 `ARGUMENTS: <your input>` 追加到 skill 内容的末尾，以便 Claude 仍然看到用户输入的内容。

用户也可以在一条消息的开头堆叠多个 skills。从 v2.1.199 开始，输入 `/code-review /fix-issue 123` 会加载两个 skills 并将尾部文本 `123` 作为 `$ARGUMENTS` 传递给每个 skills。在早期版本中，只有第一个 skill 加载并接收 `/fix-issue 123` 作为文字参数文本。

Claude Code 扩展第一个 skill 加上最多五个堆叠在其后的 skills。扩展在第一个不是内联用户可调用 skill 的令牌处停止，因此作为 [分叉 subagent](#run-skills-in-a-subagent) 运行的 skill 或其参数本身可能以斜杠命令开头的 skill（如 `/loop` ）也会在那里结束；该令牌及其后的所有内容成为每个扩展 skill 的参数文本。

要按位置访问单个参数，使用 `$ARGUMENTS[N]` 或较短的 `$N` ：

```yaml
---
name: migrate-component
description: Migrate a component from one framework to another
---

Migrate the $ARGUMENTS[0] component from $ARGUMENTS[1] to $ARGUMENTS[2].
Preserve all existing behavior and tests.
```

运行 `/migrate-component SearchBar React Vue` 会将 `$ARGUMENTS[0]` 替换为 `SearchBar` ， `$ARGUMENTS[1]` 替换为 `React` ， `$ARGUMENTS[2]` 替换为 `Vue` 。使用 `$N` 简写的相同 skill：

```yaml
---
name: migrate-component
description: Migrate a component from one framework to another
---

Migrate the $0 component from $1 to $2.
Preserve all existing behavior and tests.
```

### 🔀 在 subagent 中运行 skills

当你想让 skill 在隔离中运行时，在你的 frontmatter 中添加 `context: fork` 。skill 内容变成驱动 subagent 的提示。它将无法访问你的对话历史。

`context: fork` 仅对具有明确说明的 skills 有意义。如果你的 skill 包含”使用这些 API 约定”之类的指南而没有任务，subagent 会收到指南但没有可操作的提示，并返回而没有有意义的输出。

Skills 和 [subagents](https://code.claude.com/docs/zh-CN/sub-agents) 以两个方向协同工作：

| 方法                          | 系统提示                  | 任务              | 也加载                                |
| ----------------------------- | ------------------------- | ----------------- | ------------------------------------- |
| 带有 `context: fork` 的 Skill | 来自代理类型              | SKILL.md 内容     | CLAUDE.md，除非代理是 Explore 或 Plan |
| 带有 `skills` 字段的 Subagent | Subagent 的 markdown 正文 | Claude 的委派消息 | 预加载的 skills + CLAUDE.md           |

使用 `context: fork` ，你在你的 skill 中编写任务并选择一个代理类型来执行它。内置的 Explore 和 Plan 代理 [跳过 CLAUDE.md 和 git 状态](https://code.claude.com/docs/zh-CN/sub-agents#what-loads-at-startup) 以保持其上下文较小，因此使用 `agent: Explore` 的分叉 skill 仅看到 SKILL.md 内容和代理自己的系统提示。对于反向情况，其中你定义使用 skills 作为参考资料的自定义 subagent，请参阅 [Subagents](https://code.claude.com/docs/zh-CN/sub-agents#preload-skills-into-subagents) 。

此 skill 在分叉的 Explore 代理中运行研究。skill 内容变成任务，代理提供针对代码库探索优化的只读工具：

```yaml
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:

1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references
```

当此 skill 运行时：

1. 创建一个新的隔离上下文
2. Subagent 接收 skill 内容作为其提示（“Research $ARGUMENTS thoroughly…”）
3. `agent` 字段确定执行环境（模型、工具和权限）
4. 结果被总结并返回到你的主对话

`agent` 字段指定要使用的 subagent 配置。选项包括内置代理（ `Explore` 、 `Plan` 、 `general-purpose` ）或来自 `.claude/agents/` 的任何自定义 subagent。如果省略，使用 `general-purpose` 。

---

## 📌 总结

**Skills 的本质**：用自然语言定义的、具有特定领域上下文的逻辑指令集，通过延迟加载优化 Token 消耗，本质上是 sub-agent。

**Skills 的价值**：

- **模块化**：每个 Skill 专注一项能力，互不干扰
- **可复用**：换项目时直接迁移，新人易读懂
- **按需加载**：元数据常驻，正文按需注入，不挤占上下文

**Skills 与其他组件的关系**：

- Prompt 承载意图
- Function Calling 实现交互
- MCP 负责连通外部系统
- Skills 负责编排复杂任务流

**适用场景**：当用户的 Agent 工作流节点增多、审查标准变复杂、团队需要协作时，Skills 是将"隐性知识"显性化、工程化的最佳实践。

---

