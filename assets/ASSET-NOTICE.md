# Visual asset notice

The hero source artwork was generated specifically for Launch GitHub Project with OpenAI image-generation tooling on 2026-08-13. It contains no third-party photograph, logo, mascot or supplied reference image. Deterministic typography and crops are applied by `scripts/build_visuals.py` to create `hero.png`, `hero.zh-CN.png` and `social-preview.png`.

`audit-proof.png` and `audit-proof.zh-CN.png` are deterministic project-owned diagrams built from the documented self-audit in `examples/self-audit-bundle-safety.md`. `activation-proof.png` is built from the saved Codex first-audit activation check. The flow diagram and icon are original geometric artwork.

Run `python3 scripts/build_visuals.py` in an environment with Pillow to reproduce the composed raster assets from the checked-in `hero-art.png` source. These public assets are distributed with the project under the [MIT License](../LICENSE).
