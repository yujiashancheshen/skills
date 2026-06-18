---
name: fullstack-development
description: 基于详细设计文档推进前后端开发，按模块产出 dev-plan-<模块>.md 并用 AskUserQuestion 确认，再走 TDD（后端用 tdd-guide agent 做 Go 入口驱动单测、前端做 Vue 组件测试），每个完成模块产出 dev-test-<模块>.md 报告并逐条映射验收标准。当用户要进入开发、按设计实现功能、做 TDD、写 dev-plan/dev-test，或提到“前后端开发、按 tech-spec 开发、实现这个需求、跑入口单测”时就应使用本 skill——即使没明说“用这个 skill”，只要是从设计文档推进编码实现，也应主动使用。
---

# fullstack-development

根据《详细设计文档》(`design-detail.md`) 推进前后端开发。后端 Go 多模块、前端 Vue。

核心流程：

1. **按模块写执行计划文件** `dev-plan-<模块>.md` → 给出路径 → `AskUserQuestion` 确认
2. **多模块时再 Ask 是否并行**（一模块一子 agent，最多 5 个）
3. **调用 TDD agent 执行**（后端用 `tdd-guide`；先确认 agent 存在，否则报错）
4. **每个完成的模块跑入口/组件测试 → 产出 `dev-test-<模块>.md` 报告**

> 编码规范参考项目根 CLAUDE.md 或项目既有编码规范。

## 一、何时使用
- 输入是一份 `design-detail.md` / 设计文档，希望直接进入开发
- 需求涉及后端 HTTP、MQ、command 等明确入口，和/或前端 Vue 页面与组件
- 需求可能跨多个后端模块和前端模块
- 希望按 TDD 推进并按入口测试口径出报告

## 二、输入要求
输入一份详细设计，至少包含：需求目标、涉及模块、入口清单（HTTP / MQ / command / 前端组件）、关键数据结构或上下游约束、验收标准。

缺失项不要硬猜，先在计划里标注「待确认」，让用户在 Ask 阶段补齐。

## 三、固定执行流程

### Step 1：先检索本地代码
写计划前做一次基础检索：
- 读 `design-detail.md` 全文
- 后端：用 Glob/Grep 在涉及模块目录查现有同名 controller、service、handler、MQ 消费器
- 前端：查现有同名页面、`.vue` 组件、接口封装
- 确认引用到的文件路径、函数名、组件名是**真实存在或确认要新增**的

不要展开成长篇报告，只保证后面写 plan 引用的内容真实可对齐。

### Step 2：按模块产出执行计划文件
执行计划**必须以文件形式落盘**，不允许只在对话里输出。

**位置**：`design-detail.md` 同级目录。
**命名**：`dev-plan-<模块名>.md`，一模块一份。前后端分属不同模块时各一份（如 `dev-plan-demo-service.md`、`dev-plan-demo-frontend.md`）。跨模块共享结构体在每份里都列依赖点。

#### 每份 dev-plan 必含三块（顺序不变）

##### 文件变更总览

| 文件路径 | 新增/修改 | 职责/一句话变更概要 |
|---|---|---|
| `demo-service/controllers/ticket/create.go` | 新增 | 提交工单 HTTP 入口 |
| `demo-frontend/ticket/components/SubmitDialog.vue` | 新增 | 提交工单弹窗组件 |

要求：尽量落到具体文件，无法精确的标「待确认」；**不包含测试文件**，只列生产代码/配置/定义文件；按文件目录顺序排序；表是范围边界，后续新增文件应在表内。

##### 数据结构定义
优先写：**跨模块共享**、**模块内跨包使用**、影响上下游联调/MQ/类库下沉的定义。可直接给 Go 结构体定义、JSON 结构、TS 接口/类型（前端）。重点把**共享边界**讲清楚，不写实现逻辑。

##### 任务分解
任务总数 **≤10 个**。合并粒度：同入口多条验收→1 个任务；同目录/同领域多个入口→可合 1 个任务；每模块通常 1~3 个任务。

每个任务必含：
- **A. 可导出的结构体/组件** — 后端 exported structs；前端组件名与 props 契约
- **B. 可导出的函数/方法签名** — 仅签名不写实现；不确定的标「待确认」
- **C. 逻辑概述** — 自然语言或伪代码（**禁止写真实现代码**）
- **D. 测试表格**

| 测试对象 | 是否入口/组件测试 | 测试方法名 | 一句话总结测什么 |
|---|---|---|---|
| `ApiTicketCreate` | 是 | `TestApiTicketCreate_SuccessWithoutInflight` | 无在途工单提交成功 |
| `SubmitDialog.vue` | 是 | `submit_dialog_blocks_empty_content` | 内容为空时阻断提交 |

