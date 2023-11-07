"""
Copyright (c) 2023 qdiaps

Програмне забеспечення поширюється з ліцензією MIT.
Детальніше дивіться у файлі LICENSE.
"""

import json

from os.path import isfile

def serialization(to_json, path):
	with open(path, 'w') as file:
		json.dump(to_json, file, ensure_ascii=False, sort_keys=True, indent=2)

def deserialization(path):
	if isfile(path):
		with open(path) as file:
			return json.load(file)
	else:
		print(f'Такого файлу немає: {path}')