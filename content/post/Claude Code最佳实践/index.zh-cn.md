---
date : '2026-06-27T17:18:00+08:00'
draft : false
title : 'Claude Code 最佳实践'
image : ""
categories : ["AI Coding"]
tags : []
description : "整理Claude Code的实用技巧与最佳实践，覆盖安装配置、核心命令、CLAUDE.md记忆、Subagents、MCP扩展等高频使用场景"
---

## 🧠 什么是 Claude Code

Claude Code 是 Anthropic 推出的**终端优先（Terminal-First）的 AI 编程助手**，它不是一个聊天框里的代码补全插件，而是一个直接运行在本地命令行、能够**读取、编辑、执行**真实项目代码的 Agent。

与传统的 IDE 插件式 Copilot 不同，Claude Code 把模型放进了你熟悉的开发环境里——Shell、文件树、Git、测试、构建脚本——让模型拥有和开发者一样的“动手能力”。

### 📖 核心理念

- **Agent 而非补全**：模型不只生成代码片段，而是会主动规划、调用工具、执行命令、回看结果。
- **终端即界面**：所有交互都发生在命令行中，没有额外的 IDE 锁定，跨编辑器、跨语言、跨项目通用。
- **上下文即工程**：通过 `CLAUDE.md`、Subagents、Skills、MCP 等机制，把项目的“隐性知识”显性化喂给模型。

### ⚖️ 与传统 AI 编程助手的区别

| 维度 | 传统 Copilot | Claude Code |
|------|--------------|-------------|
| **交互形态** | 行内补全 / 聊天面板 | 终端会话 + 多轮规划 |
| **环境感知** | 当前打开的文件 | 整个仓库、Git 历史、CLI 工具链 |
| **执行能力** | 只能生成代码建议 | 可读、写、执行、回滚 |
| **记忆机制** | 无持久化 | `CLAUDE.md` + 项目级上下文 |
| **扩展能力** | 插件市场 | MCP 协议 + Subagents + Skills |

> 简单说：传统 Copilot 帮你打字，Claude Code 帮你**做事**。

---

## 🛠️ 安装与配置

### 💻 安装方式

Claude Code 通过 npm 全局安装，安装前需要 Node.js 18+：

```bash
# 全局安装
npm install -g @anthropic-ai/claude-code

# 安装完成后启动
claude
```

启动后会引导你完成 OAuth 登录，登录成功后即可在当前目录下使用。

### 🎛️ 基础配置

Claude Code 的配置主要围绕三件事：

1. **环境变量**：API Key、模型选择、Token 限额等
2. **全局偏好**：默认行为、主题、快捷键
3. **项目配置**：放在项目根目录的 `.claude/` 目录和 `CLAUDE.md`

```bash
# 初始化当前项目（生成 CLAUDE.md 和 .claude 配置目录）
claude init

# 查看当前配置
claude config list

# 修改某一项配置
claude config set model claude-opus-4
```

> 提示：如果是第一次接触 Claude Code，可以先在空目录里 `claude init`，熟悉一下它生成的目录结构和 `CLAUDE.md` 模板。

---

## ⌨️ 核心命令与快捷键

### 🔄 常用斜杠命令

Claude Code 内置了一组以 `/` 开头的命令，覆盖日常高频操作：

- `/init`：在当前目录生成 `CLAUDE.md` 项目记忆文件
- `/compact`：当上下文变长时压缩对话历史，节省 Token
- `/clear`：清空当前会话上下文，开启新对话
- `/resume`：恢复历史会话，继续之前的任务
- `/memory`：打开 `CLAUDE.md` 进行编辑
- `/agents`：管理 Subagents 配置
- `/mcp`：管理 MCP 服务器连接
- `/review`：让模型审查当前分支的代码改动
- `/security-review`：执行安全审查
- `/cost`：查看当前会话的 Token 消耗
- `/help`：查看所有可用命令

### 💡 高效交互技巧

