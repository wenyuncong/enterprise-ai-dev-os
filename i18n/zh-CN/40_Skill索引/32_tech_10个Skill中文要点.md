# tech 层 10 个 Skill 中文要点（下）| Tech Layer Chinese Essentials

> **源文件**：skills/tech/{python-fastapi,react-frontend,springboot-patterns,springboot-security,tailwind-css-patterns,tailwind-design-system,typescript-advanced-types,vue,vue-best-practices,vue-pinia-best-practices}/SKILL.md
> **源版本**：未标注（以各 SKILL.md frontmatter 为准）
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：本文件是**中文要点提炼**，不是逐句译文；正文与 references 保留英文，避免与上游分叉。

## 0. 一览表

| Skill | 技术栈 | 一句话职责 | 何时加载 |
|---|---|---|---|
| `python-fastapi` | Python / FastAPI | `router -> service -> repository` 分层、Pydantic 校验、async 纪律、依赖注入与 pytest 覆盖 | 编写或评审 FastAPI 服务、新增端点或 model、排查校验与异步问题时 |
| `react-frontend` | React 18+ / TypeScript | 函数组件与 hooks、display only 视图、状态归属、四态渲染与组件测试 | 编写或评审 React 页面、组件、hook、store，接 API 或修渲染问题时 |
| `springboot-patterns` | Java / Spring Boot | REST 结构、分层、DTO 与校验、事务、缓存、异步、限流、可观测性与生产默认值 | 设计 Spring MVC / WebFlux 接口、规划分层与事务、做生产默认定型时 |
| `springboot-security` | Java / Spring Security | 认证、授权、输入校验、SQL 注入防护、密码编码、CSRF、密钥管理、安全头、CORS、限流、依赖漏洞 | 新增认证鉴权、处理用户输入与文件上传、配置 CORS 或安全头、做安全评审时 |
| `tailwind-css-patterns` | Tailwind CSS | 工具类组合、移动优先断点、布局与间距、排版、交互状态、暗色模式、可访问性与生产清理 | 给 React / Vue / Svelte 组件写样式、搭响应式布局、整理 CSS 工作流时 |
| `tailwind-design-system` | Tailwind CSS v4 | 设计令牌层级、CSS-first 配置、CVA 组件变体、主题与暗色模式、v3 到 v4 迁移 | 建组件库、落地设计令牌与主题、统一 UI 模式、升级到 v4 时 |
| `typescript-advanced-types` | TypeScript | 泛型与约束、条件类型与 `infer`、映射类型、模板字面量类型、工具类型与类型测试 | 实现复杂类型逻辑、抽可复用类型工具、设计类型安全 API 客户端时 |
| `vue` | Vue 3.5 | 组合式 API 优先、`<script setup lang="ts">` 宏、响应式系统、内置组件与自定义指令 | 编写 Vue SFC、定义 props 与 emits、处理响应式与监听、用内置组件时 |
| `vue-best-practices` | Vue 3 | 五步工作流：架构与组件边界、响应式与 SFC 规范、可选特性按需引入、性能后置、自检收口 | 任何 Vue、`.vue` 文件、Vue Router、Pinia 或 Vite + Vue 任务 |
| `vue-pinia-best-practices` | Vue 3 / Pinia | 状态归属判定、setup store、`storeToRefs` 保持响应式、actions 归位、store 独立测试 | 新建、评审、调试或重构 Pinia store，出现响应式失效或筛选刷新丢失时 |

## 1. `python-fastapi` — FastAPI 后端

- **源文件**：`skills/tech/python-fastapi/SKILL.md`
- **上游来源**：frontmatter 只有 `name` 与 `description`，未署第三方作者；`SKILL_MANIFEST.json` 记录的 source 为 `tech skill library`，即内部技术栈库。因此本条目按「内部技术栈库」据实标注。
- **用途**：管 FastAPI 服务的后端工程口径。用 `router -> service -> repository` 分层把 HTTP 传输与业务真相分开；用 Pydantic schema 在边界完成输入输出校验；用 async/await 保证 I/O 不阻塞事件循环；用依赖注入（`Depends` / `Annotated`）装配认证、数据库会话与配置；用 pytest 覆盖成功路径与每一条失败路径。源文件的目标表述是让 FastAPI 服务保持确定性：schema 显式、分层干净、异步有纪律、服务可单测，并与方法论的后端真相链（truth -> service -> orchestration -> API）对齐。
- **何时加载**：创建、扩展或评审 FastAPI / Python API 时；动手写 router、Pydantic schema、SQLAlchemy model 或 service 方法之前；排查校验缺陷、异步死锁、依赖注入重构，或需要补 pytest 覆盖时。源文件把「Use before」单列，说明它是**写码前**的强制前置，不是事后参考。
- **核心规则要点**（源 `## Rule`，6 条，逐条转写）：
  - 分层：`router -> service -> repository`；router 只把 HTTP 映射成 service 调用，**禁止**承载业务逻辑。
  - 每一个输入与输出都必须定义 Pydantic schema；边界先校验，service 层才开始执行。
  - async 端点必须 await 全部 I/O；**禁止**在 `async def` 内调用同步 DB / HTTP 而阻塞事件循环。
  - 无静默失败（no silent failures）：抛领域异常，交由 FastAPI exception handler 映射成响应；**禁止**裸 `except` 加 `pass`。
  - 单一真相（single truth）：领域规则与计算只在 service 层实现一次；model 是数据，不是逻辑。
  - 库优先（library first）：优先 `FastAPI` + `SQLAlchemy` + `Pydantic` + `pytest`，不手写校验层或 ORM 包装。
  - 源文件未单列 `## MUST DO` / `## MUST NOT DO` / `## Constraints` 小节；禁令以 `## Guardrails` 的 Never / Do not 句式给出。
- **关键做法**（源 `## Workflow`，5 步顺序固定）：
  1. 先声明 Pydantic schema（request、response、internal 三类），再写端点。
  2. 写 service 层并显式抛领域异常；router 保持薄。
  3. 用 `Depends` / `Annotated` 配置依赖注入，覆盖认证、DB session 与 settings。
  4. 写 pytest：用 `httpx` TestClient 覆盖 happy path 与每一条失败路径。
  5. 验证：先跑 pytest，再真实调用端点，确认状态码与 payload。
  - 迁移用 Alembic 显式管理；**禁止**让 model 隐式改动 schema。日志用 structlog / 标准库 logging 的结构化日志并带 request ID。
  - 源文件未给出运行命令；实际服务通常以 `uvicorn` 启动 ASGI 应用（此为通用做法，不是源文件内容）。
- **常见坑（反模式）**：
  1. 把业务逻辑塞进 router、Pydantic validator 或 SQLAlchemy event 里（源 `## Guardrails` 第 1 条）。
  2. 在同一个 async 端点里混用同步与异步 ORM 调用（源 `## Guardrails` 第 2 条）——典型后果是事件循环被阻塞。
  3. 日志里打印密钥或完整请求体（源 `## Guardrails` 第 3 条）；必须改为结构化日志并带 request ID。
  4. 用裸 `except` 加 `pass` 吞异常，调用方只看到成功或 500，属静默失败。
  5. 让 ORM model 隐式改表结构，迁移与代码脱钩，环境漂移不可避免。
- **可执行检查清单**：
  - [ ] router 内没有业务规则、计算或状态流转。
  - [ ] 每个端点的输入与输出都有独立 Pydantic schema。
  - [ ] 所有 `async def` 路径上的 I/O 都被 await，无同步阻塞调用。
  - [ ] 领域异常显式抛出，并已注册到 FastAPI exception handler。
  - [ ] `Depends` / `Annotated` 统一提供 DB session、认证与 settings。
  - [ ] schema 变更走 Alembic 迁移文件，不存在隐式建表。
  - [ ] pytest 覆盖 happy path 与每条失败路径，`httpx` TestClient 全绿。
  - [ ] 日志为结构化格式、含 request ID，且不含密钥与完整请求体。
- **上游维护提示**：本 Skill 属仓库内 tech 层能力包（无第三方作者），中文版**只出中文要点、不译正文与 references**，避免产生第二份真相源。

## 2. `react-frontend` — React 前端

