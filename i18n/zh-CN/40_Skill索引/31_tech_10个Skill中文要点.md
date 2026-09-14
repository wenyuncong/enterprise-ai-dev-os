# tech 层 10 个 Skill 中文要点（上）| Tech Layer Chinese Essentials

> **源文件**：skills/tech/{docker-expert,flutter-animations,flutter-expert,java-performance-governance,java-springboot,javascript-typescript-jest,multi-stage-dockerfile,mysql-best-practices,node-backend,postgresql-best-practices}/SKILL.md
> **源版本**：未标注（以各 SKILL.md frontmatter 为准；`skills/SKILL_MANIFEST.json` 记录这 10 个 Skill 的 maturity 均为 verified）
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：本文件是**中文要点提炼**，不是逐句译文；正文与 references 保留英文，避免与上游分叉。Skill 名、路径、命令、代码标识符、框架与库名一律原样保留英文。语义强度不改变：`MUST` 译为「必须」，`MUST NOT` 译为「禁止」，`SHOULD` 译为「应当」，`MAY` 译为「可以」。

---

## 0. 一览表

| Skill | 技术栈 | 一句话职责 | 何时加载 |
|---|---|---|---|
| `docker-expert` | Docker / Compose | Dockerfile、多阶段构建、Compose 编排、镜像瘦身与容器安全的全流程专家 | 容器化应用、编写或评审 Dockerfile 与 Compose 文件、优化镜像体积与构建速度时 |
| `flutter-animations` | Flutter / Dart | 隐式/显式/Hero/交错/物理五类动画的选型决策树与实现模式 | 给 Flutter 应用加动效、不确定该用哪种动画类型、排查掉帧与卡顿时 |
| `flutter-expert` | Flutter 3+ / Dart | widget 组合、Riverpod/Bloc 状态管理、GoRouter 导航与性能剖析 | 新建或扩展 Flutter 应用、实现状态管理与导航、处理平台差异、优化渲染时 |
| `java-performance-governance` | Java / Spring | 批处理效率、无界缓存、资源泄漏、SQL 成本与可观测性治理 | 批删批改变慢、内存增长或 OOM、超时、连接池耗尽，或改动缓存/线程配置前 |
| `java-springboot` | Java / Spring Boot | 项目结构、注入方式、外部化配置、分层与测试切片的工程规范 | 编写或评审 Spring Boot 后端代码、控制器、服务、仓储、配置与测试时 |
| `javascript-typescript-jest` | JS / TS / Jest | 测试结构、Mock 边界、异步用例、快照与 React 组件测试 | 新增、评审、调试或重构 Jest 测试，尤其是异步代码与被 mock 依赖存在时 |
| `multi-stage-dockerfile` | Docker | 构建阶段与运行阶段分离、层缓存排序、生产镜像加固 | 容器化任意语言应用、压缩镜像体积、改善构建缓存、加固生产镜像时 |
| `mysql-best-practices` | MySQL | 模式设计、数据类型、索引策略、EXPLAIN、事务与运维加固 | 设计或评审 MySQL 模式、编写复杂 SQL、新增索引、执行迁移或修数据一致性问题时 |
| `node-backend` | Node.js / Express / NestJS / Fastify | 分层结构、schema 校验、异步纪律、错误处理与可观测性 | 新建或评审 Node.js API、新增路由或服务方法、修异步与错误处理缺陷、补测试时 |
| `postgresql-best-practices` | PostgreSQL | 类型与约束、索引验证、EXPLAIN ANALYZE、迁移、连接池与备份演练 | 设计表结构、编写或调优查询、新增索引、评审迁移安全性、规划备份与恢复时 |

---

## 1. `docker-expert` — Docker 容器化专家

- **源文件**：`skills/tech/docker-expert/SKILL.md`
- **上游来源**：社区来源（源 frontmatter `source: community`，`category: devops`、`risk: unknown`、`date_added: "2026-02-27"`），未署具名作者；`skills/SKILL_MANIFEST.json` 记 source 为 `tech skill library`
- **用途**：把容器化的全过程经验固化成可执行专家：Dockerfile 与多阶段构建写法、镜像体积优化、容器安全加固、Docker Compose 编排、生产部署模式与故障诊断。它先做环境探测与项目结构分析，再按「问题类别 → 复杂度 → 解决方案」给出打法，最后用构建、运行时与 Compose 三条验证链收口，目标是镜像精简、不以 root 运行、上线前可扫描。
- **何时加载**：容器化一个应用、编写或评审 Dockerfile、编写或评审 Compose 文件、优化镜像体积与构建速度、排查构建慢/体积大/服务通信失败/热重载失效时加载。源文件明确划界：Kubernetes 编排（pods、services、ingress）、GitHub Actions 容器化 CI/CD、AWS ECS/Fargate 等云厂商容器服务、复杂持久化的数据库容器化，均超出本 Skill 范围，必须转交对应专家并停止。
- **核心规则要点**（`## Rule` 六条，`MUST`/`MUST NOT` 强度照抄）：
  1. 必须（MUST）用多阶段构建压缩镜像体积。
  2. 生产环境禁止（MUST NOT）以 root 运行，必须创建具名 UID/GID 用户并切换 `USER`。
  3. 必须锁定基础镜像版本，禁止浮动标签导致构建不可复现。
  4. 必须提供 `.dockerignore` 控制构建上下文。
  5. 服务必须带健康检查（Health check mandatory for services）。
  6. 密钥只能走构建期 secret 或运行时注入，禁止进入镜像层。
  源文件未单列 `## Constraints` 与 `## MUST DO` / `## MUST NOT DO` 小节；其约束分布在 `## Rule`、六大 `Core Expertise Areas` 与 `## Code Review Checklist` 中。从正文再提炼的硬性要求：依赖安装必须与源码拷贝分层（先 `COPY package*.json` 再 `npm ci`，最后 `COPY . .`），把高频变更的层排在后面以保住层缓存；运行时优先 distroless 或 alpine；包管理器缓存必须在同一个 `RUN` 层内清理；后端网络应当设 `internal: true` 隔离；必须显式声明 CPU/内存上限与重启策略。
- **关键做法**：
  - 标准三阶段模板：`AS deps` 装生产依赖、`AS build` 编译、`AS runtime` 只拷产物；运行时用 `COPY --from=deps --chown=nextjs:nodejs` 与 `COPY --from=build --chown=nextjs:nodejs` 带权限拷贝。
  - 非 root 落地：`addgroup -g 1001 -S nodejs && adduser -S nextjs -u 1001`，随后 `USER nextjs`（也可写 `USER 1001`）。
  - 健康检查：`HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 CMD curl -f http://localhost:3000/health || exit 1`；复杂场景把脚本放到 `/usr/local/bin/health-check.sh` 并 `chmod +x` 后交给 `HEALTHCHECK`。
  - 编排就绪顺序：`depends_on: db: condition: service_healthy`，并给 db 配 `pg_isready` 的 `CMD-SHELL` 健康检查。
  - 密钥：Compose 侧用 `secrets` + `external: true` 与 `POSTGRES_PASSWORD_FILE` 这类 `*_FILE` 变量；构建侧用 BuildKit `RUN --mount=type=secret,id=api_key`。
  - 缓存与多架构：`RUN --mount=type=cache,target=/root/.npm`；`docker buildx create --name multiarch-builder --use` 配合 `docker buildx build --platform linux/amd64,linux/arm64 -t myapp:latest --push .`。
  - 资源与韧性：`deploy.resources.limits`（cpus、memory）与 `reservations`；`restart_policy` 的 `condition: on-failure`、`delay`、`max_attempts`、`window`。
  - 开发覆盖：独立 `target: development`，`volumes` 挂 `.:/app` 并用匿名卷遮住 `/app/node_modules`、`/app/dist`，开 `NODE_ENV=development`、`DEBUG=app:*` 与调试端口 `9229:9229`，`command: npm run dev`。
  - 验证链：构建期 `docker build --no-cache -t test-build .`、`docker history test-build --no-trunc`、`docker scout quickview test-build`；运行期 `docker run --rm -d --name validation-test test-build` + `docker exec validation-test ps aux`；编排期 `docker-compose config`。
- **常见坑（反模式）**（源文件在 `## Common Issue Diagnostics` 与检查清单中点名）：
  1. 依赖与源码一起 `COPY`，任何代码改动都击穿依赖层缓存，构建从分钟级退化到 10 分钟以上。
  2. 缺 `.dockerignore`，构建上下文过大，缓存频繁失效。
  3. 密钥硬编码在 `ENV` 或镜像层里，安全扫描直接失败。
  4. 以默认用户（root）运行，且基础镜像长期不更新，漏洞扫描不过。
  5. 服务缺健康检查，`depends_on` 只能按启动顺序而非就绪状态编排，导致间歇性连接失败。
  6. 生产镜像残留构建工具与包管理器缓存，镜像超过 1GB、部署变慢。
  7. 镜像层里先装依赖再 `npm cache clean` 却写在另一个 `RUN` 层，缓存实际没被清掉。
  8. 服务命名与端口随意，缺自定义网络，出现 DNS 解析失败、端口冲突、服务发现不通。
  9. 开发态与生产态混用一个 target，热重载失效、调试端口暴露进生产镜像。
