import unreal
imc=unreal.load_asset("/Game/ShrinkRooms/Player/IMC_Default")
mv=unreal.load_asset("/Game/ShrinkRooms/Player/IA_Move")
rt=unreal.load_asset("/Game/ShrinkRooms/Player/IA_Retry")
imc.unmap_all()
def K(n):
    k=unreal.Key(); k.set_editor_property("key_name",n); return k
def mk(cls):
    return unreal.new_object(cls, outer=imc)
def add(action,keyname,negate=False,swizzle=False):
    m=imc.map_key(action,K(keyname))
dkm=imc.get_editor_property("default_key_mappings")
maps=[]
def mapping(action,keyname,negate=False,swizzle=False):
    m=unreal.EnhancedActionKeyMapping()
    m.set_editor_property("action",action); m.set_editor_property("key",K(keyname))
    mods=[]
    if swizzle:
        s=mk(unreal.InputModifierSwizzleAxis); s.set_editor_property("order",unreal.InputAxisSwizzle.YXZ); mods.append(s)
    if negate: mods.append(mk(unreal.InputModifierNegate))
    m.set_editor_property("modifiers",mods); maps.append(m)
for k in ("D","Right"): mapping(mv,k)
for k in ("A","Left"): mapping(mv,k,negate=True)
for k in ("W","Up"): mapping(mv,k,swizzle=True)
for k in ("S","Down"): mapping(mv,k,negate=True,swizzle=True)
mapping(rt,"R"); mapping(rt,"Gamepad_FaceButton_Top")
for k in ("Gamepad_DPad_Right",): mapping(mv,k)
mapping(mv,"Gamepad_DPad_Left",negate=True)
mapping(mv,"Gamepad_DPad_Up",swizzle=True)
mapping(mv,"Gamepad_DPad_Down",negate=True,swizzle=True)
dkm.set_editor_property("mappings",maps)
imc.set_editor_property("default_key_mappings",dkm)
unreal.EditorAssetLibrary.save_loaded_asset(imc)
print("OK",len(maps))
