# タスク: Shrink Rooms 3D

**入力**: spec.md, plan.md, data-model.md, quickstart.md
**形式**: `- [ ] T### [P?] [US?] 内容 (パス)` / [P] = 並行可
**パス基準**: `ShrinkRooms3D/Content/ShrinkRooms/`(以下 `C/`)
**テスト**: 自動テストは対象外。各フェーズ末に PIE の手動確認を行う。

## Phase 1: Setup
- [x] T001 UE5.7.4 で新規プロジェクト作成(Blueprint, スターターコンテンツなし) (`ShrinkRooms3D/`)
- [x] T002 `.gitignore` 作成(Binaries/Intermediate/Saved/DerivedDataCache/.vs)と git 初期化 (`.gitignore`)
- [x] T003 [P] フォルダ構成作成 (`C/Core, Player, Objects, Stages, UI, Art`)
- [x] T004 [P] Enhanced Input: IA_Move(Axis2D), IA_Retry, IMC_Default (`C/Player/`)
- [x] T005 [P] 仮アセット用の基本マテリアル(単色)とキューブ/シリンダーを用意 (`C/Art/`)

## Phase 2: 基盤(全ストーリーの前提)
- [x] T006 BPI_GridActor インターフェース作成 (`C/Core/BPI_GridActor`)
- [x] T007 BP_GridActorBase: GridCoord, BlocksMovement, Pushable, Crushable (`C/Objects/BP_GridActorBase`)
- [x] T008 BP_GridManager: 座標↔ワールド変換、占有 Map、セル種別 (`C/Core/BP_GridManager`)
- [x] T009 BP_GridManager: `TryMove` と `AdvanceTurn` の骨組み (`C/Core/BP_GridManager`)
- [x] T010 BP_TurnGameMode と BP_GameInstance(現在ステージ) (`C/Core/`)
- [x] T011 BP_GridPlayer: 入力 → TryMove、移動中の入力ロック (`C/Player/BP_GridPlayer`)
- [x] T012 固定トップダウンカメラ(ステージサイズ追従) (`C/Player/BP_GridPlayer`)

## Phase 3: US1 - 1ステージをクリア (P1) 🎯 MVP
- [x] T013 [US1] BP_BoxWood: 押される処理(1個のみ) (`C/Objects/BP_BoxWood`)
- [x] T014 [US1] TryMove の箱押し判定(奥が空きのみ、失敗時はターン消費なし) (`C/Core/BP_GridManager`)
- [x] T015 [US1] BP_Goal と到達判定 (`C/Objects/BP_Goal`)
- [x] T016 [US1] WBP_Clear とクリア遷移 (`C/UI/WBP_Clear`)
- [x] T017 [US1] L_Stage01 を試作配置(床・壁・箱・ゴール) (`C/Stages/L_Stage01`)
- [x] T018 [US1] 手動確認: 開始 → 移動 → 箱押し → クリア

## Phase 4: US2 - 壁収縮と失敗/リトライ (P1)
- [x] T019 [US2] ステージ設定(StageId→GridManager のインスタンス変数: 範囲、ShrinkEvents、TurnLimit、NextLevel。DataTable の代わり)(StageId/サイズ/ShrinkSchedule/TurnLimit/NextStageId) (`C/Stages/DT_Stages`)
- [x] T020 [US2] BP_ShrinkWall: ラウンド終了時に ShrinkSchedule に従い指定の辺を1マス収縮 (`C/Objects/BP_ShrinkWall`)
- [x] T021 [US2] 収縮時の箱処理: 押せるなら押す(木箱) (`C/Core/BP_GridManager`)
- [x] T022 [US2] BP_BoxIron: 潰れない。収縮が止まる (`C/Objects/BP_BoxIron`)
- [x] T023 [US2] 木箱: 押せない時に潰れて消える(FR-013/014) (`C/Objects/BP_BoxWood`)
- [x] T024 [US2] プレイヤー圧死判定、クリア優先 (`C/Core/BP_GridManager`)
- [x] T025 [US2] WBP_HUD(残りターン、ステージ名) (`C/UI/WBP_HUD`)
- [x] T026 [US2] WBP_GameOver と R キー/ボタンでリトライ (`C/UI/WBP_GameOver`)
- [x] T027 [US2] 手動確認: 放置で圧死、木箱潰れ、鉄箱停止、リトライ