- **多行输入**：使用 `\` 续行，或者在引号内写多行；按两次回车提交
- **@ 引用文件**：`@src/main.go` 可以让模型直接读取引用文件的内容
- **! 运行命令**：`!git status` 让 Claude Code 执行 Shell 命令并把输出回灌到上下文
- **图片拖入**：直接把截图拖进终端，模型可以“看到”报错截图或设计稿
- **Plan 模式**：先让模型给出执行计划，确认后再让其实施，避免误改

```bash
# 示例：在 Plan 模式下让模型规划重构方案
claude --plan "重构用户模块的权限校验逻辑"
```

---

## 📁 CLAUDE.md 项目记忆

`CLAUDE.md` 是 Claude Code 的**项目级记忆文件**，相当于给模型的一份“新员工入职手册”。每次会话开始时，它的内容会自动注入到上下文。

### 🗂️ 分层记忆
记忆文件分三层：
- 根目录的 `CLAUDE.md`：项目级通用规则
- 子目录的 `CLAUDE.md`：模块级特殊约定（模型就近加载）
- 全局的 `~/.claude/CLAUDE.md`：个人偏好（跨项目生效）

```text
my-project/
├── CLAUDE.md              # 项目级
├── pkg/
│   └── CLAUDE.md          # 公共库约定
├── internal/
│   └── service/
│       └── CLAUDE.md      # 业务层特殊规范
```
### 🧩 记忆文件的最佳实践

#### 💰 复利工程
几乎每个教程都会提到，`CLAUDE.md` ，但多数人把它写成了一篇又臭又长的说明文档，塞满了废话
Anthropic 内部团队分享过，他们认为 `CLAUDE.md` 最佳实践是：每次Claude犯了一个错误，都要记录在 `CLAUDE.md` 中。不是人工维护，而是模型自己记录。每次纠正错误，最后加一句
```text
把这个教训更新到 `CLAUDE.md` 中，确保你以后不会再犯
```
Claude 写给自己看的建议，它自己最明白如果遵守。

#### 🧹 定期更新瘦身
Claude.md要定期瘦身。写了三个月，其中可能有很多过时的规则，可以隔几周让Claude帮你review一篇，删除掉不再使用的规则。保持精简。这个文件每个会话都会加载，越短越好。

- **保持简洁**：只写“必须知道”的东西，过长的 `CLAUDE.md` 会挤占 Token
- **分模块组织**：用清晰的二级标题区分“构建命令”、“代码规范”、“禁止事项”
- **定期更新**：项目演进时同步更新，否则模型会按过时规则办事
- **避免敏感信息**：不要把密钥、Token、内部域名写进去

## ⚙️ Hook 的最佳实践
CLAUDE.md本质上只是建议，Claude大多数时候遵守，但是他不是强制的。Hooks是强制的。
hook真正的价值在于控制Claude的行为，这是传统工具无法做到的。

hooks最优价值的用法有以下几点

### 🎯 使用 SessionStart 动态加载 skill

Claude Code 的 skill 系统有一个字符预算，默认是上下文窗口的 2%（大约 16,000 字符）。所有 skill 的描述信息需要塞进这个预算里，Claude 才知道有哪些 skill 可以用。当你装的 skill 越来越多，超出预算的 skill 就会被静默丢弃——你以为装了，其实 Claude 根本看不见。跑 /context 可以看到被排除的 skill 有哪些。

解决方案:不要一股脑把所有 skill 都装上，用 SessionStart hook 根据当前项目的技术栈动态挂载。

这样你可以在 ~/.claude/skill-library/ 里攒几十个 skill，但每个项目启动时只挂载真正用得上的那几个。字符预算花在刀刃上，不会因为装了一堆 Python skill 把你 React 项目里急需的前端 skill 给挤掉了。

---

## 🌀 并行工作
先说一个反直觉的情况：Anthropic 内部团队分享过，他们认为Claude Code 最大的生产力提升来自同时开3-5个会话并行干活

具体操作是用git worktree。你可以直接在命令行输入
```bash
claude --worktree
```
它会自动帮你创建一个隔离的工作目录，在里面开一个全新的会话。加上--tmux参数，会自动在tmux中打开一个新的窗口。

举一个实际场景:你同时要改一个API的逻辑，修复一个前端bug，写一个单元测试。以前只能排队干，现在使用三个worktree并行工作。每个里面都有一个Claude在干活
---

## ✅ 验证能力

Anthropic 官方 power user tips 里面，加粗标注了一句话：如果你只学一个技巧，请学这个——给 Claude 一种验证自己输出的方式。
道理很简单：如果 Claude 能自己跑测试、自己检查结果，它就能自己迭代到正确为止。你只需要把验证手段告诉它。

做后端？让它跑完代码之后自动跑测试。做前端？装 Chrome 扩展。这个扩展的价值被严重低估了——想想看，你让一个工程师写网页但不给他浏览器用，能写出好东西吗？装了扩展之后，Claude 能看到页面长什么样，能自己迭代到视觉效果满意为止。

Desktop 版本内置了一个浏览器，能自动启动和测试 Web 服务器。如果你在 CLI 或 VS Code 里工作，用 Chrome 扩展也能达到类似效果。

还有个 /simplify 命令，在改完代码之后跑一下，它会启动多个并行 agent，从代码复用、质量、效率、规范合规几个维度同时审查你刚改的代码。一个命令完成一轮 code review。

更高阶的验证方式：让 Claude 自己质疑自己。做完研究或分析之后，告诉它：

## 🤖 Subagents 分工协作

当一个任务涉及多个领域（前端 + 后端 + 数据库 + 测试）时，可以让 Claude Code 启动**多个 Subagent** 并行处理：Subagent 的本质是上下文隔离。主 agent 处理核心逻辑，子 agent 负责具体的子任务，做完把结果交回来。主 agent 的上下文窗口保持干净，不会被大量细节信息污染。

最直接的用法：在你的 prompt 后面加一句 "use subagents"，Claude 就会自动把任务拆分成多个子任务并行处理。

```bash
# 让模型自主决定是否拆 Subagent
claude "为这个新功能补全前后端实现、数据库迁移脚本和单测，
        可以拆成多个 subagent 并行执行"