- **可执行检查清单**：
  - [ ] 依赖层先于源码层，且包管理器缓存在同一 `RUN` 层内清理。
  - [ ] 存在 `builder` / `runtime` 分离的多阶段构建，生产阶段只含必要产物。
  - [ ] 构建上下文受 `.dockerignore` 约束，基础镜像选型有理由（alpine / distroless / scratch）。
  - [ ] 创建了具名 UID/GID 的非 root 用户，并用 `USER` 生效。
  - [ ] 密钥未出现在 `ENV`、`ARG` 默认值或镜像层中。
  - [ ] 每个服务都有健康检查，`depends_on` 使用 `condition: service_healthy`。
  - [ ] 自定义网络已配置，后端网络使用 `internal: true`。
  - [ ] 资源上限与 `restart_policy` 已声明；开发态与生产态 target 分离。
- **源文件核查发现（过时/矛盾）**：
  - 验证命令仍是 Compose V1 写法 `docker-compose config`，Compose V2 为 `docker compose config`（子命令带空格）。
  - Compose 示例首行 `version: '3.8'` 属历史字段，Compose V2 / Compose Specification 已废弃该顶层字段。
  - 示例基础镜像 `node:18-alpine` 与 `gcr.io/distroless/nodejs18-debian11` 指向已到生命周期的 Node 18 线；Rule 第 3 条要求锁定版本，但全部示例都使用浮动标签，规则与示例自相矛盾。
  - `npm ci --only=production` 的 `--only` 在 npm 7+ 已废弃，现应使用 `npm ci --omit=dev`。
  - 安全示例末尾的 `# Drop capabilities, set read-only root filesystem` 只是注释，没有对应的 `--cap-drop`、`read_only: true` 或 `security_opt` 写法；Rule 与检查清单要求的能力限制缺少可执行落点。
  - 转交目标 `kubernetes-expert` 在正文里被标注为 future，与 `github-actions-expert`、`devops-expert`、`database-expert` 一道都不在本仓库 49 个正式 Skill 名单内，交接话术会指向不存在的 Skill。
- **上游维护提示**：正文与 references 保留英文；本要点为中文提炼。上游更新后需复核：Compose 命令与 `version` 字段口径、Node 基础镜像版本线、`npm ci` 参数，以及转交专家清单是否已在本仓库落地。

---

## 2. `flutter-animations` — Flutter 动画实现

- **源文件**：`skills/tech/flutter-animations/SKILL.md`
- **上游来源**：第三方上游（源 frontmatter `metadata.author: Stanislav [MADTeacher] Chernyshev`、`version: "1.0"`），无 `source` 字段；`skills/SKILL_MANIFEST.json` 记 source 为 `tech skill library`
- **用途**：给 Flutter 动效提供完整的选型与实现路径：先用「动画类型决策树」把需求归到隐式动画、显式动画、Hero 转场、交错动画或物理动画五类之一，再给出每一类的标准组件、代码骨架与性能约束。它同时覆盖隐式动画组件清单、`AnimationController` 生命周期、Hero 共享元素、`Interval` 时序编排与物理模拟，最后用 DO / DON'T 两张清单收口可维护性与体验。
- **何时加载**：为 Flutter 应用添加动效、判断该用隐式还是显式动画、实现共享元素转场或交错入场、做拖拽与弹簧手感、以及优化动画性能与无障碍时加载。
- **核心规则要点**（`## Rule` 五条）：
  1. 简单场景应当优先用隐式动画（`AnimatedContainer`、`AnimatedOpacity` 等），不引入控制器。
  2. 复杂序列必须用 `AnimationController`（显式动画）获得完整生命周期控制。
  3. 必须始终 `dispose` 控制器。
  4. 必须在目标真机上测试，不能只在模拟器上验收。
  5. UI 反馈类动效的时长应当控制在 300ms 以内。
  源文件未单列 `## Constraints` / `## Guardrails` 小节，约束实际落在 `## Rule`、各小节 `Best Practices` 与文末 `### DO` / `### DON'T` 中。决策树的判据是：动画只作用于单个属性且由状态变化触发 → 隐式；需要完整生命周期控制、多属性同时动、要响应动画状态 → 显式；两个路由间共享同一元素 → Hero；多个动画需要顺序或重叠 → 交错；要自然物理手感、拖拽与滚动手势 → 物理。
- **关键做法**：
  - 隐式组件：`AnimatedContainer`（尺寸、颜色、装饰、内边距）、`AnimatedOpacity`、`TweenAnimationBuilder`（免样板的自定义 tween），以及 `AnimatedPadding`、`AnimatedPositioned`、`AnimatedAlign`、`AnimatedSwitcher`、`AnimatedDefaultTextStyle`；必须显式给出 `duration` 与 `curve`，必要时用 `onEnd` 回调。
  - 显式三件套：`AnimationController(duration: ..., vsync: this)` 驱动、`Tween<double>(begin: 0, end: 300).animate(_controller)` 插值、`CurvedAnimation(parent: _controller, curve: Curves.easeInOut)` 加曲线。
  - 重建策略：可复用组件用 `AnimatedWidget`（构造时传 `listenable`），复杂组件用 `AnimatedBuilder(animation: animation, builder: ..., child: child)`，把不随动画变化的子树通过 `child` 传进去以免重建。
  - 状态监听：`animation.addStatusListener` 处理 `AnimationStatus.completed` / `dismissed` 做往返播放；多属性动画把 tween 声明为 `static final` 并复用 `evaluate(animation)`。
  - 内置转场：`FadeTransition`、`ScaleTransition`、`SlideTransition`、`SizeTransition`、`RotationTransition`、`PositionedTransition`，优先复用而非自造。
  - Hero：两端 `Hero(tag: ...)` 必须使用同一 tag（常用数据对象本身），两端 widget 树保持相似；图片外包一层 `Material(color: Colors.transparent)` 获得「弹起」效果；圆角展开用 `ClipOval` + `ClipRect` 的 `RadialExpansion` 搭配 `MaterialRectCenterArcTween` 做中心点插值；需要时用 `HeroMode` 关闭。
  - 交错动画：所有子动画共用一个控制器，用 `CurvedAnimation(curve: Interval(0.0, 0.100, curve: Curves.ease))` 这类区间把每个属性错开；控制器总时长必须覆盖所有区间，例如把「初始延迟 + 交错步长 × 条目数 + 按钮延迟 + 按钮时长」相加得到总时长。
  - 物理动画：`_controller.fling(velocity: 2.0)`；`_controller.animateWith(SpringSimulation(...))` 配合 `SpringDescription(mass, stiffness, damping)`；可选 `BouncingScrollSimulation`、`ClampingScrollSimulation`、`GravitySimulation`。
  - 调试：用 `timeDilation` 放慢动画观察时序。
- **常见坑（反模式）**（源文件 `### DON'T` 与各节 Best Practices 点名）：
  1. 忘记 `dispose` 控制器，直接造成内存泄漏。
  2. 在动画监听里用 `setState()`，本可用 `AnimatedBuilder` / `AnimatedWidget` 精确重建。
  3. 假设动画瞬时完成、不处理 `AnimationStatus`，往返播放与收尾逻辑错乱。
  4. 过度动画：动效过多反而干扰用户，源文件明确要求克制。
  5. 使用不平滑曲线，动画出现「jerky」顿挫感。
  6. 忽略无障碍，不尊重系统的 `disableAnimations` 偏好。
  7. 嵌套隐式动画，带来额外性能开销。
  8. Hero 两端 tag 不一致或 widget 树差异过大，转场塌陷。
  9. 交错动画的控制器时长没有覆盖全部 `Interval`，后半段被截断。
  10. 只在模拟器上验收动画，实际设备上不流畅。
- **可执行检查清单**：
  - [ ] 用决策树确认动画类型，简单属性动画是否已优先用隐式组件。
  - [ ] 每个 `AnimationController` 都在 `dispose` 中释放。
  - [ ] 动画驱动重建走 `AnimatedBuilder` / `AnimatedWidget`，未用 `setState()`。
  - [ ] 所有动画都显式声明 `duration` 与 `curve`。
  - [ ] UI 反馈类动效时长在 300ms 以内。
  - [ ] Hero 两端 tag 一致，图片外包 `Material(color: Colors.transparent)`。
  - [ ] 控制器总时长覆盖全部 `Interval`。
  - [ ] 已处理 `disableAnimations` 无障碍偏好，并在目标真机上验证。
- **源文件核查发现（过时/矛盾）**：
  - Rule 第 5 条要求动画时长 300ms 以内，但正文示例出现 `Duration(seconds: 2)` 的控制器、1 秒的 `TweenAnimationBuilder`、以及 250ms / 500ms 的交错菜单动效；源文件没有说明「300ms 仅适用于 UI 反馈类」这一例外，规则与示例存在明显张力。
  - `## Resources` 声明了 `assets/templates/implicit_animation.dart`、`explicit_animation.dart`、`hero_transition.dart`、`staggered_animation.dart` 四个模板，但仓库中 `skills/tech/flutter-animations/` 下只有 `SKILL.md` 与 `references/` 的 6 个 markdown 文件，`assets/templates/` 目录不存在，模板引用全部失效。
  - `references/` 下的 `implicit.md`、`explicit.md`、`hero.md`、`staggered.md`、`physics.md`、`curves.md` 均存在，参考指引有效。
  - 示例使用 Flutter 内置具名颜色常量（如蓝、红），在项目内应改用主题变量，避免硬编码颜色。
- **上游维护提示**：正文与 references 保留英文；本要点为中文提炼。上游更新后需复核：动画时长规则与示例是否已对齐、`assets/templates/` 是否补齐、以及 `Curves` / `AnimationStatus` API 是否随 Flutter 版本调整。

---

## 3. `flutter-expert` — Flutter 跨端开发

