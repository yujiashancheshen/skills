---
name: e2e-testing
description: 用 Playwright 编写并执行浏览器端到端（e2e）测试，从需求规格准入 Case 或已实现功能归纳用户旅程，用语义定位写稳定用例、全新执行，产出 e2e-test-report.md 并把每条准入 Case 映射到结果；支持项目内落盘用例与 playwright MCP 实时驱动两条路径。当用户要做 e2e 测试、端到端验证、回归关键业务流程、用 Playwright/浏览器验证页面，或提到“e2e、端到端、Playwright、用户旅程、回归测试”时就应使用本 skill——即使没明说“写 e2e”，只要是要从用户视角验证整条流程能否跑通，也应主动使用。
---

# e2e-testing

基于《需求规格文档》(`requirement-spec.md`) 的准入 Case 或已实现功能，用 **Playwright** 编写并执行浏览器端到端测试，产出 `e2e-test-report.md`。

核心原则：**用例来源于准入 Case，验证用户可观察的端到端行为，不验证内部实现细节。**

## 适用场景
- 需求/功能已实现，需要从用户视角验证关键业务流程能跑通
- 已有 `requirement-spec.md` 准入 Case，或能从功能页面归纳出关键路径
- 需要回归一批关键用户旅程（journey）并出报告

不适用于：
- 单个函数/组件级别的单测（用 fullstack-development 的入口/组件测试）
- 纯接口契约测试（用接口级测试）

## 输入与输出
- **输入**：`requirement-spec.md` 准入 Case（优先）/ 已实现的前端页面与可访问环境 URL
- **输出**：Playwright 测试用例文件 + `e2e-test-report.md`（与需求文档同目录）

## 必问清单（开始前用 AskUserQuestion）
1. **被测环境 URL 与账号**：测试环境地址、是否需要登录、测试账号怎么来（必问）
2. **测试用例存放位置**：复用项目已有 Playwright 目录，还是新建（必问）
3. **执行方式**：用项目内 Playwright（`@playwright/test`）写落盘用例，还是用 playwright MCP 实时驱动浏览器做探索性验证（必问）

信息不足不要硬猜，先把缺口列入问题再继续。

## 工作流

### Step 1：梳理关键旅程
- 读 `requirement-spec.md`，把准入 Case 归并成若干**用户旅程（journey）**
- 一个 journey = 一条可从入口走到可观察结果的完整路径（如「提交工单 → 看到待审批」）
- 优先覆盖：核心正常流程、关键异常流程、关键状态流转
- 谨慎纳入：纯集成/并发/时序类（这些不适合 e2e）

把 journey 列成清单，每条标注「覆盖哪些准入 Case」。

### Step 2：探查页面真实结构
写用例前，先确认选择器真实存在，禁止凭空捏造 selector：
- 用 playwright MCP（`browser_navigate` + `browser_snapshot`）打开页面拿真实可访问性快照，或读前端 `.vue` 源码确认元素
- 优先用**语义定位**：`getByRole`、`getByLabel`、`getByText`、`getByPlaceholder`
- 仅在语义定位不可行时才用 `data-testid`；若页面缺测试锚点，在报告里标注「建议前端补 data-testid」

### Step 3：编写/执行用例（按必问第 3 条选择的执行方式分两条路径）

两条路径**通用要求**：
- 断言**用户可观察结果**：页面文案、状态、列表项、URL、toast 文案；不要断言后端 DB 状态、内部接口调用细节
- 条件触发的提示文案与 `requirement-spec.md` 保持一致
- 一个 journey 对应一条用例，名称表达验收意图

**路径 A：项目内 Playwright 落盘用例（默认，可回归）**
- 一个 journey 一个 `test()`，写成 `.spec.ts` 落盘
- 用 **web-first 断言**（`await expect(locator).toBeVisible()` 等），不要用固定 `sleep`/`waitForTimeout`
- 登录等公共前置抽到 fixture / `beforeEach` / `storageState`

