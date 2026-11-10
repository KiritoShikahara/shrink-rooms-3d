import unreal
actors=unreal.EditorLevelLibrary.get_all_level_actors()
if not any(a.get_actor_label()=="PostFX" for a in actors):
    a=unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.PostProcessVolume, unreal.Vector(0,0,0))
    a.set_actor_label("PostFX")
else:
    a=[x for x in actors if x.get_actor_label()=="PostFX"][0]
a.set_editor_property("unbound", True)
s=a.get_editor_property("settings")
def ov(n,v):
    s.set_editor_property("override_"+n,True); s.set_editor_property(n,v)
ov("bloom_intensity",0.8); ov("vignette_intensity",0.45)
ov("auto_exposure_method",unreal.AutoExposureMethod.AEM_MANUAL); ov("auto_exposure_bias",11.0)
ov("color_saturation",unreal.Vector4(1.1,1.1,1.1,1.0))
a.set_editor_property("settings",s)
for l in actors:
    if l.get_actor_label()=="Sun":
        l.get_component_by_class(unreal.DirectionalLightComponent).set_editor_property("intensity",6.0)
        l.get_component_by_class(unreal.DirectionalLightComponent).set_editor_property("light_color",unreal.Color(255,236,214,255))
print("ppv ok")