- **源文件**：`skills/tech/flutter-expert/SKILL.md`
- **上游来源**：第三方上游（源 frontmatter `license: MIT`、`metadata.author: https://github.com/Jeffallan`、`version: "1.1.0"`、`domain: frontend`、`role: specialist`、`scope: implementation`、`output-format: code`、`related-skills: react-native-expert, test-master, fullstack-guardian`）；`skills/SKILL_MANIFEST.json` 记 source 为 `tech skill library`
- **用途**：定位为「高级移动工程师」，覆盖 Flutter 3 + Dart 的完整工程面：widget 组合与 `const` 优化、Riverpod / Bloc 状态管理、GoRouter 导航与深链、平台相关实现、widget 级测试与 DevTools 性能剖析。它给出五步核心工作流（Setup → State → Widgets → Test → Optimize），每一步都绑定验证命令与失败恢复路径，并通过 references 表按主题按需加载细节。
- **何时加载**：构建跨平台 Flutter 应用、实现 Riverpod 或 Bloc/Cubit 状态管理、用 GoRouter 搭路由与深链、写自定义 widget 与动画、优化 Flutter 性能、处理平台差异时加载。frontmatter 的 `triggers` 为 Flutter、Dart、widget、Riverpod、Bloc、GoRouter、cross-platform。
- **核心规则要点**（`## Rule` 五条 + `## Constraints` 两组）：
  1. widget 的 `build` 方法必须保持纯且快。
  2. 状态管理必须用 Provider/Riverpod/Bloc 之一，「选一种并保持一致」。
  3. 平台相关代码必须藏在抽象之后。
  4. 必须做 widget 级测试，不能只有单元测试。
  5. 尽可能处处使用 `const` 构造器。
  `### MUST DO`：尽可能用 `const` 构造器；列表必须实现正确的 keys；状态消费必须用 `Consumer` / `ConsumerWidget` 而非 `StatefulWidget`；遵循 Material/Cupertino 设计指南；用 DevTools 剖析并修掉 jank；用 `flutter_test` 测 widget。
  `### MUST NOT DO`：禁止在 `build()` 方法内部构建 widget；禁止直接改状态（必须创建新实例）；禁止用 `setState` 管理应用级状态；禁止在静态 widget 上漏掉 `const`；禁止忽略平台差异；禁止用重计算阻塞 UI 线程（必须用 `compute()`）。
- **关键做法**：
  - 五步工作流与验证点：1）Setup 用 `flutter pub get` 拉依赖并配好路由；2）State 定义 Riverpod provider 或 Bloc/Cubit，用 `flutter analyze` 验证，报告问题必须修完再审；3）Widgets 构建可复用、`const` 优化的组件，每个功能后跑 `flutter test`，失败就用 Flutter DevTools 查 widget 树；4）Test 写 widget 与集成测试，用 `flutter test --coverage` 确认，覆盖率下降就补针对性用例；5）Optimize 用 `flutter run --profile` 配合 DevTools 剖析，检查 Performance overlay 的重建次数，隔离昂贵的 `build()`，加 `const` 或把状态移近消费方。
  - Riverpod 正确写法：`StateNotifierProvider<CounterNotifier, int>` 定义 provider，`CounterNotifier extends StateNotifier<int>`，`increment()` 里 `state = state + 1`（新实例，绝不原地改）；消费端用 `class CounterView extends ConsumerWidget` + `ref.watch(counterProvider)`；写操作用 `ref.read(counterProvider.notifier).increment()`。
  - 反例对照：应用级状态放 `setState` 会导致整棵子树重建；正确做法是局部化的 Riverpod consumer。
  - 按需加载 references：`references/riverpod-state.md`（状态管理、provider、notifier）、`references/bloc-state.md`（Bloc、Cubit、事件驱动、复杂业务逻辑）、`references/gorouter-navigation.md`（导航、路由、深链）、`references/widget-patterns.md`（UI 组件与 `const` 优化）、`references/project-structure.md`（项目架构）、`references/performance.md`（优化、剖析、jank 修复）。这 6 个文件在仓库中均存在。
  - 故障恢复表：`flutter analyze` 报错 → 修被标记的行，缺 import 时先 `flutter pub get`；widget 测试断言失败 → 状态变更后用 `tester.pumpAndSettle()`，核对 finder 选择器；加包后构建失败 → `flutter pub upgrade --major-versions` 并查 pub.dev 兼容性；jank / 掉帧 → `RepaintBoundary`、把重活移到 `compute()`、补 `const`；热重载不生效 → 用 hot restart（终端按 `R`）重置全应用状态。
  - 交付模板：widget 代码（含正确 `const`）、Provider/Bloc 定义、按需的路由配置、测试文件结构，四件一起给。
- **常见坑（反模式）**（源文件 `### MUST NOT DO` 与故障表点名）：
  1. 用 `setState` 管应用级状态，触发整棵子树重建。
  2. 在 `build()` 方法内部构建 widget。
  3. 直接修改状态对象而不是创建新实例。
  4. 静态 widget 漏写 `const`，额外重建。
  5. 在 `build` 或 UI 线程做重计算，不用 `compute()`。
  6. 列表缺 keys，滚动与增删时状态错位。
  7. 忽略平台特定行为差异。
  8. widget 测试异步状态未落定就断言，未用 `pumpAndSettle()`。
  9. 出现 jank 时不看重建次数、不隔离昂贵 `build()` 就盲调。
  10. 依赖包版本冲突时硬改 `pubspec.yaml` 而不走 `flutter pub upgrade --major-versions`。
- **可执行检查清单**：
  - [ ] `flutter analyze` 零告警后再进入下一步。
  - [ ] 状态管理只选一种方案，未混用 Riverpod 与 Bloc。
  - [ ] 状态消费走 `ConsumerWidget` / `Consumer`，未用 `StatefulWidget`。
  - [ ] 能加 `const` 的构造器都加了；列表都有 keys。
  - [ ] 每个功能后跑过 `flutter test`，并用 `--coverage` 确认覆盖率未下降。
  - [ ] 用 `flutter run --profile` + DevTools 检查过重建次数，重活已移到 `compute()`。
  - [ ] 平台差异代码藏在抽象之后。
  - [ ] 交付包含 widget、状态定义、路由配置与测试文件结构。
- **源文件核查发现（过时/矛盾）**：
  - 唯一的状态管理代码示例使用 `StateNotifierProvider` 与 `StateNotifier`，这在新版 Riverpod 中已是旧写法（官方推荐迁移到 `NotifierProvider` / `Notifier`），而 `references/riverpod-state.md` 是唯一的 Riverpod 细节来源，示例与参考可能存在版本口径差异。
  - 描述写「Flutter 3+ / Dart」，但 `const CounterView({super.key})`、`required this.child` 等写法属较新的 Dart 空安全与 super 参数语法，源文件未标注最低 Flutter / Dart 版本。
  - frontmatter 声明了 `related-skills: react-native-expert, test-master, fullstack-guardian`，这三个名字都不在本仓库 49 个正式 Skill 名单内，跨 Skill 引用无法解析。
  - 故障表里的 `flutter pub upgrade --major-versions` 是真实存在的子命令，但会一次跨大版本升级全部依赖，源文件未提示它带来的破坏性影响与回滚方式。
- **上游维护提示**：正文与 references 保留英文；本要点为中文提炼。上游更新后需复核：Riverpod 示例是否已迁到 `NotifierProvider`、最低 Flutter / Dart 版本声明、以及 `related-skills` 是否对齐本仓库 Skill 名单。

---

## 4. `java-performance-governance` — Java 性能与内存治理

- **源文件**：`skills/tech/java-performance-governance/SKILL.md`
- **上游来源**：仓库内自研提炼，frontmatter 无第三方作者；`skills/SKILL_MANIFEST.json` 记 source 为 `GERP batch-operation and memory-leak governance extraction`
- **用途**：把 Java 后端的可预测劣化模式变成一套诊断与修复手册。源文件开篇就点明问题集：无界缓存、缺失的 `finally` 清理、每请求日志与正则重写、超大线程池、逐行批处理。它把「集合式批处理」与「内存泄漏治理」的经验通用化，要求先拿证据定位根因再改代码，明确反对用重启或加大堆来掩盖泄漏。它属于治理型 Skill：既管修复动作，也管「不许怎么修」。
- **何时加载**：诊断变慢的批删/批改/批审、内存增长或 OOM、超时、连接池耗尽时；评审性能敏感的 Spring / MyBatis 代码、准备新增缓存或线程/异步配置之前；做内存泄漏排查、批处理 SQL 重构、索引规划与可观测性建设时。
- **核心规则要点**（`## Rule` 六条，全部为强制约束）：
  1. 禁止静默降级：改代码前必须用证据（profile、日志、指标）定位根因；禁止用重启或加堆来掩盖泄漏。
  2. 批处理必须是集合式的：一次有界 SQL 能做完的事，禁止循环单行删除/更新。
  3. 每个跨请求获取的资源都必须在 `finally` 中释放（thread-local、schema/租户上下文、流、连接）。
  4. 缓存必须有界且可淘汰：无界的 `ConcurrentMapCacheManager` 或只增不减的 map 会泄漏内存。
  5. 查询必须有索引背书：接受慢查询前先跑 EXPLAIN / 看执行计划；循环里禁止 N+1。
  6. 可观测性优先：结构化日志、请求 ID、连接池与缓存指标要在优化之前就位。
  源文件未单列 `## Constraints` / `## MUST DO` 小节；强制项集中在 `## Rule` 与 `## Guardrails`。
