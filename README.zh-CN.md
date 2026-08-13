# Launch GitHub Project

**把本地项目变成陌生访客能看懂、能试用、能验证的 GitHub 发布。**

[English](README.md) · [安装](docs/INSTALL.zh-CN.md) · [首次发布指南](docs/FIRST-GITHUB-LAUNCH.zh-CN.md) · [最新 Release](https://github.com/weike-zhang/launch-github-project/releases/latest)

当项目已经能在本地使用，但公开发布面仍不确定时，可以使用这个 Agent Skill：README 没说清使用结果；通用清单把所有项目都当成软件应用；公开主张与证据对不上；或者本地版本、开放 PR、默认分支和 Release 已经发生漂移。

Launch GitHub Project 会先只读审计，再判断项目类型，只准备访客做出判断、尝试使用和核验证据确实需要的材料。它可以拦截高风险公开文件并生成确定性的 ZIP，但不会把“扫描干净”冒充成安全、采用或质量证明。所有远程动作都需要明确目标和明确授权。

**安装前先看证据：** [真实自审与修复](examples/self-audit-bundle-safety.md) · [v0.1.2 Release 与 ZIP](https://github.com/weike-zhang/launch-github-project/releases/tag/v0.1.2) · [已公开的试运行输入与输出](evals/results/model-comparison.md)

## 安装并调用

```bash
npx skills add weike-zhang/launch-github-project --skill launch-github-project -g
```

然后在要准备发布的项目中调用：

```text
使用 $launch-github-project 审计这个项目的 GitHub 发布面。
先只读，告诉我这个项目类型真正需要的最小公开面、每项主张的证据，
以及发布前必须由我决定的事项。没有我的明确授权，不要执行远程动作。
```

本地检出、校验和更新命令见[安装文档](docs/INSTALL.zh-CN.md)。

第一次响应应该先判断项目类型，分开事实与假设，列出有理由生成的最小公开材料，为每项公开主张挂上证据，并在任何远程动作前停下来等待决定。如果一上来就编辑文件或默认生成所有材料，请停止执行并反馈客户端及版本；当前项目尚未声称所有 Agent Skills 客户端的行为都已经验证。

## 项目会发生什么变化

| 当前状态 | Skill 产生的结果 |
| --- | --- |
| 所有项目套同一个 README 模板 | 根据软件、Agent Skill、数据集、研究、课程、设计资源、作品集或其他真实项目类型组织读者路径和证据 |
| 不确定哪些文件可以公开 | 在打包前给出脱敏的密钥发现、公开面阻断项和必须确认的素材权利 |
| 把脚本通过写成产品效果证明 | 把发布完整性、行为证据、采用证据和流行度分开报告 |
| 本地版本、开放 PR、默认分支和 Release 不一致 | 生成 Release 页面并显式核对发布状态，不把“已经上传”写成“已经发布” |
| 传播从排日历或求 Star 开始 | 根据真正目标、受众和已有证据选择最小传播路径 |

它可以按需准备 README、安装或复现步骤、示例、数据卡、方法、视觉预览、隐私与许可说明、Release 页面、发布 ZIP 或传播简报；不会默认把全部文件都生成一遍。

<img src="assets/hero.png" alt="Launch GitHub Project 的审计、证据、打包与发布工作流" width="760">

## 本仓库的真实证据

这个项目已经用自己审计过自己。第一次自审发现：文件符号链接可能把项目外的字节写入发布 ZIP。0.1.2 会在读取前拒绝文件和目录符号链接，同时明确保留尚未消除的并发替换边界。

- [复现、根因、修复与限制](examples/self-audit-bundle-safety.md)
- [v0.1.2 Release 页面与已验证 ZIP](https://github.com/weike-zhang/launch-github-project/releases/tag/v0.1.2)
- [已公开输入、响应对照与限制的传播试运行](evals/results/model-comparison.md)

这只是一组探索性对照，不是基准测试，也不能预测 Star、采用或传播效果。

## 证据与兼容性

| 使用面 | 状态 | 证据 |
| --- | --- | --- |
| Skills CLI 仓库发现 | 已验证 | 可以从公开仓库发现可安装的 `launch-github-project` Skill |
| 发布工具回归 | Python 3.12 已验证 | [测试](tests/test_release_tools.py)与 [GitHub Actions](https://github.com/weike-zhang/launch-github-project/actions/workflows/validate.yml) |
| 夹具与类型路径覆盖 | 仅发布完整性 | `python3 evals/validate_fixtures.py`，不是模型质量分数 |
| 传播行为 | 仅探索性证据 | 一组已公开[输入与基线/Skill 响应](evals/results/model-comparison.md)的对照 |
| 其他 Agent Skills 客户端 | 未验证 | 欢迎提交兼容性报告 |

## 权限与限制

- 密钥发现基于规则匹配，仍需人工判断；输出不会回显完整匹配值。
- 自动检查不能证明素材权利、隐私安全、产品质量或用户采用。
- 发布打包器会拒绝符号链接和非常规文件，但它不是抵御恶意并发替换的通用沙箱。
- 安装 Skill 不代表已经允许它创建仓库、Push、修改可见性、发布 Release 或向外部平台发帖；每个远程动作都需要明确目标和授权。
- 工作笔记应放在 `.launch-github-project/`，该目录默认被 Git 忽略，也不会进入发布包。

完整边界见 [PRIVACY.md](PRIVACY.md)、[SECURITY.md](SECURITY.md)和[视觉素材说明](assets/ASSET-NOTICE.md)。

## 工作方式

![先审计、分类、证明和打包，再明确交接远程动作](assets/launch-flow.svg)

1. 先只读检查事实、风险、缺口和 Git 状态。
2. 先判断主要项目类型，再选择公开材料。
3. 为核心承诺建立读者路径和直接证据。
4. 验证链接、密钥、公开面、版本信息和发布包。
5. 只交接或执行得到明确授权的远程动作，最后以未登录访客身份核验结果。

## 贡献与许可

最有价值的贡献是可复现的发布失败、当前分类没有处理好的项目类型，或无法核验证据的公开主张。参见 [CONTRIBUTING.md](CONTRIBUTING.md)。

MIT 许可。Built by [Weike Zhang](https://github.com/weike-zhang)。
