# データモデル

## DT_Stages (DataTable, 行: StageId)
| 列 | 型 | 内容 |
|---|---|---|
| StageId | Name | Stage01..05 |
| LevelName | Name | L_Stage01.. |
| GridWidth/GridHeight | Integer | 盤面サイズ |
| ShrinkSchedule | Array of struct (Turn, Side, Amount) | 何ターン目の終了時に、どの辺(N/E/S/W)を何マス縮めるか |
| TurnLimit | Integer | 収縮完了までの手数(HUD 表示用、スケジュールから算出) |
| NextStageId | Name | 次ステージ(最後は None) |

## セル種別 (Enum E_CellType)
Floor, Wall, Pit, PressurePlate, Goal

## アクター共通 (BP_GridActorBase)
- GridCoord (Integer2): 現在座標
- BlocksMovement (Boolean), Pushable (Boolean), Crushable (Boolean)
- インターフェース BPI_GridActor: `OnTurnAdvanced`, `OnPushed`, `OnCrushed`

## ギミック
- BP_Key: KeyId。取得でプレイヤーの KeyIds に追加。
- BP_Door: RequiredKeyId または LinkedPlateId。Open/Closed。
- BP_PressurePlate: PlateId。上に乗っているアクターがあれば Active。
- BP_Pit: 木箱/鉄箱が入ると埋まる。プレイヤーが入ると即死。
- BP_ShrinkWall: 辺ごとの Margin(縮んだ量)、現在ターン。ラウンド終了時に ShrinkSchedule を参照する。

## BP_SaveGame
- ClearedStageIndex (Integer)
