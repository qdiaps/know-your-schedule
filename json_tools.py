"""
Copyright (c) 2023 qdiaps

Програмне забеспечення поширюється з ліцензією MIT.
Детальніше дивіться у файлі LICENSE.
"""

import json
import os

def serialization(to_json, path):
	with open(path, 'w') as file:
		json.dump(to_json, file, ensure_ascii=False, sort_keys=True, indent=2)

def deserialization(path):
	if os.path.isfile(path):
		try:
			with open(path) as file:
				return json.load(file)
		except Exception:
			print('Exception: json_tools.py -> deserialization()')
		finally:
			return 
	else:
		open(path, 'w')