import jmespath
import datetime
from jmespath import search
import json
import time
import requests
import os
import regex as re
import urllib.request
print(datetime.datetime.now())


f = open('data.json')
data = json.load(f)
data_dict = json.loads(data)
course_name = "testing"



def download_files(data_dict, course_name):
    os.mkdir(course_name)
    for key, values in data_dict.items():
        week_directory = course_name + "/" + key
        os.mkdir(week_directory)
        starting_num = 0
        for sec_key, item in values.items():
            starting_num += 1
            if item["type"] == "lecture":
                name = re.sub('[?|:|>|<|*|"]', "", item["name"])
                temp_dict = week_directory + "/" + str(starting_num) + "_item_" + name
                os.mkdir(temp_dict)
                # with open(temp_dict + '/video.txt', 'w') as txt_f:
                #     txt_f.write(item["high_res_vid_url"])
                url_link1 = item["high_res_vid_url"]
                # url_link2 = "https://d3c33hcgiwev3.cloudfront.net/abhM6dA4EeWi0Q60YgYqQQ.processed/full/720p/index.webm?Expires=1640822400&Signature=SV93lY6LmgmJpdKxI0-s763TG3DhMkSW2n7me8j2a91EPPzSfCY9DnzrLwjE~nXoTFzGmhQ6J5ZcdUOyU0GjIFCNh7XyT2z9eDAgiFvE2C0RC28fQHqc9JU4ouPyvH3Ce~bvbELDQQSTT2kBA~P7BFkkwkiaEn09I06mGrlWHvw_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A"
                # url_link3 = "https://d3c33hcgiwev3.cloudfront.net/abhM6dA4EeWi0Q60YgYqQQ.processed/full/720p/index.webm?Expires=1640822400&Signature=SV93lY6LmgmJpdKxI0-s763TG3DhMkSW2n7me8j2a91EPPzSfCY9DnzrLwjE~nXoTFzGmhQ6J5ZcdUOyU0GjIFCNh7XyT2z9eDAgiFvE2C0RC28fQHqc9JU4ouPyvH3Ce~bvbELDQQSTT2kBA~P7BFkkwkiaEn09I06mGrlWHvw_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A"
                urllib.request.urlretrieve(url_link1, 'asas.mp4')
                b = 1


download_files(data_dict, course_name)