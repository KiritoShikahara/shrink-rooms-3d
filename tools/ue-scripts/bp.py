import subprocess, json, sys
CLI="unrealengine-cli"
def run(*a):
    r=subprocess.run([CLI,"--output","json",*a],capture_output=True,text=True,encoding="utf-8")
    try: d=json.loads(r.stdout)
    except Exception: raise SystemExit(f"FAIL {a}\n{r.stdout}\n{r.stderr}")
    if not d.get("ok",True): raise SystemExit(f"FAIL {a}\n{json.dumps(d,ensure_ascii=False)[:800]}")
    return d.get("data",d)
class BP:
    def __init__(s,path,graph="EventGraph"): s.p=path; s.g=graph; s.x=0
    def n(s,typ,member=None,parent=None,**pins):
        a=["blueprint","add-node",s.p,"--type",typ,"--graph",s.g]
        if member: a+=["--member",member]
        if parent: a+=["--member-parent",parent]
        d=run(*a); i=d["id"]
        for k,v in pins.items(): setpin(s,i,k,v)
        return i
    def c(s,a,b): run("blueprint","connect",s.p,a,b,"--graph",s.g)
    def chain(s,*ids):
        for a,b in zip(ids,ids[1:]): s.c(a+".then",b+".execute")
    def var(s,name,typ,default=None):
        a=["blueprint","add-variable",s.p,name,"--type",typ,"--instance-editable"]
        if default is not None: a+=[f"--default={default}"]
        run(*a)
    def fn(s,name,params=(),returns=(),pure=False):
        a=["blueprint","add-function",s.p,name]
        for p in params: a+=["--param",p]
        for r in returns: a+=["--returns",r]
        if pure: a.append("--pure")
        return run(*a)
    def graph(s,g=None): return run("blueprint","graph",s.p,"--graph",g or s.g)
    def compile(s): return run("blueprint","compile",s.p)
    def save(s): return run("blueprint","save",s.p)

def pins(b,i):
    return [(p["name"],p["direction"][0],p["type"]) for p in {x["id"]:x for x in b.graph()["nodes"]}[i]["pins"]]
K="KismetMathLibrary"
BASE="/Game/ShrinkRooms/Objects/BP_GridActorBase"
def mcall(b,fn,cls=K,**ins):
    n=b.n("CallFunction",fn,cls)
    for k,v in ins.items():
        if isinstance(v,str) and "." in v and v.split(".")[0].startswith("N"): b.c(v,n+"."+k)
        else: setpin(b,n,k,v)
    return n
def AND(b,a,c): return mcall(b,"BooleanAND",A=a,B=c)+".ReturnValue"
def OR(b,a,c): return mcall(b,"BooleanOR",A=a,B=c)+".ReturnValue"
def NOT(b,a): return mcall(b,"Not_PreBool",A=a)+".ReturnValue"
def vg(b,name,parent=None,target=None):
    n=b.n("VariableGet",name,parent)
    if target: b.c(target,n+".self")
    return n+"."+name
def vs(b,name,value=None,parent=None,target=None):
    n=b.n("VariableSet",name,parent)
    if target: b.c(target,n+".self")
    if value is not None:
        if isinstance(value,str) and value.split(".")[0].startswith("N") and "." in value: b.c(value,n+"."+name)
        else: setpin(b,n,name,value)
    return n

def clean(b,keep=("N1","N2")):
    for _ in range(40):
        ids=[n["id"] for n in b.graph()["nodes"] if n["id"] not in keep]
        if not ids: return
        try: run("blueprint","remove-node",b.p,ids[0],"--graph",b.g)
        except SystemExit: pass

def setpin(b,n,k,v): run("blueprint","set-pin","--graph",b.g,"--",b.p,n,k,str(v))

def seq(b,*ids):
    for a,c in zip(ids,ids[1:]): b.c(a+".then",c+".execute")
