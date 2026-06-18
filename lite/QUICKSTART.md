# 快速开始 | Quick Start

> 5 分钟引入 AI 开发工程规范的最简路径

---

## 这是什么

一个轻量级的 AI 辅助开发规范文件集合。包含：
- 强制执行顺序（避免跳步错误）
- 会话启动检查（避免遗忘未完成任务）
- 每日文档回写（跨会话保留上下文）

**完整版**包含 42 个专项 Skill、4 层架构、自动进化机制。见 [README.md](../README.md)。

---

## 安装（30 秒）

### 方式一：CLI

```bash
npx enterprise-ai-methodology init --lite
```

### 方式二：手动

```bash
# 复制规则
cp lite/rules/AGENTS.md {your-project}/

# 复制文档模板
cp -r lite/docs/_templates/ {your-project}/docs/

# 初始化文档目录
mkdir -p {your-project}/docs/每日调研回写
mkdir -p {your-project}/docs/全项目总控
```

---

## 第一次使用

1. 在 AI 编码工具中打开你的项目
2. 说："开始任务：[描述你要做的事]"
3. AI 会自动读取 AGENTS.md，按规则执行

---

## 你会注意到的变化

- AI 不会再跳过数据库检查直接写代码
- AI 会先确认表结构再写 Mapper
- 每个会话结束时，AI 会记录今天的发现
- 同一个错误不会再出现第三次

---

## 升级到完整版

当你觉得"每日文档回写确实有用，但想更系统化"时：

1. 复制核心技能：`cp -r skills/core/ {your-project}/skills/`
2. 选择技术栈技能：`cp -r skills/tech/vue/ {your-project}/skills/`
3. 初始化全部文档：`cp -r docs/_templates/ {your-project}/docs/`

完整版提供：自动任务路由、复杂任务分解、跨领域架构治理、Skill 自动进化。

---

## 适用场景

| 场景 | 适合 |
|---|---|
| 个人项目（< 5 人） | ✅ |
| 小型 SaaS | ✅ |
| 企业内部工具 | ✅ |
| 中大型 ERP/管理系统 | 建议直接用完整版 |
| 多团队协作 | 建议直接用完整版 |