- **关键做法**：
  - 五步工作流：1）抓基线——堆、缓存、连接池、线程指标与出问题操作的延迟；2）复现并剖析——定位到具体根因（无界缓存 / 缺 finally / N+1 / 缺索引）；3）修根因——给缓存加边界，补 `finally` 清理，改集合式 SQL，加索引，给线程池定界；4）用新鲜证据验证——前后延迟对比、内存趋势、执行计划、池使用率；5）记录模式——同一根因复发就沉淀到可复用检查清单或 Skill。
  - 常见根因对照（`## Common Root Causes`，6 行表）：无界缓存（`ConcurrentMapCacheManager` / 只增 map）→ 堆稳步上涨 → 限大小 + TTL/淘汰；缺 `finally` 清理（thread-local / 租户 / schema 上下文）→ 跨请求串数据 → 一律在 `finally` 释放；每请求 DB 日志与 SQL 正则重写 → CPU 高、请求慢 → 降到 debug 级别并预编译；超大异步池或无界队列 → 线程耗尽 → 池 + 队列定界并设拒绝策略；逐行批删批改 → 线性超时 → 集合式 SQL + 索引 + 分页批处理；N+1 查询或缺索引 → 列表变慢 → EXPLAIN、加索引、批量取数。
  - `## Guardrails` 四条硬禁止：禁止靠加大堆或重启服务来「修」内存泄漏；禁止在集合式语句可用时逐行删除/更新；禁止在没有 EXPLAIN 基线时加索引，禁止在没有边界与淘汰策略时加缓存；优化必须由证据驱动，记录前后数字而不是凭感觉。
- **常见坑（反模式）**（源文件根因表与 Guardrails 点名）：
  1. 用重启服务或调大堆参数掩盖内存泄漏，问题周期性复发。
  2. 使用无界缓存或只增不减的 map，堆持续上涨直至 OOM。
  3. thread-local、租户上下文、schema 上下文未在 `finally` 释放，造成跨请求数据串味（拿到别的租户的数据）。
  4. 每次请求都打 DB 日志、每次都做 SQL 正则重写，CPU 被吃满。
  5. 异步线程池超大且队列无界，压力下线程耗尽且没有拒绝策略。
  6. 循环里逐行删除/更新，耗时随数据量线性增长直至超时。
  7. 循环内触发 N+1 查询，或缺少支撑索引。
  8. 没有 EXPLAIN 基线就加索引、没有淘汰策略就加缓存。
  9. 只凭感觉宣称「优化了」，不记录前后延迟、内存趋势、执行计划与池使用率。
- **可执行检查清单**：
  - [ ] 已抓取堆、缓存、连接池、线程与目标操作的延迟基线。
  - [ ] 已用 profile / 日志 / 指标把根因定位到具体一项，而非笼统「慢」。
  - [ ] 每处跨请求资源获取都有对应的 `finally` 释放。
  - [ ] 缓存均已声明大小上限与 TTL/淘汰策略。
  - [ ] 批量写/删已改为集合式有界 SQL，必要时分页。
  - [ ] 慢查询已跑 EXPLAIN 并确认走索引，无 N+1。
  - [ ] 异步池与队列有界，并配置了拒绝策略。
  - [ ] 优化前后数字已记录，并沉淀为可复用清单。
- **源文件核查发现（过时/矛盾）**：源文件仅 49 行，未单列 `## Common 坑`（只给根因表）、无 `references/` 目录、无代码示例，EXPLAIN 也只给动词未给命令模板，落地时需要自行补 SQL 形式。文本未标注 Spring Boot / JDK 版本；`ConcurrentMapCacheManager` 属 Spring Framework 通用缓存抽象，源文件未提示在需要淘汰策略时应换成带界与 TTL 能力的 CacheManager 实现（如 Caffeine 系）。此外 `## Rule` 与 `## Guardrails` 有语义重叠（「不得用重启掩盖泄漏」在两边各出现一次），维护时应当合并口径以免改动时漏改一处。
- **上游维护提示**：正文与 references 保留英文；本要点为中文提炼。上游更新后需复核：Rule 与 Guardrails 的重复项是否已合并、是否补充 EXPLAIN 命令示例，以及缓存实现口径是否随 Spring 版本切换。

---

## 5. `java-springboot` — Spring Boot 工程实践

- **源文件**：`skills/tech/java-springboot/SKILL.md`
- **上游来源**：仓库内自研提炼，frontmatter 无第三方作者与版本字段；`skills/SKILL_MANIFEST.json` 记 source 为 `tech skill library`
- **用途**：给 Spring Boot 应用定一套一致的工程规范，覆盖九个面：项目结构与打包、依赖注入与组件、配置管理、Web 层控制器、Service 层、数据层仓储、日志、测试与安全。核心诉求是「结构一致、依赖显式、可测可维护」：构造器注入取代字段注入、配置外部化、DTO 隔离实体、全局异常处理、测试切片而非全上下文启动。
- **何时加载**：构建、评审、重构或排障 Spring Boot 应用时加载，具体包括 Java 后端项目、REST 控制器、服务、仓储、参数校验、事务、配置、日志、测试与项目结构相关任务。触发条件取自 frontmatter description，源文件未单列 `## When to Use` 小节。
- **核心规则要点**（`## Rule` 五条 + 各节硬性要求）：
  1. 必须用构造器注入（Constructor injection over field injection）。
  2. 必须通过 `application.yml` 外部化配置。
  3. 必须使用 `@RestController` + `@RequestMapping` 模式。
  4. 必须用 `@ControllerAdvice` 做全局异常处理。
  5. 测试必须用测试切片（`@WebMvcTest`、`@DataJpaTest`），而不是每次都起完整上下文。
  其余强制项：依赖字段声明为 `private final`；按功能/领域分包（如 `com.example.app.order`、`com.example.app.user`）而不是按层分包（`com.example.app.controller`、`com.example.app.service`）；用 `@ConfigurationProperties` 做类型安全绑定；用 Spring Profiles（`application-dev.yml`、`application-prod.yml`）区分环境；禁止硬编码密钥，必须用环境变量或专用密钥管理工具（HashiCorp Vault、AWS Secrets Manager）；禁止把 JPA 实体直接暴露给客户端，必须用 DTO；用 Java Bean Validation 的 `@Valid`、`@NotNull`、`@Size` 校验请求体；业务逻辑全部放进 `@Service`；Service 必须无状态；`@Transactional` 加在 Service 方法上，且「加在必要的最细粒度」；密码必须用强哈希（BCrypt）编码。
- **关键做法**：
  - 项目结构：Maven（`pom.xml`）或 Gradle（`build.gradle`）管理依赖；用 Spring Boot starters（`spring-boot-starter-web`、`spring-boot-starter-data-jpa`）简化依赖。
  - Web 层：RESTful 端点设计一致；DTO 进 DTO 出；`@ControllerAdvice` + `@ExceptionHandler` 保证错误响应一致。
  - 数据层：仓储继承 `JpaRepository` 或 `CrudRepository`；复杂查询用 `@Query` 或 JPA Criteria API；用 DTO projection 只取必要字段。
  - 日志：用 SLF4J；Logger 声明固定为 `private static final Logger logger = LoggerFactory.getLogger(MyClass.class);`；必须用参数化消息 `logger.info("Processing user {}...", userId);` 而非字符串拼接，以改善性能。
  - 测试：Service 与组件用 JUnit 5 + Mockito 写单元测试；跨上下文用 `@SpringBootTest`；控制器用 `@WebMvcTest`、仓储用 `@DataJpaTest` 做隔离；可靠集成测试可以考虑 Testcontainers 接真实数据库与消息中间件。
  - 安全：用 Spring Security 做认证与授权；密码用 BCrypt；用 Spring Data JPA 或参数化查询防 SQL 注入，用正确输出编码防 XSS。
- **常见坑（反模式）**（源文件以正向规则反推点名的禁止项）：
  1. 用字段注入（`@Autowired` 打在字段上），依赖不显式、难测。
  2. 按层分包（controller / service / repository 各一个大包），领域内聚性差。
  3. 把 JPA 实体直接返回给客户端，暴露持久化结构并引发懒加载与序列化问题。
  4. 硬编码密钥或把密钥写进配置文件。
  5. Service 持有可变状态，破坏单例语义。
  6. `@Transactional` 加得过粗（整类或过大方法），事务范围超出必要。
  7. 用字符串拼接打日志，既有性能开销又易注入。
  8. 所有测试都用 `@SpringBootTest` 起完整上下文，测试慢且脆。
  9. 明文存储密码或使用弱哈希。
- **可执行检查清单**：
  - [ ] 所有必需依赖走构造器注入，字段为 `private final`。
  - [ ] 包结构按功能/领域划分，而非按层划分。
  - [ ] 配置放在 `application.yml`，敏感项走环境变量或密钥管理工具。
  - [ ] 用 `@ConfigurationProperties` 做类型安全绑定，环境差异用 Profiles。
  - [ ] API 出入口都是 DTO，实体不出仓储层。
  - [ ] 请求体有 `@Valid` + `@NotNull` / `@Size` 校验，异常由 `@ControllerAdvice` 统一映射。
  - [ ] `@Transactional` 只加在必要的最细粒度 Service 方法上，且 Service 无状态。
  - [ ] 控制器/仓储测试使用 `@WebMvcTest` / `@DataJpaTest` 切片；日志使用 SLF4J 参数化写法；密码用 BCrypt 编码。
- **源文件核查发现（过时/矛盾）**：源文件把 Bean Validation 写作 `JSR 380`，这是 Java EE 8 时代的规范编号；Spring Boot 3 已迁移到 `jakarta.validation`（Jakarta Bean Validation 3.x），照抄 `JSR 380` 与 `javax.*` 口径会在 Spring Boot 3 项目里选错依赖坐标。全文未标注 Spring Boot / JDK 版本，示例与命名空间也都是版本无关写法，使用时需要按项目实际版本对齐。源文件未单列 `## Constraints`、`## Guardrails`、`## Common Pitfalls` 与 `## References` 小节，约束分散在各正向小节中，缺少反面清单与代码示例。
- **上游维护提示**：正文与 references 保留英文；本要点为中文提炼。上游更新后需复核：Bean Validation 规范编号与 `jakarta.*` 命名空间、测试切片注解是否随 Spring Boot 大版本调整，以及是否补齐密钥管理与事务边界的反例。

