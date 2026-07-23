# Skills

Agent 技能集合，涵盖研发流水线、技术内容制作等场景。每个 Skill 是一个独立目录，不绑定具体业务。

## 研发流水线 Skills

五个 skill 串成一条从需求到测试的链路，前一个产物喂给下一个：

```
需求材料
  └─(clarifying-requirements)→ requirement-spec.md + requirement-question.md
        └─(outline-design)→ design-outline.md
              └─(detailed-design)→ design-detail.md
                    └─(fullstack-development)→ 代码 + dev-plan-*.md + dev-test-*.md
                          └─(e2e-testing)→ e2e 用例 + e2e-test-report.md
```

各环节可独立使用，不要求一定从头跑完整条链路。

| Skill | 能力 | 主要输入 | 主要产物 |
| --- | --- | --- | --- |
| [clarifying-requirements](./clarifying-requirements/SKILL.md) | 需求澄清，整理可评审的需求规格。把零散的需求材料（原始需求文档、PRD、问答记录、原型、UI 设计图）整理成可评审的《需求规格文档》，做歧义澄清、与现有代码的冲突核对、EARS 验收标准与准入 Case | 原始需求 / 原型 / UI 图 / 代码 | `requirement-spec.md`、`requirement-question.md` |
| [outline-design](./outline-design/SKILL.md) | 概要设计（前后端联合，固定章节）。基于需求规格、UI 稿、原型、API 平台与现有代码，产出前后端联合的《概要设计文档》，固定章节为可行性分析/前端方案/后端方案/接口文档，前端按 Vue 页面与 .vue 组件、后端按 Go 模块/接口/MQ 概览，不下钻到详细设计 | 需求规格 / 代码 | `design-outline.md` |
| [detailed-design](./detailed-design/SKILL.md) | 前后端详细设计（后端逐模块 + 前端逐组件）。把概要设计或需求规格细化为前后端《详细设计文档》，后端 Go 按模块写领域层/接口/入口程序（含 ER、跨模块链路、变更复杂度节点表、入口验证 case），前端 Vue 按页面→组件树→逐组件写 Props/事件/接口调用/前端验收点，所有"已存在"实体都对照真实代码做真实性校验 | 概要设计 / 代码 | `design-detail.md` |
| [fullstack-development](./fullstack-development/SKILL.md) | 前后端开发（计划落盘 + TDD + 测试报告）。基于详细设计文档推进前后端开发，按模块产出 dev-plan 并用 AskUserQuestion 确认，再走 TDD（后端用 tdd-guide agent 做 Go 入口驱动单测、前端做 Vue 组件测试），每个完成模块产出 dev-test 报告并逐条映射验收标准 | 详细设计 | 代码、`dev-plan-*.md`、`dev-test-*.md` |
| [e2e-testing](./e2e-testing/SKILL.md) | Playwright 浏览器端到端测试与报告。用 Playwright 编写并执行浏览器端到端（e2e）测试，从需求规格准入 Case 或已实现功能归纳用户旅程，用语义定位写稳定用例、全新执行，产出 e2e-test-report.md 并把每条准入 Case 映射到结果 | 需求规格准入 Case / 已实现页面 | e2e 用例、`e2e-test-report.md` |

### 约定

- 文档与产物默认中文落盘，不只在对话里输出。
- 设计/开发阶段对「已存在」实体做真实性校验，禁止凭空虚构表名、接口 path、Topic/Tag、组件名。
- 模块名一律用 `<模块名>` 占位，范例统一使用中性场景，不含具体业务。

## 技术内容制作 Skills

把技术内容做成专业好看的视觉产物。

| Skill | 能力 | 主要输入 | 主要产物 |
| --- | --- | --- | --- |
| [programmer-illustration](./programmer-illustration/SKILL.md) | **技术配图生成**。把技术内容（文章、PPT 要点、架构、观点、数据）变成专业好看的配图。核心思路：**不让用户硬写提示词**，而是选一套打磨好的模板、填空、调出图 API。目标用户**审美不行、说不清要什么风格**。默认由模型替用户决定风格，不要一上来就甩「你想要哪种风格」这种用户答不上来的问题。支持 6 种风格：**科技插画风**（流程、转化链路、能力分层）、**暗色科技风**（架构、AI、安全、性能、底层系统）、**等距立体风**（系统架构、基础设施、技术栈分层、部署拓扑）、**数据卡片风**（指标、数据、对比、榜单、benchmark）、**手绘涂鸦风**（观点、踩坑、认知反差、金句传播）、**清新流程风**（多阶段业务流程、服务链路、SOP、用户旅程、运营 playbook，信息量大、要分阶段+分泳道+带循环） | 技术内容 / 主题 | 专业技术配图 PNG |
| [tech-deck](./tech-deck/SKILL.md) | **技术演示文稿生成**。把技术内容做成业内顶尖水准的 HTML 演示文稿/幻灯片。支持多种设计风格模板，产出可直接演示的 HTML 文件 | 技术内容 / PPT 要点 / 文章 | HTML 演示文稿 |
| [ppt-beautify](./ppt-beautify/SKILL.md) | **PPT 美化**。使用参考 PPT 的风格美化草稿 PPT，保留内容的同时将图片中嵌入的文字转换为可编辑的 PPT 文本，仅保留真实视觉资产（如肖像、logo、商标、截图、照片）的图片 | 草稿 PPT + 风格参考 PPT | 美化后的可编辑 PPT |

---

## 使用方式

每个 skill 目录下都有 `SKILL.md` 详细说明触发时机、工作流程、产物规范。在 Claude Code 中通过 Skill 工具调用，或按各 skill 的触发描述自动匹配使用。
