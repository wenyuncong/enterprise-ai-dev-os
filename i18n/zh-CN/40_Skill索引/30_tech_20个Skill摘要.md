# tech 层 20 个 Skill 中文摘要 | Tech Layer Skills

> **源文件**：skills/tech/*/SKILL.md、skills/SKILL_MANIFEST.json
> **源版本**：SKILL_MANIFEST.json updatedAt 2026-07-28
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：**tech 层只出中文摘要，不出全文译文**；Skill 名、代码、API 名、命令一律保持英文。

---

## 0. 一览表

| Skill | 技术栈 | 中文名 | 一句话职责 | 何时加载 |
|---|---|---|---|---|
| `docker-expert` | Docker / 容器 | Docker 容器化专家 | Dockerfile 与 Compose 写法、多阶段构建、镜像瘦身与容器安全 | 容器化应用、评审 Dockerfile / Compose |
| `flutter-animations` | Flutter / Dart | Flutter 动画实现 | 隐式、显式、Hero、交错与物理动画的选型与实现 | 加动效、选动画类型、排查掉帧 |
| `flutter-expert` | Flutter / Dart | Flutter 跨端开发 | Flutter 3+ widget、Riverpod/Bloc 状态管理、GoRouter 导航 | 建或扩展 Flutter 应用、优化渲染 |
| `java-performance-governance` | Java / Spring | Java 性能与内存治理 | 批处理效率、无界缓存、资源泄漏、SQL 成本与可观测性 | 批处理变慢、内存增长、OOM、超时 |
| `java-springboot` | Java / Spring Boot | Spring Boot 工程实践 | 项目结构、构造器注入、外部化配置、分层与测试切片 | 编写或评审 Spring Boot 后端代码 |
| `javascript-typescript-jest` | JS / TS / Jest | Jest 测试实践 | 测试结构、Mock 边界、异步用例与快照测试 | 编写、评审、调试 Jest 测试 |
| `multi-stage-dockerfile` | Docker | 多阶段 Dockerfile 优化 | 构建与运行阶段分离、层缓存排序、生产镜像加固 | 压缩镜像体积、改善构建缓存 |
| `mysql-best-practices` | MySQL | MySQL 最佳实践 | 模式设计、数据类型、索引策略、EXPLAIN、事务与运维 | 设计或评审模式、SQL、迁移 |
| `node-backend` | Node.js | Node.js 后端工程 | Express/NestJS/Fastify 分层、schema 校验、异步纪律 | 编写或评审 Node.js API |
| `postgresql-best-practices` | PostgreSQL | PostgreSQL 最佳实践 | 类型与约束、索引、EXPLAIN ANALYZE、迁移、连接池 | 设计表结构、调优查询、评审迁移 |
| `python-fastapi` | Python / FastAPI | FastAPI 后端工程 | 分层服务、Pydantic 校验、async 端点、pytest | 编写或评审 FastAPI 服务 |
| `react-frontend` | React / TypeScript | React 前端工程 | display only 组件、hooks、状态归属、四态渲染 | 编写或评审 React 页面与组件 |
| `springboot-patterns` | Java / Spring Boot | Spring Boot 架构模式 | REST API 结构、分层、DTO、缓存、异步、限流、日志 | 选型架构与 API 模式 |
| `springboot-security` | Java / Spring Security | Spring Boot 安全加固 | 认证鉴权、CSRF、密钥管理、安全响应头、限流 | 加固或审计 Spring Boot API |
| `tailwind-css-patterns` | Tailwind CSS | Tailwind CSS 样式模式 | 响应式断点、布局、间距、排版、暗色模式 | 写组件样式、搭响应式布局 |
| `tailwind-design-system` | Tailwind CSS | Tailwind 设计系统 | 设计令牌、CSS-first 配置、组件变体、主题与迁移 | 建组件库、统一 UI 模式 |
| `typescript-advanced-types` | TypeScript | TypeScript 高级类型 | 泛型、条件类型、映射类型、模板字面量类型 | 复杂类型逻辑、类型安全重构 |
| `vue` | Vue 3 | Vue 3 组合式 API | script setup 宏、响应式系统、内置组件与指令 | 编写 Vue SFC 与组合式逻辑 |
| `vue-best-practices` | Vue 3 | Vue 生产最佳实践 | 架构确认、响应式与 SFC 规范、性能优化、收尾自检 | 任何 Vue、Vue Router、Pinia 任务 |
| `vue-pinia-best-practices` | Vue 3 / Pinia | Pinia 状态管理 | store 拆分、setup store、响应式消费与 actions | 新建、评审、调试 Pinia store |

---

## 1. `docker-expert` — Docker 容器化专家

- **源文件**：`skills/tech/docker-expert/SKILL.md`
- **上游来源**：frontmatter `source: community`（`category: devops`、`risk: unknown`、`date_added: 2026-02-27`），未署具名作者
- **用途**：管容器化全过程：Dockerfile 写法、多阶段构建、Compose 编排、安全加固与生产部署模式。目标是镜像精简、不以 root 运行、上线前可扫描。
- **覆盖范围**：Dockerfile 最佳实践、多阶段构建、镜像瘦身、Docker Compose、容器安全、部署模式、故障诊断
- **何时加载**：容器化应用、编写或评审 Dockerfile 与 Compose 文件、排查镜像体积与构建速度时加载；Kubernetes 与云厂商容器服务超出范围。
- **上游维护提示**：本 Skill 源自第三方上游，**中文版不做正文翻译**，避免与上游分叉；需要细节时查英文原文。

## 2. `flutter-animations` — Flutter 动画实现

- **源文件**：`skills/tech/flutter-animations/SKILL.md`
- **上游来源**：frontmatter `metadata.author: Stanislav [MADTeacher] Chernyshev`、`version: "1.0"`
- **用途**：管 Flutter 动效的选型与实现：隐式动画、显式 AnimationController、Hero 共享元素转场、交错与物理动画。给出动画类型决策树、实现模式与性能约束。
- **覆盖范围**：AnimatedContainer / AnimatedOpacity、TweenAnimationBuilder、AnimationController、Tween、Hero 转场、交错动画、物理动画、性能与体验
- **何时加载**：为 Flutter 应用添加动效、不确定该用哪种动画类型、或动画卡顿需要优化时加载。
- **上游维护提示**：本 Skill 源自第三方上游，**中文版不做正文翻译**，避免与上游分叉；需要细节时查英文原文。

## 3. `flutter-expert` — Flutter 跨端开发

- **源文件**：`skills/tech/flutter-expert/SKILL.md`
- **上游来源**：frontmatter `metadata.author: https://github.com/Jeffallan`、`license: MIT`、`version: "1.1.0"`
- **用途**：管 Flutter 3+ 跨端应用开发：widget 组合、Riverpod/Bloc 状态管理、GoRouter 导航、平台适配与性能优化。要求 build 方法保持纯而快，状态方案只选一种并保持一致。
- **覆盖范围**：Flutter 3 / Dart、widget、Riverpod、Bloc、GoRouter、平台通道、性能优化、widget 级测试
- **何时加载**：新建或扩展 Flutter 应用、实现状态管理或导航、处理平台差异、优化渲染性能时加载。
- **上游维护提示**：本 Skill 源自第三方上游，**中文版不做正文翻译**，避免与上游分叉；需要细节时查英文原文。

## 4. `java-performance-governance` — Java 性能与内存治理

- **源文件**：`skills/tech/java-performance-governance/SKILL.md`
- **上游来源**：frontmatter 无第三方作者；`SKILL_MANIFEST.json` 记录 source 为 `GERP batch-operation and memory-leak governance extraction`（本仓库自研提炼）
- **用途**：管 Java / Spring 性能与内存治理：批处理效率、无界缓存、资源泄漏、finally 释放、SQL 成本与可观测性。把劣化模式固化成诊断与修复手册，坚持 no silent degradation。
- **覆盖范围**：集合式批处理、无界缓存、finally 清理、线程池与连接池、EXPLAIN 索引、结构化日志
- **何时加载**：批删批改变慢、内存增长或 OOM、超时、连接池耗尽，以及评审性能敏感代码、新增缓存或线程配置前加载。
- **上游维护提示**：本 Skill 属仓库内 tech 层能力包，**中文版不做正文翻译**；需要细节时查英文原文。

## 5. `java-springboot` — Spring Boot 工程实践

- **源文件**：`skills/tech/java-springboot/SKILL.md`
- **上游来源**：frontmatter 无第三方作者；`SKILL_MANIFEST.json` 记录 source 为 `tech skill library`
- **用途**：管 Spring Boot 工程规范：项目结构、构造器注入、外部化配置、REST 控制器、分层与测试切片。目标是让应用结构一致、依赖显式、可测可维护。
- **覆盖范围**：Maven / Gradle、Spring Boot starters、构造器注入、@ConfigurationProperties、@ControllerAdvice、@Transactional、测试切片、SLF4J 参数化日志
- **何时加载**：搭建或评审 Spring Boot 项目、编写控制器与服务和仓储、处理配置与异常、补测试时加载。
- **上游维护提示**：本 Skill 属仓库内 tech 层能力包，**中文版不做正文翻译**；需要细节时查英文原文。

## 6. `javascript-typescript-jest` — Jest 测试实践

- **源文件**：`skills/tech/javascript-typescript-jest/SKILL.md`
- **上游来源**：frontmatter 无第三方作者；`SKILL_MANIFEST.json` 记录 source 为 `tech skill library`
- **用途**：管 JS / TS 的 Jest 测试写法：测试结构、Mock 策略、异步用例、快照与 React 组件测试。核心是只 mock 外部边界，不断言私有实现细节。
- **覆盖范围**：describe / it 结构、jest.mock、jest.spyOn、async 与 resolves/rejects、快照测试、React Testing Library、userEvent、常用 matcher
- **何时加载**：新增、评审、调试或重构 Jest 测试，尤其是异步代码与被 mock 依赖存在时加载。
- **上游维护提示**：本 Skill 属仓库内 tech 层能力包，**中文版不做正文翻译**；需要细节时查英文原文。

## 7. `multi-stage-dockerfile` — 多阶段 Dockerfile 优化

- **源文件**：`skills/tech/multi-stage-dockerfile/SKILL.md`
- **上游来源**：frontmatter 无第三方作者；`SKILL_MANIFEST.json` 记录 source 为 `tech skill library`
- **用途**：管多阶段 Dockerfile 的构建优化：构建阶段与运行阶段分离、只拷贝运行产物、基础镜像选择与层缓存排序。产出体积更小、更易扫描的生产镜像。
- **覆盖范围**：builder / runtime 分阶段、COPY --from、distroless 与 slim 基础镜像、.dockerignore、层缓存顺序、非 root 用户、HEALTHCHECK
- **何时加载**：容器化任意语言应用、需要压缩镜像体积、改善构建缓存或加固生产镜像时加载。
- **上游维护提示**：本 Skill 属仓库内 tech 层能力包，**中文版不做正文翻译**；需要细节时查英文原文。

## 8. `mysql-best-practices` — MySQL 最佳实践

- **源文件**：`skills/tech/mysql-best-practices/SKILL.md`
- **上游来源**：frontmatter 无第三方作者；`SKILL_MANIFEST.json` 记录 source 为 `tech skill library`
- **用途**：管 MySQL 模式与查询工程：表结构与数据类型、索引策略、EXPLAIN 调优、事务边界、复制与运维加固。保证改库前后都可验证、可回滚。
- **覆盖范围**：InnoDB 存储引擎、数据类型、主键与外键、索引与 composite index、EXPLAIN、事务、JSON 支持、主从复制、安全与维护
- **何时加载**：设计或评审 MySQL 模式、编写复杂 SQL、新增索引、执行迁移或修数据一致性问题时加载。
- **上游维护提示**：本 Skill 属仓库内 tech 层能力包，**中文版不做正文翻译**；需要细节时查英文原文。

## 9. `node-backend` — Node.js 后端工程

- **源文件**：`skills/tech/node-backend/SKILL.md`
- **上游来源**：frontmatter 无第三方作者；`SKILL_MANIFEST.json` 记录 source 为 `tech skill library`
- **用途**：管 Node.js 后端（Express / NestJS / Fastify）：分层结构、schema 校验、异步纪律、错误处理与可观测性。业务真相留在 service 层，路由只做传输，坚持 no silent failures。
- **覆盖范围**：route → service → repository 分层、zod / class-validator 校验、async/await 无游离 Promise、错误中间件、supertest 测试、结构化日志
- **何时加载**：新建或评审 Node.js API、新增路由或服务方法、修异步与错误处理缺陷、补测试时加载。
- **上游维护提示**：本 Skill 属仓库内 tech 层能力包，**中文版不做正文翻译**；需要细节时查英文原文。

## 10. `postgresql-best-practices` — PostgreSQL 最佳实践

- **源文件**：`skills/tech/postgresql-best-practices/SKILL.md`
- **上游来源**：frontmatter 无第三方作者；`SKILL_MANIFEST.json` 记录 source 为 `tech skill library`
- **用途**：管 PostgreSQL 数据层：类型与约束、索引、EXPLAIN ANALYZE、事务、迁移、连接池与备份演练。先保证正确性再谈性能，慢查询必须给计划与定向修复。
- **覆盖范围**：数据类型与约束、外键、索引验证、EXPLAIN ANALYZE、Alembic / Flyway 迁移、PgBouncer 连接池、备份与恢复演练
- **何时加载**：设计表结构、编写或调优查询、新增索引、评审迁移安全性、规划备份与恢复时加载。
- **上游维护提示**：本 Skill 属仓库内 tech 层能力包，**中文版不做正文翻译**；需要细节时查英文原文。

## 11. `python-fastapi` — FastAPI 后端工程

- **源文件**：`skills/tech/python-fastapi/SKILL.md`
- **上游来源**：frontmatter 无第三方作者；`SKILL_MANIFEST.json` 记录 source 为 `tech skill library`
- **用途**：管 FastAPI 后端工程：router → service → repository 分层、Pydantic 输入输出校验、async 端点、依赖注入与 SQLAlchemy 持久化。异常交给统一处理器映射，坚持 no silent failures。
- **覆盖范围**：Pydantic schema、async/await 与事件循环、Depends 依赖注入、SQLAlchemy、Alembic 迁移、pytest 与 httpx TestClient
- **何时加载**：编写或评审 FastAPI 服务、新增端点或模型、排查校验与异步问题、补 pytest 覆盖时加载。
- **上游维护提示**：本 Skill 属仓库内 tech 层能力包，**中文版不做正文翻译**；需要细节时查英文原文。

## 12. `react-frontend` — React 前端工程

- **源文件**：`skills/tech/react-frontend/SKILL.md`
- **上游来源**：frontmatter 无第三方作者；`SKILL_MANIFEST.json` 记录 source 为 `tech skill library`
- **用途**：管 React 18+ 前端工程：函数组件与 hooks、display only 视图、状态归属、错误边界与组件测试。业务计算、状态流转与权限判断一律不进组件与 useMemo。
- **覆盖范围**：函数组件与 hooks、TypeScript props、数据层与 react-query、状态归属、四态渲染、useMemo 仅作性能用途、Vitest + React Testing Library
- **何时加载**：编写或评审 React 页面、组件、hook、store，新增状态、接 API、修渲染或性能问题时加载。
- **上游维护提示**：本 Skill 属仓库内 tech 层能力包，**中文版不做正文翻译**；需要细节时查英文原文。

## 13. `springboot-patterns` — Spring Boot 架构模式

- **源文件**：`skills/tech/springboot-patterns/SKILL.md`
- **上游来源**：frontmatter `origin: ECC`，未署具名作者
- **用途**：管 Spring Boot 架构与 API 模式：REST 结构、controller → service → repository 分层、DTO 与校验、缓存、异步、限流与日志。为可扩展的生产级服务提供成套模式。
- **覆盖范围**：REST API 结构、Spring Data JPA、DTO 与校验、异常处理、缓存、异步与后台任务、Bucket4j 限流、可观测性与生产默认值
- **何时加载**：设计 Spring MVC / WebFlux 接口、规划分层与事务、接入缓存与异步、做生产默认定型时加载。
- **上游维护提示**：本 Skill 源自第三方上游，**中文版不做正文翻译**，避免与上游分叉；需要细节时查英文原文。

## 14. `springboot-security` — Spring Boot 安全加固

- **源文件**：`skills/tech/springboot-security/SKILL.md`
- **上游来源**：frontmatter `origin: ECC`，未署具名作者
- **用途**：管 Spring Boot 安全加固：认证与鉴权、输入校验、CSRF、密钥管理、安全响应头、CORS、限流与依赖漏洞。用于上线前的安全评审与配置定型。
- **覆盖范围**：JWT / OAuth2、OncePerRequestFilter、@PreAuthorize 方法级鉴权、Bean Validation、BCrypt / Argon2、CSRF 与安全头、密钥管理、限流、依赖 CVE 扫描
- **何时加载**：新增认证与鉴权、处理用户输入与文件上传、配置 CORS 或安全头、管理密钥、做安全审计时加载。
- **上游维护提示**：本 Skill 源自第三方上游，**中文版不做正文翻译**，避免与上游分叉；需要细节时查英文原文。

## 15. `tailwind-css-patterns` — Tailwind CSS 样式模式

- **源文件**：`skills/tech/tailwind-css-patterns/SKILL.md`
- **上游来源**：frontmatter 无第三方作者；`SKILL_MANIFEST.json` 记录 source 为 `tech skill library`
- **用途**：管 Tailwind CSS 工具类写法：响应式断点、布局与间距、排版、交互状态、暗色模式与组件抽取。目标是样式一致可维护，不与行内样式混用。
- **覆盖范围**：移动优先断点、flexbox 与 grid 布局、间距与排版刻度、交互状态、暗色模式、动画过渡、生产清理配置
- **何时加载**：给 React / Vue / Svelte 组件写样式、搭响应式布局、实现暗色模式或整理 CSS 工作流时加载。
- **上游维护提示**：本 Skill 属仓库内 tech 层能力包，**中文版不做正文翻译**；需要细节时查英文原文。

## 16. `tailwind-design-system` — Tailwind 设计系统

- **源文件**：`skills/tech/tailwind-design-system/SKILL.md`
- **上游来源**：frontmatter 无第三方作者；`SKILL_MANIFEST.json` 记录 source 为 `tech skill library`
- **用途**：管 Tailwind v4 设计系统建设：先定设计令牌再做组件、CSS-first 配置、组件变体、主题与无障碍。组件只能引用令牌，禁止硬编码取值。
- **覆盖范围**：@theme 令牌、语义色、CSS 自定义属性主题、组件变体、暗色模式、响应式与可访问性、v3 到 v4 迁移清单
- **何时加载**：搭建组件库、落地设计令牌与主题、统一 UI 模式、从 Tailwind v3 升级到 v4 时加载。
- **上游维护提示**：本 Skill 属仓库内 tech 层能力包，**中文版不做正文翻译**；需要细节时查英文原文。

## 17. `typescript-advanced-types` — TypeScript 高级类型

- **源文件**：`skills/tech/typescript-advanced-types/SKILL.md`
- **上游来源**：frontmatter 无第三方作者；`SKILL_MANIFEST.json` 记录 source 为 `tech skill library`
- **用途**：管 TypeScript 类型系统进阶：泛型与约束、条件类型、映射类型、模板字面量类型与工具类型。目标是编译期拦截错误。
- **覆盖范围**：泛型与 extends 约束、条件类型与 infer、映射类型、模板字面量类型、可辨识联合、类型守卫、类型测试与编译性能
- **何时加载**：实现复杂类型逻辑、抽可复用类型工具、设计类型安全 API 客户端或从 JS 迁移到 TS 时加载。
- **上游维护提示**：本 Skill 属仓库内 tech 层能力包，**中文版不做正文翻译**；需要细节时查英文原文。

## 18. `vue` — Vue 3 组合式 API

- **源文件**：`skills/tech/vue/SKILL.md`
- **上游来源**：frontmatter `metadata.author: Anthony Fu`、`metadata.source: Generated from https://github.com/vuejs/docs, scripts at https://github.com/antfu/skills`、`version: "2026.1.31"`
- **用途**：管 Vue 3 组合式 API 写法：script setup 宏、响应式系统、生命周期、内置组件与自定义指令。基于 Vue 3.5，新代码一律使用 Composition API。
- **覆盖范围**：defineProps / defineEmits / defineModel / defineExpose、ref 与 shallowRef、computed 与 watch、composables 与 effectScope、Transition / Teleport / Suspense / KeepAlive、v-memo、自定义指令
- **何时加载**：编写 Vue SFC、定义组件 props 与 emits、处理响应式与监听、使用内置组件或自定义指令时加载。
- **上游维护提示**：本 Skill 源自第三方上游，**中文版不做正文翻译**，避免与上游分叉；需要细节时查英文原文。

## 19. `vue-best-practices` — Vue 生产最佳实践

- **源文件**：`skills/tech/vue-best-practices/SKILL.md`
- **上游来源**：frontmatter `metadata.author: github.com/vuejs-ai`、`license: MIT`、`version: "18.0.0"`
- **用途**：管 Vue 3 生产最佳实践工作流：先确认架构与组件边界，再落实响应式与 SFC 规范，最后做性能优化与交付自检。核心是 one source of truth，其余全部派生。
- **覆盖范围**：Vue 3 与 script setup lang="ts"、组件边界与 props/emits 契约、响应式与 computed、SFC 结构与模板安全、可选特性按需引入、性能优化、收尾自检
- **何时加载**：任何 Vue、.vue 文件、Vue Router、Pinia 或 Vite + Vue 任务；编写前按工作流顺序逐段执行。
- **上游维护提示**：本 Skill 源自第三方上游，**中文版不做正文翻译**，避免与上游分叉；需要细节时查英文原文。

## 20. `vue-pinia-best-practices` — Pinia 状态管理

- **源文件**：`skills/tech/vue-pinia-best-practices/SKILL.md`
- **上游来源**：frontmatter `author: github.com/vuejs-ai`、`license: MIT`、`version: 1.0.0`
- **用途**：管 Pinia 状态管理：状态该放哪、setup store 写法、响应式解构与 actions 归位。要求状态可预测、可测、范围恰当，不把持久业务真相只放在前端状态里。
- **覆盖范围**：store 拆分与 setup store、storeToRefs、actions 与副作用、URL 承载临时筛选、SSR 与 DevTools 状态、store 独立测试
- **何时加载**：新建、评审、调试或重构 Pinia store，出现响应式失效、筛选刷新丢失、SSR 状态异常时加载。
- **上游维护提示**：本 Skill 源自第三方上游，**中文版不做正文翻译**，避免与上游分叉；需要细节时查英文原文。

---

## 附录 A：技术栈 → Skill 选择建议（按前端/后端/数据库/容器/移动分类）

| 分类 | 首选 Skill | 配套 Skill | 选择要点 |
|---|---|---|---|
| 前端框架 | `vue`、`vue-best-practices`、`react-frontend` | `typescript-advanced-types` | 写组件逻辑先加载框架 Skill；任何 Vue 任务都从 `vue-best-practices` 的工作流起步 |
| 前端状态 | `vue-pinia-best-practices` | `vue-best-practices` | 只有需要跨页面共享状态时才引入 Pinia；临时筛选优先放 URL |
| 样式与设计系统 | `tailwind-css-patterns` | `tailwind-design-system` | 单组件样式用 patterns；建组件库与令牌体系用 design-system |
| 后端（Java） | `java-springboot`、`springboot-patterns` | `springboot-security`、`java-performance-governance` | 先工程规范再架构模式；上线前必过安全加固；批处理与缓存改动走性能治理 |
| 后端（Node） | `node-backend` | `javascript-typescript-jest`、`typescript-advanced-types` | 分层与校验一次定好；测试用 Jest Skill 的 Mock 边界规则 |
| 后端（Python） | `python-fastapi` | `postgresql-best-practices` | 先声明 Pydantic schema 再写端点；持久化与迁移按数据库 Skill 执行 |
| 数据库 | `mysql-best-practices`、`postgresql-best-practices` | 对应后端 Skill | 按实际引擎二选一，不要混用两套索引与迁移口径 |
| 容器与交付 | `multi-stage-dockerfile` | `docker-expert` | 只优化 Dockerfile 用 multi-stage；涉及 Compose、安全加固、构建诊断时升级到 docker-expert |
| 移动端 | `flutter-expert` | `flutter-animations` | 应用骨架与状态管理用 flutter-expert；动效单独加载 flutter-animations |
| 自动化测试 | `javascript-typescript-jest` | 各框架 Skill | 测试与实现分开加载，避免把测试约定的 Mock 规则带进生产代码 |

## 附录 B：第三方上游 Skill 清单与不翻译理由

汇总口径：以每个 `SKILL.md` 的 frontmatter 为准逐条核对（`metadata.author` / `metadata.source` / `author` / `source` / `origin`）。

| Skill | 上游作者 / 来源（frontmatter 原文） | 处理口径 |
|---|---|---|
| `vue` | `metadata.author: Anthony Fu`；`metadata.source: Generated from https://github.com/vuejs/docs, scripts at https://github.com/antfu/skills` | 不翻译正文，避免与上游分叉 |
| `vue-best-practices` | `metadata.author: github.com/vuejs-ai`；`license: MIT`；`version: "18.0.0"` | 不翻译正文，避免与上游分叉 |
| `vue-pinia-best-practices` | `author: github.com/vuejs-ai`；`license: MIT`；`version: 1.0.0` | 不翻译正文，避免与上游分叉 |
| `flutter-expert` | `metadata.author: https://github.com/Jeffallan`；`license: MIT`；`version: "1.1.0"` | 不翻译正文，避免与上游分叉 |
| `flutter-animations` | `metadata.author: Stanislav [MADTeacher] Chernyshev`；`version: "1.0"` | 不翻译正文，避免与上游分叉 |
| `docker-expert` | `source: community`（`category: devops`、`risk: unknown`、`date_added: "2026-02-27"`），未署具名作者 | 不翻译正文，避免与上游分叉 |
| `springboot-patterns` | `origin: ECC`，未署具名作者 | 不翻译正文，避免与上游分叉 |
| `springboot-security` | `origin: ECC`，未署具名作者 | 不翻译正文，避免与上游分叉 |

**不翻译理由（统一）**：以上 8 个 Skill 由第三方作者或上游仓库维护，正文随上游持续演进。若中文版逐句翻译，会产生第二份真相源，上游一旦更新就无法低成本同步，方法论审计与 Skill 健康检查也会出现英文断言缺失。因此 tech 层统一「只出中文摘要，不译正文」，摘要负责说清管什么、何时加载，细节一律回到英文原文。

**其余 12 个 Skill 的来源说明**：`java-performance-governance` 的 `SKILL_MANIFEST.json` source 为 `GERP batch-operation and memory-leak governance extraction`（本仓库自研提炼）；另外 11 个（`java-springboot`、`javascript-typescript-jest`、`multi-stage-dockerfile`、`mysql-best-practices`、`node-backend`、`postgresql-best-practices`、`python-fastapi`、`react-frontend`、`tailwind-css-patterns`、`tailwind-design-system`、`typescript-advanced-types`）的 source 均为 `tech skill library`，frontmatter 无第三方作者。它们同样只出摘要、不出全文译文，口径与第三方 Skill 一致，便于整层统一维护与同步。