- **源文件**：`skills/tech/react-frontend/SKILL.md`
- **上游来源**：frontmatter 只有 `name` 与 `description`，未署第三方作者；`SKILL_MANIFEST.json` 记录的 source 为 `tech skill library`，即内部技术栈库。
- **用途**：管 React 18+ 与 TypeScript 的前端工程口径：函数组件与 hooks、display only 视图、状态归属划分、数据层收口（fetch wrapper / react-query）、四态渲染、错误边界与组件测试。源文件的目标表述是让视图保持确定性与一致性，即「界面只负责渲染，后端负责决策」，并明确要阻断典型漂移：把业务运算、重复状态与静默错误处理写进组件。
- **何时加载**：创建、扩展或评审 React 页面、组件、hook 或 store 时；动手写带 props 的组件、新增状态、接 API 调用之前；排查渲染缺陷、状态重复、性能审计，或补组件测试时。
- **核心规则要点**（源 `## Rule`，7 条）：
  - 视图为纯展示（display only）：**禁止**在界面内计算业务逻辑、价格、校验判定或状态流转；向 API 请求受支持的命令并渲染结果。
  - 使用函数组件加 hooks；新代码**禁止**用 class 组件；所有 props 与 state 都要有 TypeScript 类型。
  - 单一真相：同一个派生值**禁止**在两处各算一次；在一个 selector 或 hook 内派生并复用。
  - 服务端状态走数据层（fetch wrapper / react-query），**禁止**散落成一堆 `useEffect` 调用。
  - `useMemo` 与 `useCallback` 内**禁止**放业务逻辑；它们只用于引用稳定性与性能。
  - 每一次异步取数都必须处理四态：loading、empty、error、edge；错误按正确的通知分级上浮，绝不静默。
  - 库优先：优先 `react-query`、`zod`（与后端共享）与成熟组件库，不自行造抽象。
  - 源文件未单列 `## MUST DO` / `## MUST NOT DO` / `## Constraints` 小节；禁令集中在 `## Guardrails`。
- **关键做法**（源 `## Workflow`，5 步）：先确认真相在后端 / API，组件只做 API 数据到 UI 的映射；定义带类型的 props 与带类型的 API 响应类型，必要时在边界校验；再选状态归属——服务端数据归数据层、UI 状态归组件本地、共享 UI 状态进 store；然后显式渲染四态，任何路径都不留静默出口；最后用 Vitest 加 React Testing Library 写渲染与交互测试，并在浏览器中做运行时验证。
- **常见坑（反模式）**：
  1. **禁止**在组件、selector 或 `useMemo` 里算价格、合计、状态流转或权限判断（源 `## Guardrails` 第 1 条）。
  2. 同一个字段定义散落在多个组件里；必须集中到数据层或共享类型（源 `## Guardrails` 第 2 条）。
  3. 直接硬编码颜色或文案；必须使用主题变量与 i18n key（源 `## Guardrails` 第 3 条）。
  4. fetch 外层套空 catch 块，错误被吞掉不上浮；必须映射为可见反馈（源 `## Guardrails` 第 4 条）。
  5. 把服务端状态塞进组件本地 state，再用多个 `useEffect` 手工同步，直接制造重复真相。
- **可执行检查清单**：
  - [ ] 组件内没有业务运算、价格、校验或权限判定。
  - [ ] 所有 props 与 state 都有显式 TypeScript 类型。
  - [ ] 服务端数据只经数据层进入视图，无散落的 `useEffect` 取数。
  - [ ] `useMemo` / `useCallback` 只承担引用稳定与性能职责。
  - [ ] 每个异步路径都渲染 loading、empty、error、edge 四态。
  - [ ] 错误按通知分级上浮，没有空 catch。
  - [ ] 颜色来自主题变量、文案来自 i18n key。
  - [ ] Vitest 加 React Testing Library 的组件测试通过，并在浏览器复核。
- **上游维护提示**：本 Skill 属仓库内 tech 层能力包（无第三方作者），中文版**只出中文要点、不译正文**。源文件未给出启动命令；React 项目本地复现通常在浏览器中通过 `npm run dev` 一类开发服务器进行（此为通用做法，不是源文件内容）。

## 3. `springboot-patterns` — Spring Boot 架构模式

- **源文件**：`skills/tech/springboot-patterns/SKILL.md`
- **上游来源**：frontmatter 含 `origin: ECC`，未署具名作者，属**第三方上游**。正文由上游维护，中文版不翻译，避免与上游分叉。
- **用途**：管 Spring Boot 的架构与 API 模式：分层架构、DDD 模式、CQRS、事件驱动设计与微服务模式，并给出 REST 结构、Spring Data JPA、DTO 与校验、异常集中处理、缓存、异步、限流、可观测性与生产默认值等成套做法。源文件目标是可扩展、可维护、可测试的生产级服务。
- **何时加载**（源 `## When to Activate`，6 条）：用 Spring MVC 或 WebFlux 构建 REST API；组织 controller → service → repository 分层；配置 Spring Data JPA、缓存或异步处理；添加校验、异常处理或分页；配置 dev / staging / production 的 profiles；用 Spring Events 或 Kafka 实现事件驱动模式。
- **核心规则要点**：
  - 源 `## Rule` 五条模式：① Controller-Service-Repository 分层；② DTO 用于 API 契约、entity 用于持久化；③ 跨边界通信用 domain events；④ 新行为用 feature flag 控制；⑤ 外部调用加 circuit breaker。
  - REST 结构：`@RestController` 加 `@RequestMapping("/api/...")` 加 `@Validated`；构造器注入 service；列表默认 `page=0`、`size=20`；创建成功返回 `HttpStatus.CREATED`（201）。
  - Repository：继承 `JpaRepository`；自定义查询用 `@Query` 加 `@Param` 绑定参数，**禁止**字符串拼接。
  - Service：写操作用 `@Transactional`；查询用 `@Transactional(readOnly = true)`。
  - DTO 与校验：请求与响应用 `record`；约束注解包括 `@NotBlank`、`@Size(max=...)`、`@NotNull`、`@FutureOrPresent`、`@NotEmpty`，元素级校验写作 `List<@NotBlank String>`。
  - 异常集中处理：`@ControllerAdvice` 分别处理 `MethodArgumentNotValidException`（返回 400 并把字段错误拼成消息）、`AccessDeniedException`（返回 403）、兜底 `Exception`（返回 500，记录堆栈但**不把细节外泄**）。
  - 缓存：配置类需 `@EnableCaching`；读用 `@Cacheable(value=..., key="#id")`，失效用 `@CacheEvict`。
  - 异步：配置类需 `@EnableAsync`；`@Async` 方法返回 `CompletableFuture`。
  - 日志：SLF4J 参数化写法 `log.info("generate_report marketId={}", marketId)`；失败用 `log.error(..., ex)` 后重新抛出。
  - 过滤器：`OncePerRequestFilter` 中记录 method、uri、status、durationMs，并且耗时统计必须放在 `try/finally` 里以保证必然执行。
  - 分页排序：`PageRequest.of(pageNumber, pageSize, Sort.by("createdAt").descending())`。
  - 外部调用容错：重试加指数退避 `Thread.sleep((long) Math.pow(2, attempts) * 100L)`；捕获 `InterruptedException` 时必须执行 `Thread.currentThread().interrupt()` 恢复中断标志。
  - 限流安全口径：**`X-Forwarded-For` 默认不可信**，因为客户端可以伪造。只有在四条同时满足时才使用转发头——应用在可信反向代理之后、注册了 `ForwardedHeaderFilter` bean、配置了 `server.forward-headers-strategy=NATIVE` 或 `FRAMEWORK`、且代理对该头是覆写而非追加。不满足时应直接使用 `request.getRemoteAddr()`；**禁止**直接读取 `X-Forwarded-For`。
  - 后台任务：用 `@Scheduled` 或接 Kafka、SQS、RabbitMQ 队列；handler 必须幂等且可观测。
  - 可观测性：Logback encoder 输出 JSON 结构化日志；指标用 Micrometer 加 Prometheus / OTel；链路用 Micrometer Tracing 加 OpenTelemetry 或 Brave。
  - 生产默认值：构造器注入优先、避免字段注入；Spring Boot 3+ 打开 `spring.mvc.problemdetails.enabled=true` 以按 RFC 7807 返回错误；按负载配置 HikariCP 连接池大小与超时；用 `@NonNull` 与 `Optional` 做空安全。
  - 源文 `Remember` 总结：controller 保持薄、service 保持聚焦、repository 保持简单、错误集中处理，并以可维护性与可测试性为优化目标。
  - 源文件未单列 `## MUST DO` / `## MUST NOT DO` / `## Constraints` 小节；强制项以上述 `## Rule` 与各模式小节为准。
- **关键做法**：把「薄 controller、聚焦 service、简单 repository、集中错误处理」当作分层验收口径；缓存与异步先确认注解已启用再写业务注解；外部依赖统一走重试与 circuit breaker；对外错误用 RFC 7807 或统一 `ApiError` 结构，不泄露内部堆栈。
- **常见坑（反模式）**：
  1. 限流按 `X-Forwarded-For` 判定客户端 IP，头可伪造，限流等于失效。
  2. 用 `Thread.sleep` 做退避却吞掉 `InterruptedException`、不恢复中断标志。
  3. 缺 `@EnableCaching` / `@EnableAsync` 就写 `@Cacheable` / `@Async`，注解静默失效且不报错。
  4. 缓存只读不失效，缺 `@CacheEvict` 造成脏数据。
  5. 兜底 `Exception` handler 把异常细节或堆栈返回给客户端。
  6. 用字段注入代替构造器注入，破坏可测性并隐藏循环依赖。
