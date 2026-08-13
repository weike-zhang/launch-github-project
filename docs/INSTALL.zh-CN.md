# 安装

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
python evals/validate_fixtures.py
```

发布 ZIP 会拒绝符号链接和其他非常规文件，不会跟随链接或静默打包。

Skill 只准备本地发布材料，不会创建或修改 GitHub 仓库。