---

## 6. `javascript-typescript-jest` — Jest 测试实践

- **源文件**：`skills/tech/javascript-typescript-jest/SKILL.md`
- **上游来源**：仓库内自研提炼，frontmatter 无第三方作者与版本字段；`skills/SKILL_MANIFEST.json` 记 source 为 `tech skill library`
- **用途**：让 JS/TS 的 Jest 测试聚焦、可维护，并且「验证行为而不是实现对实现细节过拟合」。源文件给出五步工作流（定位行为 → 选最窄可靠测试类型 → 只 mock 外部边界 → 断言可观察结果 → 跑测试并修第一个失败断言），随后分五小节展开测试结构、Mock 策略、异步代码、快照测试、React 组件测试，最后附常用 matcher 清单与三条防护规则。
- **何时加载**：为 JS/TS 代码、React 组件、异步代码或被 mock 依赖新增、评审、调试、重构 Jest 测试时加载；触发条件覆盖「测试结构、Mock 策略与常见模式」。源文件未单列 `## When to Use` 小节，触发条件取自 frontmatter description。
- **核心规则要点**（`## Rule` 五条）：
  1. 一个模块一个 `describe`，一个行为一个 `it`。
  2. 必须 mock 外部依赖，禁止 mock 被测单元本身。
  3. 异步测试必须返回 promise 或使用 async/await。
  4. 业务逻辑的分支覆盖率最低 80%。
  5. 测试名必须描述行为，而不是描述实现。
  其余强制项来自 `## Guardrails`：禁止在可断言公开行为时去断言私有实现细节；禁止让 mock 在测试之间共享而不 reset 或 cleanup；应当优先确定性测试，而不是 sleep、真实网络调用或依赖时钟的断言。文件命名必须用 `.test.ts` 或 `.test.js` 后缀，测试文件放在被测代码旁边或专用 `__tests__` 目录，结构统一为 `describe('Component/Function/Class', () => { it('should do something', () => {}) })`。
- **关键做法**：
  - Mock 分层：模块级用 `jest.mock()`，单个函数用 `jest.spyOn()`；用 `mockImplementation()` 或 `mockReturnValue()` 定义 mock 行为；在 `afterEach` 里用 `jest.resetAllMocks()` 复位。
  - 异步：必须 return promise 或 async/await；用 `resolves` / `rejects` matcher 断言 Promise；慢测试用 `jest.setTimeout()` 调整超时。
  - 快照：只用于变化不频繁的 UI 组件或复杂对象；快照必须保持小而聚焦；提交前必须仔细审阅快照变更。
  - React 组件：用 React Testing Library 而不是 Enzyme；测用户行为与可访问性；按可访问性 role、label 或文本内容查询元素；用 `userEvent` 而不是 `fireEvent`，交互更接近真实用户。
  - matcher 速查：相等用 `toBe` / `toEqual`；真假用 `toBeTruthy` / `toBeFalsy`；数值用 `toBeGreaterThan` / `toBeLessThanOrEqual`；字符串用 `toMatch(/pattern/)` / `toContain('substring')`；数组用 `toContain(item)` / `toHaveLength(3)`；对象用 `toHaveProperty('key', value)`；异常用 `toThrow()` / `toThrow(Error)`；mock 用 `toHaveBeenCalled()` / `toHaveBeenCalledWith(arg1, arg2)`。
- **常见坑（反模式）**（源文件 Rule 与 Guardrails 点名）：
  1. mock 被测单元本身，测试退化为自我验证。
  2. 测试名描述实现细节（如方法名、内部调用顺序），重构即失效。
  3. 异步测试既不 return promise 也不用 async/await，断言在 Promise 落定前执行。
  4. 跨测试共享 mock 且不 reset 或 cleanup，出现顺序依赖的偶发失败。
  5. 断言私有实现细节，而公开行为未被覆盖。
  6. 用 sleep、真实网络调用或依赖系统时钟制造不确定性。
  7. 快照体积过大、提交前不审快照变更，把回归当成「正常更新」提交。
  8. 用 Enzyme 或 `fireEvent` 替代 React Testing Library / `userEvent`。
  9. 业务逻辑分支覆盖率低于 80% 就宣称完成。
- **可执行检查清单**：
  - [ ] 测试文件名符合 `.test.ts` / `.test.js`，位置符合邻近或 `__tests__` 约定。
  - [ ] 一个模块一个 `describe`，一个行为一个 `it`，名称描述行为。
  - [ ] 只 mock 网络、存储、定时器或昂贵依赖等外部边界。
  - [ ] 每个 `afterEach` 都做了 mock 复位或清理。
  - [ ] 异步用例 return promise 或使用 async/await，并优先用 `resolves` / `rejects`。
  - [ ] 快照小而聚焦，且提交前已人工审阅差异。
  - [ ] React 组件测试用 React Testing Library + `userEvent`，按可访问性 role/label 查询。
  - [ ] 业务逻辑分支覆盖率不低于 80%，未使用 sleep 或真实网络。
- **源文件核查发现（过时/矛盾）**：
  - `## Effective Mocking` 建议在 `afterEach` 里统一用 `jest.resetAllMocks()`。该 API 会连 `mockReturnValue` / `mockImplementation` 一起清掉，模块级 mock 的返回值会在下一个用例中丢失；源文件未区分 `jest.clearAllMocks()`（只清调用记录）、`jest.resetAllMocks()`（再清实现）与 `jest.restoreAllMocks()`（还原被 spy 的原函数）三者语义，照抄容易造成难以定位的失败。
  - 「Use React Testing Library over Enzyme」属历史口径：Enzyme 在 React 17 之后已无官方维护适配器，本条对比对现代 React 18+ 项目已无选型意义。
  - 源文件未标注 Jest 主版本、`testEnvironment` 配置与 ESM/`transform` 口径，而 `jest.mock()` 在 ESM 下的行为与 CJS 差异较大。
  - 源文件未单列 `## Constraints` / `## MUST DO` / `## MUST NOT DO` 小节，强制项集中在 `## Rule` 与 `## Guardrails`，缺少代码示例与 `references/` 目录。
- **上游维护提示**：正文与 references 保留英文；本要点为中文提炼。上游更新后需复核：mock 复位 API 的推荐用法（clear / reset / restore 的选择）、Enzyme 对比条目是否删除、以及 Jest 版本与 ESM 配置口径是否补齐。

---

## 7. `multi-stage-dockerfile` — 多阶段 Dockerfile 优化

- **源文件**：`skills/tech/multi-stage-dockerfile/SKILL.md`
- **上游来源**：仓库内自研提炼，frontmatter 无第三方作者与版本字段；`skills/SKILL_MANIFEST.json` 记 source 为 `tech skill library`
- **用途**：专注「把任意语言或框架的应用打成生产级最小镜像」这一件事：用 builder 阶段做编译与依赖安装、用独立 runtime 阶段只放运行必需物，再通过基础镜像选型、层缓存排序、`.dockerignore` 与安全加固，产出更小、更易扫描的镜像。与 `docker-expert` 的分工是：本 Skill 只管 Dockerfile 本身，一旦涉及 Compose 编排、容器运行时安全策略或构建故障诊断，就升级到 `docker-expert`。
- **何时加载**：容器化任意语言或框架的应用、需要压缩镜像体积、分离构建依赖与运行依赖、改善构建缓存行为、加固生产镜像时加载。触发条件取自 frontmatter description，源文件未单列 `## When to Use` 小节。
- **核心规则要点**（`## Rule` 五条）：
  1. 必须分阶段：builder 阶段负责编译，runtime 阶段只负责执行。
  2. 只能用 `COPY --from=builder` 拷运行产物。
  3. runtime 阶段必须用 distroless 或 slim 基础镜像。
  4. 层缓存策略：必须先拷依赖文件再拷源码。
  5. 镜像必须在部署前通过安全扫描。
  正文 `## Multi-Stage Structure` 补充：阶段必须用 `AS` 关键字取有意义的名字（如 `FROM node:18 AS builder`），并按「依赖 → 构建 → 测试 → 运行」的逻辑顺序排列。`## Base Images` 要求从官方最小基础镜像起步、指定精确版本标签以保证可复现（如 `python:3.11-slim` 而非 `python`）、runtime 阶段可用 distroless、兼容时用 Alpine 换取更小体积、运行镜像只保留最小必要依赖。`## Layer Optimization` 要求把高频变更的指令排在低频变更之后、用 `.dockerignore` 收窄构建上下文、用 `&&` 合并相关 `RUN` 减少层数、用 `COPY --chown` 一步设好权限。`## Security Practices` 要求禁止以 root 运行（用 `USER`）、从最终镜像移除构建工具与多余包、扫描漏洞、设置受限文件权限、用多阶段构建避免构建密钥进入最终镜像。`## Performance Considerations` 要求用 build arguments 承载环境间会变的配置、按「最不常变 → 最常变」排序利用缓存、可行时并行化构建步骤、设置 `NODE_ENV=production` 这类运行时环境变量、用 `HEALTHCHECK` 提供适配应用类型的健康检查。