- **可执行检查清单**：
  - [ ] controller 内没有业务规则，只有 HTTP 到 service 的映射。
  - [ ] API 出入参用 DTO，持久化对象不直接暴露给接口。
  - [ ] 写事务与只读事务已按语义区分。
  - [ ] 参数校验注解覆盖所有入口 DTO，校验失败有统一错误结构。
  - [ ] 缓存读写配对，失效路径完整。
  - [ ] `@EnableCaching` 与 `@EnableAsync` 已在配置类启用。
  - [ ] 外部调用有超时、重试与 circuit breaker。
  - [ ] 限流不依赖未配置可信代理的转发头。
  - [ ] 日志为结构化格式，异常有堆栈与业务键，且不含敏感数据。
- **上游维护提示**：本 Skill 源自第三方上游（`origin: ECC`），中文版**只出中文要点、不译正文与代码块**；细节与更新以英文原文为准，避免与上游分叉。

## 4. `springboot-security` — Spring Boot 安全加固

- **源文件**：`skills/tech/springboot-security/SKILL.md`
- **上游来源**：frontmatter 含 `origin: ECC`，未署具名作者，属**第三方上游**。正文由上游维护，中文版不翻译。
- **用途**：管 Spring Security 的配置与评审口径：认证流程、授权模式、OAuth2 / OIDC 集成、JWT 处理与安全响应头。源文件的目标是确保 Spring Boot 应用按当前最佳实践被保护起来。以下各项为**强制要求**，不是建议。
- **何时加载**（源 `## When to Activate`，7 条）：添加认证（JWT、OAuth2、session 式）；实现授权（`@PreAuthorize`、基于角色的访问）；校验用户输入（Bean Validation、自定义 validator）；配置 CORS、CSRF 或安全响应头；管理密钥（Vault、环境变量）；添加限流或暴力破解防护；扫描依赖 CVE。
- **核心规则要点**：
  - 源 `## Rule` 五条：① **禁止**把密钥存进代码或配置文件；② 密码必须用 BCrypt 或 Argon2 哈希；③ JWT 必须短过期并配 refresh token 模式；④ 状态变更操作必须启用 CSRF 保护；⑤ 必须配置安全响应头（CSP、HSTS、X-Frame-Options）。
  - 认证：优先无状态 JWT，或带吊销列表的不透明 token；session cookie 必须带 `httpOnly`、`Secure`、`SameSite=Strict`；token 校验用 `OncePerRequestFilter` 或 resource server。
  - 授权：必须启用 `@EnableMethodSecurity`；用 `@PreAuthorize("hasRole('ADMIN')")` 或 `@PreAuthorize("@authz.canEdit(#id)")` 等表达式；默认拒绝（deny by default），只暴露必需的 scope。
  - 输入校验：controller 上用 `@Valid`；DTO 上施加 `@NotBlank`、`@Email`、`@Size` 或自定义 validator；任何 HTML 在渲染前必须按白名单做净化。
  - SQL 注入防护：使用 Spring Data repository 或参数化查询；native query 必须用 `:param` 绑定，**禁止**拼接字符串。派生查询（如 `findByEmailAndActiveTrue`）自动参数化，属首选。
  - 密码编码：**禁止**明文存储；必须用 `PasswordEncoder` bean（示例为 cost factor 12 的 `BCryptPasswordEncoder`），**禁止**手写哈希逻辑。
  - CSRF：浏览器 session 应用必须保持 CSRF 开启，并把 token 放进表单或请求头；纯 Bearer token 的 API 可以关闭 CSRF，改用无状态认证（`csrf(csrf -> csrf.disable())` 配 `SessionCreationPolicy.STATELESS`）。
  - 密钥管理：**禁止**密钥入源码；从环境变量或 vault 加载；`application.yml` 保持无凭据，只写占位符（如 `${DB_PASSWORD}`）；Spring Cloud Vault 用 `${VAULT_TOKEN}`；token 与数据库凭据必须定期轮换。
  - 安全响应头：CSP 指令 `default-src 'self'`；`frameOptions` 用 `sameOrigin`；启用 `xssProtection`；`referrerPolicy` 用 `NO_REFERRER`。
  - CORS：必须在 security filter 层配置，而不是 per-controller；**生产环境禁止使用通配符 `*`**；示例把允许来源限定为具体域名，方法限定 GET/POST/PUT/DELETE，头限定 Authorization 与 Content-Type，配 `setAllowCredentials(true)`、`setMaxAge(3600L)` 并只注册到 `/api/**`。
  - 限流：对昂贵端点用 Bucket4j 或网关层限流；突增必须记日志并告警；超限返回 429 并给 retry 提示。
  - 依赖安全：CI 中必须跑 OWASP Dependency Check / Snyk；Spring Boot 与 Spring Security 必须保持在受支持版本；已知 CVE 必须让构建失败。
  - 日志与 PII：**禁止**记录密钥、token、密码或完整卡号（PAN）；敏感字段必须脱敏；使用结构化 JSON 日志。
  - 文件上传：必须校验大小、content type 与扩展名；必须存到 web root 之外；必要时做扫描。
  - 源文件未单列 `## MUST DO` / `## MUST NOT DO` / `## Constraints` 小节；强制项以 `## Rule` 与 `## Checklist Before Release` 为准。
- **关键做法**：源文 `Remember` 给出四条底线——默认拒绝、校验输入、最小权限、安全先于配置（secure-by-configuration first）。评审顺序建议按认证 → 授权 → 输入校验 → 数据访问 → 密钥 → 响应头与跨域 → 限流 → 依赖 → 日志与上传。
- **常见坑（反模式）**：
  1. `application.yml` 里提交明文密码——直接违反密钥外部化要求。
  2. 生产 CORS 用通配符来源并同时允许携带凭据，等于对任意站点开放。
  3. 浏览器 session 应用关掉 CSRF，或反过来给纯 Bearer token API 硬套 CSRF 开关导致功能异常。
  4. 自写哈希或明文存密码，绕过 `PasswordEncoder`。
  5. 只做入口 Bean Validation，漏掉 native query 拼接与 HTML 白名单净化。
  6. 日志或异常响应里带出 token、密码或完整卡号。
  7. 依赖长期不升级、CI 不做 CVE 扫描，已知漏洞进入生产。
- **可执行检查清单**（据源 `## Checklist Before Release` 10 条转写）：
  - [ ] auth token 校验正确且过期处理正确。
  - [ ] 每条敏感路径都有授权守卫。
  - [ ] 所有输入都经过校验与净化。
  - [ ] 不存在字符串拼接的 SQL。
  - [ ] CSRF 姿态与应用类型匹配（session 应用开启，纯 token API 用无状态）。
  - [ ] 密钥已外部化，仓库内无任何提交的凭据。
  - [ ] 安全响应头已配置（CSP、frameOptions、xssProtection、referrerPolicy）。
  - [ ] API 已限流。
  - [ ] 依赖已扫描且处于受支持版本。
  - [ ] 日志中不含敏感数据。
- **上游维护提示**：本 Skill 源自第三方上游（`origin: ECC`），中文版**只出中文要点、不译正文与代码块**。安全要求按原文强度转写为「必须 / 禁止」，未作弱化；细节与更新以英文原文为准。

## 5. `tailwind-css-patterns` — Tailwind CSS 样式模式

