# Visual asset notice

The hero source artwork was generated specifically for Project Publisher with OpenAI image-generation tooling on 2026-08-13. It contains no third-party photograph, logo, mascot or supplied reference image. Deterministic typography and crops are applied by `scripts/build_visuals.py` to create `hero.png`, `hero.zh-CN.png` and `social-preview.png`.

`activation-proof.png` is a version-pinned Release artifact built from the saved Codex first-audit activation check. The icon is original geometric artwork. The current README keeps observed failures in searchable text and code blocks instead of adding more raster diagrams.

Run `python3 scripts/build_visuals.py` in an environment with Pillow to reproduce the composed raster assets from the checked-in `hero-art.png` source. These public assets are distributed with the project under the [MIT License](../LICENSE).