```
你也可以精细控制。在 .claude/agents/ 目录下创建 .md 文件来定义专属 agent：每个 agent 可以配置独立的名称、颜色、可用工具、权限模式、甚至使用不同的模型。跑 /agents 就能看到管理界面。

一个实战场景：PR 提交后，自动触发一组 agent，分别检查逻辑错误、安全漏洞、性能回退，然后各自贴出 inline 评论。Anthropic 内部就是这么搞的——代码产出上去了，review 反而成了瓶颈，于是他们把 review 也自动化了。

还有一种玩法叫 worktree agent。在 agent 的 frontmatter 里加上 isolation: worktree：

然后跟 Claude 说："把所有同步 IO 迁移到异步。分成 10 批，启动 10 个带 worktree 隔离的并行 agent。每个 agent 独立测试自己的修改，测试通过后自动提 PR。"

```markdown
# .claude/agents/worktree-worker.md

---

name: worktree-worker
model: haiku
isolation: worktree

---
```

10 个 agent 同时在 10 个隔离目录里干活，互不干扰。大规模重构从噩梦变成了一杯咖啡的事。

---
## 🔌 MCP 与扩展能力

**MCP（Model Context Protocol）** 是 Claude Code 连接外部工具和数据源的标准协议。通过 MCP，模型可以读写数据库、查询 GitHub、调用内部 API、操作 Figma 等。

常见的高频 MCP 服务器：

- **文件系统**：跨目录读取项目文档
- **GitHub**：查看 PR、Issue、Code Review
- **PostgreSQL / MySQL**：直接查询开发库
- **Figma**：读取设计稿
- **Slack / Notion**：读取团队知识库

```bash
# 添加一个 MCP 服务器
claude mcp add postgres "postgresql://user:pass@localhost:5432/mydb"

# 列出已配置的 MCP 服务器
claude mcp list

# 在对话中使用 MCP 工具
claude "查一下 users 表里最近 7 天注册量最高的 10 个城市"
```

> 安全提示：MCP 服务器拥有真实的数据访问权限，**仅添加你信任的服务器**，并在生产库中谨慎使用。

---


## ⚠️ 常见陷阱与最佳实践

| 陷阱 | 表现 | 建议 |
|------|------|------|
| **上下文过载** | 模型开始“失忆”，理解错需求 | 用 `/compact` 压缩，定期 `/clear` 开启新对话 |
| **指令过宽** | 模型改了不该改的文件 | 任务要具体，限定文件范围；先 Plan 再执行 |
| **盲目信任** | 模型生成了看起来对、实际有 bug 的代码 | **必须 review**，跑测试；不要跳过这一步 |
| **忽视 Git** | 改动后无法回滚 | 重要操作前先 `git commit` 留个回滚点 |
| **MCP 误用** | 模型意外删了生产数据 | MCP 服务器只连开发环境，生产操作走人工 |
| **忽略 CLAUDE.md** | 模型每次都“重新学”规范 | 团队约定写进 `CLAUDE.md`，让规则自动生效 |

三条黄金法则：

1. **小步快跑**：一次只让模型做一件事，做完 review 后再继续
2. **先 Plan 后动手**：复杂任务先让模型出方案，确认后再执行
3. **Git 是安全网**：任何重要改动前先 commit，模型搞砸了随时回滚

---

## 📝 总结

Claude Code 的核心价值，是把 AI 从“代码生成器”升级为“能独立完成任务的工程协作者”。要真正用好它，关键在于三件事：

- **清晰的项目记忆**：写好 `CLAUDE.md`，把团队的隐性规则显性化
- **合适的任务边界**：把大任务拆成可验收的小任务，先 Plan 再执行
- **工程化的安全网**：Git、MCP 权限、Code Review，缺一不可

当你把 Claude Code 当作一个“需要规范、需要 review、需要边界”的同事来对待，而不是一个“无所不能的魔法”，它才能真正稳定地提升你的开发效率。

> 一句话总结：**Claude Code 不会取代工程师，但会用 Claude Code 的工程师，会取代不会用的人。**

---

**参考资料：**

- [Claude Code 官方文档](https://code.claude.com/docs)
- [Claude Code 官方文档](https://code.claude.com/docs/zh-CN/overview)
- [Model Context Protocol 官方仓库](https://modelcontextprotocol.io/)
- [Anthropic 工程博客：Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