要求：入口验收必须有测试；测试名直接表达验收意图；这张表里的方法名是**契约**，开发阶段不允许偷偷改名，改名要回到 Step 3 重新 Ask。

**任务完成判据**：本任务相关代码写完 **且** 本任务测试表里全部用例 fresh GREEN。

### Step 3：写完计划，询问用户确认
**触发条件**：`dev-plan-*.md` 全部写完。
调用 `AskUserQuestion`，列出所有已生成的 `dev-plan-*.md` **绝对路径**，问用户「有没有问题」。
选项：`✅ 没问题，可以开始` / `❌ 有问题，需要调整`。
用户选「有问题」或给修改意见 → 修改对应文件 → **改完必须再 Ask 一次**，直到确认「没问题」。

### Step 4：多模块时询问是否并行
仅当 `dev-plan-*.md` 多于一份时执行。调用 `AskUserQuestion`：是否开启子 agent 并行开发（一模块一子 agent，最多 5 个）。
选项：`是，并行` / `否，按顺序串行`。建议：模块间强依赖顺序时串行；边界清晰时并行。

「最多 5 个」名额只统计实际 spawn 的子 agent；由主流程直接开发的前端模块（§5.1 例外）不占名额。

### Step 5：调用 agent 执行开发

#### 5.1 先确认 agent 存在
后端按以下顺序查找 TDD agent：
1. `Agent` 工具可用 `subagent_type` 列表里是否有 `tdd-guide` 或带前缀的同名 agent
2. 文件系统 Glob：`~/.claude/**/agents/tdd-guide.md`、项目 `.claude/agents/tdd-guide.md`

**任一找到即可用。找不到必须报错并停止**：
> 错误：未找到 tdd-guide agent。请先安装/启用对应 agent 后重试。

**前端 Vue 模块的口径（唯一例外）**：后端模块必须 spawn agent；前端模块若环境中没有可用的前端 TDD/实现 agent，则**允许主流程直接按 TDD 推进**（先写组件测试 RED → 再写实现 GREEN），这是对「禁止主流程假扮 agent」红线的明确豁免。判定顺序：先查是否有可用前端 agent（同 5.1 查找方式），有就 spawn、没有才由主流程亲自做，二选一，不要既 spawn 又自己写。

#### 5.2 调用方式
**后端模块必须**通过 `Agent` 工具调用，不允许在主上下文里假扮 agent（前端模块按 §5.1 的例外口径处理）。
**入参核心**：每个 agent 的 prompt 只传**该模块的 `dev-plan-<模块>.md` 绝对路径** + `design-detail.md` 路径 + 测试规范要点，让 agent 自己读文件，不要把全文塞进 prompt。

**串行**（单模块或用户选串行）：依次调用。
**并行**（多模块且用户选并行）：一模块一子 agent，**单条消息内同时发起 N 个 Agent 调用，N ≤ 5**；模块数 > 5 先并行前 5 个，等回执完成再发下一批。

要求每个 agent：严格按计划任务顺序推进；每任务先写测试再写实现（RED → GREEN）；测试方法名与计划契约一致；任务完成 = 代码写完 + 该任务测试表全部用例 fresh GREEN；完成后按 §5.3 回执。

#### 5.3 回执统一格式
```
模块：<模块名>
是否完成：是 / 否
未完成原因：<具体卡点；已完成填"无">
下一步：<下一步该做什么；已完成填"进入测试报告阶段">
```
主流程汇总回执；未完成模块进入「修复-重试」或「回 plan 调整」分支，判据：**同一模块重试 ≤ 2 次仍卡在 RED 或同一卡点，则回 Step 3 用 AskUserQuestion 同步问题并调整 dev-plan**，不要无限重试。

---

### 后端入口单元测试书写要求（内联摘要）

#### 什么叫入口单元测试
不是只测 controller / consumer 这一层自己的几行代码，而是：从入口打进去（HTTP / MQ / command）→ mock 掉所有底层 IO → 用最终可观察结果表达验收标准。即「入口驱动的链路单测」。

#### 适合写的场景
- HTTP 接口：参数非法报错、参数合法成功/失败、关键返回字段、空数据/no-op
- MQ 消费入口：非法 JSON、no-op 条件、状态推进、下游副作用
- command 入口：定时任务/脚本任务从入口打进去的可观察结果

#### 不适合硬写在入口层的内容
纯内部实现细节、纯负向副作用、分布式锁/并发竞争/重试时序、DTO 已明示的字段集合空洞断言。这些更适合 service / domain / integration 层。

