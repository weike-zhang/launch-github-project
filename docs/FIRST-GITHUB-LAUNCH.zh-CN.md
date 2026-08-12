# 第一次把项目发布到 GitHub：新手操作指南

这份指南按“本地准备 → GitHub 网页建仓 → 第一次 Push → 发布后维护”排列。所有远程操作都需要你自己登录并确认；本项目不会替你创建仓库或修改账号。

## 1. 先整理个人资料

你已经决定使用展示名 **Weike Zhang**，并计划把登录名改成 **weike-zhang**。建议资料先采用：

- Name：`Weike Zhang`
- Bio：`Building grounded AI tools and open-source workflows for learning, shipping, and sharing.`
- URL：先留空，等有稳定主页再填
- Avatar：使用你愿意公开长期使用的头像；不要直接上传带私人信息的照片

改用户名时，GitHub 会尝试保留旧链接跳转，但外部引用、包管理器、签名和本地 remote 仍应检查。改完后重新打开个人主页，确认新 URL 可访问。

## 2. 在 GitHub 网页创建空仓库

1. 右上角 `+` → `New repository`。
2. 先看 Owner。如果仍显示 `mumianwei`，推荐先把 GitHub 登录名改为 `weike-zhang`，刷新建仓页后再继续。
3. 按下表逐项填写，不需要自行改写。

### Grounded AI Mentor

| 页面字段 | 精确填写值 |
| --- | --- |
| Owner | `weike-zhang` |
| Repository name | `grounded-ai-mentor` |
| Description | `A zero-assumption AI mentor that teaches computer science and AI through the projects learners actually build.` |
| Choose visibility | 已确认火焰图片公开使用权则选 `Public`；否则选 `Private` |
| Add README | `Off` |
| Add .gitignore | `No .gitignore` |
| Add license | `No license` |

Repository name 不要填带空格的 `Grounded AI Mentor`，否则 GitHub 会生成大写的 `Grounded-AI-Mentor`，与已有 Skill 名和链接不一致。

### Launch GitHub Project

| 页面字段 | 精确填写值 |
| --- | --- |
| Owner | `weike-zhang` |
| Repository name | `launch-github-project` |
| Description | `Prepare any project for a safe, evidence-based GitHub launch: README, risk checks, release bundle, and goal-driven distribution.` |
| Choose visibility | `Public` |
| Add README | `Off` |
| Add .gitignore | `No .gitignore` |
| Add license | `No license` |

`No .gitignore` 和 `No license` 在这一页的意思是“不让 GitHub 自动新建”。两个本地项目都已经包含 `.gitignore` 和 MIT `LICENSE`，不是没有这些文件。

4. 点击 `Create repository`。
5. 创建后复制 HTTPS 或 SSH 地址，但先不要执行网页建议的二次初始化命令。

## 3. 本地第一次提交

在项目目录执行：

```bash
git init
git add .
git diff --cached --check
git commit -m "Initial public release"
git branch -M main
git remote add origin https://github.com/weike-zhang/<repository>.git
git push -u origin main
```

如果目录已经是 Git 仓库，不要再次 `git init`；先运行 `git status`，确认没有不属于本次发布的文件。推送前再次运行密钥扫描：

```bash
python skills/launch-github-project/scripts/check_secrets.py . --json
```

## 4. 发布页与仓库设置

Push 成功后，在仓库 `Settings` 中检查：

- About 的 description、topics、网站地址；
- `Issues` 是否开启，以及是否需要 Issue 模板；
- `Discussions` 是否真的有人维护；没有维护能力时先不开；
- 默认分支为 `main`；
- Security policy 指向 `SECURITY.md`；
- License 显示与仓库文件一致。

首个 Release 可在 `Releases` → `Draft a new release` 创建，标签使用 `v0.1.0`，复制 `release/v0.1.0.md`。Release 只发布已经本地验证过的 ZIP 或源码，不要把 `.env`、私有状态目录和原始个人素材上传。

## 5. 第一次传播怎么规划

不要先排“第 1 天、第 2 天”的固定日历。先回答三个问题：

1. 你想要的是真实试用、贡献者、反馈，还是个人品牌？
2. 哪一个证据已经能公开：行为对照、可复现命令、视觉预览、案例还是数据卡？
3. 你真正会维护哪些渠道？

然后只选一条主路径：一个可点击仓库入口 + 一份与证据匹配的短内容 + 一个明确的反馈入口。传播材料模板在 `release/` 和 `skills/launch-github-project/assets/distribution/`。

## 6. 发布后的最小维护承诺

公开前写清楚支持范围、兼容性状态、隐私边界和下一步。收到 Issue 后，优先修复会阻止首次成功运行的问题；不要为了星标数量承诺无法维护的路线图。