- **关键做法**：
  - 阶段命名与顺序：`dependencies → build → test → runtime`，每阶段用 `AS` 命名，runtime 只从 builder 拷产物。
  - 基础镜像：官方最小镜像起步，精确版本标签，runtime 侧 distroless 或 slim，兼容时 Alpine。
  - 层缓存：先 `COPY` 依赖清单再装依赖，最后 `COPY` 源码；相关 `RUN` 用 `&&` 合并；用 `COPY --chown` 一次设权限。
  - 缓存与体积：`.dockerignore` 收窄上下文，构建工具与包管理器缓存必须留在 builder 阶段，不进 runtime。
  - 安全：`USER` 切换非 root；扫描最终镜像；最小化安装包；构建密钥留在 builder 阶段。
  - 性能：`ARG` 承载环境差异；层按变更频率排序；可行时并行；设运行时环境变量；加 `HEALTHCHECK`。
- **常见坑（反模式）**（源文件以正向规则反推点名的禁止项）：
  1. 单一阶段构建，编译工具链与源码全部留进生产镜像，体积膨胀。
  2. builder 与 runtime 不分，或 runtime 里再装一次依赖。
  3. 基础镜像用浮动标签（如只写 `python`），构建不可复现。
  4. 先 `COPY . .` 再装依赖，任何源码改动都击穿依赖层缓存。
  5. 无 `.dockerignore`，构建上下文夹带无关文件甚至敏感文件。
  6. 以 root 运行，且从最终镜像删除构建工具这一步被省略。
  7. 把构建期密钥写在阶段里并留在最终镜像。
  8. 缺少安全扫描步骤却宣布可部署；缺少 `HEALTHCHECK`。
  9. `RUN` 命令分散成多层，既增加层数又无法在一次层内清理缓存。
- **可执行检查清单**：
  - [ ] builder 与 runtime 阶段分离，且各阶段用 `AS` 命名。
  - [ ] 只通过 `COPY --from=builder` 拷运行产物，运行镜像无构建工具。
  - [ ] runtime 基础镜像为 distroless 或 slim，并指定精确版本标签。
  - [ ] 依赖清单先于源码 `COPY`，层按「最不常变 → 最常变」排列。
  - [ ] `.dockerignore` 已就位，构建上下文无冗余文件。
  - [ ] 相关 `RUN` 用 `&&` 合并，缓存清理与安装在同一层。
  - [ ] 存在 `USER` 非 root、受限文件权限与漏洞扫描步骤。
  - [ ] 已设置运行时环境变量与 `HEALTHCHECK`。
- **源文件核查发现（过时/矛盾）**：
  - 示例 `FROM node:18 AS builder` 指向已到生命周期的 Node 18 线；`python:3.11-slim` 虽仍受安全支持但非当前主线版本。
  - Rule 第 5 条要求「镜像必须在部署前通过安全扫描」，但全文没有给出任何扫描命令（对比 `docker-expert` 给了 `docker scout quickview`），规则缺少可执行落点。
  - `## Performance Considerations` 写「Set appropriate environment variables like NODE_ENV=production」，这是 shell 赋值写法；在 Dockerfile 中必须写成 `ENV NODE_ENV=production`（或 `ARG` + `ENV`），照抄会变成无效指令或构建错误。
  - 文中要求「用适当的 healthcheck」，但未给 `HEALTHCHECK` 的参数示例（`--interval`、`--timeout`、`--start-period`、`--retries`），落地时仍需回查 `docker-expert`。
  - 源文件未单列 `## Constraints` / `## MUST DO` / `## MUST NOT DO` 与 `## References` 小节，也无 `references/` 目录。
- **上游维护提示**：正文与 references 保留英文；本要点为中文提炼。上游更新后需复核：示例基础镜像版本线、是否补上扫描命令与 `HEALTHCHECK` 参数示例、以及 `NODE_ENV` 的 Dockerfile 正确写法。

---

## 8. `mysql-best-practices` — MySQL 最佳实践

- **源文件**：`skills/tech/mysql-best-practices/SKILL.md`
- **上游来源**：仓库内自研提炼，frontmatter 无第三方作者与版本字段；`skills/SKILL_MANIFEST.json` 记 source 为 `tech skill library`
- **用途**：让 MySQL 的模式与查询工作「正确、耐久、高性能、可恢复」。覆盖面最广：存储引擎选型与数据类型、主键策略、索引类型与索引指南、EXPLAIN 分析与分页写法、JSON 支持与生成列、事务与隔离级别、读写分离与复制延迟、权限与 SSL 加固、日常维护与监控查询、`my.cnf` 推荐配置。工作流强制「先核实现状再改 SQL」，并要求迁移、回滚、种子数据三者分开保存。
- **何时加载**：创建或评审 MySQL 模式、编写复杂 SQL、新增索引、执行迁移、修数据一致性问题、做性能计划时加载。源文件未单列 `## When to Use` 小节，触发条件取自 frontmatter description。
- **核心规则要点**（`## Rule` 六条）：
  1. 每张表都必须有主键。
  2. 必须为外键列与 WHERE 条件列建索引。
  3. 查询上线前必须先用 `EXPLAIN`。
  4. 多条语句的变更必须放进事务。
  5. 迁移必须版本化且可回滚。
  6. 生产代码禁止 `SELECT *`。
  `## Workflow` 五步：先核实当前表结构、索引、行数与约束再改 SQL；按访问模式决定数据类型、键、索引与事务边界；重要查询用 `EXPLAIN` 或等价证据验证；迁移、回滚与种子数据分离；记录模式变更证据供评审。
- **关键做法**：
  - 存储引擎：默认 InnoDB（ACID、行级锁）；MyISAM 只在读多且无事务需求时考虑；MEMORY 用于高速临时表。建表示例统一 `ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci`。
  - 数据类型：够用即可的最小类型；能用 `INT UNSIGNED` 就不用 `BIGINT`；金额必须用 `DECIMAL` 而不是 `FLOAT`/`DOUBLE`；固定取值集合用 `ENUM`；变长用 `VARCHAR`、定长用 `CHAR`；必须始终用 `utf8mb4` 以支持完整 Unicode。
  - 主键：InnoDB 用自增整数主键；分布式系统可考虑用 `BINARY(16)` 存 UUID（写入 `UUID_TO_BIN(UUID())`，查询 `UUID_TO_BIN('...')`）；尽量避免复合主键。
  - 索引：多数查询用 B-tree（默认），文本搜索用 `FULLTEXT`，地理数据用 `SPATIAL`，高频查询考虑覆盖索引；复合索引把选择性最高的列放最前；避免单独索引低基数列；必须监控并清理无用索引；`WHERE`、`JOIN`、`ORDER BY`、`GROUP BY` 用到的列都要评估建索引；可用 `information_schema.STATISTICS` 查索引基数。
  - 查询优化：用 `EXPLAIN FORMAT=JSON` 看执行计划，重点看 `type: ALL` 的全表扫描、索引是否被用上、扫描行数与返回行数的差距；分页用 `LIMIT`，大偏移必须改用 keyset 分页（`WHERE (order_date, order_id) < (?, ?)` 配合降序 `ORDER BY` 与 `LIMIT`）；能用 `JOIN` 就别用子查询；重复查询用 prepared statement。
  - JSON：MySQL 5.7+ 用 `JSON` 类型存半结构化数据；为高频访问的 JSON 字段建生成列（`user_id INT UNSIGNED AS (payload->>'$.user_id') STORED`）再建索引；查询用 `JSON_EXTRACT` 或 `->` / `->>` 运算符。
  - 事务：InnoDB 才能事务；事务要短以减少锁竞争；选合适隔离级别（示例 `SET TRANSACTION ISOLATION LEVEL READ COMMITTED`）；优雅处理死锁。
  - 复制与高可用：读查询走副本；连接池配合读写分离；必须监控复制延迟。安全：强密码 + SSL/TLS、最小权限、prepared statement 防注入、审计敏感操作（示例用 `GRANT SELECT, INSERT, UPDATE, DELETE` 与 `ALTER USER ... REQUIRE SSL`）。
  - 维护与监控：`ANALYZE TABLE` 更新优化器统计、`OPTIMIZE TABLE` 回收空间、`CHECK TABLE` 校验完整性；查慢查询、`SHOW FULL PROCESSLIST`、`SHOW ENGINE INNODB STATUS`、按 `information_schema.TABLES` 看表大小。
- **常见坑（反模式）**（源文件 `### Avoiding Common Pitfalls` 与各节点名）：
  1. 在索引列上套函数：`WHERE YEAR(order_date) = 2024`，必须改成范围比较 `order_date >= '2024-01-01' AND order_date < '2025-01-01'`。
  2. 隐式类型转换：`WHERE user_id = '123'`（列为 INT），必须写成 `WHERE user_id = 123`。
  3. 前导通配符模糊匹配 `LIKE '%phone%'` 无法走索引，文本匹配应改用 `MATCH ... AGAINST` 全文检索。
  4. 生产代码用 `SELECT *`。
  5. 用 `FLOAT`/`DOUBLE` 存金额，精度丢失。
  6. 大偏移分页（`LIMIT 20 OFFSET 0` 数值很大时），应用 keyset 分页替代。
  7. 事务过长导致锁竞争，或不处理死锁。
  8. 单独索引低基数列、长期不清理无用索引。
  9. 未跑 `EXPLAIN` 就把查询上线。
  10. 无必要地使用复合主键。
