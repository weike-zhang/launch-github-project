<p align="center">
  <img src="assets/hero.zh-CN.png" alt="Project Publisher 审查、定位、发布项目，并让公开材料跟上后续更新" width="100%">
</p>

<p align="center">
  <strong>项目已经变了，README、Release 和宣发内容还停在旧版本。Project Publisher 先找出哪里没跟上，再补你同意补的公开材料；远程操作仍由你决定。</strong>
</p>

<p align="center">
  <a href="#先找出最影响传播的缺口">先找出最影响传播的缺口</a> ·
  <a href="examples/self-audit-bundle-safety.md">看它抓到的发布包泄漏</a> ·
  <a href="README.md">English</a>
</p>

很多项目不是做不出来，而是公开以后没人看懂、没人愿意试：名字只说了一个小功能，README 从维护者视角开场，安装入口藏得太深，Release 只列改动，项目更新以后旧文案还在继续传播。

Project Publisher 负责项目对外发布后的整套工作：审查现状、梳理名字和定位、准备最小可用的发布材料、把真实证据变成宣发内容，并在后续更新时重新对齐 README、Release 和公开承诺。第一轮只读，先告诉你最值得处理的缺口。

软件、Agent Skill、数据集、研究、课程、设计资源、作品集和混合项目都能用；它不会把不同项目硬塞进同一套模板。改文件和操作 GitHub 仍然需要你的明确授权。

从公开仓库安装 Project Publisher 和随包的 Humanizer：

```bash
git clone https://github.com/weike-zhang/project-publisher.git
python3 project-publisher/scripts/install.py
```

集成安装器会一次加入 Project Publisher、随包的 Humanizer 和依赖提醒 Hook，并检查必需的命令行工具。安装后需要在 `/hooks` 中审查并信任该 Hook，安装器不会代替用户授权。Project Publisher 会先固定事实、命令和证据边界，再调用 Humanizer。如果某项依赖安装失败、被拒绝或当前宿主不可用，它会在进入相关阶段时说明受影响的证据和降级路径。[查看完整安装路径与边界](docs/INSTALL.zh-CN.md)。

然后对 Codex 说：`使用 $project-publisher 看一下这个项目现在对外讲得清不清楚。先只读，告诉我最影响传播的一个问题。` 第一轮不会改文件。

v0.3.0 已经从干净临时目录完成[公网克隆、集成安装和 Skills CLI 发现验证](evals/results/public-install-v0.3.0.md)；[Codex 首次审计记录对应旧名称下已经发布的 v0.2.0 Skills-only 路径](evals/results/codex-first-audit-v0.2.0.md)。

## 别把项目外的文件一起发出去

这个 Skill 给自己的仓库做发布体检时，发现项目里的符号链接可以读取项目目录之外的文件。旧版本会把文件内容装进 ZIP。

```text
project/
├── README.md
└── outside.txt -> /etc/hosts

停止打包：outside.txt 是符号链接
ZIP 没有生成，目标文件没有读取
```

现在遇到这类链接会直接停止打包，目标文件不会被读取。发布体检还会检查你最终交出去的 ZIP。

