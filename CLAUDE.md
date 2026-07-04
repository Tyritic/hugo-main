# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

这是一个基于 Hugo 的个人博客项目，使用 hugo-theme-stack 主题。博客内容以中文为主，支持中英双语。

## Commands

### Build & Development

```bash
# 开发服务器（带实时预览）
hugo server

# 构建静态站点到 public/ 目录
hugo

# 创建新博客文章
hugo new content post/<文章目录>/index.zh-cn.md

# 创建新分类
hugo new content categories/<分类名>/_index.md

# 创建新标签
hugo new content tags/<标签名>/_index.md
```

### Testing

此项目为静态站点，无需运行测试。通过 `hugo server` 预览验证内容。

## Architecture

### Content Structure

```
content/
├── post/              # 博客文章（主要内容区）
│   └── <文章目录>/
│       ├── index.zh-cn.md   # 中文文章
│       ├── index.en.md      # 英文文章（可选）
│       └── *.png/jpg        # 文章内图片
├── categories/        # 文章分类
│   └── <分类名>/_index.md
├── tags/             # 文章标签
│   └── <标签名>/_index.md
└── page/
    └── links/        # 友情链接配置
```

### Front Matter 标准格式

所有博客文章必须包含以下 front matter：

```yaml
---
date : '2025-01-01T08:00:00+08:00'  # ISO 格式，保留 +08:00
draft : false                        # 是否为草稿
title : '文章标题'
image : ""                           # 封面图（可为空）
categories : ["分类"]                # 数组格式
tags : ["标签1", "标签2"]            # 数组格式，可为空数组 []
description : "文章摘要"
math : true                          # 可选，数学公式多时添加
---
```

### Hugo Shortcodes

支持的自定义短代码（使用 `{{}}` 包裹）：

```markdown
# 引用块
{{< quote author="作者" source="作品名" url="可选链接" >}}
引用内容
{{< /quote >}}

# B站视频（从 URL 提取 BV号）
{{< bilibili BV1BPSdYHEbj 1 >}}

# 提示块（类型：tip、info、warning、note）
{{< notice tip >}}
提示内容
{{< /notice >}}
```

### Theme Configuration

- 主题：hugo-theme-stack（在 themes/ 目录，通过 Git submodule 管理）
- 主配置文件：`hugo.yaml`
- 默认语言：简体中文 (zh-cn)
- 评论系统：Waline + Giscus

### Special Directories

- `CS-Base-main/`：外部计算机科学知识库（MySQL、Network、OS 等主题）
- `static/`：静态资源（favicon、全局图片）
- `public/`：Hugo 构建输出目录（不提交到 Git）
- `.uploads/`：临时上传文件存储

## Blog Content Guidelines

### 标题 Emoji 规则

- 所有标题必须有语义相关的 emoji
- 全文所有级别的标题 emoji 严格不重复
- 不使用乱码 emoji（如 `�`）

### 图片处理

使用 HTML 标签并设置合适宽度：

```html
<div align="center">
  <img src="image.png" alt="具体描述" width="82%">
</div>
```

宽度参考：
- 架构图/流程图：82%-92%
- 代码截图：80%-90%
- 局部界面：55%-70%
- 小图标：40%-55%

### 代码块

必须指定语言标识符：

```language
代码内容
```

### 数学公式

- 行内公式：`$...$`
- 独立公式：`$$...$$`
- 多公式时在 front matter 添加 `math: true`

## Project-Specific Agents

### blog-formatter Agent

专用于博客内容生成和格式化的 subagent，位于 `.claude/agents/blog-formatter.md`。

**使用场景：**
- 生成新博客文章（自动处理 front matter、emoji、图片、代码块）
- 格式化现有博客（修正 emoji、图片宽度、分割线等）
- 博客合规性检查

**调用方式：**

```javascript
// 通过 Agent 工具调用
Agent({
  agentType: "blog-formatter",
  prompt: "格式化 content/post/某文章/index.zh-cn.md"
})
```

详细规范参考 `content/post/博客使用指南/index.zh-cn.md`。

## Git Workflow

- 主分支：main
- 部署：推送到 main 分支后，GitHub Pages 自动构建并发布到 https://Tyritic.github.io
- Git submodule：themes/hugo-theme-stack（不要直接修改）

## Notes

- 所有博客文章图片必须存放在文章目录内（使用相对路径）
- 文章目录名即为 URL slug（通过 permalinks 配置）
- 修改 hugo.yaml 后需重启 `hugo server`
- 友情链接在 `content/page/links/_index.md` 中配置
