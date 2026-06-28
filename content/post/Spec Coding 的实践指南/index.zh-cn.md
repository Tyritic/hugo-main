---
date : '2026-06-27T20:30:00+08:00'
draft : false
title : 'Spec Coding 的实践指南'
image : ""
categories : ["AI Coding"]
tags : ["Spec Coding"]
description: "记录一次完整的 Spec Coding 实践指南——从需求拆解、规格撰写，到 AI 实现、验证归档的全链路复盘。"
---

## 🏗️ 让 AI 基础建设

### 🗂️ 项目背景和环境准备

#### 📖 项目背景
本文假设你已经有一个需求，需要使用 Spec Coding 来实现。这个系统引入AI coding的目标很直接:让AI熟知所有规则和业务背景，独立完成从需求分析到代码实现的全流程，人只做设计审核和最终决策。但由于这个系统历史悠久，存在许多历史包袱，并且各个模块开发时间不同，人工编写的代码又缺乏强力的规范，又没有文档传承。人为理解已经是困难至极。
现在最大的难点更在于:如何让AI理解这个系统的复杂业务逻辑，以及各种历史包袱代码。

#### ⚙️ 环境准备
本文采用Claude Code作为Agent，Spec Coding 框架选择OpenSpec。同时通过SuperPowers遵循TDD原则，即先写测试，再写实现。

### 🧱 构建AI Coding的背景上下文
在让 AI 接手开发之前，需要完成三项基础建设。这三项工作非常重要，直接影响AI生成的代码质量和准确性。三项工作都可以让 AI 来做初版，然后人工修正，再反过来用修正结果改进代码。

#### 📄 生成项目级CLAUDE.md的初稿
使用/init命令生成项目级的CLAUDE.md文件。执行上述命令 Claude Code 会阅读项目源码，输出它理解到的架构约定和模式。这一步通常只能覆盖一部分规则，比如模块结构、包命名、错误处理方式等从代码里就能读出来。

#### 🧠 人工补充隐形业务规则
AI 生成的 CLAUDE.md 初始稿通常只能覆盖一部分业务规则，比如模块结构、包命名、错误处理方式等从代码里就能读出来。人工补充这些规则，是确保 AI 能够正确理解业务逻辑的关键。这些规则需要人工根据业务背景，拆分到规则文件中。
```markdown
├── CLAUDE.md                    # 主入口，指向各规则文件
└── rules/
    ├── code-style.md            # 命名、日志格式、错误处理
    ├── pipeline-architecture.md # 并发管道约束、统计规范、反模式禁止
    ├── commands.md              # 子命令基线、共享参数约束、日期默认值规则
    └── database-access.md       # 数据库访问规范
```
规则内容必须足够的具体，可映射到真实代码路径，避免写成"要注意性能"这种模凌两可的描述，AI无法执行这种口号。

最后还要告诉AI要保持维护所有Rules，比如我会在CLAUDE.md中增加以下指令：
```markdown
- 更新对应模块代码时同步更新对应的规则文件。
- 更新各个模块代码时，必须同步更新对应的文档目录下的文档，以及集成测试目录下的测试用例。       
```

#### 🔍 让AI反向Review历史代码
规则完善后，就可以让 Claude Code 用这套规则扫描所有存量代码，找出不符合规则的地方。此时只需要告诉claude code修复这些问题，它就会触发superpowers的skill自行修复

### 💡 让AI理解设计理念和业务逻辑
规则约束的是"怎么写代码"，但 AI 还需要理解"为什么这样设计"，才能在新需求时做出正确的架构决策。

#### 📚 让AI根据代码生成初版设计文档
让 Claude Code 阅读模块的所有代码实现，生成三份文档：
- design.md: 代码架构设计文档，描述当前代码实现下的数据流、预处理规则、退款处理、消费摊销、汇总口径与校验规则，不展开命令行操作说明。
- readme.md: 模块使用说明文档，只描述如何使用此模块的可执行命令，各个功能和参数说明，不涉及业务逻辑。
- user-guide.md: 业务指南文档，用于描述纯粹的业务逻辑，不展开代码细节。
在系统中每个模块都编写对应的三份文档，确保 AI 能够正确理解业务逻辑。
```markdown
├── design.md
├── readme.md
├── user-guide.md
```

#### 🛠️ 人工审核和修正设计文档
代码里体现不出来的业务背景需要手动补充

#### 🔁 让AI根据设计文档再次Review代码
文档补充完整后，让 AI 对照文档检查代码实现，找出"文档说是这样，代码不是这样"的地方。

### 🧪 补充单元测试和集成测试