- **源文件**：`skills/tech/tailwind-css-patterns/SKILL.md`
- **上游来源**：frontmatter 含 `name`、`description` 与 `allowed-tools: Read, Write, Edit, Glob, Grep, Bash`，未署第三方作者；`SKILL_MANIFEST.json` 记录的 source 为 `tech skill library`，即内部技术栈库。
- **用途**：管 Tailwind CSS 的工具类组合模式：utility-first 写法、移动优先响应式断点、布局（flexbox 与 grid）、间距与排版刻度、交互状态、暗色模式、组件抽取、生产清理与可访问性。源文件的目标是让 Tailwind 用法在不同项目间保持一致、可维护。源文件自称覆盖 v4.1+ 特性，包括 CSS-first 配置、自定义 utility 与增强的开发体验。
- **何时加载**（源 `## When to Use`，7 条）：用工具类给 React / HTML 组件写样式；用断点搭响应式布局；实现 flexbox 与 grid 布局；管理间距、颜色与排版；创建自定义设计系统；做移动优先优化；构建暗色模式界面。
- **核心规则要点**：
  - 源 `## Rule` 五条：① 工具类直接写在标记里，重复 3 次以上才抽 `@apply`；② 响应式必须移动优先，断点用 `sm` / `md` / `lg` / `xl`；③ 暗色模式走 class 策略；④ 自定义设计令牌放在 `tailwind.config` 的 `theme.extend`；⑤ **禁止**把行内样式与 Tailwind 混用。
  - 断点刻度（源文给出）：`sm:` 640px 起、`md:` 768px 起、`lg:` 1024px 起、`xl:` 1280px 起、`2xl:` 1536px 起。基准样式写移动端，再用前缀向上覆盖。
  - 布局：`.flex` 配 `items-center` / `justify-between`；响应式方向 `flex-col md:flex-row`；网格 `grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4`；容器 `container mx-auto px-4 max-w-7xl`。
  - 间距：使用 Tailwind 间距刻度（4、8、12、16 等）；`p-4` / `px-4 py-8` / `space-y-4`；响应式间距 `p-4 md:p-8 lg:p-12`。
  - 排版：`text-4xl font-bold`、`text-sm text-gray-600`、`leading-relaxed tracking-wide`；响应式标题 `text-2xl md:text-4xl lg:text-6xl`。
  - 交互状态：`hover:`、`focus:ring-2 focus:ring-blue-200`、`active:`、`disabled:opacity-50 disabled:cursor-not-allowed`，父级联动用 `group` 与 `group-hover:`。
  - 组件模式（源 `## Component Patterns`）：Card、Responsive User Card、Navigation Bar、Form Elements、Modal/Dialog 均给出完整工具类组合；结构类模式可复用，但按 `## Rule` 第 1 条应在重复 3 次以上时才抽 `@apply`。
  - 暗色模式：`dark:bg-gray-900 dark:text-white` 一类成对写法；在 `tailwind.config.js` 设 `darkMode: 'class'`（源注释允许 `'media'`），但 `## Rule` 第 3 条明确以 class 策略为准。
  - 性能与清理：`content` 必须正确配置扫描路径（含 `./src/**/*.{js,ts,jsx,tsx,vue,svelte}` 等），否则生产构建会漏样式；`jit` 加速构建；`aspect-video` 固定比例；`content-visibility` 与 `contain` 优化离屏与绘制。
  - 可访问性：焦点样式需满足 WCAG AA，提供 skip link（`sr-only focus:not-sr-only`），图标按钮加 `aria-label`，颜色对比需达标，动画必须尊重 `prefers-reduced-motion`（`motion-reduce:transition-none`、`motion-safe:`）。
  - v4.1 配置：用 `@import "tailwindcss"` 加 `@theme` 做 CSS-first 配置；自定义 utility 用 `@utility`；Vite 集成用 `@tailwindcss/vite` 插件；原生 CSS 变量可直接写进任意值 `bg-[var(--color-brand-500)]`；容器查询用 `@container` 配 `@lg:` / `@2xl:`。
  - 源 `## Constraints and Warnings` 七条：类名过长会降低可读性、需要时抽组件；生产构建必须正确配置 purge 的 content 路径；任意值应当少用，优先设计令牌；**禁止**让 `@apply` 配复杂选择器而引发优先级问题；暗色模式需要正确配置策略；JIT 模式下部分动态拼接的模式可能检测不到，必要时用 safelist；浏览器兼容性以官方文档为准。
  - 源文件未单列 `## MUST DO` / `## MUST NOT DO` 小节；强制与禁令以 `## Rule` 与 `## Constraints and Warnings` 为准。
- **关键做法**：源 `## Instructions` 给了 7 步执行序：移动优先起手 → 使用设计令牌 → 组合工具类 → 抽取重复组件类 → 在 `tailwind.config.js` 定制主题 → 为生产配置 content 路径做清理 → 在所有断点尺寸验证布局。`## Best Practices` 另有 10 条，其中第 5 条明确「优先工具类而非 `@apply`，可维护性更好」，第 9 条与第 10 条指向 v4.1 的 `@theme` 与 `@utility`。
- **常见坑（反模式）**：
  1. 类名串过长导致可读性崩溃；应在重复 3 次以上时抽组件或组件类。
  2. 生产构建漏配 `content` 路径，purge 把实际使用的类删掉，线上样式缺失。
  3. 滥用任意值（如任意像素写法），绕开设计令牌刻度，视觉一致性失控。
  4. `@apply` 配复杂选择器引发优先级问题。
  5. 动态拼接类名在 JIT 下检测不到，类名未生成；必须用 safelist。
  6. 暗色模式未配置策略就直接写 `dark:` 前缀，全部失效。
  7. 忽略 `prefers-reduced-motion` 与焦点可见性，无障碍不达标。
- **可执行检查清单**：
  - [ ] 基准样式为移动端，响应式前缀只向上覆盖。
  - [ ] 间距、颜色、排版全部取自 Tailwind 刻度或设计令牌。
  - [ ] 重复 3 次以上的模式已抽成组件或组件类。
  - [ ] 标记中不存在行内样式与 Tailwind 混用。
  - [ ] `content` 路径覆盖全部模板来源，生产构建样式完整。
  - [ ] 动态类名已用 safelist 或改为静态写法。
  - [ ] 暗色模式策略已在配置中显式声明并验证。
  - [ ] 焦点样式、`aria-label` 与 `motion-reduce` 均满足无障碍要求。
- **上游维护提示**：本 Skill 属仓库内 tech 层能力包（无第三方作者），中文版**只出中文要点、不译正文与代码块**。源文件在同一篇内同时给出 v4.1 CSS-first 配置与 v3 时代的 JavaScript 配置，属内部时序混写；细节与更新以英文原文为准。颜色一律以设计令牌表述，本要点不粘贴任何十六进制颜色字面量。

## 6. `tailwind-design-system` — Tailwind 设计系统

- **源文件**：`skills/tech/tailwind-design-system/SKILL.md`
- **上游来源**：frontmatter 只有 `name` 与 `description`，未署第三方作者；`SKILL_MANIFEST.json` 记录的 source 为 `tech skill library`，即内部技术栈库。
- **用途**：管 Tailwind CSS v4（2024+）的设计系统建设：CSS-first 配置、设计令牌、组件变体、响应式模式与可访问性。源文件开头即声明本 Skill 面向 Tailwind CSS v4，v3 项目应改查官方 upgrade guide。
- **何时加载**（源 `## When to Use This Skill`，6 条）：用 Tailwind v4 建组件库；用 CSS-first 配置落地设计令牌与主题；构建响应式且可访问的组件；在代码库内统一 UI 模式；从 Tailwind v3 迁移到 v4；用原生 CSS 特性设置暗色模式。
- **核心规则要点**：
  - 源 `## Rule` 五条：① 必须先定义令牌再写组件（颜色、间距、排版、阴影）；② 运行时主题必须用 CSS 自定义属性；③ 每个组件必须引用设计令牌，**禁止**硬编码取值；④ 令牌用法必须有可视化示例文档；⑤ 令牌与组件的版本必须分开管理。
  - **设计令牌层级（三层，源 `## Core Concepts` 第 1 条）**：Brand Tokens（抽象层）→ Semantic Tokens（用途层）→ Component Tokens（具体层）。源文示例链路为 `oklch(...)` → `--color-primary` → `bg-primary`。组件只能引用语义层或组件层令牌，**禁止**越过语义层直接绑定品牌层取值。
  - 令牌族与命名：语义色含 `--color-background`、`--color-foreground`、`--color-primary`、`--color-secondary`、`--color-muted`、`--color-accent`、`--color-destructive`、`--color-border`、`--color-ring`、`--color-card`，以及各自的 `-foreground` 配对令牌与 `--color-ring-offset`；圆角令牌 `--radius-sm|md|lg|xl`；动画令牌 `--animate-fade-in`、`--animate-fade-out`、`--animate-slide-in`、`--animate-slide-out`；容器查询令牌 `--container-xs|sm|md|lg`。颜色建议用 OKLCH，以获得更好的感知均匀性。
  - **组件架构（源 `## Core Concepts` 第 2 条）**：固定五段式 `Base styles → Variants → Sizes → States → Overrides`。`Pattern 1` 用 `CVA`（class-variance-authority）的 `cva(...)` 加 `VariantProps` 定义变体与尺寸，配 `cn()`（`clsx` 加 `tailwind-merge`）合并类名，并用 `Slot` 支持 `asChild`；`Pattern 2` 用复合组件（`Card` / `CardHeader` / `CardTitle` / `CardDescription` / `CardContent` / `CardFooter`）暴露结构槽位；`Pattern 3` 表单组件把 `error` 映射为 `aria-invalid` 与 `aria-describedby`，错误文案带 `role="alert"`；`Pattern 4` 用 `cva` 做响应式 `Grid` 与 `Container`；`Pattern 5` 用原生 CSS 动画与 `@starting-style` 做入场；`Pattern 6` 用主题 provider 切换 `.dark` 类。
  - React 19 口径：ref 已是普通 prop，**禁止**再使用 `forwardRef`。
  - v4 关键变化对照（源 `## Key v4 Changes`）：`tailwind.config.ts` → CSS 里的 `@theme`；`@tailwind base/components/utilities` → `@import "tailwindcss"`；`darkMode: "class"` → `@custom-variant dark (&:where(.dark, .dark *))`；`theme.extend.colors` → `@theme { --color-*: value }`；`require("tailwindcss-animate")` → `@theme` 内的 CSS `@keyframes` 加 `@starting-style` 入场动画。
  - 暗色模式：用 `@custom-variant dark` 定义变体，在 `.dark` 作用域下重写同一批 CSS 自定义属性，而不是在组件里写两套颜色类。
  - 令牌修饰符：引用其它 CSS 变量时用 `@theme inline`；希望未被引用也生成变量时用 `@theme static`；用 `--color-*: initial` 清空默认命名空间后自定义。
  - 半透明色阶：用 `color-mix(in oklab, var(--color-primary) N%, transparent)` 从语义令牌派生，**禁止**另存独立颜色值。
  - `## Best Practices` 的 Do：用 `@theme` 块、用 OKLCH 颜色、用 `CVA` 组合变体、用语义令牌（`bg-primary` 而不是色阶类名）、用 `size-*` 简写、补齐可访问性（ARIA 与焦点态）。Don't：**禁止**再用 `tailwind.config.ts`；**禁止**再用 `@tailwind` 指令；**禁止**再用 `forwardRef`；**禁止**随意使用任意值，应扩展 `@theme`；**禁止**硬编码颜色，必须用语义令牌；**禁止**忘记暗色模式，两个主题都要测。
  - v3 到 v4 迁移清单 10 条：把 `tailwind.config.ts` 换成 CSS `@theme` 块；把 `@tailwind base/components/utilities` 换成 `@import "tailwindcss"`；把颜色定义移入 `@theme { --color-*: value }`；把 `darkMode: "class"` 换成 `@custom-variant dark`；把 `@keyframes` 移入 `@theme` 块（保证随主题产出）；把 `require("tailwindcss-animate")` 换成原生 CSS 动画；把 `h-10 w-10` 改成 `size-10`；移除 `forwardRef`；考虑改用 OKLCH；用 `@utility` 指令替代自定义插件。
  - 源文件未单列 `## MUST DO` / `## MUST NOT DO` / `## Constraints` 小节；强制与禁令以 `## Rule` 与 `## Best Practices` 为准。
