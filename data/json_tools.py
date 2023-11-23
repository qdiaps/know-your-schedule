import json
import os

def create_path(file_name: str) -> str:
	return f'data/{file_name}'

def serialization(to_json: object, file_name: str) -> None:
	path = create_path(file_name)
	with open(path, 'w') as file:
		json.dump(to_json, file, ensure_ascii=False, indent=2)

def deserialization(file_name: str) -> object:
	path = create_path(file_name)
	from_json = {}
	if os.path.isfile(path):
		try:
			with open(path) as file:
				from_json = json.load(file)
		except Exception:
			print('Exception: json_tools.py -> deserialization()')
		finally:
			return from_json
	else:
		open(path, 'w')