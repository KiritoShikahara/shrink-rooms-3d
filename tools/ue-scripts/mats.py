import unreal
mel=unreal.MaterialEditingLibrary; eal=unreal.EditorAssetLibrary
P=unreal.MaterialProperty
COL={'M_Floor':(0.35,0.35,0.4),'M_Wall':(0.15,0.15,0.2),'M_BoxWood':(0.6,0.4,0.2),'M_BoxIron':(0.5,0.55,0.6),'M_Player':(0.2,0.6,1.0),'M_Goal':(0.2,0.9,0.3),'M_Pit':(0.02,0.02,0.02),'M_Plate':(0.9,0.8,0.2),'M_Door':(0.7,0.2,0.2),'M_Key':(1.0,0.85,0.1)}
spec={ # name: (rough, metallic, emissive multiplier)
 "M_Floor":(0.8,0.0,0),"M_Wall":(0.6,0.1,0),"M_BoxWood":(0.7,0.0,0),"M_BoxIron":(0.35,0.9,0),
 "M_Player":(0.3,0.0,1.2),"M_Goal":(0.4,0.0,4),"M_Pit":(1.0,0.0,0),"M_Plate":(0.4,0.0,2),"M_Door":(0.5,0.2,0.3),"M_Key":(0.2,0.8,3)}
for n,(r,m,e) in spec.items():
    mat=eal.load_asset(f"/Game/ShrinkRooms/Art/{n}")
    c=unreal.LinearColor(*COL[n],1)
    rn=mel.create_material_expression(mat,unreal.MaterialExpressionConstant,-400,200); rn.set_editor_property("r",r); mel.connect_material_property(rn,"",P.MP_ROUGHNESS)
    mn=mel.create_material_expression(mat,unreal.MaterialExpressionConstant,-400,300); mn.set_editor_property("r",m); mel.connect_material_property(mn,"",P.MP_METALLIC)
    if e>0:
        en=mel.create_material_expression(mat,unreal.MaterialExpressionConstant3Vector,-400,400)
        en.set_editor_property("constant",unreal.LinearColor(c.r*e,c.g*e,c.b*e,1)); mel.connect_material_property(en,"",P.MP_EMISSIVE_COLOR)
    mel.recompile_material(mat); eal.save_loaded_asset(mat)
print("done")
