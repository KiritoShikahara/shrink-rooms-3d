# 通しプレイで見つけた不具合と対処

| # | 症状 | 原因 | 対処 |
|---|---|---|---|
| 1 | どのキーを押しても +X に動く | IMC の modifier(Negate/Swizzle)が保存されず null | modifier の outer を IMC にして作り直し、`pie input` の実キーで W/A/S/D を確認 |
| 2 | 3D 画面が真っ暗 | マネージャーのルートがカメラ。レベル配置の回転 0 で水平を向いていた | レベルに `CameraActor`(真下向き)を置き、`SetViewTargetWithBlend` の対象にした |
| 3 | 全アクターが原点に集まる | `Mesh` がルートで、`SetRelativeLocation` が XY を 0 に上書き | `SnapToGrid` で Z も `MeshZ` から設定し、相対位置の変更を削除 |
| 4 | 画面の左右が逆 | UE の上視点では 上=+X, 右=+Y | ワールド座標をグリッドの X/Y と入れ替え(`SnapToGrid`、`UpdateWalls`、カメラ) |
| 5 | 全部が木箱の色 | 子 BP のコンポーネント編集が親テンプレートを共有 | `BodyMaterial`/`MeshScale`/`MeshZ` 変数を子 BP に持たせ、BeginPlay で適用 |
| 6 | 勝利時に失敗音が鳴る(作成中に発見) | 音を分岐の誤った枝につないだ | 配線を修正 |
| 7 | レベル切替で `level open` が失敗 | 未保存のレベルがある | 切替前に `level save --all` |
