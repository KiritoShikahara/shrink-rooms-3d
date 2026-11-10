import unreal
a=unreal.load_asset("/Game/ShrinkRooms/Player/IA_Pause"); a.set_editor_property("trigger_when_paused",True); unreal.EditorAssetLibrary.save_loaded_asset(a); print("ok")
