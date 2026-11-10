# Shrink Rooms 3D

Steam「Shrink Rooms」を 3D トップダウンで作った、UE5.7.4(Blueprint のみ)のパズルゲームです。

## 遊び方
- 移動: WASD / 矢印キー(1入力=1ターン)。リトライ: R
- 移動キーは視点の向き(90度ごと)に合わせて切り替わる
- 視点: Q/E = 左右に回す、Z/X = 傾きを変える、マウスホイール = ズーム(初期は斜め60度)
- 箱を押して、毎ターンの終わりに縮む壁に潰される前にゴール(緑)へ行く。
- 木箱は壁に潰される。鉄箱は潰れず、壁を止める。
- 鍵(黄)で扉(赤)が開く。感圧板(黄色い床)の上に箱を置くと扉が開く。落とし穴(黒)には木箱を押し込んで埋める。

## 主な機能
- グリッド/ターン制の箱押しパズル(5ステージ)。毎ターンの終わりに壁が縮む。次に縮む壁は赤く光り、HUD にも出る。
- ギミック: 木箱(潰れる)、鉄箱(壁を止める)、鍵と扉、感圧板と扉、落とし穴(箱で埋める)。
- 斜め視点と視点移動、効果音と BGM、タイトルの3D背景、ポーズメニュー、ステージ選択、セーブ/CONTINUE。
- ゲームパッド対応(十字キーで移動、右スティックで視点、Start でポーズ)。

## 開き方
1. UE 5.7.4 で `ShrinkRooms3D/ShrinkRooms3D.uproject` を開く。
2. `L_Title` を開いて Play。

## 構成
- `Content/ShrinkRooms/Core`: `BP_GridManager`(盤面・ターン・収縮)、`BP_GameInstance`(遷移・セーブ)、`BP_SaveGame`
- `Content/ShrinkRooms/Objects`: `BP_GridActorBase` と各ギミック
- `Content/ShrinkRooms/Player`: `BP_GridPlayer`、Enhanced Input
- `Content/ShrinkRooms/UI`: タイトル、HUD、クリア、ゲームオーバー、全クリア
- `Content/ShrinkRooms/Stages`: `L_Title`、`L_Stage01`〜`L_Stage05`
- 仕様・計画・タスク: `specs/001-shrink-rooms-3d/`(各ステージの解法は `solutions.md`)

## テスト
UE エディタを起動した状態で(`unrealengine-cli setup --prebuilt` と `unrealengine-cli editor open` の後)、`python tools/ue-scripts/regress.py` を実行します。5ステージの解法、失敗とリトライ、箱が潰れる/鉄箱が壁を止める、ポーズ、タイトル、ステージ選択の19項目を PIE で確認します。