## Phase 5: US3 - ギミック (P2)
- [x] T028 [P] [US3] BP_Key (`C/Objects/BP_Key`)
- [x] T029 [P] [US3] BP_Door(鍵/感圧板で開閉) (`C/Objects/BP_Door`)
- [x] T030 [P] [US3] BP_PressurePlate (`C/Objects/BP_PressurePlate`)
- [x] T031 [P] [US3] BP_Pit(プレイヤー即死、箱で埋まる) (`C/Objects/BP_Pit`)
- [x] T032 [US3] AdvanceTurn にギミック更新を組み込み(順序は plan 参照) (`C/Core/BP_GridManager`)
- [x] T033 [US3] HUD に所持鍵表示 (`C/UI/WBP_HUD`)
- [x] T034 [US3] 手動確認: 鍵→扉、板→扉、穴の即死/埋め

## Phase 6: US4 - 5ステージとタイトル (P2)
- [x] T035 [US4] L_Stage01 を本設計(導入: 移動・収縮・出口) (`C/Stages/L_Stage01`)
- [x] T036 [P] [US4] L_Stage02 箱押し(木箱) (`C/Stages/L_Stage02`)
- [x] T037 [P] [US4] L_Stage03 鍵と扉 + 鉄箱 (`C/Stages/L_Stage03`)
- [x] T038 [P] [US4] L_Stage04 感圧板 (`C/Stages/L_Stage04`)
- [x] T039 [P] [US4] L_Stage05 落とし穴 + 総合 (`C/Stages/L_Stage05`)
- [x] T040 [US4] 各ステージの解法を記録 (`specs/001-shrink-rooms-3d/solutions.md`)
- [x] T041 [US4] WBP_Title と L_Title(スタート/続きから) (`C/UI/WBP_Title`)
- [x] T042 [US4] 次ステージ遷移(DT_Stages.NextStageId) (`C/Core/BP_GameInstance`)
- [x] T043 [US4] WBP_AllClear と最終ステージ後の処理 (`C/UI/WBP_AllClear`)
- [x] T044 [US4] BP_SaveGame: 到達ステージの保存/読込 (`C/Core/BP_SaveGame`)
- [x] T045 [US4] 手動確認: タイトル → 1〜5 → AllClear → 再起動で続き

## Phase 7: 修正・調整 (FR-016)
- [x] T046 通しプレイで不具合を洗い出し、`bugs.md` に記録 (`specs/001-shrink-rooms-3d/bugs.md`)
- [x] T047 入力まわりの修正(連打、アニメ中入力、同時押し)
- [x] T048 収縮・判定の境界ケース修正(同ターン到達、箱連続、穴と収縮の同時)
- [x] T049 難易度調整(ShrinkSchedule、配置)と、詰み回避の確認
- [ ] T050 操作感調整(移動速度、カメラ、リトライ速度 2秒以内)
- [ ] T051 BP 整理(コメント、命名、ノード整列、未使用ノード削除)

## Phase 8: グラフィックス向上 (FR-015)
- [x] T052 [P] 壁・床・箱・鉄箱のマテリアルとインスタンス (`C/Art/M_*, MI_*`)
- [x] T053 [P] ライティング: 部屋の雰囲気、影、ポストプロセス (`C/Art/PP_*`)
- [ ] T054 [P] 収縮の演出(壁の動き、カメラシェイク、ダスト) (`C/Art/NS_*`)
- [ ] T055 [P] 箱が潰れる/穴が埋まる/扉が開く演出 (`C/Art/NS_*`)
- [ ] T056 [P] UI のデザイン統一(フォント、色、フェード) (`C/UI/`)
- [x] T057 [P] サウンド(移動、押す、収縮、クリア、失敗、BGM)。小さい圧縮音源のみ (`C/Art/Audio/`)
- [ ] T058 パフォーマンス確認(PIE で 60fps、不要なアセットを削除)

## Phase 9: 提出整備
- [x] T059 未使用アセット削除、テクスチャのサイズ縮小
- [x] T060 プロジェクトサイズを計測(2GB 未満) (`quickstart.md` のチェックリスト)
- [x] T061 クリーンクローンから起動確認(プラグインの問題なし)
- [x] T062 README に操作と構成を記載 (`README.md`)
- [x] T063 quickstart のチェックリストを全項目確認
- [x] T064 提出前に uproject から UnrealCliBridge と PythonScriptPlugin を削除(確認者の環境で動かない恐れ) (`ShrinkRooms3D/ShrinkRooms3D.uproject`)

## 依存関係
- Phase 1 → 2 → 3(MVP) → 4 → 5 → 6 → 7 → 8 → 9
- Phase 5 の T028〜T031 は並行可。Phase 6 の T036〜T039 は並行可。
- Phase 8 は Phase 7 完了後(修正前に見た目を変えると不具合の切り分けが難しくなるため)。

## 実装方針
- MVP: Phase 1〜3 で1面が通ること。
- 以降は1フェーズずつ完了 → 手動確認 → 次へ。
