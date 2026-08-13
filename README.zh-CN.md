# Launch GitHub Project

**别让一个能打的项目，死在 README、Release 和一张没人想点开的封面上。**

很多项目不是做得差，而是发布得太像内部资料：开头全是架构，安装入口藏在后面，没有截图，没有证据，Release 只剩一串更新清单。访客没看完开头，就关掉页面。

Launch GitHub Project 专门收拾这个烂摊子。它先把项目审一遍，再把 README、视觉证据、安装路径、Release 页面和发布包理顺。先拿证据，再讲故事；没有授权，绝不碰远程仓库。

**两步开始：**

```bash
npx skills add weike-zhang/launch-github-project --agent codex --skill launch-github-project -g -y
```

然后对 Codex 说：`使用 $launch-github-project 给这个项目做一次 GitHub 发布体检。先只读。`

**别先听我吹，直接看证据：** [它真抓到过的发布漏洞](examples/self-audit-bundle-safety.md) · [Codex 首次审计实测](evals/results/codex-first-audit-v0.2.0.md) · [最新 Release](https://github.com/weike-zhang/launch-github-project/releases/latest)

<p align="center">
  <img src="assets/hero.zh-CN.png" alt="Launch GitHub Project 把能运行的本地项目经过审计、证明、打包与核验，变成别人看得懂、试得动、查得到证据的公开发布" width="100%">
</p>

<p align="center">
  <a href="README.md">English</a> ·
  <a href="docs/INSTALL.zh-CN.md">安装方式</a> ·
  <a href="docs/FIRST-GITHUB-LAUNCH.zh-CN.md">首次发布指南</a> ·
  <a href="https://github.com/weike-zhang/launch-github-project/releases/latest">Release</a>
</p>

<p align="center">
  <a href="https://github.com/weike-zhang/launch-github-project/actions/workflows/validate.yml"><img alt="校验状态" src="https://github.com/weike-zhang/launch-github-project/actions/workflows/validate.yml/badge.svg"></a>
  <a href="https://github.com/weike-zhang/launch-github-project/releases/latest"><img alt="最新版本" src="https://img.shields.io/github/v/release/weike-zhang/launch-github-project"></a>
  <a href="LICENSE"><img alt="MIT 许可" src="https://img.shields.io/badge/license-MIT-52D6A3"></a>
</p>

## 不是讲概念：它真抓到过一个越界打包漏洞

<img src="assets/audit-proof.zh-CN.png" alt="一次真实自审：被 Git 跟踪的符号链接离开项目目录，发布被阻断，修复后通过回归测试并公开剩余边界" width="100%">

第一次拿自己开刀，它就发现了一个真问题：仓库里一个看起来正常的文件，实际上可能通过符号链接，把项目外的内容塞进发布 ZIP。

现在，打包器会在读取前拒绝文件和目录符号链接；回归测试把修复钉死；尚未消除的并发替换风险也明确写进文档。不是一句“安全可靠”，而是把事故、修复和边界一起摆出来。

[看完整复现、根因和限制](examples/self-audit-bundle-safety.md) · [看修复该问题的 v0.1.2 Release](https://github.com/weike-zhang/launch-github-project/releases/tag/v0.1.2)

## 两步，先给项目做一次发布体检

```text
使用 $launch-github-project 审计这个项目的 GitHub 发布面。
先只读，判断项目类型、真正需要的最小公开面、每项主张背后的证据，
以及发布前必须由我决定的事项。没有我的明确授权，不要执行远程动作。
```

它不会一上来就乱改文件，也不会先问你十几个问题。第一轮应该先给出这样的体检单：

```text
主要类型        Agent Skill
已经具备        SKILL.md、安装入口、脚本、发布历史
最伤转化        首屏没有直接证据，访客看不出用了会怎样
发布阻断        插件版本和最新 Release 对不上
需要你拍板      素材权利、仓库可见性、准确远程目标
本轮已执行      无——只读审计
```

具体结果会随仓库变化，但顺序不会变：先看事实，再找缺口；先说明为什么要改，再动手；远程操作必须逐项授权。

## 它到底会把什么改好

| 现在的问题 | 改完以后 |
| --- | --- |
| README 像功能清单，用户看不出和自己有什么关系 | 开头先讲用户处境、能得到什么、证据在哪、第一步怎么做 |
| 项目里哪些能公开、哪些不能公开，全靠猜 | 给出脱敏密钥发现、公开面阻断项和必须确认的素材权利 |
| 测试一通过，就被包装成“产品有效” | 把发布完整性、行为证据、用户采用和流行度分开讲，不互相冒充 |
| Release 页面靠手写，版本一多就漂 | 从结构化证据生成页面，图片、说明、安装、兼容性和限制跟着版本走 |
| 源码 ZIP 里可能混入缓存、私有状态甚至越界文件 | 生成确定性发布包，拒绝符号链接，并真的列出、解压、复核 |
| 本地、PR、Tag、Release 各说各话 | 上线前核对四个状态，不把“已经上传”包装成“已经发布” |

软件、Agent Skill、数据集、研究、课程、设计资源、作品集和混合项目都能用。它不会强迫所有项目套同一份模板，也不会为了显得成熟，硬造网站、社区、基准测试和路线图。

## 能自动拦的交给机器，必须拍板的留给人

| 自动检查 | 仍然必须有人判断 |
| --- | --- |
| 本地链接、占位符、机器路径 | 第一屏到底有没有让目标用户产生兴趣 |
| 脱敏密钥模式 | 命中的内容到底是不是秘密或个人信息 |
| 嵌套仓库、编辑器文件、内部草稿、身份设置文案 | 图片、数据和截图有没有权利公开 |
| Release 页面是否陈旧、语义版本是否一致 | 证据够不够支撑对外承诺 |
| ZIP 内容、符号链接、确定性和实际解压 | 这个仓库该不该公开、应该发到哪里 |

扫描全绿，只能说明门禁通过；不能证明项目安全、好用，更不能证明有人需要。

## 从“本地能跑”到“公开能打”

1. 先只读：检查文件、Git 状态、风险和缺口。
2. 再分类：先搞清项目是什么，再决定需要哪些发布材料。
3. 亮证据：把核心承诺和真实输入、输出、截图或复现步骤连起来。
4. 做发布：验证链接、密钥、公开内容、图片、版本和真实 ZIP。
5. 上线前：生成 Release 页面，只执行得到明确授权的远程动作。
6. 上线后：站在陌生访客视角，再验一次仓库首页和 Release。

## 兼容性：哪些已经验证，哪些绝不吹

| 使用面 | 当前状态 | 证据 |
| --- | --- | --- |
| 公开 v0.2.0：全局安装 → 调用 → 首次审计 | Codex CLI 0.147.0-alpha.6.5 已验证 | [安装、干净夹具和实测输出](evals/results/codex-first-audit-v0.2.0.md#post-publication-check) |
| 本地 0.2.0 候选版：项目级安装 → 调用 → 首次审计 | 发布前在同一客户端已验证 | [候选版夹具、命令和脱敏输出](evals/results/codex-first-audit-v0.2.0.md#release-candidate-check) |
| 发布脚本 | Python 3.12 已验证 | [回归测试](tests/test_release_tools.py)与 [GitHub Actions](https://github.com/weike-zhang/launch-github-project/actions/workflows/validate.yml) |
| 项目类型路径与评估文件 | 只验证结构完整 | [夹具校验器](evals/validate_fixtures.py)，不是模型质量分数 |
| 传播行为 | 只有一组探索性对照 | [完整输入、基线、Skill 响应与限制](evals/results/model-comparison.md) |
| 其他 Agent Skills 客户端 | 未验证 | 欢迎提交包含客户端和版本的实测报告 |

## 权限与限制：没授权，不碰你的 GitHub

- 安装 Skill 不等于允许它建仓库、Push、改可见性、发 Release 或替你发帖。每一个远程动作都要有准确目标和明确授权。
- 密钥扫描靠规则匹配，不能替代人工判断。
- 打包器会拒绝符号链接和非常规文件，但它不是抵御恶意并发替换的通用沙箱。
- 自动检查不能证明素材权利、隐私安全、产品质量、用户采用或未登录页面渲染。
- 工作笔记放进 `.launch-github-project/`；这个目录默认忽略，也不会进入发布包。

完整边界见 [PRIVACY.md](PRIVACY.md)、[SECURITY.md](SECURITY.md)和[视觉素材说明](assets/ASSET-NOTICE.md)。

## 想贡献？别夸，直接拿失败案例来

最有价值的贡献不是一句“很棒”，而是一个能复现的发布失败：哪种项目被分类错了、哪条首次使用路径走不通、哪项公开主张找不到证据。参见 [CONTRIBUTING.md](CONTRIBUTING.md)。

MIT 许可。Built by [Weike Zhang](https://github.com/weike-zhang)。
