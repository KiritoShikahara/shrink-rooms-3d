import unreal
by={a.get_actor_label():a for a in unreal.EditorLevelLibrary.get_all_level_actors()}
if "Fill" in by: unreal.EditorLevelLibrary.destroy_actor(by["Fill"])
sk=by["Sky"].get_component_by_class(unreal.SkyLightComponent); sk.set_editor_property("intensity",2.2); sk.set_editor_property("real_time_capture",False)
print("ok")
