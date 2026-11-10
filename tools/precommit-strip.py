import json
p="ShrinkRooms3D/ShrinkRooms3D.uproject"
d=json.load(open(p)); d["Plugins"]=[x for x in d["Plugins"] if x["Name"] not in ("PythonScriptPlugin","UnrealCliBridge")]
json.dump(d,open(p,"w"),indent="\t")
