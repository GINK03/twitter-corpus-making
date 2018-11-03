from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
from hashlib import sha256
import os

consumer_key=os.environ['consumer_key']
consumer_secret=os.environ['consumer_secret']
access_token=os.environ['access_token']
access_token_secret=os.environ['access_token_secret']

class StdOutListener(StreamListener):
		""" A listener handles tweets that are received from the stream.
		This is a basic listener that just prints received tweets to stdout.
		"""
		def on_data(self, data):
				obj = json.loads(data)
				serialized = json.dumps(obj, indent=2, ensure_ascii=False)
				hashed = sha256(bytes(serialized, 'utf8')).hexdigest()
				open(f'jsons/{hashed}', 'w').write( serialized )
				print(serialized)
				return True

		def on_error(self, status):
				print(status)

def random_sample():
		l = StdOutListener()
		auth = OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		stream = Stream(auth, l)
		stream.sample(languages=['ja'])	

def filter_words():
		l = StdOutListener()
		auth = OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		stream = Stream(auth, l)
		stream.filter(languages=["ja"], track=['ベイスターズ', 'FGO', '艦これ', 'パズドラ', 'モンスト', 'オセロニア'])

def rap(func):
	func()
from concurrent.futures import ProcessPoolExecutor as PPE
if __name__ == '__main__':
	with PPE(max_workers=2) as exe:
		exe.map(rap, [random_sample, filter_words])
