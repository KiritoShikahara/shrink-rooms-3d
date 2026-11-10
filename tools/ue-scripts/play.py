import sys, subprocess, json, time
def cli(*a,check=True,timeout=200):
    r=subprocess.run(["unrealengine-cli","--output","json",*a],capture_output=True,text=True,encoding="utf-8",timeout=timeout)
    try: d=json.loads(r.stdout)
    except Exception: return {"ok":False,"raw":r.stdout[:300]+r.stderr[:300]}
    return d
def prop(label,p):
    d=cli("pie","get",label,p)
    return d.get("data",{}).get("properties",{}).get(p)
def pos(label):
    return (int(prop(label,"GridX")),int(prop(label,"GridY")))
DIR={"R":(1,0),"L":(-1,0),"U":(0,1),"D":(0,-1)}
def play(level,moves,shot=None,boxes=()):
    cli("pie","stop"); cli("level","save","--all")
    cli("level","open","/Game/ShrinkRooms/Stages/"+level)
    r=cli("pie","start"); 
    if not r.get("ok",True): print("start",str(r)[:200])
    cli("pie","wait","--seconds","0.5")
    if shot: cli("pie","screenshot","--filename",shot)
    for m in moves:
        dx,dy=DIR[m]; cli("pie","call","GridPlayer",f"Step {dx} {dy}"); cli("pie","wait","--seconds","0.1")
    out=dict(player=pos("GridPlayer"),turn=prop("GridManager","TurnCount"),state=prop("GridManager","GameState"),bounds=[prop("GridManager",k) for k in ("MinX","MaxX","MinY","MaxY")],keys=prop("GridManager","KeyCount"))
    for b in boxes: out[b]=pos(b)
    if shot: cli("pie","screenshot","--filename",shot.replace(".png","_end.png"))
    cli("pie","stop")
    return out
if __name__=="__main__":
    print(play(sys.argv[1],sys.argv[2],shot=(sys.argv[3] if len(sys.argv)>3 else None)))