- **可执行检查清单**：
  - [ ] 每张表都有主键，且 InnoDB 用自增整数主键。
  - [ ] 所有外键列与 `WHERE` / `JOIN` / `ORDER BY` / `GROUP BY` 列都有索引评估记录。
  - [ ] 复合索引把选择性最高的列放最前，无单独的低基数索引。
  - [ ] 关键查询都用 `EXPLAIN`（或 `EXPLAIN FORMAT=JSON`）确认无全表扫描。
  - [ ] 金额字段为 `DECIMAL`，字符集为 `utf8mb4`。
  - [ ] 多条语句的变更包在事务内，事务尽量短并处理死锁。
  - [ ] 迁移已版本化、可回滚，且与种子数据分离。
  - [ ] 无 `SELECT *`、无索引列函数、无隐式类型转换、无前导通配符。
- **源文件核查发现（过时/矛盾）**：
  - 复制状态查询 `SHOW SLAVE STATUS\G` 在 MySQL 8.0.22+ 已弃用，现行写法为 `SHOW REPLICA STATUS`；`SLAVE` 术语整体已被 `REPLICA` 取代，同一节里新旧两套口径并存。
  - 配置块列出 `query_cache_type = 0`，注释自身也写明「disabled in MySQL 8.0+」；query cache 在 MySQL 8.0 已被移除（5.7 即弃用），把它列为推荐配置与 `## Core Principles` 里「Implement connection pooling and query caching appropriately」相互矛盾。
  - `innodb_log_file_size = 256M` 在 MySQL 8.0.30+ 已被 `innodb_redo_log_capacity` 取代，属弃用参数。
  - `innodb_buffer_pool_size = 70%_of_RAM` 不是合法取值语法（该参数取字节值），照抄会启动失败；这是占位说明而非可粘贴配置。
  - 建表示例使用 `TINYINT(1)`：整数类型的显示宽度在 MySQL 8.0.17+ 已弃用。
  - `SELECT * FROM mysql.slow_log` 只有在 `log_output` 包含 `TABLE` 时才存在该表，源文件未提示这一前提。
  - 索引检查与表大小查询里的 `table_schema = 'your_database'` 是占位字符串，直接执行会返回空结果。
  - `ALTER TABLE products ADD FULLTEXT INDEX ...` 与 `MATCH ... AGAINST` 用法正确，但全文未标注所依据的 MySQL 版本，配置段与语法段跨越了 5.7 与 8.0 两代口径。
- **上游维护提示**：正文与 references 保留英文；本要点为中文提炼。上游更新后需复核：复制状态命令、`innodb_log_file_size` 与 `innodb_redo_log_capacity` 的取舍、query cache 条目是否删除、以及整数显示宽度写法。

---

## 9. `node-backend` — Node.js 后端工程

- **源文件**：`skills/tech/node-backend/SKILL.md`
- **上游来源**：仓库内自研提炼，frontmatter 无第三方作者与版本字段；`skills/SKILL_MANIFEST.json` 记 source 为 `tech skill library`
- **用途**：让 Node.js 后端保持确定性：稳定的分层、严格的输入校验、显式的异步处理与可测单元，使 AI 生成的端点与手写端点在形状上完全一致。适用 Express、NestJS、Fastify 三类服务，核心主张是「业务真相只在 service 层存在一次，路由与中间件只负责传输」，并明确要求 no silent failures。
- **何时加载**：创建、扩展或评审 Node.js / Express / NestJS / Fastify API 时；在写路由处理器、service 方法或仓储查询之前；修 async/await 缺陷、做错误处理审计、做校验与 schema 工作或补测试时。
- **核心规则要点**（`## Rule` 六条，全部为强制项）：
  1. 必须分层：route/controller → service → repository；路由处理器与中间件内禁止放业务逻辑。
  2. 单一真相：校验 schema、领域规则与计算只在 service 层存在一次，禁止在处理器里重算。
  3. 每个异步操作都必须被 await 或显式处理，禁止游离 Promise（floating promises）；未处理的 rejection 必须让进程失败。
  4. 禁止静默失败：必须捕获、记录并按正确级别暴露错误；禁止用空 catch 块吞掉异常。
  5. 每个边界输入都必须在进入 service 层之前用 schema 校验（`zod` 或 `class-validator`）。
  6. 库优先：优先用成熟包（`express`、`fastify`、`nest`、`zod`、`pino`），禁止手搓工具函数。
  源文件未单列 `## Constraints` / `## MUST DO` 小节，强制项集中在 `## Rule` 与 `## Guardrails`。
- **关键做法**：
  - 五步工作流：1）先分清哪一层拥有真相（service），哪一层只做传输（route/controller）；2）写处理器之前先定输入 schema 与响应形状；3）service 方法带显式错误类型，由处理器把错误映射成 HTTP 响应；4）为成功路径与失败路径各补一个聚焦测试（`supertest` + `jest`/`vitest`）；5）验证——先跑测试，再真实调用端点确认状态码与载荷。
  - `## Guardrails` 四条禁令：禁止把业务逻辑（定价、状态流转、权限判定）放进路由处理器或中间件；禁止忽略被拒绝的 Promise，禁止使用空 catch 块；禁止把密钥写进代码或配置文件，必须用环境变量与密钥管理服务；避免深层回调链，优先 async/await 配合 try/catch 或错误边界中间件。
  - 工具选型口径：HTTP 框架在 `express`、`fastify`、`nest` 中选；校验在 `zod` 或 `class-validator` 中选；日志用 `pino`。
- **常见坑（反模式）**（源文件 Rule 与 Guardrails 点名）：
  1. 在路由处理器或中间件里写业务逻辑（定价、状态流转、权限判定）。
  2. 校验规则、领域规则或计算在处理器与 service 各写一遍，形成双真相源。
  3. 游离 Promise 未 await 也未 catch，异常变成未处理 rejection。
  4. 用空 catch 块吞掉异常，故障静默传播。
  5. 未在边界用 schema 校验就把原始输入交给 service 层。
  6. 自研工具函数替代成熟包，重复造轮子。
  7. 密钥写进代码或配置文件。
  8. 深层回调链嵌套，错误传播路径不可读。
- **可执行检查清单**：
  - [ ] 分层清晰：route/controller → service → repository，处理器内无业务逻辑。
  - [ ] 每个边界输入都有 schema 校验，且校验 schema 只定义一次。
  - [ ] 所有异步调用都被 await 或显式 `.catch` 处理，无游离 Promise。
  - [ ] 无空 catch 块；错误按正确级别记录并映射为 HTTP 响应。
  - [ ] service 方法定义显式错误类型，处理器负责错误到状态码的映射。
  - [ ] 成功路径与失败路径各有一个聚焦测试（`supertest` + `jest`/`vitest`）。
  - [ ] 密钥来自环境变量或密钥管理服务，未出现在代码与配置文件。
  - [ ] 无深层回调链；使用了成熟包而非自研工具。
- **源文件核查发现（过时/矛盾）**：源文件仅 38 行，未单列 `## Constraints` 与 `## Common Pitfalls` 小节，无代码示例、无 `references/` 目录，落地细节需要靠 `## Rule` 与 `## Guardrails` 自行展开。「Unhandled rejections fail the process」在现代 Node 版本下默认成立（自 Node 15 起未处理 rejection 默认抛错终止），但源文件未标注 Node 版本，也未提示可用 `--unhandled-rejections` 调整这一行为。校验库写「`zod` 或 `class-validator`」但未区分适用场景：`class-validator` 依赖装饰器与 `reflect-metadata`，主要服务 NestJS 风格；Express/Fastify 项目通常直接用 `zod`。测试栈写 `supertest + jest/vitest`，未说明两个测试运行器之间的选型口径。
- **上游维护提示**：正文与 references 保留英文；本要点为中文提炼。上游更新后需复核：Node 版本与未处理 rejection 的默认行为说明、校验库选型口径、测试运行器选型，以及是否补齐代码示例。

---

## 10. `postgresql-best-practices` — PostgreSQL 最佳实践

- **源文件**：`skills/tech/postgresql-best-practices/SKILL.md`
- **上游来源**：仓库内自研提炼，frontmatter 无第三方作者与版本字段；`skills/SKILL_MANIFEST.json` 记 source 为 `tech skill library`
- **用途**：把 PostgreSQL 当作本方法论默认的关系型真相存储（DB → 后端 → API），保证数据层确定：正确的约束、被证明有效的索引、安全的迁移、可观测的查询性能，让 single source of truth 规则在存储层依然成立。它的七条规则有一条主线：先正确性，后性能；先证据，后优化；迁移可逆；连接池必配；备份与恢复演练属于模式生命周期的一部分。
- **何时加载**：设计表或 schema、编写复杂查询、新增索引、执行迁移时；创建新表、修改列、写报表查询之前；做慢查询调优、N+1 修复、迁移安全评审或备份恢复规划时。
- **核心规则要点**（`## Rule` 七条，全部为强制项）：
  1. 先为正确性设计：显式类型、`NOT NULL`、check 约束与外键都要在建索引之前完成。
  2. 索引必须为「已存在的查询」而建，而不是为「可能会用到的列」而建；必须用 `EXPLAIN ANALYZE` 验证。
  3. 每次变更一个迁移（Alembic / Flyway）；迁移是只追加（append-only）且可回滚的。
  4. 事务负责多语句一致性；复合写禁止依赖隐式 autocommit。
  5. 生产环境必须使用连接池（PgBouncer 或应用级池）；禁止每请求开一个连接。
  6. 禁止静默降级：慢查询必须拿到 `EXPLAIN ANALYZE` 与定向修复，禁止用 workaround 或接受 N+1。
  7. 备份与恢复演练是 schema 生命周期的一部分，不是事后补的。
  源文件未单列 `## Constraints` / `## MUST DO` 小节；强制项集中在 `## Rule` 与 `## Guardrails`。
