import unreal
actors=unreal.EditorLevelLibrary.get_all_level_actors()
by={a.get_actor_label():a for a in actors}
a=by["PostFX"]; s=a.get_editor_property("settings")
s.set_editor_property("auto_exposure_bias",9.6)
a.set_editor_property("settings",s)
sun=by["Sun"].get_component_by_class(unreal.DirectionalLightComponent); sun.set_editor_property("intensity",3.5)
if "Fill" not in by:
    f=unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.DirectionalLight, unreal.Vector(0,0,1600), unreal.Rotator(0,-155,-60))
    f.set_actor_label("Fill")
else: f=by["Fill"]
fc=f.get_component_by_class(unreal.DirectionalLightComponent)
fc.set_editor_property("intensity",1.4); fc.set_editor_property("cast_shadows",False)
sk=by["Sky"].get_component_by_class(unreal.SkyLightComponent); sk.set_editor_property("intensity",0.8)
print("ok")