#### 写法要求
- 优先验证**可观察结果**：HTTP 看 `errNo` / `errMsg` / `data`；MQ 看是否报错、是否执行某条 SQL、是否触发下游
- 不要断言「内部 new 了某 command」「调用了某 helper」
- 写数据/重副作用的入口测试建议单独拆 `_test.go` 文件
- 测试名直接表达验收意图，如 `TestApiTicketCreate_SuccessWithoutInflight`

#### mock 原则
- MySQL：`sqlmock` 或项目自有的 mock helper
- Redis：`redismock` 或项目自有的 mock helper
- 外部 API：项目自有的 API mock 封装或 `httptest`
- MQ 输出：项目自有的 MQ mock helper

原则：**mock IO 边界，不 mock 入口内部实现细节**。

#### 先浅后深
先立轻量测试（非法参数、空列表、no-op、简单成功路径），再补重链路测试（SQL side effects、状态推进、分支、失败但仍应保留主流程结果）。

### 前端组件测试书写要求（内联摘要）
- 优先验证**用户可观察行为**：渲染结果、提交后状态、错误提示文案、按钮置灰/隐藏、空态/loading
- mock 接口请求（如 mock 接口封装层），断言组件对返回结果的反应
- 不要断言内部私有方法是否被调用、某 ref 中间值
- 测试名表达验收意图，如 `submit_dialog_blocks_empty_content`
- 与 `design-detail.md` 前端验收点逐条对应

### Step 6：每个完成的模块跑测试并出报告
Step 5 已在开发中写了测试。Step 6 **只做两件事**：
1. **逐个模块**对**本次新增的入口/组件测试**做一次 fresh 重跑
2. 产出报告文件

#### 6.1 报告文件
- **位置**：`design-detail.md` 同级目录
- **命名**：`dev-test-<模块名>.md`，与 `dev-plan-<模块名>.md` 一一对应
- 多模块时每模块一份，可选再写 `dev-test-summary.md` 汇总

#### 6.2 报告必含

| 入口/组件 | 验收标准描述 | 测试方法名 | 是否通过 | 备注 |
|---|---|---|---|---|
| `HTTP 提交工单` | 无在途工单提交成功 | `TestApiTicketCreate_SuccessWithoutInflight` | ✅ | |
| `SubmitDialog.vue` | 内容为空阻断提交 | `submit_dialog_blocks_empty_content` | ✅ | |

表后给出：验收映射率（已映射验收/全部验收）、方法通过率（fresh 通过/已映射方法）、验收通过率（既映射又通过/全部验收，**最终判定指标**）、未覆盖项清单。

#### 6.3 执行要求
- fresh 跑（不允许「刚才跑过」代替）
- 读取完整输出，确认 exit code
- 只跑**本次新增**的入口/组件测试，不顺手扩到全仓回归

## 四、产物清单
```
<design-detail同目录>/
├── design-detail.md           # 输入
├── dev-plan-<模块A>.md         # 计划，用户确认过
├── dev-plan-<模块B>.md
├── dev-test-<模块A>.md         # 测试报告
├── dev-test-<模块B>.md
└── dev-test-summary.md        # 多模块时可选汇总
```

## 五、执行阶段红线
- ❌ 计划没用 AskUserQuestion 确认就开始开发
- ❌ 计划只在对话里出，不落盘成 `dev-plan-<模块>.md`
- ❌ 用户改了计划后没有再 Ask 一次
- ❌ 多模块时擅自决定并行/串行
- ❌ 跳过查找 tdd-guide agent 这一步
- ❌ 后端模块在主上下文里假扮 agent，不真的 spawn agent（前端模块见 §5.1 例外）
- ❌ 并行子 agent 超过 5 个
- ❌ 计划「逻辑概述」里写真实现代码
- ❌ 把入口验收全下沉到 service 层测试
- ❌ Step 6 用「刚才跑过」代替 fresh 执行
- ❌ Step 6 顺手回归全仓而不是只跑本次新增的测试

## 六、成功标准
1. 每个模块都有用户确认过的 `dev-plan-<模块>.md`
2. 计划含三块：文件变更总览 / 数据结构定义 / 任务分解
3. 后端开发通过 `Agent` 工具调用 tdd-guide 完成
4. 多模块并行/串行经用户确认
5. 每个完成的模块都跑了 fresh 入口/组件测试
6. 每个完成的模块都产出 `dev-test-<模块>.md` 报告
7. 报告逐条映射验收标准，而不是只说「测试通过」