- **关键做法**：
  - 五步工作流：1）写 schema——类型、约束、外键齐全，并说明该表服务的业务规则；2）写查询——加索引前后各跑一次 `EXPLAIN ANALYZE`，用计划证明改善；3）加迁移——单步可回滚，并分别测试升级与回滚；4）验证数据完整性——做定向回读，确认计划里索引确实被使用；5）记录证据——计划输出、行数、前后延迟。
  - `## Guardrails` 四条禁令：禁止在没有 `EXPLAIN ANALYZE` 基线的情况下加索引，禁止为猜测的列建索引；禁止在没有备份与回滚路径的情况下删除或重写数据；当 service 层拥有真相时，禁止把业务逻辑放进存储过程或触发器；避免 `SELECT *` 与无类型列，schema 必须显式且可审计。
  - 工具口径：迁移用 Alembic 或 Flyway；连接池用 PgBouncer 或应用级池。
- **常见坑（反模式）**（源文件 Rule 与 Guardrails 点名）：
  1. 先建索引后补约束，约束缺失时索引无法保证正确性。
  2. 为「可能有一天会用到」的列建索引，制造写放大与无用维护成本。
  3. 没有 `EXPLAIN ANALYZE` 基线就加索引，无法证明改善。
  4. 一个迁移里塞多个变更，或迁移不可逆，回滚无路。
  5. 复合写依赖隐式 autocommit，中途失败留下半完成状态。
  6. 每个请求新开连接，不配 PgBouncer 或应用级连接池。
  7. 用 workaround 掩盖慢查询，或默认接受 N+1。
  8. 把业务逻辑放进存储过程或触发器，与 service 层争夺真相归属。
  9. 没有备份与回滚路径就删数据或重写数据。
  10. 使用 `SELECT *` 与无类型列。
- **可执行检查清单**：
  - [ ] 表的类型、`NOT NULL`、check 约束与外键齐备，并写明所服务的业务规则。
  - [ ] 索引只为已存在的查询而建，且有 `EXPLAIN ANALYZE` 前后对比。
  - [ ] 迁移一次一个变更、只追加、可回滚，升级与回滚都测过。
  - [ ] 复合写包在事务里，未依赖隐式 autocommit。
  - [ ] 生产环境已配 PgBouncer 或应用级连接池，无每请求新连接。
  - [ ] 慢查询有 `EXPLAIN ANALYZE` 输出与定向修复，未接受 N+1。
  - [ ] 业务逻辑留在 service 层，未下沉到存储过程或触发器。
  - [ ] 备份与恢复演练已执行并记录；无 `SELECT *` 与无类型列。
- **源文件核查发现（过时/矛盾）**：源文件仅 39 行，未单列 `## Constraints` 与 `## Common Pitfalls` 小节，无 SQL 示例、无 `references/` 目录，`EXPLAIN ANALYZE` 只给动词未给命令形式（对比 `mysql-best-practices` 给了 `EXPLAIN FORMAT=JSON`）。文中并列 Alembic（Python 生态）与 Flyway（JVM 生态），但未说明跨语言项目应按哪一侧落地。连接池只写「PgBouncer 或应用级池」，未给 PgBouncer 的池模式（session / transaction / statement）口径——不同池模式对 prepared statement 与 session 级特性的兼容性差异很大，选错会让上层 ORM 行为改变。源文件也未标注 PostgreSQL 主版本，使用分区、`GENERATED` 列、`MERGE` 等新特性时需要另行核对版本支持情况。
- **上游维护提示**：正文与 references 保留英文；本要点为中文提炼。上游更新后需复核：是否补 `EXPLAIN ANALYZE` 示例与 SQL 片段、PgBouncer 池模式口径、迁移工具选型说明，以及 PostgreSQL 主版本依赖说明。

---

## 附录 A：这 10 个 Skill 的选型速查

| 场景 | 首选 Skill | 配套 Skill | 选择要点 |
|---|---|---|---|
| 只优化 Dockerfile | `multi-stage-dockerfile` | `docker-expert` | 只做构建/运行阶段分离与镜像瘦身时用前者；涉及 Compose 编排、容器运行时安全、构建故障诊断时升级到 `docker-expert` |
| 容器化与编排全流程 | `docker-expert` | `multi-stage-dockerfile` | 先按 `docker-expert` 的 Rule 与检查清单定容器标准，Dockerfile 细节交给 `multi-stage-dockerfile` |
| Flutter 应用骨架 | `flutter-expert` | `flutter-animations` | 项目结构、状态管理（Riverpod/Bloc 二选一）、GoRouter 导航、性能剖析走 `flutter-expert` |
| Flutter 动效 | `flutter-animations` | `flutter-expert` | 先用动画类型决策树定位类型；动效实现与状态管理交接时回到 `flutter-expert` |
| Java 后端工程规范 | `java-springboot` | `java-performance-governance` | 结构、注入、配置、分层、测试切片走 `java-springboot` |
| Java 批处理与内存问题 | `java-performance-governance` | `java-springboot` | 出现批处理变慢、堆增长、超时、池耗尽时切到性能治理；新增缓存或线程配置前必须先过它 |
| JS/TS 测试 | `javascript-typescript-jest` | `node-backend` | Mock 边界、异步写法、覆盖率口径以 Jest Skill 为准；生产代码分层以 `node-backend` 为准 |
| Node.js API | `node-backend` | `javascript-typescript-jest` | 分层与单一真相先定好，再用 Jest Skill 补成功/失败两条路径的测试 |
| MySQL 数据层 | `mysql-best-practices` | 对应后端 Skill | `EXPLAIN`、InnoDB、迁移可回滚、`utf8mb4` 与 `DECIMAL` 为硬约束 |
| PostgreSQL 数据层 | `postgresql-best-practices` | 对应后端 Skill | 先约束后索引，`EXPLAIN ANALYZE` 为唯一性能证据，迁移只追加且可回滚 |
| 两个数据库 Skill 的二选一 | 按实际引擎选 | — | MySQL 与 PostgreSQL 的索引、迁移、连接池口径不同，禁止混用两套实践 |

**分层与升级路径**：容器类任务从 `multi-stage-dockerfile` 起步，需要编排或运行时安全时升级到 `docker-expert`；Java 后端从 `java-springboot` 起步，一旦涉及批处理、缓存、线程池或索引成本就叠加 `java-performance-governance`；数据层按实际引擎在 `mysql-best-practices` 与 `postgresql-best-practices` 之间择一，不要两套并用。本文件中出现的技能组合建议均由这 10 个 Skill 的正文与 frontmatter 触发条件推导，未引入本层之外的 Skill。

---

## 附录 B：上游来源清单

来源字段以每个 `SKILL.md` 的 frontmatter 为准，并与 `skills/SKILL_MANIFEST.json` 逐条核对（两者不一致处已在下表备注）。

| Skill | frontmatter 来源 / 作者 | `SKILL_MANIFEST.json` 记录 | 处理口径 |
|---|---|---|---|
| `docker-expert` | `source: community`；`category: devops`；`risk: unknown`；`date_added: "2026-02-27"`；未署具名作者 | source `tech skill library`；maturity `verified` | 正文与 references 保留英文，仅出中文要点，避免与上游分叉 |
| `flutter-animations` | `metadata.author: Stanislav [MADTeacher] Chernyshev`；`version: "1.0"`；无 `source` 字段 | source `tech skill library`；maturity `verified` | 同上；本 Skill 无 `references/` 之外的模板目录，模板引用失效需上游补齐 |
| `flutter-expert` | `license: MIT`；`metadata.author: https://github.com/Jeffallan`；`version: "1.1.0"`；`related-skills: react-native-expert, test-master, fullstack-guardian` | source `tech skill library`；maturity `verified` | 同上；`related-skills` 指向本仓库不存在的 Skill |
| `java-performance-governance` | 无第三方作者字段，仅 `name` 与 `description` | source `GERP batch-operation and memory-leak governance extraction`；maturity `verified` | 仓库内自研提炼；正文保留英文，仅出中文要点 |
| `java-springboot` | 无第三方作者与版本字段 | source `tech skill library`；maturity `verified` | 仓库内能力包；正文保留英文，仅出中文要点 |
| `javascript-typescript-jest` | 无第三方作者与版本字段 | source `tech skill library`；maturity `verified` | 仓库内能力包；正文保留英文，仅出中文要点 |
| `multi-stage-dockerfile` | 无第三方作者与版本字段 | source `tech skill library`；maturity `verified` | 仓库内能力包；正文保留英文，仅出中文要点 |
| `mysql-best-practices` | 无第三方作者与版本字段 | source `tech skill library`；maturity `verified` | 仓库内能力包；正文保留英文，仅出中文要点 |
| `node-backend` | 无第三方作者与版本字段 | source `tech skill library`；maturity `verified`；description 与 frontmatter 措辞略有差异 | 仓库内能力包；正文保留英文，仅出中文要点 |
| `postgresql-best-practices` | 无第三方作者与版本字段 | source `tech skill library`；maturity `verified`；description 与 frontmatter 措辞略有差异 | 仓库内能力包；正文保留英文，仅出中文要点 |

**统一维护口径**：这 10 个 Skill 中，2 个带第三方署名（`flutter-animations`、`flutter-expert`）、1 个标注为社区来源（`docker-expert`），其余 7 个为仓库内能力包。无论来源如何，本文件一律只产出中文要点、不产出逐句译文：正文与 `references/` 继续作为唯一真相源，中文要点只负责「管什么、何时加载、规则强度、关键做法、常见坑、可执行清单」，细节一律回到英文原文。上游更新时按 00_导读/03_翻译口径与同步规则.md 第 6 节定位受影响小节，只改对应要点，并在 `90_校验/校验报告.md` 记录同步日期。
