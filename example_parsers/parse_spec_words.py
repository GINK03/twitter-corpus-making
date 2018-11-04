from pathlib import Path
import json
for path in Path('../jsons').glob('*'):
	obj = json.load(path.open())
	user = obj['user']
	text = obj['text']
	if '判例' not in text:
		continue
	print(obj['created_at'], user['screen_name'], obj['text'].replace('\n', ' '))