- **关键做法**：先令牌后组件；用 `cn()` 统一类名合并以避免冲突；变体与尺寸用 `CVA` 类型化而不是字符串拼接；焦点态统一抽成 `focusRing` 常量、禁用态抽成 `disabled` 常量；暗色模式通过覆盖 CSS 自定义属性实现，组件类名保持不变。
- **常见坑（反模式）**：
  1. 用色阶类名代替语义令牌，品牌换肤与主题切换全部失效。
  2. 继续使用 `tailwind.config.ts`、`@tailwind` 指令或 `forwardRef`——v4 与 React 19 下均属被替换项。
  3. 组件里直接写具体颜色值或任意值，不经过 `@theme`。
  4. 只做亮色主题、不验证暗色主题。
  5. 把 `@keyframes` 写在 `@theme` 之外，导致引用 `--animate-*` 时关键帧不产出。
  6. 令牌层级越级引用：组件直接绑定品牌层，之后调整语义层无法生效。
  7. 令牌与组件版本不分开管理，升级令牌会连带破坏组件契约。
- **可执行检查清单**：
  - [ ] 令牌先于组件定义，颜色、间距、排版、阴影齐备。
  - [ ] 组件类名只引用语义或组件令牌，无具体颜色值。
  - [ ] `@theme` 块承担全部主题配置，仓库内无 `tailwind.config.ts`。
  - [ ] `@keyframes` 位于 `@theme` 内，动画令牌可被引用。
  - [ ] 变体与尺寸用 `CVA` 定义并带类型。
  - [ ] 暗色模式通过 `.dark` 覆盖令牌实现，两套主题均已验证。
  - [ ] 焦点态、禁用态与 ARIA 属性齐备。
  - [ ] 迁移按 v3 到 v4 清单逐项核对完成。
- **上游维护提示**：本 Skill 属仓库内 tech 层能力包（无第三方作者），中文版**只出中文要点、不译正文与代码块**。为遵守中文版口径，本要点一律以「设计令牌 / OKLCH」表述颜色，**不粘贴任何十六进制颜色字面量**；源文件中出现十六进制字面量的两处示例属源文件内部矛盾，已记入附录 B。

## 7. `typescript-advanced-types` — TypeScript 高级类型

- **源文件**：`skills/tech/typescript-advanced-types/SKILL.md`
- **上游来源**：frontmatter 只有 `name` 与 `description`，未署第三方作者；`SKILL_MANIFEST.json` 记录的 source 为 `tech skill library`，即内部技术栈库。
- **用途**：管 TypeScript 类型系统的进阶用法：泛型与约束、条件类型、映射类型、模板字面量类型、工具类型与类型级编程。源文件的目标是把类型系统用到编译期安全上，而不止于基础标注。
- **何时加载**（源 `## When to Use This Skill`，8 条）：构建类型安全的库或框架；创建可复用的泛型组件；实现复杂类型推断逻辑；设计类型安全的 API 客户端；构建表单校验系统；创建强类型配置对象；实现类型安全的状态管理；把 JavaScript 代码库迁移到 TypeScript。
- **核心规则要点**：
  - 源 `## Rule` 五条：① 优先类型推断，只在边界写标注；② 状态机用可辨识联合（discriminated union）；③ 穷尽检查用 `never`；④ 泛型约束用 `extends`，不用 `any`；⑤ 避免类型断言 `as`，改用类型守卫。
  - 泛型：`function identity<T>(value: T): T`；约束用 `T extends HasLength`；多参数用 `merge<T, U>(...) => T & U`。
  - 条件类型：`T extends string ? true : false`；用 `infer R` 提取返回类型；分布式条件类型对联合逐项分发；嵌套条件可定义 `TypeName<T>` 一类类型映射。
  - 映射类型：`readonly [P in keyof T]: T[P]` 做只读；`[P in keyof T]?: T[P]` 做可选；键重映射用 `as` 子句（如 `as \`get${Capitalize<string & K>}\``）；按值类型过滤属性用 `PickByType<T, U>`。
  - 模板字面量类型：`\`on${Capitalize<EventName>}\`` 生成事件名联合；`Uppercase` / `Lowercase` / `Capitalize` / `Uncapitalize` 做字符串变换；可用递归类型构造点分路径联合（如配置键路径）。
  - 内置工具类型：`Partial`、`Required`、`Readonly`、`Pick`、`Omit`、`Exclude`、`Extract`、`NonNullable`、`Record`。
  - 推断技巧：`infer` 提取数组元素类型、`Promise` 内部类型与函数参数元组；类型守卫写作 `value is string`；断言函数写作 `asserts value is string`。
  - 高级模式（源 `## Advanced Patterns`）：类型安全事件发射器 `TypedEventEmitter`；类型安全 API 客户端（`EndpointConfig` 配 `ExtractParams` / `ExtractBody` / `ExtractResponse` 与可变元组参数，让缺少必填 body 直接编译报错）；类型安全 Builder（`RequiredKeys` / `OptionalKeys` / `IsComplete` 配 `this` 类型约束，必填字段未设齐时 `build()` 不可调用）；`DeepReadonly` 与 `DeepPartial`；类型安全表单校验；可辨识联合状态机与 `reducer`。
  - 最佳实践 10 条：用 `unknown` 代替 `any`；对象形状优先 `interface`；联合与复杂类型用 `type`；尽量让 TypeScript 推断；抽可复用 helper 类型；用 const 断言保留字面量类型；避免类型断言、改用类型守卫；复杂类型加 JSDoc；开启全部 strict 编译选项；用类型测试验证类型行为（如 `AssertEqual`、`ExpectError`）。
  - 性能约束：避免深层嵌套条件类型；能用简单类型就用简单类型；缓存复杂类型计算；限制递归类型的递归深度；生产构建可用构建工具跳过类型检查。
  - 源文件未单列 `## Workflow` 与 `## Guardrails` 小节，也未单列 `## MUST DO` / `## MUST NOT DO` / `## Constraints`；执行序由 `## When to Use This Skill` 与 `## Best Practices` 承担。
- **关键做法**：类型级 API 设计走「用联合表达状态、用 `never` 兜穷尽、用 `extends` 收窄输入、用守卫收窄输出」四步；可复用类型工具集中放一处并在类型测试中固定其行为，避免类型逻辑散落。
- **常见坑（反模式）**（源 `## Common Pitfalls` 7 条转写）：
  1. 滥用 `any`，TypeScript 的类型保护形同虚设。
  2. 忽略 strict 空值检查，编译通过但运行时出错。
  3. 类型写得过于复杂，显著拖慢编译。
  4. 不用可辨识联合，白白丢失类型收窄机会。
  5. 忘记 `readonly` 修饰，产生非预期可变。
  6. 循环类型引用导致编译器报错。
  7. 不处理边界情况，如空数组或 null。
- **可执行检查清单**：
  - [ ] 公共 API 的输入输出类型显式，内部尽量靠推断。
  - [ ] 类型中不出现 `any`，未知输入一律用 `unknown`。
  - [ ] 状态机全部用可辨识联合表达，`switch` 有 `never` 兜底。
  - [ ] 泛型参数都有 `extends` 约束。
  - [ ] 收窄用类型守卫或断言函数，不用 `as` 强行断言。
  - [ ] 可复用类型工具有类型测试覆盖（`AssertEqual` 一类）。
  - [ ] strict 编译选项全部开启。
  - [ ] 复杂类型已评估编译耗时，递归深度受控。
- **上游维护提示**：本 Skill 属仓库内 tech 层能力包（无第三方作者），中文版**只出中文要点、不译正文与代码块**；细节与更新以英文原文为准。

