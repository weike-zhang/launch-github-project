# 安装

这个版本已经验证的要求：

- 使用 Git 下载和检查仓库；
- 使用 Python 3.10 或更高版本运行集成安装器、内置审计、Release 页面和打包脚本；
- 只有选择“仅安装 Skills”的备选方式时才需要 Node.js 和 `npx`。

## 推荐安装

下面的命令要等远程仓库得到授权并改名为 `project-publisher` 后才成为公网安装路径。在此之前请使用当前本地检出，文档不把新远程地址写成已经发布。

```bash
git clone https://github.com/weike-zhang/project-publisher.git
python3 project-publisher/scripts/install.py
```

这个集成安装路径会一次安装 Project Publisher 和随包提供的 Humanizer，检查必需的命令行工具，安装依赖提醒 Hook，并记录每个组件的状态。安装后在 Codex 中打开 `/hooks`，审查 `dependency-guard`，确认接受源码后再信任它。Codex 不允许安装器代替用户授予这项信任。

Project Publisher 只在事实稿稳定后用 File mode 或 Embedded mode 调用 Humanizer。主 Skill 会在真正进入对应阶段时再检查依赖。如果安装失败、用户拒绝 Hook，或当前宿主没有暴露某个伴随能力，Project Publisher 必须说明哪项证据受影响以及可用的降级路径，不得静默跳过。

新的集成路径已用当前本地候选版和解压后的 Release ZIP 验证：两个 Skills 均已安装，必需工具通过预检，Hook 已注册为等待信任，重复执行不会重复写入。下一个版本发布前，它还不是已发布的公网路径。之前 v0.2.0 的 Skills-only 路径已用 Codex CLI `0.147.0-alpha.6.5` 在干净项目中做过发布后验证。安装后，在目标项目中启动一个新的 Codex 任务，再输入：

```text
使用 $project-publisher 看一下这个项目现在对外讲得清不清楚。
先只读，告诉我新访客最可能在哪一步看不懂或不想试。
不要编辑文件，也不要执行远程动作。
```

第一次响应可以和保存的[激活验证记录](../evals/results/codex-first-audit-v0.2.0.md)对照。未明确列出的客户端和版本仍然属于未验证。

更新已有的本地检出，并仅替换安装器管理的 Project Publisher 组件：

```bash
git -C project-publisher pull --ff-only
python3 project-publisher/scripts/install.py --yes
```

安装器替换不同的 Skill 安装前会保留带时间戳的备份。安装状态写入 `~/.codex/project-publisher/install-state.json`。

## 仅安装 Skills 的备选方式

```bash
npx skills add weike-zhang/project-publisher \
  --agent codex --skill project-publisher humanizer -g -y
```

这条命令会同时安装两个 Skills，但不会安装依赖提醒 Hook，也不会执行集成工具预检。只在宿主或管理员另行管理 Hook 时使用它。

## 本地检出

持续开发时，把两个 Skills 和 Hook 都链接到当前检出：

```bash
python3 scripts/install.py --mode link --yes
```

之后对检出的修改会在新 Codex 任务中直接可见，无需重新安装。Hook 内容变化后仍需重新审查，因为 Codex 会把信任绑定到当前 Hook 定义。

## 本地验证

```bash
python3 -m unittest discover -s tests -v
python3 skills/project-publisher/scripts/audit_repository.py . --json
python3 skills/project-publisher/scripts/check_secrets.py . --json
python3 skills/project-publisher/scripts/check_links.py .
python3 skills/project-publisher/scripts/review_public_surface.py . --strict
python3 skills/project-publisher/scripts/generate_release_page.py . --check-all
python3 evals/validate_fixtures.py
```

发布 ZIP 会拒绝符号链接和其他非常规文件，不会跟随链接或静默打包。

Skill 默认只在本地工作；安装或调用本身不会触发远程操作。创建仓库、Push、修改可见性、发布 Release 和外部发帖都需要明确目标与明确授权，并应由专门的 GitHub 工作流执行。
