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
	for path in paths:
		try:
			obj = json.load(path.open())
			created_at = datetime.strptime(obj['created_at'], '%a %b %d %H:%M:%S +0000 %Y') + timedelta(hours=9)
			day = created_at.day
			hour = created_at.hour
			#print(created_at)
			if time_freq.get( (day, hour) ) is None:
				time_freq[ (day, hour) ] = 0
			time_freq[ (day, hour) ] += 1
		except Exception as ex:
			print(ex)

	return time_freq

args = [(key,paths) for key,paths in key_paths.items()]
time_freq = {}
with PPE(max_workers=12) as exe:
	for _time_freq in exe.map(pmap, args):
		for time, freq in _time_freq.items():
			if time_freq.get(time) is None:
				time_freq[time] = 0
			time_freq[time]+=freq
for time, freq in sorted( time_freq.items(), key=lambda x:x[0]):
	print(time, freq)

