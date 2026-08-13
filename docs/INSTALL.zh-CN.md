# 安装

这个版本已经验证的要求：

- 使用 Skills CLI 安装时需要 Node.js 和 `npx`；
- 运行内置审计、Release 页面和打包脚本时使用 Python 3.12。

## 推荐安装

```bash
npx skills add weike-zhang/launch-github-project --skill launch-github-project -g
```

## 本地检出

在仓库父目录中，使用同一个 Skills CLI 安装本地检出：

```bash
npx skills add ./launch-github-project --skill launch-github-project -g
```

这样不依赖某个客户端特有的本地插件命令。也可以把 `skills/launch-github-project/` 复制到客户端的 Agent Skills 目录并重启。

## 本地验证

```bash
python -m unittest discover -s tests -v
python skills/launch-github-project/scripts/audit_repository.py . --json
python skills/launch-github-project/scripts/check_secrets.py . --json
python skills/launch-github-project/scripts/check_links.py .
python skills/launch-github-project/scripts/review_public_surface.py . --strict
python skills/launch-github-project/scripts/generate_release_page.py . --check-all
python evals/validate_fixtures.py
```

发布 ZIP 会拒绝符号链接和其他非常规文件，不会跟随链接或静默打包。

Skill 默认只在本地工作；安装或调用本身不会触发远程操作。创建仓库、Push、修改可见性、发布 Release 和外部发帖都需要明确目标与明确授权，并应由专门的 GitHub 工作流执行。