[看完整复现、根因和限制](examples/self-audit-bundle-safety.md) · [看旧名称下修复该问题的 v0.1.2 Release](https://github.com/weike-zhang/launch-github-project/releases/tag/v0.1.2)

## 先找出最影响传播的缺口

下面这条公网安装路径已经从干净目录验证：

```text
使用 $project-publisher 看一下这个项目现在对外讲得清不清楚。
先只读，告诉我新访客最可能在哪一步看不懂或不想试、判断依据是什么，
以及最小的修改范围。
没有我的明确授权，不要执行远程动作。
```

第一轮只读检查会返回一份这样的结果：

```text
主要类型        Agent Skill
已经具备        SKILL.md、安装入口、脚本、发布历史
主要缺口        首屏没有直接证据，访客看不出用了会怎样
发布阻断        插件版本和最新 Release 对不上
需要你拍板      素材权利、仓库可见性、准确远程目标
本轮已执行      无；只读审计
```

具体结果会随仓库变化。Skill 会先核对事实并说明需要改什么，远程操作则逐项等待授权。

## 它会处理哪些问题

| 现在的问题 | 改完以后 |
| --- | --- |
| 名字只描述一个示例、平台或发布阶段 | 用熟悉的词说清长期角色，剩余精度交给简介和证据 |
| README 像功能清单，用户看不出和自己有什么关系 | 开头先讲用户处境、能得到什么、证据在哪、第一步怎么做 |
| 项目已经更新，README 还在教旧功能和旧命令 | 改完项目后重新通读现有 README；需要更新就直接覆盖旧内容，不另放一份建议稿 |
| 每个小节都塞一张图，中文还可能错字或变形 | 默认只保留头图；路径和短输出用代码块，有真实数据才生成图表 |
| 项目里哪些能公开、哪些不能公开，全靠猜 | 给出脱敏密钥发现、公开风险和必须确认的素材权利 |
| 测试一通过，就被包装成“产品有效” | 把发布完整性、行为证据、用户采用和流行度分开讲，不互相冒充 |
| Release 页面靠手写，版本一多就漂 | 从结构化证据生成页面，图片、说明、安装、兼容性和限制跟着版本走 |
| 源码 ZIP 里可能混入缓存、私有状态甚至越界文件 | 生成确定性发布包，拒绝符号链接，并真的列出、解压、复核 |
| 本地、PR、Tag、Release 各说各话 | 上线前核对四个状态，不把“已经上传”包装成“已经发布” |
| 宣发只是宣布“项目上线了” | 先拿出有用结果、抓到的失败或可复现证据，再决定在哪传播 |

软件、Agent Skill、数据集、研究、课程、设计资源、作品集和混合项目都能用。它不会强迫所有项目套同一份模板，也不会为了显得成熟，硬造网站、社区、基准测试和路线图。

## 自动检查和人工判断

| 自动检查 | 仍然必须有人判断 |
| --- | --- |
| 本地链接、占位符、机器路径 | 第一屏到底有没有让目标用户产生兴趣 |
| 脱敏密钥模式 | 命中的内容到底是不是秘密或个人信息 |
| 嵌套仓库、编辑器文件、内部草稿、身份设置文案 | 图片、数据和截图有没有权利公开 |
| Release 页面是否陈旧、语义版本是否一致 | 证据够不够支撑对外承诺 |
| ZIP 内容、符号链接、确定性和实际解压 | 这个仓库该不该公开、应该发到哪里 |

扫描全绿只表示自动门禁通过。项目是否安全、好用或有需求，仍需其他证据。

## 项目公开以后仍然继续

1. 只读检查文件、Git 状态、风险和缺口。
2. 判断项目类型，并核对名字和一句话承诺是否匹配长期角色。
3. 用真实输入输出、截图或复现步骤支撑公开主张。
4. 检查链接、密钥、公开内容、图片、版本和实际 ZIP。
5. 准备 Release 和有证据的宣发材料，只执行得到明确授权的远程操作。
6. 发布后以访客身份检查结果；项目变化后再同步更新公开材料。

## 兼容性与验证状态

| 使用面 | 当前状态 | 证据 |
| --- | --- | --- |
| 公开 v0.2.0：全局安装 → 调用 → 首次审计 | Codex CLI 0.147.0-alpha.6.5 已验证 | [安装、干净夹具和实测输出](evals/results/codex-first-audit-v0.2.0.md#post-publication-check) |
| 旧名称下的本地 0.2.0 候选版：项目级安装 → 调用 → 首次审计 | 发布前在同一客户端已验证 | [候选版夹具、命令和脱敏输出](evals/results/codex-first-audit-v0.2.0.md#release-candidate-check) |
| 公开 v0.3.0：克隆 → 集成安装 → Skills CLI 发现 | 仓库改名后已验证 | [干净临时目录验证](evals/results/public-install-v0.3.0.md) |
| 发布脚本 | 已发布 v0.2.0 路径在 Python 3.12 验证 | [回归测试](tests/test_release_tools.py)与 [旧仓库路径下的 GitHub Actions](https://github.com/weike-zhang/launch-github-project/actions/workflows/validate.yml) |
| 项目类型路径与评估文件 | 只验证结构完整 | [夹具校验器](evals/validate_fixtures.py)，不是模型质量分数 |
| 传播行为 | 只有一组探索性对照 | [完整输入、基线、Skill 响应与限制](evals/results/model-comparison.md) |
| 其他 Agent Skills 客户端 | 未验证 | 欢迎提交包含客户端和版本的实测报告 |

## 权限与限制

- 安装 Skill 不等于允许它建仓库、Push、改可见性、发 Release 或替你发帖。每一个远程动作都要有准确目标和明确授权。
- 密钥扫描靠规则匹配，不能替代人工判断。
- 打包器会拒绝符号链接和非常规文件，但它不是抵御恶意并发替换的通用沙箱。
- 自动检查不能证明素材权利、隐私安全、产品质量、用户采用或未登录页面渲染。
- 工作笔记放进 `.project-publisher/`；这个目录默认忽略，也不会进入发布包。

完整边界见 [PRIVACY.md](PRIVACY.md)、[SECURITY.md](SECURITY.md)、[视觉素材说明](assets/ASSET-NOTICE.md)和[第三方依赖说明](THIRD-PARTY-NOTICES.md)。

## 贡献可复现的失败案例

最有价值的贡献是可复现的发布失败，例如项目类型分类错误、首次使用流程中断，或公开主张缺少可核验的证据。参见 [CONTRIBUTING.md](CONTRIBUTING.md)。

MIT 许可。作者：[Weike Zhang](https://github.com/weike-zhang)。
