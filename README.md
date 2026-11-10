# Shrink Rooms 3D

Steam「Shrink Rooms」を 3D トップダウンで作った、UE5.7.4(Blueprint のみ)のパズルゲームです。

## 遊び方
- 移動: WASD / 矢印キー(1入力=1ターン)。リトライ: R
- 箱を押して、毎ターンの終わりに縮む壁に潰される前にゴール(緑)へ行く。
- 木箱は壁に潰される。鉄箱は潰れず、壁を止める。
- 鍵(黄)で扉(赤)が開く。感圧板(黄色い床)の上に箱を置くと扉が開く。落とし穴(黒)には木箱を押し込んで埋める。

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
