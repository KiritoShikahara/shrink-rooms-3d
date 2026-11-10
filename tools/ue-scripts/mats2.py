import unreal
mel=unreal.MaterialEditingLibrary; eal=unreal.EditorAssetLibrary; P=unreal.MaterialProperty
def node(mat,cls,x=0,y=0): return mel.create_material_expression(mat,cls,x,y)
def const(mat,v,x=0,y=0):
    n=node(mat,unreal.MaterialExpressionConstant,x,y); n.set_editor_property("r",v); return n
def c3(mat,r,g,b,x=0,y=0):
    n=node(mat,unreal.MaterialExpressionConstant3Vector,x,y); n.set_editor_property("constant",unreal.LinearColor(r,g,b,1)); return n
def fresh(name,rough,metal):
    path=f"/Game/ShrinkRooms/Art/{name}"
    if eal.does_asset_exist(path): eal.delete_asset(path)
    m=unreal.AssetToolsHelpers.get_asset_tools().create_asset(name,"/Game/ShrinkRooms/Art",unreal.Material,unreal.MaterialFactoryNew())
    mel.connect_material_property(const(m,rough,-400,200),"",P.MP_ROUGHNESS); mel.connect_material_property(const(m,metal,-400,300),"",P.MP_METALLIC)
    return m
def pulse(m,speed,lo,hi):
    t=node(m,unreal.MaterialExpressionTime,-900,500)
    s=node(m,unreal.MaterialExpressionSine,-700,500); s.set_editor_property("period",1.0/speed*6.2831853); mel.connect_material_expressions(t,"",s,"")
    mu=node(m,unreal.MaterialExpressionMultiply,-500,500); mel.connect_material_expressions(s,"",mu,"A"); mu.set_editor_property("const_b",(hi-lo)/2)
    ad=node(m,unreal.MaterialExpressionAdd,-300,500); mel.connect_material_expressions(mu,"",ad,"A"); ad.set_editor_property("const_b",(hi+lo)/2)
    return ad
# C-02: checker floor from world position
m=fresh("M_Floor",0.85,0.0)
wp=node(m,unreal.MaterialExpressionWorldPosition,-1400,0)
off=node(m,unreal.MaterialExpressionAdd,-1200,0); mel.connect_material_expressions(wp,"",off,"A"); off.set_editor_property("const_b",50.0)
dv=node(m,unreal.MaterialExpressionDivide,-1000,0); mel.connect_material_expressions(off,"",dv,"A"); dv.set_editor_property("const_b",100.0)
fl=node(m,unreal.MaterialExpressionFloor,-800,0); mel.connect_material_expressions(dv,"",fl,"")
mr=node(m,unreal.MaterialExpressionComponentMask,-650,-60); mr.set_editor_property("r",True); mr.set_editor_property("g",False); mr.set_editor_property("b",False); mel.connect_material_expressions(fl,"",mr,"")
mg=node(m,unreal.MaterialExpressionComponentMask,-650,60); mg.set_editor_property("r",False); mg.set_editor_property("g",True); mg.set_editor_property("b",False); mel.connect_material_expressions(fl,"",mg,"")
sm=node(m,unreal.MaterialExpressionAdd,-500,0); mel.connect_material_expressions(mr,"",sm,"A"); mel.connect_material_expressions(mg,"",sm,"B")
hf=node(m,unreal.MaterialExpressionMultiply,-380,0); mel.connect_material_expressions(sm,"",hf,"A"); hf.set_editor_property("const_b",0.5)
fr=node(m,unreal.MaterialExpressionFrac,-260,0); mel.connect_material_expressions(hf,"",fr,"")
ck=node(m,unreal.MaterialExpressionMultiply,-140,0); mel.connect_material_expressions(fr,"",ck,"A"); ck.set_editor_property("const_b",2.0)
lp=node(m,unreal.MaterialExpressionLinearInterpolate,0,0)
mel.connect_material_expressions(c3(m,0.30,0.32,0.38,-300,-200),"",lp,"A"); mel.connect_material_expressions(c3(m,0.22,0.24,0.30,-300,-100),"",lp,"B"); mel.connect_material_expressions(ck,"",lp,"Alpha")
mel.connect_material_property(lp,"",P.MP_BASE_COLOR); mel.recompile_material(m); eal.save_loaded_asset(m)
# C-10: pulsing emissive materials
spec={"M_Goal":((0.2,0.9,0.3),0.4,4.0,2.0,0.5,1.0),"M_Key":((1.0,0.85,0.1),0.2,3.0,1.5,0.6,1.0),"M_Plate":((0.9,0.8,0.2),0.4,2.0,1.0,0.5,1.0),"M_Player":((0.2,0.6,1.0),0.3,1.2,1.0,0.8,1.0)}
metal={"M_Key":0.8}
for n,(col,rough,em,speed,lo,hi) in spec.items():
    m=fresh(n,rough,metal.get(n,0.0))
    mel.connect_material_property(c3(m,*col,-400,0),"",P.MP_BASE_COLOR)
    e=c3(m,col[0]*em,col[1]*em,col[2]*em,-400,100); p=pulse(m,speed,lo,hi)
    mu=node(m,unreal.MaterialExpressionMultiply,-100,100); mel.connect_material_expressions(e,"",mu,"A"); mel.connect_material_expressions(p,"",mu,"B")
    mel.connect_material_property(mu,"",P.MP_EMISSIVE_COLOR); mel.recompile_material(m); eal.save_loaded_asset(m)
# C-11: wall with danger parameter (0 normal, 1 warning stripes/pulse)
m=fresh("M_Wall",0.6,0.1)
dg=node(m,unreal.MaterialExpressionScalarParameter,-900,300); dg.set_editor_property("parameter_name","Danger"); dg.set_editor_property("default_value",0.0)
lp=node(m,unreal.MaterialExpressionLinearInterpolate,-300,0)
mel.connect_material_expressions(c3(m,0.15,0.15,0.2,-600,-100),"",lp,"A"); mel.connect_material_expressions(c3(m,0.6,0.07,0.05,-600,0),"",lp,"B"); mel.connect_material_expressions(dg,"",lp,"Alpha")
mel.connect_material_property(lp,"",P.MP_BASE_COLOR)
p=pulse(m,5.0,0.3,1.0); em=c3(m,3.0,0.25,0.1,-600,200)
mu=node(m,unreal.MaterialExpressionMultiply,-300,250); mel.connect_material_expressions(em,"",mu,"A"); mel.connect_material_expressions(p,"",mu,"B")
mu2=node(m,unreal.MaterialExpressionMultiply,-100,250); mel.connect_material_expressions(mu,"",mu2,"A"); mel.connect_material_expressions(dg,"",mu2,"B")
mel.connect_material_property(mu2,"",P.MP_EMISSIVE_COLOR); mel.recompile_material(m); eal.save_loaded_asset(m)
print("mats2 ok")
