from pathlib import Path
import json
from datetime import *
from concurrent.futures import ProcessPoolExecutor as PPE


key_paths = {}
for index, path in enumerate(Path('../jsons').glob('*')):
	key = index%12
	if key_paths.get(key) is None:
		key_paths[key] = []
	key_paths[key].append(path)

def pmap(arg):
	key, paths = arg
	time_freq = {}
	fp = open(f'tweets_{key:04d}.txt', 'w')
	for path in paths:
		try:
			obj = json.load(path.open())
			created_at = datetime.strptime(obj['created_at'], '%a %b %d %H:%M:%S +0000 %Y') + timedelta(hours=9)
			day = created_at.day
			hour = created_at.hour
			text = obj['text']
			fp.write(text.replace('\n', ' ') + '\n')
		except Exception as ex:
			print(ex)
	return 

args = [(key,paths) for key,paths in key_paths.items()]
with PPE(max_workers=12) as exe:
	exe.map(pmap, args)

