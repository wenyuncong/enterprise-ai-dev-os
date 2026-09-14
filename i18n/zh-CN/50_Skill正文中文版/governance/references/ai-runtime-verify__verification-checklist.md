# 运行时验证清单 | Runtime Verification Checklist

> **源文件**：skills/governance/ai-runtime-verify/references/verification-checklist.md
> **源版本**：未标注
> **译文日期**：2026-09-14
> **术语依据**：00_导读/02_术语对照表.md
> **翻译口径**：全量对应；英文标识符、命令、代码块、门禁代号原样保留。
> **说明**：本文件是 Skill `ai-runtime-verify` 的配套参考文件中中文对照版，不是正式加载源。

---

> `ai-runtime-verify` Skill 的配套参考文件。
> 当人工复核验证结果，或扩展验证引擎时，使用本检查清单。

---

## P0：必须通过（阻断） | P0: Must Pass (Blocking)

### 1. 无控制台错误 | No Console Errors

- **检查**：`consoleErrors.length === 0`
- **原因**：任何未捕获的 JS 错误或 console.error 都表明代码已损坏
- **常见原因**：函数未定义、变量未定义、API 响应解析错误、React/Vue 渲染错误
- **误报**：第三方统计脚本、浏览器扩展干扰（必要时过滤）

### 2. 加载遮罩已移除 | Loading Overlay Removed

- **检查**：不存在匹配 `.loading-overlay.active`、`#loadingOverlay.active` 或类似选择器的元素
- **原因**：加载遮罩卡住意味着页面从未完成初始化
- **常见原因**：缺少 `renderCard`、缺少 `closeModal`、`render()` 中未处理的 promise rejection、API 失败且无错误处理
- **需警惕的模式**：`render()` 添加了 `.active` 类，却因提前 return 或异常而从未移除它

### 3. 核心 DOM 已渲染 | Core DOM Renders

- **检查**：主内容元素可见且文本超过 10 个字符
- **原因**：主区域为空或被隐藏，意味着应用外壳渲染了但内容没有
- **常见原因**：API 返回空且未处理空状态、路由失败、条件渲染出错

### 4. API 响应正常 | API Responses OK

- **检查**：API 调用没有 4xx/5xx 响应
- **原因**：后端错误会级联为前端失败
- **常见原因**：API 路由缺失、数据库连接失败、schema 不匹配、查询参数非法

### 5. 无白屏 | No White Screen

- **检查**：空白归一化后 body 的 textContent 超过 15 个字符
- **原因**：页面真正空白意味着什么都没渲染
- **常见原因**：DOM 操作前的致命 JS 错误、CSS 隐藏了全部内容、HTML 模板为空

### 6. 无无限刷新 | No Infinite Refresh

- **检查**：验证窗口期内导航次数 <= 5
- **原因**：刷新循环浪费资源并使页面不可用
- **常见原因**：路由守卫重定向到自身、effect hook 缺少依赖数组、错误处理器中调用 `location.reload()`

---

## P1：应当通过（警告） | P1: Should Pass (Warning)

### 7. 关键交互可用 | Key Interactions Work

- **检查**：至少找到 1 个可点击按钮
- **原因**：无任何操作的只读页面可能是有意为之，但通常意味着 UI 缺失

### 8. 表单输入可用 | Form Inputs Functional

- **检查**：至少 1 个可编辑输入项能获得焦点并被填写
- **原因**：无法接受输入的表单就是坏表单
- **例外**：只读查看页可以合理地没有可编辑输入项

### 9. Tab 切换可用 | Tab Switching Works

- **检查**：如果存在 Tab，点击非激活 Tab 会显示新内容
- **原因**：Tab 切换损坏意味着有一半 UI 无法访问
- **例外**：单 Tab 页面不需要 Tab 切换

---

## P2：锦上添花（信息性） | P2: Nice to Have (Informational)

### 10. 无布局溢出 | No Layout Overflow

- **检查**：在 1440px 视区宽度下没有横向滚动条
- **原因**：横向溢出说明响应式设计已损坏
- **常见原因**：固定宽度元素大于视区、负边距、绝对定位未做容器约束

### 11. 无 404 资源 | No 404 Assets

- **检查**：所有非 API 资源均加载成功
- **原因**：CSS/JS/图片缺失会降低体验
- **常见原因**：路径错误、资源被删除、构建产物未部署

---

## 结果解读 | Interpreting Results

| 总体 | P0 状态 | 动作 |
|---|---|---|
| `passed: true` | 全部 P0 通过 | ✅ 页面已通过运行时验证。可以进入 “done” 声明。 |
| `passed: false` | 任一 P0 失败 | ❌ 页面已损坏。在声称完成之前必须修复 P0 失败项。 |
| `passed: true` 但带 P1 警告 | 全部 P0 通过 | ⚠️ 页面可用但存在 UX 问题。时间允许时修复 P1 警告。 |

---

## 扩展验证引擎 | Extending the Verification Engine

新增一项检查：

1. 在 `skills/governance/ai-runtime-verify/scripts/verify.js` 的 `try` 块内添加检查逻辑
2. 把检查加入对应数组（`p0Checks`、`p1Checks` 或 `p2Checks`）
3. 用新的检查描述更新本清单
4. 在 `SKILL.md` 的 Evolution History 中递增 Skill 版本
