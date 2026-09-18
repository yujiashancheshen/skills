# Skills

Agent 技能集合，涵盖技术内容、图表、演示文稿与 PPT 制作。每个 Skill 是一个独立目录，不绑定具体业务。

## 技术内容制作 Skills

把技术内容做成专业好看的视觉产物。

| Skill | 能力 | 主要输入 | 主要产物 |
| --- | --- | --- | --- |
| [diagram-design](./diagram-design/SKILL.md) | **编辑型图表设计**。生成架构图、流程图、时序图、数据图表等自包含 HTML/SVG，也可重绘 Mermaid 和 draw.io | 自然语言 / Mermaid / draw.io / 品牌信息 | HTML，按需导出 SVG/PNG |
| [programmer-illustration](./programmer-illustration/SKILL.md) | **技术配图生成**。把技术内容（文章、PPT 要点、架构、观点、数据）变成专业好看的配图。核心思路：**不让用户硬写提示词**，而是选一套打磨好的模板、填空、调出图 API。目标用户**审美不行、说不清要什么风格**。默认由模型替用户决定风格，不要一上来就甩「你想要哪种风格」这种用户答不上来的问题。支持 6 种风格：**科技插画风**（流程、转化链路、能力分层）、**暗色科技风**（架构、AI、安全、性能、底层系统）、**等距立体风**（系统架构、基础设施、技术栈分层、部署拓扑）、**数据卡片风**（指标、数据、对比、榜单、benchmark）、**手绘涂鸦风**（观点、踩坑、认知反差、金句传播）、**清新流程风**（多阶段业务流程、服务链路、SOP、用户旅程、运营 playbook，信息量大、要分阶段+分泳道+带循环） | 技术内容 / 主题 | 专业技术配图 PNG |
| [tech-deck](./tech-deck/SKILL.md) | **技术演示文稿生成**。把技术内容做成业内顶尖水准的 HTML 演示文稿/幻灯片。支持多种设计风格模板，产出可直接演示的 HTML 文件 | 技术内容 / PPT 要点 / 文章 | HTML 演示文稿 |
| [ppt-beautify](./ppt-beautify/SKILL.md) | **PPT 美化**。使用参考 PPT 的风格美化草稿 PPT，保留内容的同时将图片中嵌入的文字转换为可编辑的 PPT 文本，仅保留真实视觉资产（如肖像、logo、商标、截图、照片）的图片 | 草稿 PPT + 风格参考 PPT | 美化后的可编辑 PPT |
| [wx-writer](./wx-writer/SKILL.md) | **固定个人风格的公众号写作与改稿**。由它主导选题、提纲、正文、改稿和 HTML，并在开稿前、初稿后调用 `human-writing` 做写作质量检查 | 选题 / 素材 / 已有文章 | 文章正文、公众号兼容 HTML |

## 上游 Skill

### wx-writer 的写作依赖

使用 `wx-writer` 时需同时安装 [`human-writing`](https://github.com/KKKKhazix/human-writing)。该依赖不包含在本仓库中，应按上游说明安装仓库内的 `human-writing/` 技能目录。

- 当前配合使用的版本：`1.1.0`
- 上游固定提交：[`4fda173f3fef7fb808f3eba991eeb2528ea4b189`](https://github.com/KKKKhazix/human-writing/commit/4fda173f3fef7fb808f3eba991eeb2528ea4b189)
- 上游保持原样，个人风格和兼容约定记录在 `wx-writer` 中。
- `wx-writer` 主导流程，在开稿阶段加载写作规则，初稿后调用审阅；`human-writing` 不直接覆盖稿件。明显的新冲突先向用户说明并确认。

### diagram-design 的来源

`diagram-design/` 是从上游仓库指定 commit 导入的原样快照，当前不包含本地修改。

- 上游仓库：<https://github.com/cathrynlavery/diagram-design>
- 上游目录：`skills/diagram-design`
- 分支：`main`
- Commit：[`2724fd2efd8c6737f6fa704fbf5da52d67375497`](https://github.com/cathrynlavery/diagram-design/commit/2724fd2efd8c6737f6fa704fbf5da52d67375497)

---

## 使用方式

每个 skill 目录下都有 `SKILL.md` 详细说明触发时机、工作流程、产物规范。在 Claude Code 中通过 Skill 工具调用，或按各 skill 的触发描述自动匹配使用。
