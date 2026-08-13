# 第一次把本地项目发布到 GitHub

这份指南适用于已经有本地项目、准备第一次公开或私有发布的人。顺序是：确认边界 → 本地审计 → 建立版本历史 → 创建远程仓库 → Push → 按项目类型决定是否需要 Release → 访客核验。

安装 Project Publisher 不会自动获得任何 GitHub 远程权限。创建仓库、Push、修改可见性和发布 Release 都需要明确的仓库目标与授权。

## 1. 先确认发布边界

在修改文件前写清楚：

- 谁应该使用这个项目，以及使用后能得到什么；
- 仓库名称、Owner、Public/Private 和默认分支；
- 代码、文档、数据和视觉素材分别允许怎样复用；
- 哪些本地状态、账号信息、客户材料或原始素材不得公开；
- 第一个版本要证明的核心承诺，以及能够公开的直接证据。

不确定素材权利时，先保留在本地，不要用“以后再确认”的说明把素材一起发布。

## 2. 先只读审计

在项目目录调用：

```text
使用 $project-publisher 看一下这个项目发布前还缺什么。
先只读，告诉我新访客最可能在哪一步看不懂或不想试，并列出证据、风险和必须由我决定的事项。
不要修改文件，也不要执行远程动作。
```

如果你正在维护 **Project Publisher 本仓库本身**，可以运行下面的仓库内脚本：

```bash
python3 skills/project-publisher/scripts/audit_repository.py . --json
python3 skills/project-publisher/scripts/check_secrets.py . --json
python3 skills/project-publisher/scripts/check_links.py .
python3 skills/project-publisher/scripts/review_public_surface.py . --strict
```

自动检查通过只代表没有命中已配置的阻断规则；素材权利、公开主张、Git 身份和访客体验仍需人工确认。

对于其他项目，不要照抄上面的 `skills/project-publisher/...` 路径。通过 Skills CLI 安装后，应调用 Skill，让代理从已安装的 Skill 目录使用这些脚本；普通目标项目里不会自动出现这组路径。

## 3. 建立本地版本历史

先检查当前目录：

```bash
git status
```

只有当输出明确表示“不是 Git 仓库”时，才初始化：

```bash
git init
git add .
git diff --cached --check
git commit -m "Initial public release"
git branch -M <default-branch>
```

如果已经是 Git 仓库，不要重复初始化或覆盖历史。先查看 `git status`、最近提交、作者身份和将要公开的差异。

## 4. 创建空的 GitHub 仓库

在 GitHub 新建仓库时确认：

- Owner 和仓库名称与本地文档一致；
- 可见性与前面确认的边界一致；
- Description 用一句话说清用户结果，不堆内部机制；
- 如果本地已有 README、`.gitignore` 和 LICENSE，不要让 GitHub 再生成一套；
- 暂时没有稳定主页时，Homepage 留空，不要填仓库自身 URL。

复制最终 HTTPS 或 SSH 地址，然后在本地添加：

```bash
git remote add origin https://github.com/<owner>/<repository>.git
git remote -v
git push -u origin <default-branch>
```

添加 remote 前先运行 `git remote -v`；如果已经存在 `origin`，先核对，不要直接覆盖。

## 5. 判断是否需要 Release

并非所有项目都需要 GitHub Release。只有当项目存在可下载版本、可复现快照、安装包、数据快照或需要稳定引用的里程碑时，才准备 Release 页面和资产。纯作品集、持续更新的文档或尚无版本承诺的资料库，可以先只发布默认分支并写清当前状态。

如果需要 Release，让已安装的 Skill 根据项目事实准备结构化规格和页面；不要在普通目标项目里直接调用本仓库相对路径。维护 **Project Publisher 本仓库本身** 时，才可以这样生成：

先准备结构化 Release 规格，再生成页面：

```bash
mkdir -p release
cp skills/project-publisher/assets/release/release-page.json \
  release/v0.1.0.json
# 编辑 release/v0.1.0.json，把示例值替换为这个版本的真实证据
python3 skills/project-publisher/scripts/generate_release_page.py . \
  --spec release/v0.1.0.json \
  --output release/v0.1.0.md
```

页面至少应包含：更新理由、主要变化、安装或更新命令、实际验证、兼容性、已知限制和资产名称。

发布包必须放在项目目录外：

```bash
python3 skills/project-publisher/scripts/build_release_bundle.py . \
  --output /tmp/project-v0.1.0.zip
unzip -t /tmp/project-v0.1.0.zip
```

列出并实际解压 ZIP 后，再创建标签和 Release。标签、插件或包版本、Release 页面和资产文件名必须一致。开放 PR 只是已经上传的工作，不是已经发布的版本。

已经安装并登录 GitHub CLI 时，可以在明确确认 Owner、仓库和版本后执行：

```bash
git tag v0.1.0
git push origin v0.1.0
gh release create v0.1.0 /tmp/project-v0.1.0.zip \
  --repo <owner>/<repository> \
  --title "v0.1.0" \
  --notes-file release/v0.1.0.md
```

如果不用 CLI，在 GitHub 仓库的 **Releases → Draft a new release** 中选择同一标签、粘贴生成的正文并上传已验证资产。无论哪种方式，创建标签和 Release 都是新的远程动作，需要再次确认目标与授权。

## 6. 以目标访客身份核验

公开仓库用未登录窗口核验；私有仓库用权限最小、确实属于目标读者的账号核验，不要把 Owner 视角当作访客视角。发布后检查仓库首页；如果项目需要 Release，再检查 Release 页面：

- 首屏能否看出适用对象、使用结果、直接证据和第一步；
- 中英文链接、图片、安装命令和相对链接是否正常；
- About description、Topics、License、默认分支和 Social Preview 是否正确；
- Release 标签、正文、资产名称和 GitHub 显示的 SHA-256 是否一致；
- Contributors、提交作者和最近历史是否都是有意公开的身份。

成功 Push 或 CI 通过都不能替代这一步。

## 7. 只传播已经有证据的结果

先确定想获得的是试用、问题报告、贡献、引用还是职业对话，再选择最小渠道组合。优先展示一个可复现结果、被拦住的真实失败或可解释的案例，不要把 Star 当成产品有效性的证据，也不要承诺无法维护的社区和路线图。
