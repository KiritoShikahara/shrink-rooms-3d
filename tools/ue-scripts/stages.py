import sys, subprocess, json, time
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from bp import run
O="/Game/ShrinkRooms/Objects/"
CLS={"P":"/Game/ShrinkRooms/Player/BP_GridPlayer","W":O+"BP_Wall","B":O+"BP_BoxWood","I":O+"BP_BoxIron","K":O+"BP_Key","D":O+"BP_Door","T":O+"BP_PressurePlate","X":O+"BP_Pit","G":O+"BP_Goal"}
def cli(*a):
    r=subprocess.run(["unrealengine-cli","--output","json",*a],capture_output=True,text=True,encoding="utf-8")
    try: d=json.loads(r.stdout)
    except Exception: raise SystemExit(f"FAIL {a}\n{r.stdout[:400]}{r.stderr[:400]}")
    if not d.get("ok",True): raise SystemExit(f"FAIL {a} {json.dumps(d)[:400]}")
    return d.get("data",d)
def setp(label,prop,val): cli("prop","set","--",label,prop,str(val))
def build(name,stage,nxt,last,events,limit,items,bounds=(0,6,0,6)):
    path=f"/Game/ShrinkRooms/Stages/{name}"
    try: cli("level","save","--all")
    except SystemExit: pass
    try: cli("level","open",path)
    except SystemExit:
        cli("level","new",path)
    for a in cli("level","actor","list"):
        if a["label"] not in ("WorldSettings",) and a["class"] not in ("WorldSettings",):
            try: cli("level","actor","destroy",a["label"])
            except SystemExit: pass
    cli("level","actor","spawn","/Game/ShrinkRooms/Core/BP_GridManager","--location","0,0,0","--label","GridManager")
    mn,mx,my0,my1=bounds
    for k,v in (("MinX",mn),("MaxX",mx),("MinY",my0),("MaxY",my1),("TurnLimit",limit),("StageNumber",stage),("NextLevel",nxt),("IsLastStage","true" if last else "false")):
        setp("GridManager",k,v)
    for e in events: cli("prop","array","GridManager","ShrinkEvents","append","--value",str(e))
    n=0
    for kind,x,y,*ex in items:
        label="GridPlayer" if kind=="P" else f"{kind}{n}"; n+=1
        cli("level","actor","spawn",CLS[kind],"--location",f"{y*100},{x*100},0","--label",label)
        setp(label,"GridX",x); setp(label,"GridY",y)
        for k,v in (ex[0].items() if ex else []): setp(label,k,v)
    cx=(mn+mx)*50; cy=(my0+my1)*50; cz=((mx-mn)+(my1-my0)+6)*50
    cli("level","actor","spawn","CameraActor","--location",f"{cy},{cx},{cz}","--rotation=-90,0,0","--label","StageCamera")
    cli("level","actor","spawn","DirectionalLight","--location","0,0,1500","--rotation=-55,25,0","--label","Sun")
    cli("level","actor","spawn","SkyLight","--location","0,0,800","--label","Sky")
    setp("WorldSettings","DefaultGameMode","/Game/ShrinkRooms/Core/BP_TurnGameMode.BP_TurnGameMode_C")
    cli("level","save")
    print("built",name,len(items))
def walls_col(x,ys): return [("W",x,y) for y in ys]
STAGES={
 "L_Stage01":dict(stage=1,nxt="L_Stage02",last=False,events=[61,70,103,112,121],limit=12,items=[("P",1,1),("G",5,5)]),
 "L_Stage02":dict(stage=2,nxt="L_Stage03",last=False,events=[52,71,80],limit=8,items=[("P",1,3),("B",3,3),("G",5,5),("W",5,1),("B",6,1)]+walls_col(3,[0,1,2,4,5,6])),
 "L_Stage03":dict(stage=3,nxt="L_Stage04",last=False,events=[61,103,112,120],limit=12,items=[("P",1,1),("K",1,5),("D",5,3,{"LinkId":0}),("G",6,3),("I",6,1)]+walls_col(5,[0,1,2,4,5,6])),
 "L_Stage04":dict(stage=4,nxt="L_Stage05",last=False,events=[82,91,103],limit=10,items=[("P",2,5),("B",2,3),("T",2,1),("D",4,3,{"LinkId":1}),("G",5,3)]+walls_col(4,[0,1,2,4,5,6]),),
 "L_Stage05":dict(stage=5,nxt="L_Title",last=True,events=[90,102,113,141],limit=14,items=[("P",1,3),("B",2,3),("B",1,2),("X",3,3),("X",4,3),("G",6,3)]+walls_col(3,[0,1,2,4,5,6])+walls_col(4,[0,1,2,4,5,6])),
}
# plates need LinkId=1 too
STAGES["L_Stage04"]["items"][2]=("T",2,1,{"LinkId":1})
if __name__=="__main__":
    for n in (sys.argv[1:] or STAGES):
        build(n,**STAGES[n])
