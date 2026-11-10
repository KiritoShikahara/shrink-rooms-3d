# UE 自動化スクリプト

`unrealengine-cli`(エディタ起動中)で Blueprint とレベルを作った補助スクリプトです。
- `bp.py`: `blueprint`/`tool call` の薄いラッパー(`BP` クラス、`mcall`、`vg`、`vs` など)
- `stages.py`: L_Stage01〜05 を作り直す(`python stages.py [L_Stage03]`)
- `play.py`: PIE で解法を再生して検証(`python play.py L_Stage01 RRRRUUUU`)
- `mats.py` `ppv*.py` `imc.py`: マテリアル、ポストプロセス、入力割り当て(`python_exec` に渡す)

使う前に `unrealengine-cli setup --prebuilt` と `editor open` が必要です。
