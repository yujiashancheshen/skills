# skills

通用研发流水线 Skill 集合，每个 Skill 是一个独立目录，**不绑定具体业务**。技术栈默认：后端 Go 多模块、前端 Vue、e2e 用 Playwright。

## 流水线

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

## Skills

| Skill | 作用 | 主要输入 | 主要产物 |
| --- | --- | --- | --- |
| [clarifying-requirements](./clarifying-requirements/SKILL.md) | 需求澄清，整理可评审的需求规格 | 原始需求 / 原型 / UI 图 / 代码 | `requirement-spec.md`、`requirement-question.md` |
| [outline-design](./outline-design/SKILL.md) | 概要设计（前后端联合，固定章节） | 需求规格 / 代码 | `design-outline.md` |
| [detailed-design](./detailed-design/SKILL.md) | 前后端详细设计（后端逐模块 + 前端逐组件） | 概要设计 / 代码 | `design-detail.md` |
| [fullstack-development](./fullstack-development/SKILL.md) | 前后端开发（计划落盘 + TDD + 测试报告） | 详细设计 | 代码、`dev-plan-*.md`、`dev-test-*.md` |
| [e2e-testing](./e2e-testing/SKILL.md) | Playwright 浏览器端到端测试与报告 | 需求规格准入 Case / 已实现页面 | e2e 用例、`e2e-test-report.md` |

## 约定

- 文档与产物默认中文落盘，不只在对话里输出。
- 设计/开发阶段对「已存在」实体做真实性校验，禁止凭空虚构表名、接口 path、Topic/Tag、组件名。
- 模块名一律用 `<模块名>` 占位，范例统一使用中性场景，不含具体业务。
