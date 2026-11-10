# 引き継ぎ (2026-11-10 11:21 / main)

次の一手: `specs/001-shrink-rooms-3d/improvement-tasks.md` の A-01(移動を 0.12 秒の補間にする。判定は即時、見た目だけ補間)から始める。

## 完了
- Spec Kit 導入、憲章、`specs/001-shrink-rooms-3d/{spec,plan,data-model,quickstart,tasks}.md`
- UE5.7.4 の Blueprint のみのプロジェクト `ShrinkRooms3D/`(5ステージ、タイトル、HUD、クリア、ゲームオーバー、全クリア、セーブ/CONTINUE)
- 5ステージの解法は PIE で検証済み(`specs/001-shrink-rooms-3d/solutions.md`)。実キー入力の WASD も確認済み
- 不具合と対処: `specs/001-shrink-rooms-3d/bugs.md`
- 改善100件の計画: `specs/001-shrink-rooms-3d/improvement-tasks.md`
- 公開リポジトリ: https://github.com/KiritoShikahara/shrink-rooms-3d(`main` は同期済み)

## 残り(優先順)
- 改善タスク P1(49件)。まず M1: A、B、C、D の P1
- `tasks.md` の未完了 6件: T050(操作感)、T051(BP 整理)、T054〜T056(演出、UI 統一)、T058(60fps 計測)
- 通常のエディタウィンドウで、画面表示を目視確認する
- 試遊(5人、説明なし)で詰まりを確認する(K-07)

## 保留
- 公開 push 済みの内容への追加 push — 変更のたびに確認する
- エンジンの修復 — Epic Launcher の「検証」(UE_5.7)。作業中に `ResavePackages` で約5200ファイルを再保存し、`SplineDeformation.uasset` を UE_5.4 のコピーで暫定復旧した

## 再開に必要なもの
- UE 5.7.4(Epic Launcher)、Visual Studio C++ ツール、Python 3
- `unrealengine-cli`(`~/.cargo/bin`、リポジトリ `github-reps-main/repos/unrealengine-cli`)
- Blueprint の自動編集をするとき:
  1. `cd ShrinkRooms3D`
  2. `unrealengine-cli setup --prebuilt`(`uproject` に `UnrealCliBridge` と `PythonScriptPlugin` が足される)
  3. `unrealengine-cli editor open`
  4. 作業後に `uproject` から2つのプラグインを外す(確認者の環境で動かなくなるため。`tasks.md` T064)
- 補助スクリプト: `tools/ue-scripts/`(`bp.py`、`stages.py`、`play.py`。使い方は同フォルダの README)
- git に入っていないもの: `doc/`(講義資料。著作物のため非公開)、`Plugins/UnrealCliBridge/`(ビルド物)、`.orchestrator/`、`roc-solo-sonnet.cmd`
- 注意:
  - `unrealengine-cli pie get` で `Player` というラベルは使えない(`GridPlayer` を使う)
  - `level open` の前に `level save --all` が必要
  - Git Bash で `/Game/...` を渡すときは `MSYS_NO_PATHCONV=1`
  - `-run=ResavePackages` は実行しない(エンジンの資産を書き換える)
