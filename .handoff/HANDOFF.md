# 引き継ぎ (2026-11-10 11:53 / main)

次の一手: `python tools/ue-scripts/regress.py` を実行して 19 項目が通ることを確認し、`specs/001-shrink-rooms-3d/improvement-tasks.md` の未着手 P1(D-01 ほこり、B-04 木箱の縮む演出、H-02 ボタン統一部品、H-05 星と自己ベスト、C-04/05/06 モデル、E-03/04/05 カメラ)から続ける。

## 完了
- ゲーム本体(5ステージ、ギミック、タイトル、HUD、クリア/ゲームオーバー/全クリア、ポーズ、ステージ選択、セーブ/CONTINUE)
- 改善タスク 100 件のうち ✅ 約 33 件、◐ 約 10 件(`improvement-tasks.md` の先頭に件数あり)
  - 移動補間、ぶつかり、伸び縮み、斜めカメラと視点移動(Q/E/Z/X/ホイール/C)、移動キーの画面基準化
  - 市松の床、光る色、ステージごとの照明色、収縮の警告(壁が光る)、次の収縮の HUD、ステージ名とヒント
  - 合成した効果音と BGM(`tools/audio-gen/`)、画面揺れ、ヒットストップ、ゲームパッド対応
  - タイトルの3D背景、扉が沈む、潰れた箱が落ちる、ゴールと鍵が回る
- 回帰テスト `tools/ue-scripts/regress.py`(19 項目、全て PASS)
- 実機: 120fps、ヒッチなし(`perf measure`)

## 残り(優先順)
- 未着手 P1: D-01(ほこり)、H-02(ボタンの共通部品)、H-05(星と自己ベスト)、C-04/05/06(モデルと質感)、E-03/04/05(カメラのイントロと画面比率)
- ◐ の仕上げ: D-03/D-05(Niagara の `RadialBurst` は呼んでいるが目視できていない)、B-04、C-06、J-01、J-04(ポーズメニューの揺れ ON/OFF は動くが、開き直すとラベルが ON に戻る)
- P2/P3 は `improvement-tasks.md` を参照

## 保留
- push — 今回は push していない(ローカルコミットのみ)。公開リポジトリへの反映は確認待ち
- エンジンの修復 — Epic Launcher の「検証」(UE_5.7)。作業中に `ResavePackages` で約5200ファイルを再保存し、`SplineDeformation.uasset` を UE_5.4 のコピーで暫定復旧した

## 再開に必要なもの
- UE 5.7.4(Epic Launcher)、Visual Studio C++ ツール、Python 3、`unrealengine-cli`
- Blueprint を自動編集するとき:
  1. `cd ShrinkRooms3D`
  2. `unrealengine-cli setup --prebuilt`
  3. `unrealengine-cli editor open`
  4. コミット前に `python tools/precommit-strip.py`(`uproject` から `UnrealCliBridge` と `PythonScriptPlugin` を外す。確認者の環境で動かなくなるため)
- 補助スクリプト: `tools/ue-scripts/`(`bp.py`、`stages.py`、`play.py`、`regress.py`、`mats2.py`、`input_cam.py` など)、`tools/audio-gen/gen.py`
- git に入っていないもの: `doc/`(講義資料。著作物のため非公開)、`Plugins/UnrealCliBridge/`、`.orchestrator/`、`roc-solo-sonnet.cmd`
- 注意:
  - `pie get` で `Player` というラベルは使えない(`GridPlayer`)
  - `level open` の前に PIE を止めて `level save --all`
  - 負の数の引数は `--location=-100,0,0` や `set-pin ... --` の形で渡す
  - 子 BP のコンポーネント編集は親の共有テンプレートを書き換えるため、見た目は変数(`BodyMaterial`、`MeshScale`、`MeshZ`)で持つ
  - 子 BP に Tick などのイベントを足すと親の処理が止まることがある。共通処理は `BP_GridActorBase` に足す
  - `-run=ResavePackages` は実行しない(エンジンの資産を書き換える)
