import json
import os

def create_path(path: str):
	return f'data/{path}'

def serialization(to_json, path: str):
	json_path = create_path(path)
	with open(json_path, 'w') as file:
		json.dump(to_json, file, ensure_ascii=False, sort_keys=True, indent=2)

def deserialization(path: str):
	json_path = create_path(path)
	if os.path.isfile(json_path):
		try:
			with open(json_path) as file:
				return json.load(file)
		except Exception:
			print('Exception: json_tools.py -> deserialization()')
		finally:
			return 
	else:
		open(json_path, 'w')