import jmespath
import scrapy
import datetime
from jmespath import search
import json
import time
import requests
import os
import regex as re
import urllib.request
print(datetime.datetime.now())


class CourseraVideosSpider(scrapy.Spider):
    name = 'coursera_videos'
    allowed_domains = ['coursera.org']
    video_api_url = "https://www.coursera.org/api/onDemandLectureVideos.v1/{course_id}~{lecture_id}?includes=video&fields=onDemandVideos.v1"
    headers = {
    'authority': 'www.coursera.org',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'accept-language': 'en',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    'x-coursera-application': 'ondemand',
    'accept': '*/*',
    'x-requested-with': 'XMLHttpRequest',
    'x-coursera-version': 'ec6ca601ce56fee6a1a3e7b753f0ff4f4c035d80',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.coursera.org/learn/html-css-javascript-for-web-developers/home/welcome'
    }
    cookie = {
        "__204u": "5574745519-1635842887586",
        "__204r": "",
        "_ga": "GA1.2.924996604.1635842889",
        "usprivacy": "1---",
        "OptanonAlertBoxClosed": "2021-11-02T08:48:20.267Z",
        "OneTrustWPCCPAGoogleOptOut": "true",
        "profileconsent": "eyI3MTY0NTQwMCI6eyJjY3BhUmVxdWlyZWQiOmZhbHNlLCJnZHByUmVxdWlyZWQiOmZhbHNlfX0=",
        "_gcl_au": "1.1.1456061497.1635842930",
        "_hjid": "0f39e25f-1f60-4354-8f97-3b49a6556a0b",
        "CSRF3-Token": "1639168153.7d3FcZIEmYfks4K1",
        "_hjSessionUser_469298": "eyJpZCI6IjdmNjc3MDQ0LTJkZjYtNTg0NC1iOTZkLWRlMzE2MmIyNzcxNyIsImNyZWF0ZWQiOjE2MzgzMDQxNTU2NDgsImV4aXN0aW5nIjp0cnVlfQ==",
        "CAUTH": "ys5dfSQYEMCi8FoYC2igTu0pq_2CL5rMREKZ4dgTJ7QEJgygpTXJU5YY8zJTAuSczEo__yayhRmA9ixxPrpfKA.dcMiZqJRulQf_ddB7ixnNw.A9Glxxaz4quFC-F4da_2ELB6av15b4L1hcE127ng71RHyhSaCl1etKtgED4t4mIWgNyXVKpY1MDFU4AKYQdOgVWyM8TLiPmE8sy8Ofpolire6FufhAptebrvercE83cLICOpDTPMj6NMH55xElFSEwTmL1BkBpv2ElDfnlig6GVg7m9zO86zE_mHoe3BIMg23pYPSaaLy0kfDiOUZHyzkM7AKLLe57LDwYT5BUsDtmF2LX7kA902C4GZ5Wuo75AWoghN9Vm76a7E3Q88pZTuYcCwpF8wfKWzIF2Db9sc2Ev1bGfuyLxiV-ss_80q69dQtjqN77-So3p4tCx8e83ihxV-D25ciwb-4eJu1u_VMMjqrLN9vHoSp5Ndp1E_rykA9G0exDFckaF9dOmlFirgcwnb4jbCbO7DBnFXkcodWU4",
        "__400v": "f899b8e3-55de-4193-938a-705e140561ab",
        "_gid": "GA1.2.124910383.1638822875",
        "stc113717": "env:1%7C20220106203434%7C20211206210435%7C2%7C1030880:20221206203435|uid:1638822874936.236369272.33789492.113717.1660582156:20221206203435|srchist:1030880%3A1%3A20211208164958%7C1030881%3A1636305146%3A20211208171226%7C1030880%3A1%3A20220106203434:20221206203435|a-rfd:www.coursera.org:20221202231324|nsc:1:20221107165814|tsa:1638822874936.452789682.15038586.2584346066891001.:20211206210435",
        "OptanonConsent": "isIABGlobal=true&datestamp=Mon+Dec+06+2021+22%3A34%3A35+GMT%2B0200+(Eastern+European+Standard+Time)&version=6.10.0&landingPath=NotLandingPage&groups=C0004%3A0%2CC0003%3A0%2CC0002%3A0%2CC0001%3A1&hosts=H3%3A0%2CH4%3A0%2CH49%3A0%2CH5%3A0%2CH6%3A0%2CH7%3A0%2CH8%3A0%2CH9%3A0%2CH10%3A0%2CH11%3A0%2CH12%3A0%2Cnpf%3A0%2CH13%3A0%2CH14%3A0%2CH15%3A0%2CH16%3A0%2CH17%3A0%2CH18%3A0%2CH53%3A0%2CH54%3A0%2CH19%3A0%2CH20%3A0%2CH21%3A0%2CH55%3A0%2CH22%3A0%2CH23%3A0%2CH47%3A0%2CH24%3A0%2CH25%3A0%2CH26%3A0%2CH27%3A0%2CH28%3A0%2CH29%3A0%2CH30%3A0%2CH31%3A0%2CH32%3A0%2CH33%3A0%2CH34%3A0%2CH35%3A0%2CH36%3A0%2Ccsg%3A0%2CH37%3A0%2Cebp%3A0%2Clit%3A0%2CH38%3A0%2CH39%3A0%2CH52%3A0%2CH40%3A0%2CH45%3A0%2CH56%3A1%2CH57%3A1&geolocation=LT%3BVL&AwaitingReconsent=false",
        "__400vt": "1638824188191",
    }
    start_url = "https://www.coursera.org/api/guidedCourseWeekCards.v1?ids=71645400~html-css-javascript-for-web-developers&fields=courseId,id,weeks"
    start_urls = ["coursera.org/"]
    skaicius = "testing"

    def start_requests(self):
        if self.skaicius != "testing":
            yield scrapy.Request(url=self.start_url, method="GET", cookies=self.cookie,
                                 callback=self.parse_course_structure, headers=self.headers)
        # for testing
        else:
            f = open('data.json')
            data = json.load(f)
            data_dict = json.loads(data)
            self.download_files(data_dict)

    def parse_course_structure(self, response):
        data_dict = {}
        course_info = json.loads(response.text)
        course_id = search("elements[0].courseId", course_info)
        course_name = "dont know how to take it yet"
        weeks = search("elements[0].weeks", course_info)
        for idx, week in enumerate(weeks):
            week_var = "week_" + str(idx + 1)
            data_dict[week_var] = {}
            content = search("modules[0].items", week)
            for idx2, item in enumerate(content):
                item_var = "item_" + str(idx2 + 1)
                temp_dict = {
                    "name": search("name", item),
                    "type": search("contentSummary.typeName", item),
                    "url": "https://www.coursera.org" + search("resourcePath", item)
                }
                if temp_dict["type"] == "lecture":
                    video_id = temp_dict["url"].split("lecture/")[1].split("/")[0]
                    video_url = self.video_api_url.format(course_id=course_id, lecture_id=video_id)
                    video_api = {"video_api_url": video_url}
                    temp_dict.update(video_api)
                    response = requests.get(url=video_url)
                    if response:
                        get_dict = json.loads(response.text)
                        high_res_vid_url = jmespath.search('linked."onDemandVideos.v1"[0].sources.byResolution."720p".webMVideoUrl', get_dict)
                        temp_dict.update({"high_res_vid_url": high_res_vid_url})
                    else:
                        temp_dict.update({"high_res_vid_url": "failed to get"})
                    time.sleep(3)
                data_dict[week_var][item_var] = temp_dict
        # for creating json file
        data_dict_string = json.dumps(data_dict)
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data_dict_string, f, ensure_ascii=False, indent=4)
        # go to next function
        self.download_files(data_dict)

    def download_files(self, data_dict, course_name="testingas"):
        os.mkdir(course_name)
        for key, values in data_dict.items():
            week_directory = course_name + "/" + key
            os.mkdir(week_directory)
            starting_num = 0
            for sec_key, item in values.items():
                if item["type"] == "lecture":
                    time.sleep(5)
                    starting_num += 1
                    name = re.sub('[?|:|>|<|*|"]', "", item["name"])
                    # temp_directory = week_directory + "/" + str(starting_num) + "_item_" + name
                    # os.mkdir(temp_directory)
                    url_link = item["high_res_vid_url"]
                    urllib.request.urlretrieve(url_link, week_directory + "/" + str(starting_num) + "_video_" + name + '.mp4')