## 8. `vue` — Vue 3 组合式 API

- **源文件**：`skills/tech/vue/SKILL.md`
- **上游来源**：frontmatter 的 `metadata.author` 为 `Anthony Fu`，`metadata.version` 为 `"2026.1.31"`，`metadata.source` 为 `Generated from https://github.com/vuejs/docs, scripts at https://github.com/antfu/skills`。正文由上游从 Vue 官方文档生成，属**第三方上游**，中文版不翻译。
- **用途**：管 Vue 3（源文声明基于 Vue 3.5）的组合式 API 写法：`<script setup>` 宏、响应式系统与生命周期、内置组件与自定义指令。参考文件分三份：`references/script-setup-macros.md`、`references/core-new-apis.md`、`references/advanced-patterns.md`。核心口径是**组合式 API 优先**，新代码一律使用组合式 API 而非 Options API。
- **何时加载**：编写 Vue SFC；定义组件 props 与 emits（`defineProps` / `defineEmits` / `defineModel`）；处理响应式、监听与生命周期；使用 `Transition`、`Teleport`、`Suspense`、`KeepAlive`、`v-memo` 或自定义指令时。
- **核心规则要点**：
  - 源 `## Rule` 五条：① 必须始终使用组合式 API 配 `<script setup lang="ts">`；② 不需要深层响应式时优先 `shallowRef` 而非 `ref`；③ 可复用逻辑抽 composables；④ `defineProps` / `defineEmits` 用 TypeScript 泛型；⑤ 新代码**禁止**使用 Options API。
  - `## Preferences` 五条与上同向：优先 TypeScript 而非 JavaScript；优先 `<script setup lang="ts">` 而非 `<script>`；为性能优先 `shallowRef`；一律组合式 API；**不鼓励**使用 Reactive Props Destructure。
  - 组件模板范式（源 `## Quick Reference`）：用 `defineProps<{ title: string; count?: number }>()` 声明 props；用 `defineEmits<{ update: [value: string] }>()` 声明事件；用 `defineModel<string>()` 声明双向绑定契约（模板侧配合 `v-model` 使用）；派生值用 `computed`；副作用用 `watch(() => props.title, ...)`；生命周期用 `onMounted`。
  - 关键导入清单：响应式 `ref`、`shallowRef`、`computed`、`reactive`、`readonly`、`toRef`、`toRefs`、`toValue`；监听 `watch`、`watchEffect`、`watchPostEffect`、`onWatcherCleanup`；生命周期 `onMounted`、`onUpdated`、`onUnmounted`、`onBeforeMount`、`onBeforeUpdate`、`onBeforeUnmount`；工具 `nextTick`、`defineComponent`、`defineAsyncComponent`。
  - 内置组件与指令：`Transition`、`Teleport`、`Suspense`、`KeepAlive`、`v-memo`、自定义指令。
  - 关于 `storeToRefs` 保持响应式：本 Skill 不涉及 Pinia；一旦涉及跨组件共享状态，消费 store 时必须用 `storeToRefs` 保持响应式，该规则由 `vue-pinia-best-practices` 给出（含 `pinia` 的 store 拆分与 actions 归位口径）。
  - 源文件未单列 `## Workflow`、`## Guardrails`、`## MUST DO` / `## MUST NOT DO`、`## Constraints` 小节；强制与禁令集中在 `## Rule` 与 `## Preferences`。
- **关键做法**：组件统一用两段式 SFC（`<script setup lang="ts">` 加 `<template>`）；props 与 emits 全部走 TypeScript 泛型以获得编译期检查；`defineModel` 只用于真正的双向契约，其余保持 props down / events up；不需要深层响应式的大对象或第三方实例用 `shallowRef` 降低代理开销。
- **常见坑（反模式）**：
  1. 新代码继续写 Options API，与本 Skill 的 `## Rule` 第 5 条直接冲突。
  2. 混用 `<script>` 与 `<script setup>`，或把 `<script setup>` 的位置与块顺序搞乱。
  3. 不需要深层响应式却一律用 `ref`，或反过来在需要深层响应式处用 `shallowRef` 导致视图不更新。
  4. 使用 Reactive Props Destructure（源文明确「不鼓励」）。
  5. 直接解构 store 状态导致丢失响应式；必须用 `storeToRefs`。
  6. 忘记在 `onUnmounted` 或 `onWatcherCleanup` 中清理副作用。
  7. 把 `v-model` 用在非双向契约上，破坏单向数据流。
- **可执行检查清单**：
  - [ ] 所有新组件使用组合式 API 与 `<script setup lang="ts">`。
  - [ ] props 与 emits 用 TypeScript 泛型声明并可编译检查。
  - [ ] 不需要深层响应式的场景已改用 `shallowRef`。
  - [ ] 可复用逻辑已抽为 composables。
  - [ ] 未使用 Reactive Props Destructure。
  - [ ] 消费 `pinia` store 时用 `storeToRefs` 保持响应式。
  - [ ] 副作用与监听器在卸载时清理。
  - [ ] 内置组件选用符合需求（`KeepAlive`、`Teleport`、`Suspense`、`Transition` 各就其位）。
- **上游维护提示**：本 Skill 源自第三方上游（Anthony Fu，由 Vue 官方文档生成），中文版**只出中文要点、不译正文与 references**。源文声明基于 Vue 3.5，但 `## Preferences` 又写「不鼓励 Reactive Props Destructure」，而 Vue 3.5 已正式支持该特性，二者存在口径张力，详见附录 B。

## 9. `vue-best-practices` — Vue 生产最佳实践

- **源文件**：`skills/tech/vue-best-practices/SKILL.md`
- **上游来源**：frontmatter 的 `license` 为 `MIT`，`metadata.author` 为 `github.com/vuejs-ai`，`metadata.version` 为 `"18.0.0"`。属**第三方上游**，中文版不翻译。
- **用途**：管 Vue 3 生产实践的工作流指令集。源文明确要求：把本 Skill 当指令集用，**按顺序**执行工作流，除非使用者显式要求换序。`description` 还声明任何 Vue、`.vue` 文件、Vue Router、Pinia 或 Vite 配 Vue 的任务都必须使用本 Skill，并声明除非项目明确要求 Options API，否则一律使用组合式 API（Composition API）。
- **何时加载**：任何 Vue、`.vue` 文件、Vue Router、Pinia 或 Vite + Vue 任务；编写前按工作流顺序逐段执行。
- **核心规则要点**：
  - 核心原则 5 条（源 `## Core Principles`）：状态可预测——one source of truth，其余全部派生；数据流显式——Props down、Events up；组件小而聚焦；避免无谓重渲染；可读性优先，写自解释代码。
  - 第 1 步（required）确认架构：默认技术栈为 Vue 3 加组合式 API 加 `<script setup lang="ts">`。只有项目明确用 Options API 才加载 `vue-options-api-best-practices`，只有明确用 JSX 才加载 `vue-jsx-best-practices`（两处都写 if available）。
  - 第 1.1 步（required）必须先读四份核心参考，并在**整个任务期间**保持在工作上下文中，而不是出问题才查：`references/reactivity.md`、`references/sfc.md`、`references/component-data-flow.md`、`references/composables.md`。
  - 第 1.2 步（required）先规划组件边界：非平凡功能动手前先写组件地图；每个组件用一句话定义单一职责；entry/root 与路由级 view 组件默认只作组合面；把功能 UI 与功能逻辑移出 entry/root/view；为每个子组件定义 props / emits 契约；新增超过一个组件时倾向 `components/<feature>/...` 与 `composables/use<Feature>.ts` 的按功能分目录。
  - 第 2 步（required）响应式：源码状态保持最小（`ref` / `reactive`），能用 `computed` 派生的全部派生；只有副作用才用 watcher；**禁止**在模板里重复做昂贵计算。
  - 第 2 步 SFC 结构与模板安全：SFC 段落顺序固定为 `<script>` → `<template>` → `<style>`；职责聚焦、大组件必须拆；模板保持声明式，分支与派生移到 script；遵守 `v-html`、列表渲染与条件渲染选型的模板安全规则。
  - 组件拆分触发条件——满足任一即必须拆：同时承担编排/状态与多段实质展示标记；存在 3 个以上独立 UI 段（如 form、filters、list、footer/status）；某模板块重复或可复用（行、卡片、列表项）。entry/root 与 view 规则：保持薄，只做 app shell / layout、provider 装配与功能组合；**禁止**把完整功能实现放进 entry/root/view。CRUD 或列表功能至少拆为 feature container、input/form、list（和/或 item）、footer/actions 或 filter/status 四类。只有极小的丢弃型 demo 才允许单文件实现，且必须显式说明为何不需要拆分。
  - 数据流：props down / events up 为主；`v-model` 只用于真正的双向组件契约；provide/inject 只用于深树依赖或共享上下文；契约用 `defineProps`、`defineEmits` 与 `InjectionKey` 显式类型化。
  - composables：逻辑被复用、带状态或副作用重时抽 composable；API 保持小而带类型、可预期；功能逻辑与展示组件分离。抽出的状态与副作用应移入 composables。
  - 第 3 步可选特性（默认**不得**添加，需求出现才加载对应 reference）：slots、fallthrough attributes、`<KeepAlive>`、`<Teleport>`、`<Suspense>`，以及动画（`<Transition>`、`<TransitionGroup>`、class-based、state-driven）；较少见的有 directives、async components、render functions、plugins，以及 state-management（应用级共享状态跨功能边界时）。跨组件共享状态落在 `state-management` 参考上，消费 store 时用 `storeToRefs` 保持响应式，细则见 `vue-pinia-best-practices`。
  - 第 4 步性能：性能是功能之后的一轮独立工作；核心行为未实现并验证之前**禁止**优化。四类对症参考：大列表渲染瓶颈走虚拟化；静态子树无谓重渲染用 `v-once` / `v-memo`；热点列表路径避免过度抽象；`updated` 钩子触发过于频繁需专门处理。
  - 第 5 步自检 12 条：核心行为达成且符合需求；四份 must-read reference 都已读并应用；响应式模型最小且可预测；SFC 结构与模板规则已遵守；组件聚焦且拆分有据；entry/root 与 view 仍为组合面（或已显式声明小 demo 例外）；拆分决策可辩护、职责边界清晰；数据流契约显式且带类型；composable 使用得当；状态与副作用已迁入 composable（如适用）；可选特性只在需求要求时使用；性能改动只在功能完成后进行。
  - 源文件未单列 `## Guardrails`、`## MUST DO` / `## MUST NOT DO`、`## Constraints` 小节；强制项以 `## Core Principles`、工作流 required 标记与 `## 5) Final self-check` 为准。
