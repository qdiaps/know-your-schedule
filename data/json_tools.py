import json
import os

def create_path(path: str) -> str:
	return f'data/{path}'

def serialization(to_json: object, path: str) -> None:
	json_path = create_path(path)
	with open(json_path, 'w') as file:
		json.dump(to_json, file, ensure_ascii=False, sort_keys=True, indent=2)

def deserialization(path: str) -> object:
	json_path = create_path(path)
	from_json = None
	if os.path.isfile(json_path):
		try:
			with open(json_path) as file:
				from_json = json.load(file)
		except Exception:
			print('Exception: json_tools.py -> deserialization()')
		finally:
			return from_json
	else:
		open(json_path, 'w')