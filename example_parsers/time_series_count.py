from pathlib import Path
import json
from datetime import *

time_freq = {}
for path in Path('../jsons').glob('*'):
	obj = json.load(path.open())
	created_at = datetime.strptime(obj['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
	day = created_at.day
	hour = created_at.hour
	#print(created_at)
	
	if time_freq.get( (day, hour) ) is None:
		time_freq[ (day, hour) ] = 0
	time_freq[ (day, hour) ] += 1

for time, freq in sorted( time_freq.items(), key=lambda x:x[0]):
	print(time, freq)