def isvalid(b,obj): return mcall(b,"IsValid","KismetSystemLibrary",Object=obj)+".ReturnValue"
def inside(b,x,y):
    n=b.n("CallFunction","IsInside"); b.c(x,n+".X"); b.c(y,n+".Y"); return n+".Result"
def getblk(b,x,y):
    n=b.n("CallFunction","GetBlockerAt"); b.c(x,n+".X"); b.c(y,n+".Y"); return n
def snap(b,obj):
    n=b.n("CallFunction","SnapToGrid",BASE); b.c(obj,n+".self"); return n
def add(b,a,c): return mcall(b,"Add_IntInt",A=a,B=c)+".ReturnValue"
def sub(b,a,c): return mcall(b,"Subtract_IntInt",A=a,B=c)+".ReturnValue"
def eqi(b,a,c): return mcall(b,"EqualEqual_IntInt",A=a,B=c)+".ReturnValue"
def sel(b,cond,a,c): return mcall(b,"SelectInt",bPickA=cond,A=a,B=c)+".ReturnValue"
def branch(b,cond):
    n=b.n("Branch"); b.c(cond,n+".Condition"); return n

def tc(_tool,**a):
    r=subprocess.run([CLI,"--output","json","tool","call",_tool,"--args",json.dumps(a)],capture_output=True,text=True,encoding="utf-8")
    try: d=json.loads(r.stdout)
    except Exception: raise SystemExit(f"FAIL {_tool} {a}\n{r.stdout}\n{r.stderr}")
    if not d.get("ok",True): raise SystemExit(f"FAIL {_tool} {a}\n{json.dumps(d,ensure_ascii=False)[:600]}")
    return d.get("data",d)

GIP="/Game/ShrinkRooms/Core/BP_GameInstance"
def wire_button(W,btn,fn):
    b=BP(W)
    ids=[n["id"] for n in b.graph()["nodes"] if "OnClicked" in n.get("title","") or "On Clicked" in n.get("title","")]
    ev=ids[-1] if ids else None
    if not ev: raise SystemExit("no event node for "+btn+str([n["title"] for n in b.graph()["nodes"]]))
    g=b.n("CallFunction","GetGameInstance","GameplayStatics")
    c=b.n("Cast",GIP); b.c(g+".ReturnValue",c+".Object")
    f=b.n("CallFunction",fn,GIP); b.c(c+".AsBP Game Instance",f+".self")
    b.c(ev+".then",c+".execute"); b.c(c+".then",f+".execute")
    return b
def build_widget(W,title,buttons,fontsize=72):
    tc("widget_create",path=W)
    tc("widget_add",path=W,**{"class":"TextBlock","name":"TitleText"})
    tc("widget_layout",path=W,widget="TitleText",anchor="Center",position=[0,-120],alignment=[0.5,0.5],autoSize=True)
    tc("widget_set_prop",path=W,widget="TitleText",property="Text",value=title)
    tc("widget_set_prop",path=W,widget="TitleText",property="Font",value=f"(Size={fontsize})")
    y=40
    for name,label,fn in buttons:
        tc("widget_add",path=W,**{"class":"Button","name":name,"isVariable":True})
        tc("widget_layout",path=W,widget=name,anchor="Center",position=[0,y],size=[300,70],alignment=[0.5,0.5])
        tc("widget_add",path=W,**{"class":"TextBlock","name":name+"Label","parent":name})
        tc("widget_set_prop",path=W,widget=name+"Label",property="Text",value=label)
        tc("widget_bind",path=W,widget=name,event="OnClicked")
        y+=90
    for name,label,fn in buttons:
        pass

def foreach(b,arr):
    n=b.n("Macro","ForEachLoop"); b.c(arr,n+".Array"); return n,n+".Array Element"
def same_cell(b,e,f2):
    return AND(b,eqi(b,vg(b,"GridX",BASE,e),vg(b,"GridX",BASE,f2)),eqi(b,vg(b,"GridY",BASE,e),vg(b,"GridY",BASE,f2)))
def remove(b,obj):
    n=b.n("CallFunction","RemoveFromGrid",BASE); b.c(obj,n+".self"); return n
