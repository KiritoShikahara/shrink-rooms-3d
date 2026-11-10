import unreal
by={a.get_actor_label():a for a in unreal.EditorLevelLibrary.get_all_level_actors()}
sk=by["Sky"].get_component_by_class(unreal.SkyLightComponent); sk.set_editor_property("intensity",4.5)
a=by["PostFX"]; s=a.get_editor_property("settings")
s.set_editor_property("override_ambient_occlusion_intensity",True); s.set_editor_property("ambient_occlusion_intensity",0.3)
a.set_editor_property("settings",s)
print("ok")
