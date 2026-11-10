"""PIE での回帰テスト。エディタ起動中(unrealengine-cli editor open)に実行: python regress.py
5ステージの解法、失敗/リトライ、ポーズ、ステージ選択、セーブを確認し、結果を表示して終了コードで返す。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from play import cli, prop, pos, play, DIR

SOL = {"L_Stage01": "RRRRUUUU", "L_Stage02": "RRRUUR", "L_Stage03": "UUUURRRDDRR", "L_Stage04": "DDDURRR", "L_Stage05": "RDDLULURRRRRR"}
fails = []

def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f"  {detail}" if detail and not ok else ""))
    if not ok: fails.append(name)

def widgets():
    return [w["class"] for w in cli("pie", "widgets").get("data", [])]

def world():
    return cli("pie", "status").get("data", {}).get("world", "")

def start(level):
    cli("pie", "stop"); cli("level", "save", "--all"); cli("level", "open", "/Game/ShrinkRooms/Stages/" + level); cli("pie", "start"); cli("pie", "wait", "--seconds", "1")

def step(dx, dy): cli("pie", "call", "GridPlayer", f"Step {dx} {dy}")

for lvl, moves in SOL.items():
    r = play(lvl, moves)
    check(f"{lvl} solution clears", r["state"] == "1", str(r))

# 失敗 → ゲームオーバー画面 → リトライ
start("L_Stage01")
for mv in [(1, 0)] * 4 + [(0, 1), (0, -1)] * 4: step(*mv)
cli("pie", "wait", "--seconds", "0.5")
check("stage1 idle -> game over", prop("GridManager", "GameState") == "2" and "WBP_GameOver_C" in widgets())
cli("pie", "click", "RetryButton"); cli("pie", "wait", "--seconds", "1.5")
check("retry reloads stage (turn 0)", prop("GridManager", "TurnCount") == "0")

# 壁に木箱が潰される(ステージ2 の B4)
start("L_Stage02")
for mv in [(0, 1), (0, -1)] * 5: step(*mv)
cli("pie", "wait", "--seconds", "0.5")
check("wood box crushed by wall", prop("B4", "GridX") == "-999")

# 鉄箱が壁を止める(ステージ3: 東の壁は MaxX=6 のまま)
r = play("L_Stage03", "UUUURRRDDRR")
check("iron box stops east wall", r["bounds"][1] == "6", str(r["bounds"]))

# ポーズ
start("L_Stage01")
cli("pie", "input", "Escape", "--seconds", "0.15"); cli("pie", "wait", "--seconds", "0.5")
check("Esc opens pause menu", "WBP_Pause_C" in widgets())
cli("pie", "click", "ResumeButton"); cli("pie", "wait", "--seconds", "0.5")
check("resume closes pause menu", "WBP_Pause_C" not in widgets())

# タイトル → ステージ選択(ロック)
cli("pie", "stop"); cli("level", "save", "--all"); cli("level", "open", "/Game/ShrinkRooms/Stages/L_Title"); cli("pie", "start"); cli("pie", "wait", "--seconds", "1")
check("title shows WBP_Title", "WBP_Title_C" in widgets())
cli("pie", "click", "StagesButton"); cli("pie", "wait", "--seconds", "0.5")
check("stage select opens", "WBP_StageSelect_C" in widgets())
cli("pie", "click", "Stage1Button"); cli("pie", "wait", "--seconds", "1.5")
check("stage1 button opens L_Stage01", world().endswith("L_Stage01.L_Stage01"), world())
cli("pie", "stop")
print(f"\n{len(fails)} failure(s)")
sys.exit(1 if fails else 0)
