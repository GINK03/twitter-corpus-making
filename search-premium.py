from TwitterAPI import TwitterAPI
import os
import datetime
from datetime import timedelta
import json
import time
consumer_key=os.environ['consumer_key']
consumer_secret=os.environ['consumer_secret']
access_token=os.environ['access_token']
access_token_secret=os.environ['access_token_secret']

# ライブラリ
# https://github.com/twitterdev/search-tweets-python
# query参考
# https://twittercommunity.com/t/premium-api-endpoint/101041/3
LABEL = 'dev2'
api = TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)

now = datetime.datetime.now()
past_year = now - timedelta(days=30)

# 時間分割して、スキャンしていく
for i in range(30*24):
	past_year += timedelta(minutes=60)
	start = past_year.strftime('%Y%m%d%H%M')
	end   = (past_year + timedelta(minutes=9)).strftime('%Y%m%d%H%M')
	print(start, end)
	r = api.request(f'tweets/search/30day/:{LABEL}',
                {'query':'FGO', 'maxResults':"100", 'fromDate':'201811010000', 'toDate':'201811012300'})
		
	buff = [item for item in r]
	obj = json.dumps(buff, indent=2, ensure_ascii=False)
	open(f'search_premiums/{start}.json', 'w').write( obj )
	time.slee(1.0)
