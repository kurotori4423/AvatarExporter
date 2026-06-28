# AGENTS.md instructions

コードには、日本語によるコメントを適宜挿入すること。
関数やクラスなどにはその言語に適したサマリーコメントを挿入する。
コメントにはコードからは読み取れない実装意図を書くこと。
修正を指示されたとき、修正を行ったという「履歴」に関してはコメントやドキュメントに残さない。これはコミットログに保持されるべき情報。

コマンドの並列実行は実行順が重要なら行わない。一つずつ順番に実行する。

## Blender Extension

このリポジトリは Blender Extension として管理する。配布用 ZIP の作成は Blender 側の Extension 管理に任せ、通常の開発検証では ZIP 作成スクリプトを追加しない。

`uv` と `fake-bpy-module` を使い、Blender 本体を起動せずにトップレベルの構文と `bpy` 参照の静的な読み込みを確認する。

```powershell
uv sync --extra dev
uv run python -m py_compile __init__.py
uv run ruff check .
uv run basedpyright
```