- **关键做法**：把「先架构、后基础、再可选、最后性能」当硬顺序；组件地图与 props/emits 契约先写；四份核心参考常驻上下文；收尾必须逐条走自检清单。
- **常见坑（反模式）**：
  1. 把整个功能写进 entry/root 或路由 view 组件，违反「组合面」要求。
  2. 跳过 `1.1` 的四份 must-read reference，凭记忆写代码。
  3. 核心行为未跑通就做性能优化，顺序颠倒。
  4. 在模板里做分支与派生计算，违反模板声明式要求。
  5. 用 `v-model` 承载所有 props 传递，破坏单向数据流。
  6. 默认引入 `<Suspense>`、`<Teleport>` 等可选特性，缺少需求依据。
  7. 解构 store 状态而不用 `storeToRefs`，造成响应式丢失。
- **可执行检查清单**：
  - [ ] 已确认默认栈为 Vue 3 加组合式 API 加 `<script setup lang="ts">`。
  - [ ] 四份 must-read reference 已在动手前读完并在任务中保持引用。
  - [ ] 非平凡功能已有组件地图与一句话职责定义。
  - [ ] entry/root 与 view 组件保持薄，功能实现已下移。
  - [ ] 源码状态最小化，其余全部用 `computed` 派生。
  - [ ] SFC 段落顺序为 `<script>` → `<template>` → `<style>`，模板保持声明式。
  - [ ] 满足任一拆分触发条件时组件已拆分。
  - [ ] props / emits 契约显式且带类型，`v-model` 只用于真双向契约。
  - [ ] 可选特性都有明确需求依据。
  - [ ] 性能优化在功能验证之后才进行。
  - [ ] 收尾已逐条走完第 5 步自检 12 条。
- **上游维护提示**：本 Skill 源自第三方上游（`github.com/vuejs-ai`，`version: "18.0.0"`，MIT），中文版**只出中文要点、不译正文与 references**。源文引用的 `vue-options-api-best-practices` 与 `vue-jsx-best-practices` 在本仓库中不存在，属悬空引用，详见附录 B。

## 10. `vue-pinia-best-practices` — Pinia 状态管理

- **源文件**：`skills/tech/vue-pinia-best-practices/SKILL.md`
- **上游来源**：frontmatter 的 `version` 为 `1.0.0`，`license` 为 `MIT`，`author` 为 `github.com/vuejs-ai`。属**第三方上游**，中文版不翻译。
- **用途**：管 Pinia 状态管理：状态该放哪里、setup store 怎么写、消费时如何保持响应式、actions 归位与 store 测试。源文目标是让 Pinia 状态可预测、可响应、可测、范围恰当，并给出常见坑与状态管理模式。
- **何时加载**：创建、评审、调试或重构 Pinia store；出现响应式失效、筛选刷新丢失、SSR 状态异常时。
- **核心规则要点**：
  - 源 `## Rule` 五条：① 一个 store 对应一个领域概念（domain concept），而不是一页一个；② 优先 setup store（组合式 API 风格，即 `defineStore` 的 setup 写法）而非 options store；③ 异步操作放 actions，**禁止**放 getters；④ store state 是响应式的，解构必须用 `storeToRefs`；⑤ store 必须能脱离组件独立测试。
  - 源 `## Workflow` 五步：① 判定状态归属——归 `pinia` store、URL/query 参数、组件局部状态还是后端数据；② 谨慎使用 setup store，并返回 DevTools、SSR、插件或持久化所需的**全部**状态；③ 在组件中消费 store state 时必须保持响应式；④ state 变更与副作用只放在 actions 里；⑤ 通过刷新页面、切换导航、检查受影响组件来验证状态行为。
  - 源 `## Guardrails` 三条：必须保持响应式时**禁止**直接解构 store state，必须用 `storeToRefs`；**禁止**把持久业务真相只放在前端状态里。**禁止**把 Pinia 当成「必须由后端 API 重新校验的数据」的缓存。
  - 故障到参考文件的索引（源文按症状给出）：启动报 `getActivePinia was called` 走 `reference/pinia-no-active-pinia-error.md`；setup store 的状态在 DevTools 或 SSR 中缺失走 `reference/pinia-setup-store-return-all-state.md`；解构 store 后 UI 不再响应式更新走 `reference/pinia-store-destructuring-breaks-reactivity.md`；store 方法在模板中调用丢失上下文走 `reference/store-method-binding-parentheses.md`；筛选条件刷新即重置或无法共享走 `reference/state-url-for-ephemeral-filters.md`；大型应用缺 DevTools 与约定走 `reference/state-use-pinia-for-large-apps.md`。
  - 关于 `storeToRefs` 保持响应式：这是本 Skill 的核心禁令之一（`## Rule` 第 4 条与 `## Guardrails` 第 1 条重复声明），即从 store 取出 state 或 getter 时禁止裸解构，必须用 `storeToRefs` 保留响应式代理。
  - 组合式 API 与 `script setup` 口径：本 Skill 的 setup store 即组合式 API 风格写法，与 `vue` 及 `vue-best-practices` 的「组合式 API 优先、使用 `<script setup lang="ts">`」口径一致；store 的消费侧代码同样写在 `<script setup>` 中。
  - 源文件未单列 `## MUST DO` / `## MUST NOT DO` / `## Constraints` 小节；强制与禁令以 `## Rule` 与 `## Guardrails` 为准。
- **关键做法**：先做状态归属判定再建 store，避免把临时筛选塞进 store；setup store 的返回值要与 DevTools、SSR、插件、持久化的可见性需求对齐；所有状态变更与副作用集中在 actions；store 用独立测试而不是靠组件测试间接覆盖。
- **常见坑（反模式）**：
  1. 直接解构 store state 或 getter，UI 不再响应式更新；必须改用 `storeToRefs`。
  2. 把必须由后端 API 重新校验的数据当成 Pinia 缓存长期持有。
  3. 把持久业务真相只放在前端状态里，与单一真相原则冲突。
  4. 按页面拆 store，领域概念碎片化，跨页共享与复用困难。
  5. 把异步操作写进 getters，破坏 getters 的纯函数语义。
  6. setup store 漏返回部分状态，导致 DevTools 看不到、SSR 水合不一致。
  7. store 与组件强耦合，无法独立测试。
- **可执行检查清单**：
  - [ ] 每个 store 对应一个领域概念，不是一页一个。
  - [ ] 使用 setup store 写法，且返回 DevTools、SSR、插件与持久化所需的全部状态。
  - [ ] 解构 state 或 getter 时一律使用 `storeToRefs`，响应式未丢失。
  - [ ] state 变更与副作用全部位于 actions，getters 保持纯净。
  - [ ] 临时筛选等易失状态放在 URL / query 参数而非 store。
  - [ ] 前端状态里不承载持久业务真相。后端数据未被 Pinia 当成免校验缓存。
  - [ ] store 有独立测试，不依赖组件挂载。
  - [ ] 已通过刷新、导航与受影响组件检查验证状态行为。
- **上游维护提示**：本 Skill 源自第三方上游（`github.com/vuejs-ai`，`version: 1.0.0`，MIT），中文版**只出中文要点、不译正文与 reference**。其参考文件目录名为 `reference/`（单数），与 `vue` 和 `vue-best-practices` 的 `references/`（复数）不一致，属命名口径不统一，详见附录 B。

## 附录 A：这 10 个 Skill 的选型速查

