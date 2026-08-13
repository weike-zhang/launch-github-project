# 安装

这个版本已经验证的要求：

- 使用 Skills CLI 安装时需要 Node.js 和 `npx`；
- 运行内置审计、Release 页面和打包脚本时使用 Python 3.12。

## 推荐安装

```bash
npx skills add weike-zhang/launch-github-project \
  --agent codex --skill launch-github-project -g -y
```

v0.2.0 发布后，上面的公网全局安装命令已经实测：Codex CLI `0.147.0-alpha.6.5` 在一个没有项目级 Skill 的干净目录中加载 GitHub 公开版本，并在只读沙箱完成第一次审计。发布前，本地候选版也通过了项目级安装路径。安装后，在目标项目中启动一个新的 Codex 任务，再输入：

```text
使用 $launch-github-project 审计这个项目的 GitHub 发布面。
先只读，不要编辑文件，也不要执行远程动作。
```

第一次响应可以和保存的[激活验证记录](../evals/results/codex-first-audit-v0.2.0.md)对照。未明确列出的客户端和版本仍然属于未验证。

更新已有的全局安装：

```bash
npx skills update launch-github-project -g -y
```

## 本地检出

在仓库父目录中，使用同一个 Skills CLI 安装本地检出：

```bash
npx skills add ./launch-github-project \
  --agent codex --skill launch-github-project --copy -y
```

这样不依赖某个客户端特有的本地插件命令。也可以把 `skills/launch-github-project/` 复制到客户端的 Agent Skills 目录并重启。

## 本地验证

```bash
python3 -m unittest discover -s tests -v
python3 skills/launch-github-project/scripts/audit_repository.py . --json
python3 skills/launch-github-project/scripts/check_secrets.py . --json
python3 skills/launch-github-project/scripts/check_links.py .
python3 skills/launch-github-project/scripts/review_public_surface.py . --strict
python3 skills/launch-github-project/scripts/generate_release_page.py . --check-all
python3 evals/validate_fixtures.py
```

发布 ZIP 会拒绝符号链接和其他非常规文件，不会跟随链接或静默打包。

Skill 默认只在本地工作；安装或调用本身不会触发远程操作。创建仓库、Push、修改可见性、发布 Release 和外部发帖都需要明确目标与明确授权，并应由专门的 GitHub 工作流执行。
