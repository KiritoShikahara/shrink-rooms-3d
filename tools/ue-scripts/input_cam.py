import unreal
at=unreal.AssetToolsHelpers.get_asset_tools(); eal=unreal.EditorAssetLibrary
def ia(name):
    p=f"/Game/ShrinkRooms/Player/{name}"
    if eal.does_asset_exist(p): a=eal.load_asset(p)
    else: a=at.create_asset(name,"/Game/ShrinkRooms/Player",unreal.InputAction,unreal.InputAction_Factory())
    a.set_editor_property("value_type",unreal.InputActionValueType.AXIS1D); eal.save_loaded_asset(a); return a
yaw,pitch,zoom=ia("IA_CamYaw"),ia("IA_CamPitch"),ia("IA_CamZoom")
def ia_bool(name):
    p=f"/Game/ShrinkRooms/Player/{name}"
    a=eal.load_asset(p) if eal.does_asset_exist(p) else at.create_asset(name,"/Game/ShrinkRooms/Player",unreal.InputAction,unreal.InputAction_Factory())
    a.set_editor_property("value_type",unreal.InputActionValueType.BOOLEAN); eal.save_loaded_asset(a); return a
reset=ia_bool("IA_CamReset"); pause=ia_bool("IA_Pause")
p="/Game/ShrinkRooms/Player/IMC_Camera"
imc=eal.load_asset(p) if eal.does_asset_exist(p) else at.create_asset("IMC_Camera","/Game/ShrinkRooms/Player",unreal.InputMappingContext,unreal.InputMappingContext_Factory())
imc.unmap_all()
def K(n):
    k=unreal.Key(); k.set_editor_property("key_name",n); return k
maps=[]
def mapping(action,key,negate=False):
    m=unreal.EnhancedActionKeyMapping(); m.set_editor_property("action",action); m.set_editor_property("key",K(key))
    m.set_editor_property("modifiers",[unreal.new_object(unreal.InputModifierNegate,outer=imc)] if negate else []); maps.append(m)
mapping(yaw,"E"); mapping(yaw,"Q",True)
mapping(pitch,"Z"); mapping(pitch,"X",True)
mapping(zoom,"MouseWheelAxis"); mapping(yaw,"Gamepad_RightX"); mapping(pitch,"Gamepad_RightY"); mapping(zoom,"Gamepad_RightTriggerAxis"); mapping(zoom,"Gamepad_LeftTriggerAxis",True); mapping(pause,"Gamepad_Special_Right"); mapping(reset,"C"); mapping(pause,"Escape")
d=imc.get_editor_property("default_key_mappings"); d.set_editor_property("mappings",maps); imc.set_editor_property("default_key_mappings",d)
eal.save_loaded_asset(imc); print("cam input ok",len(maps))