**路径 B：playwright MCP 实时驱动（探索性 / 不便落盘时）**
- 用 `browser_navigate` 打开页面，按 journey 步骤用 `browser_click` / `browser_type` / `browser_fill_form` 操作
- 每条 journey 用 `browser_snapshot` 确认页面状态、用 `browser_take_screenshot` 留证
- 把实际执行过的步骤整理成**可复现步骤清单**写入报告，便于日后补成路径 A 的落盘用例
- 断言依据同样是快照/截图里的可见文本与状态，不看内部实现

路径 A 最小示例：

```ts
import { test, expect } from '@playwright/test';

test('提交工单后展示待审批状态', async ({ page }) => {
  await page.goto('/ticket/list');
  await page.getByRole('button', { name: '提交工单' }).click();
  await page.getByLabel('工单类型').selectOption('普通');
  await page.getByLabel('工单内容').fill('e2e 测试内容');
  await page.getByRole('button', { name: '提交' }).click();

  // web-first 断言，不用固定 sleep
  await expect(page.getByText('待审批')).toBeVisible();
});

test('工单内容为空时阻断提交并提示', async ({ page }) => {
  await page.goto('/ticket/list');
  await page.getByRole('button', { name: '提交工单' }).click();
  await page.getByRole('button', { name: '提交' }).click();

  await expect(page.getByText('请填写工单内容')).toBeVisible();
});
```

### Step 4：全新执行并取证
- fresh 跑（不允许「刚才跑过」代替），读取完整输出，确认结果
- **路径 A（落盘）执行命令**：`npx playwright test`（失败定位用 `npx playwright test --trace on`，单条用 `npx playwright test -g "<测试名>"`）；确认 exit code
  - 若项目尚无 Playwright 环境：提示用户用 `npm init playwright@latest` 初始化，或确认应装在哪个前端目录后再建，不要擅自在仓库根乱装
- **路径 B（MCP 实时）执行**：用 `browser_*` 工具逐 journey 实际跑一遍，关键步骤 `browser_take_screenshot` 留证，记录每步实际结果
- 失败优先排查 selector 失效 / 等待时机 / 测试数据，不要直接放宽断言掩盖问题

### Step 5：产出报告
`e2e-test-report.md` 必含：

| Journey | 覆盖准入Case | 测试名 | 是否通过 | 备注/截图 |
|---|---|---|---|---|
| 提交工单成功 | F0-01 | `提交工单后展示待审批状态` | ✅ | |
| 提交校验失败 | F0-02 | `工单内容为空时阻断提交并提示` | ✅ | |

表后给出：准入 Case 覆盖率（已映射/全部准入 Case）、用例通过率（fresh 通过/已写用例）、**准入通过率（既映射又通过/全部准入 Case，最终判定指标）**、未覆盖项清单及原因。

**降级口径**：当没有 `requirement-spec.md` 准入 Case、仅从已实现页面归纳 journey 时，「覆盖准入Case」列改填 journey 来源（如「页面归纳」），最终判定指标改为**关键旅程通过率（fresh 通过 journey / 全部关键 journey）**，并在报告开头注明用例来源是页面归纳而非准入 Case。

## Playwright 稳定性要点
- 用语义定位器，避免脆弱的 CSS/XPath 链
- 用 web-first 断言自动等待，禁用固定 `waitForTimeout`
- 测试间相互独立、可重复运行，自带数据准备与清理
- 不依赖上一条用例留下的状态
- 把不稳定（flaky）用例单独标注隔离，不要靠重试掩盖

## 常见错误
- 凭空捏造 selector，没先看页面真实结构
- 用 `sleep` / `waitForTimeout` 等固定等待，导致 flaky
- 断言后端/DB/接口内部状态，而不是用户可观察结果
- 把并发、幂等、MQ 时序这类集成测试场景硬塞进 e2e
- 测试名写成 `test1`，看不出验收意图
- 报告只写「全部通过」，不逐条映射准入 Case
- 用例之间相互依赖执行顺序
