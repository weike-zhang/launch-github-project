# 安装

## 推荐安装

```bash
npx skills add weike-zhang/launch-github-project --skill launch-github-project -g
```

## 本地检出

Codex 用户也可以在仓库父目录安装本地插件：

```bash
codex plugin install ./launch-github-project
```

如果客户端不支持插件安装，把 `skills/launch-github-project/` 复制到客户端的 Agent Skills 目录并重启即可。

## 本地验证

```bash
python skills/launch-github-project/scripts/audit_repository.py . --json
python skills/launch-github-project/scripts/check_secrets.py . --json
python skills/launch-github-project/scripts/check_links.py .
python skills/launch-github-project/scripts/review_public_surface.py . --strict
python evals/validate_fixtures.py
```

Skill 只准备本地发布材料，不会创建或修改 GitHub 仓库。
