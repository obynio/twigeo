#!/usr/bin/python3

import json
import gmplot

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from config import Config

longs=[]
lats=[]

class StdOutListener(StreamListener):

    def on_data(self, data):
        parsed_json = json.loads(data)
        if 'coordinates' in parsed_json and parsed_json['coordinates'] is not None:
            longs.append(parsed_json['coordinates']['coordinates'][0])
            lats.append(parsed_json['coordinates']['coordinates'][1])
            print(parsed_json['id_str'])

            gmap = gmplot.GoogleMapPlotter(46.52,2.43, 6)
            gmap.heatmap(lats, longs, threshold=3, radius=20, gradient=[
                (0,0,255,0),
                (0,50,204,1),
                (0,101,153,1),
                (0,153,101,1),
                (0,204,50,1),
                (0,255,0,1),
                (51,203,0,1),
                (102,152,0,1),
                (153,101,0,1),
                (203,51,0,1),
                (255,0,0,1)])
            gmap.draw("twigeo.html")
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    auth = OAuthHandler(Config['CONSUMER_KEY'], Config['CONSUMER_SECRET'])
    auth.set_access_token(Config['ACCESS_TOKEN_KEY'], Config['ACCESS_TOKEN_SECRET'])
    stream = Stream(auth, StdOutListener())

    stream.filter(locations=[-4.9,42.36,8.42,51.23])
