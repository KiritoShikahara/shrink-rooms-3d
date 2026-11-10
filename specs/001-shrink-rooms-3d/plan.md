# 実装計画: Shrink Rooms 3D

**Spec**: [spec.md](spec.md) | **Date**: 2026-11-10

## Summary
UE5.7.4 の Blueprint のみで、グリッド/ターン制の3Dパズルを作る。盤面ロジックは `BP_GridManager` に集約し、各アクターはグリッド座標を持つ。壁収縮・箱押し・ギミックは、すべてターン進行(`AdvanceTurn`)で決定的に処理する。最後に修正とグラフィックス向上を行う。

## Technical Context
- **Engine**: UE 5.7.4 (Blueprint only, C++ なし)
- **Plugins**: 標準のみ(Enhanced Input)
- **Storage**: SaveGame (BP_SaveGame: 到達ステージ)
- **Testing**: PIE での手動プレイテスト + `quickstart.md` のチェックリスト。BP の Functional Test は任意。
- **Target**: Windows、単一プレイヤー
- **Constraints**: リポジトリ 2GB 以下、`.gitignore` 必須、移動はアニメ中入力禁止
- **Scale**: 5ステージ、各 7x7〜11x11 マス程度

## Constitution Check
| 原則 | 判定 |
|---|---|
| I 課題要件 | OK: 開始〜クリア/ゲームオーバー、前期要素を使用 |
| II BP中心 | OK: C++ なし。親BP/インターフェース/コンポーネントで共有 |
| III 提出可能性 | OK: `.gitignore` を最初に作る。標準プラグインのみ |
| IV 決定性 | OK: 物理を使わずグリッド判定で処理 |
| V 小さく作る | OK: 1面ずつ。ステージ1で縦に通してから拡張 |

## Project Structure
```
ShrinkRooms3D/                  # UE プロジェクト(リポジトリルート直下)
├── .gitignore
├── ShrinkRooms3D.uproject
└── Content/ShrinkRooms/
    ├── Core/        BP_GridManager, BP_TurnGameMode, BP_GameInstance, BP_SaveGame, BPI_GridActor
    ├── Player/      BP_GridPlayer, IA_Move, IA_Retry, IMC_Default
    ├── Objects/     BP_GridActorBase, BP_BoxWood, BP_BoxIron, BP_Key, BP_Door, BP_PressurePlate, BP_Pit, BP_Goal, BP_ShrinkWall
    ├── Stages/      DT_Stages, L_Title, L_Stage01..05
    ├── UI/          WBP_Title, WBP_HUD, WBP_Clear, WBP_GameOver, WBP_AllClear
    └── Art/         M_*, MI_*, NS_*, PP_*, Audio/
specs/001-shrink-rooms-3d/
```
**Decision**: 1つの UE プロジェクトに全て置く。ステージは各レベルへ手配置し、収縮設定とグリッドサイズは `DT_Stages`(DataTable)で管理する。

## 設計の要点
1. **BP_GridManager**: 座標 ↔ ワールド変換、セル占有表(Map: 座標 → アクター)、`TryMove(actor, dir)`、`AdvanceTurn()`。
2. **TryMove**: 壁/鉄箱/閉じた扉 → 失敗。木箱/鉄箱の先が空き → 1個だけ押す。成功時のみターン消費。
3. **AdvanceTurn 順序**: ギミック更新(感圧板) → 収縮カウント減 → 収縮実行 → 判定(圧死/落下/クリア)。クリアは圧死より優先。
4. **収縮**: Steam 準拠でラウンド終了時に行う。ステージの ShrinkSchedule に従い指定の辺を1マス内側へ。その行/列の箱を押し、押せなければ木箱は破壊、鉄箱は壁が停止。プレイヤーが残れば圧死。
5. **入力**: Enhanced Input。移動アニメ中は入力を受けない(タイムライン完了で解除)。
6. **カメラ**: 固定トップダウン(やや斜め)。ステージサイズに合わせて自動調整。

## 段階
1. Setup(プロジェクト/git/入力)
2. 基盤(グリッド/ターン/アクター基底)
3. US1: 1面クリア → US2: 収縮と失敗 → US3: ギミック → US4: 5面/タイトル/セーブ
4. 修正(バグ、バランス)
5. グラフィックス向上
6. 提出整備(サイズ確認、クリーンチェックアウト)

## Complexity Tracking
違反なし。