| 场景 | 首选 Skill | 配套 Skill | 选择要点 |
|---|---|---|---|
| 用 Python 写 API | `python-fastapi` | `postgresql-best-practices` | 先声明 Pydantic schema 再写端点；持久化与迁移按数据库 Skill 执行 |
| 用 React 写页面与组件 | `react-frontend` | `typescript-advanced-types`、`tailwind-css-patterns` | 写组件前先确认真相在后端；样式用 patterns，复杂类型用 advanced-types |
| Spring Boot 架构与 API 模式 | `springboot-patterns` | `java-springboot`、`springboot-security` | 先工程规范再架构模式；上线前必过安全加固 |
| Spring Boot 安全评审与加固 | `springboot-security` | `springboot-patterns` | 认证、授权、输入校验、CSRF、密码编码、密钥管理逐项过发布前清单 |
| 单组件样式与响应式布局 | `tailwind-css-patterns` | `tailwind-design-system` | 工具类组合与断点用 patterns；一旦要统一令牌与组件库就升级到 design-system |
| 建组件库、设计令牌与主题 | `tailwind-design-system` | `tailwind-css-patterns` | 先定令牌再做组件；v4 用 `@theme`，v3 项目先读官方升级指南 |
| 复杂类型逻辑与类型安全 API 客户端 | `typescript-advanced-types` | 对应框架 Skill | 类型工具集中放一处并配类型测试 |
| 写 Vue SFC 与组合式逻辑 | `vue` | `vue-best-practices` | 组合式 API 优先，新代码一律 `<script setup lang="ts">` |
| 任何 Vue 任务的工作流起点 | `vue-best-practices` | `vue`、`vue-pinia-best-practices` | 按五步工作流顺序执行，先架构后基础，性能最后做 |
| 前端共享状态与 `pinia` store | `vue-pinia-best-practices` | `vue-best-practices` | 先判定状态归属；临时筛选优先放 URL，消费时用 `storeToRefs` |

## 附录 B：第三方上游 Skill 清单与不翻译正文的理由

### B.1 第三方上游清单（据各 `SKILL.md` frontmatter 原文核对）

| Skill | 上游作者 / 来源（frontmatter 原文） | 处理口径 |
|---|---|---|
| `vue` | `metadata.author: Anthony Fu`；`metadata.source: Generated from https://github.com/vuejs/docs, scripts at https://github.com/antfu/skills`；`metadata.version: "2026.1.31"` | 不翻译正文，避免与上游分叉 |
| `vue-best-practices` | `metadata.author: github.com/vuejs-ai`；`license: MIT`；`metadata.version: "18.0.0"` | 不翻译正文，避免与上游分叉 |
| `vue-pinia-best-practices` | `author: github.com/vuejs-ai`；`license: MIT`；`version: 1.0.0` | 不翻译正文，避免与上游分叉 |
| `springboot-patterns` | `origin: ECC`，未署具名作者 | 不翻译正文，避免与上游分叉 |
| `springboot-security` | `origin: ECC`，未署具名作者 | 不翻译正文，避免与上游分叉 |

**其余 5 个为仓库内 tech 层能力包**：`python-fastapi`、`react-frontend`、`tailwind-css-patterns`、`tailwind-design-system`、`typescript-advanced-types` 的 frontmatter 均无第三方作者字段（`tailwind-css-patterns` 另有 `allowed-tools: Read, Write, Edit, Glob, Grep, Bash`），`SKILL_MANIFEST.json` 记录的 source 均为 `tech skill library`。它们同样只出中文要点、不译全文，便于整层统一维护与同步。

### B.2 不翻译正文的理由

1. **避免第二份真相源**：上述 5 个 Skill 由第三方作者或上游仓库维护，正文随上游持续演进。逐句翻译会产生一份会立刻过期的副本，上游一更新就无法低成本同步。
2. **保住审计断言**：`scripts/py/audit_methodology.py` 与 `scripts/py/audit_skill_health.py` 依赖英文标识符、门禁代号与英文规则措辞；纯中文替换会让断言缺失，Skill 健康分被反模式规则误扣。
3. **中文版定位是叠加层**：英文源继续作为唯一正式源，中文要点负责「管什么、何时加载、有哪些硬性规则与坑」，细节一律回到英文原文与 references。
4. **口径一致**：`00_导读/03_翻译口径与同步规则.md` 已规定中文版不修改任何英文源文件，`30_tech_20个Skill摘要.md` 也已对 tech 层建立「只出摘要、不译正文」的统一口径，本文件延续该口径并加深要点颗粒度。

### B.3 源文件中发现的过时与矛盾信息

| Skill | 位置 | 现象 | 影响与建议 |
|---|---|---|---|
| `vue` | `## Preferences` | 声明基于 Vue 3.5，同时写「Discourage using Reactive Props Destructure」，而 Vue 3.5 已正式支持该特性 | 与官方中文文档口径存在张力；引用前应回查上游最新版 |
| `vue` | frontmatter | `metadata.version: "2026.1.31"` 为日期型版本号，与语义化版本混用 | 同步规则宜按日期比对，不要按 semver 比较 |
| `vue-best-practices` | `## 1)` | 引用 `vue-options-api-best-practices` 与 `vue-jsx-best-practices`，两者在本仓库 `skills/` 下不存在 | 悬空引用；命中 Options API 或 JSX 项目时无对应 Skill 可加载 |
| `vue-best-practices` | 参考文件 | 使用 `references/`（复数）目录 | 与 `vue-pinia-best-practices` 的 `reference/`（单数）命名不一致 |
| `vue-pinia-best-practices` | `reference/` | 目录名为单数，正文链接格式为 `reference/xxx.md` | 跨 Skill 引用时容易拼错路径，建议上游统一 |
| `tailwind-css-patterns` | `## Overview` 与 `## Configuration` | 自称覆盖 v4.1+ 的 CSS-first 配置，同时给出 v3 时代的 `tailwind.config.js`、`content` 清理路径与 `jit: true` 开关 | `jit` 自 v3.0 起即为默认行为、v4 已无该选项，参考价值有限；应以上游当前文档为准 |
| `tailwind-css-patterns` | `## Performance Optimization` | HTML 示例使用 `content-visibility-auto` 与 `contain-layout` 类名，但 Tailwind 无同名内置工具类；v4 配置段定义的自定义 utility 名为 `content-auto` | 示例类名与自定义 utility 名不一致，直接照抄不会生效 |
| `tailwind-css-patterns` | `## Core Concepts` 与 `## Configuration` | 透明度写法混用 `bg-opacity-50`（v3 语法）与 v4 的斜杠语法 | v4 下应统一用斜杠透明度写法 |
| `tailwind-design-system` | `Pattern 6` 主题 provider | 在设置移动端 meta theme-color 时写入十六进制颜色字面量 | 与本 Skill「Use OKLCH colors」「Don't hardcode colors」自相矛盾；应改为从令牌读取 |
| `tailwind-design-system` | `Namespace Overrides` | 清空默认命名空间后为白、黑两个令牌赋十六进制字面量 | 同上，属内部矛盾；本要点一律以设计令牌表述 |
| `tailwind-design-system` | `## Best Practices` 与 `Advanced v4 Patterns` | `Don't use arbitrary values` 与 `@utility line-t` 中大量任意值写法并存 | 规则与示例冲突，应按「自定义 utility 内部可用、业务组件不用」理解 |
| `tailwind-design-system` | `## Best Practices` 与迁移清单 | Do 段写「Use OKLCH colors」为确定口径，迁移清单写「Consider OKLCH」为建议口径 | 语义强度不一致；以 Do 段的强制口径为准 |
| `springboot-patterns` | `## Error-Resilient External Calls` | 用 `Thread.sleep` 实现指数退避 | 在 WebFlux 等非阻塞栈上会阻塞线程；且 `## Rule` 另行要求外部调用加 circuit breaker，二者需配合使用 |
| `springboot-patterns` | `## Rate Limiting` 与 `## Production Defaults` | 限流示例按 `request.getRemoteAddr()` 取 IP，反转代理场景下取到的是代理 IP；源文以四条前置条件约束转发头 | 配置缺失时限流粒度失真，属高危默认；必须在部署清单中显式核对 |
| `springboot-patterns` | 代码示例 | 自定义重试未复用成熟库能力，与 `library first` 原则存在张力 | 生产建议改用框架级重试或专用库，并把重试与 circuit breaker 组合 |
| `python-fastapi` / `react-frontend` / `tailwind-css-patterns` / `tailwind-design-system` / `typescript-advanced-types` | frontmatter | 均无版本号字段，仅有 `name` 与 `description` | 无法按 frontmatter 判定版本；同步时只能比对正文哈希或修改时间 |

### B.4 同步建议

1. 上游 5 个 Skill 更新后，先看 frontmatter 的 `version` / `metadata.version` 与正文差异，只改受影响的小节，不整篇重写本文件。
2. 仓库内 5 个 Skill（无版本号）更新后，按正文哈希比对定位改动点。
3. 任何与本文件冲突的表述，以英文 `SKILL.md` 原文为准；本文件只做要点提炼，不承担真相源职责。