#### 📋 让AI 根据代码和文档生成初版单元测试/集成测试
直接对claude code下达指令：
参考提示词如下：
```markdown
根据当前模块的文档和代码，生成单元测试，要求代码覆盖率必须至少达到80%。单元测试中如果遇到需要依赖第三方接口服务或者数据库的情况，统一用mock代替。
```
集成测试要分开生成：
```markdown
根据当前模块的文档和代码，生成集成测试用例。尽可能覆盖更多的测试场景，设想更多的业务场景。允许你使用xxx数据库地址作为测试库，生成所需的测试数据。所有的测试场景和用例都要落实到文档中记录。
```
#### ✏️ 人工补充测试场景
AI 首次生成的测试用例通常不够完备，同样需要人工review和补充测试用例。但你不需要手动去改代码，你只需要直接告诉claude code补充哪些场景的测试，或者修改测试文档即可。

#### 🎯 AI 用测试反向 review 代码
测试跑起来之后，让 AI 分析覆盖率，找出测试暴露的逻辑分支问题，修复后再回归。关键前提：先有充分的设计文档和规则，AI 才能生成高质量测试——知道"这个字段应该是什么值"，而不是只生成结构正确但断言空洞的空壳测试。

---

## 🚀 AI Coding实践
完成了规则、文档、测试这三块基础建设，AI大模型基本上已经完全熟悉整个项目了。接下来就可以让 AI 真正接管开发流程了。开发过程中我们主要使用openspec的指令作为入口即可，superpowers的skills集合是在各个阶段自动触发的，无需手动调用。

### 📝 使用OpenSpec提案
- 命令： /opsx:propose
- 关键技巧：/opsx:propose 的输入质量直接决定生成工件的质量。模糊输入和具体输入的差距很大：一定要注意需求描述要足够具体，openspec 就能一次生成完整的文档，否则可能需要多次来回的沟通调整。

### 🧐 人工审核提案
在上一步产生的文档经过人工审核通过之后，接下来就是实施阶段。在执行 /opsx:apply 之前，必须认真审读 design.md和各个spec.md文档，给claude code提出反馈。
这一步非常关键：设计阶段发现的问题，改起来通常只需要更新文档。但如果实现到一半才发现设计有缺陷，代价高出一个数量级。

### 🌿 创建worktree，执行 apply
在启动 Claude Code 时通过 --worktree 创建隔离工作区，或使用 superpowers:using-git-worktrees skill：
参考提示词
```text
# 方式一：启动时创建 worktree
claude --worktree

# 方式二：在 Claude Code 中使用 skill
# /superpowers:using-git-worktrees
```
工作区隔离后，使用类似以下Prompt执行
```text
开始实施，整体流程使用`openspec-apply-change` skill，写代码时使用`subagent-driven-development`这个skill
```
此举触发superpowers的相关skills，开始执行任务。比如 subagent-driven-development 会创建多个子agent开始并行执行不同任务。

### 🤖 subagent-driven-development 的工作机制
对每个任务，superpowers skill 会依次循环三层：
- Implementer subagent（内嵌 TDD）:每个任务派遣一个独立的 Implementer subagent，它内部强制执行红绿重构循环：
```text
Step 1: 写一个失败的测试（RED）
Step 2: 运行测试，确认失败（必须看到失败，不能跳过）
Step 3: 写最小实现代码（GREEN）
Step 4: 运行测试，确认通过
Step 5: 重构，保持绿色
Step 6: 提交，报告状态（DONE / NEEDS_CONTEXT / BLOCKED）
```
- Spec Reviewer subagent: Implementer 完成后，派遣 Spec Reviewer 独立读代码，逐行对比 spec 和实现，验证"构建了被要求的（不多不少）"。这个 reviewer 不信任 Implementer 的声明，自己读代码验证。
- Code Quality Reviewer subagent: Spec 审核通过后，派遣 Code Quality Reviewer，验证是否"构建足够得好"：
    - 文件职责清晰，可以独立理解
    - 测试测的是真实代码而非 mock
    - 没有创建不必要的巨型文件

任一审核不通过 → Implementer 修复 → 重新审核，直到两层都通过。

### ✅ 完成验证
所有任务完成后，superpowers的verification-before-completion skill 会开始介入，要求：运行完整测试套件，贴出实际输出，才能做"完成"声明。

### 📦 归档
- 命令:/opsx:archive
完成代码验收之后将 openspec 文档（proposal design specs / tasks）提交到 master 分支，形成可回溯的变更记录。

---

## 🔄 完整协作流程
<div align="center">
  <img src="bf13394c2d1411f1861d42619244becf.png" alt="完整协作流程" width="78%" />
</div>

蓝色节点是 openspec 指令，绿色节点是 superpowers skill 自动触发点。