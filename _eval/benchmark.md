# 触发量化验证报告（trigger benchmark）

/ 方法：按官方 skill-creator「How skill triggering works」，用 3 个独立 subagent 仅凭 5 个 skill 的 name+description 对 18 条查询做路由判定，跑 3 次测稳定性，对照 ground truth。
/ 维度：本轮验证的是 **description 触发维度**（正例能否触发正确 skill、near-miss 负例能否正确拒绝），不涉及产出文档质量维度。

## 总指标

| 指标 | 数值 |
|---|---|
| 正例触发命中率（10 条） | 100%（10/10） |
| 负例正确拒绝率（8 条 near-miss） | 100%（8/8） |
| 三次运行一致性 | 100%（54/54 判定完全一致） |
| 总准确率 | 100%（54/54） |

## 逐条结果（3 次一致）

| id | 查询要点 | ground truth | 3 次判定 | 命中 |
|---|---|---|---|---|
| 1 | PRD+原型整理成可评审需求规格、澄清歧义 | clarifying-requirements | clarifying ×3 | ✅ |
| 2 | 需求自相矛盾、核对代码冲突、梳理要做啥 | clarifying-requirements | clarifying ×3 | ✅ |
| 3 | 编码前整体技术方案、前端页面/后端模块/接口MQ概览 | outline-design | outline ×3 | ✅ |
| 4 | 画 ER 图与重点流程时序、概要设计稿 | outline-design | outline ×3 | ✅ |
| 5 | 细化接口入参返回、变更复杂度、前端逐组件 | detailed-design | detailed ×3 | ✅ |
| 6 | tech-spec 写细到可直接开发、后端模块前端组件 | detailed-design | detailed ×3 | ✅ |
| 7 | 设计就绪开始写代码、TDD、先出开发计划 | fullstack-development | fullstack ×3 | ✅ |
| 8 | 按详细设计实现、后端 go 入口单测、前端 vue 组件 | fullstack-development | fullstack ×3 | ✅ |
| 9 | 用 playwright 关键流程端到端测出报告 | e2e-testing | e2e ×3 | ✅ |
| 10 | 回归用户旅程、浏览器层面验证 | e2e-testing | e2e ×3 | ✅ |
| 11 | 给已有函数补几个单测（难负例 vs fullstack） | none | none ×3 | ✅ |
| 12 | SQL 加索引优化 | none | none ×3 | ✅ |
| 13 | review go 代码并发安全 | none | none ×3 | ✅ |
| 14 | 查日志定位线上 500 | none | none ×3 | ✅ |
| 15 | 讲解 Playwright API 区别（难负例 vs e2e） | none | none ×3 | ✅ |
| 16 | 改 Vue 组件样式深色模式（难负例 vs 前端） | none | none ×3 | ✅ |
| 17 | 从零写全新 PRD（难负例 vs clarifying） | none | none ×3 | ✅ |
| 18 | markdown 导出 pdf | none | none ×3 | ✅ |

## 结论

- 5 个 skill 的中文 description 在触发维度表现满分：正例稳定触发到正确环节，4 个刻意设计的 near-miss 负例（#11 补单测、#15 Playwright 知识问答、#16 改样式、#17 写新 PRD）全部被正确拒绝，无误触发、无环节串台。
- 流水线相邻环节（概要↔详细、详细↔开发）边界清晰，未出现互相误判。
- 三次零抖动，说明 description 区分度足够、不依赖随机性。

## 后续可选

如需更强验证，可再做 **产出质量维度** benchmark：对每个 skill 各跑 with-skill vs baseline（无 skill）子 agent 执行真实设计/开发任务，用断言对产物打分。该维度成本较高（需真实执行多步任务），本轮未覆盖。
