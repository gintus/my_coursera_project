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
import functools
# print(datetime.datetime.now())


class CourseraVideosSpider(scrapy.Spider):
    name = 'coursera_videos'
    allowed_domains = ['coursera.org']
    video_api_url = "https://www.coursera.org/api/onDemandLectureVideos.v1/{course_id}~{lecture_id}?includes=video&fields=onDemandVideos.v1"
    name_api_url = "https://www.coursera.org/api/courses.v1?q=slug&slug={course_slug}&showHidden=true&fields=id,instructorIds"
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
    # course_slug = "python-data-analysis"
    course_slug = "html-css-javascript-for-web-developers"
    video_quality = "540"
    # video_quality = "720"
    start_url = "https://www.coursera.org/api/onDemandCourseMaterials.v2/?q=slug&slug={}&includes=modules%2Clessons%2CpassableItemGroups%2CpassableItemGroupChoices%2CpassableLessonElements%2Citems%2Ctracks%2CgradePolicy%2CgradingParameters&fields=moduleIds%2ConDemandCourseMaterialModules.v1(name%2Cslug%2Cdescription%2CtimeCommitment%2ClessonIds%2Coptional%2ClearningObjectives)%2ConDemandCourseMaterialLessons.v1(name%2Cslug%2CtimeCommitment%2CelementIds%2Coptional%2CtrackId)%2ConDemandCourseMaterialPassableItemGroups.v1(requiredPassedCount%2CpassableItemGroupChoiceIds%2CtrackId)%2ConDemandCourseMaterialPassableItemGroupChoices.v1(name%2Cdescription%2CitemIds)%2ConDemandCourseMaterialPassableLessonElements.v1(gradingWeight%2CisRequiredForPassing)%2ConDemandCourseMaterialItems.v2(name%2Cslug%2CtimeCommitment%2CcontentSummary%2CisLocked%2ClockableByItem%2CitemLockedReasonCode%2CtrackId%2ClockedStatus%2CitemLockSummary)%2ConDemandCourseMaterialTracks.v1(passablesCount)%2ConDemandGradingParameters.v1(gradedAssignmentGroups)&showLockedItems=true"
    start_urls = ["coursera.org/"]
    # i_am_testing = "not testing"
    i_am_testing = "downloading_videos"
    # params = {
    #     'q': 'slug',
    #     'slug': 'html-css-javascript-for-web-developers',
    #     'includes':
    #      'modules,lessons,passableItemGroups,passableItemGroupChoices,passableLessonElements,items,tracks,gradePolicy,gradingParameters',
    #     'fields':
    #      'moduleIds,onDemandCourseMaterialModules.v1(name,slug,description,timeCommitment,lessonIds,optional,learningObjectives),onDemandCourseMaterialLessons.v1(name,slug,timeCommitment,elementIds,optional,trackId),onDemandCourseMaterialPassableItemGroups.v1(requiredPassedCount,passableItemGroupChoiceIds,trackId),onDemandCourseMaterialPassableItemGroupChoices.v1(name,description,itemIds),onDemandCourseMaterialPassableLessonElements.v1(gradingWeight,isRequiredForPassing),onDemandCourseMaterialItems.v2(name,slug,timeCommitment,contentSummary,isLocked,lockableByItem,itemLockedReasonCode,trackId,lockedStatus,itemLockSummary),onDemandCourseMaterialTracks.v1(passablesCount),onDemandGradingParameters.v1(gradedAssignmentGroups)',
    #     'showLockedItems': 'true'
    # }

    def start_requests(self):
        course_url = self.start_url.format(self.course_slug)
        if self.i_am_testing != "downloading_videos" and self.i_am_testing != "api_response":
            yield scrapy.Request(url=course_url, method="GET", cookies=self.cookie,
                                 callback=self.parse_course_structure, headers=self.headers)
        # for testing collected url info
        elif self.i_am_testing == "downloading_videos":
            with open('all_lessons_dict.json') as f:
                data = json.load(f)
            data_dict = json.loads(data)
            self.download_files(data_dict, "testing HTML CSS and Javascript for Web Developers", self.video_quality)

    def parse_course_structure(self, response):
        course_info = json.loads(response.text)
        if not course_info:
            return
        # getting course name
        course_name = self.get_course_name(self.course_slug, self.name_api_url)
        course_id = search("elements[0].id", course_info)
        # getting week related data and the main dictionary dictionary in which we will store all the data
        all_lessons_dict, week_ids_dict = self.organize_week_information(course_info)
        # getting all segment related information
        segments_information = search('linked."onDemandCourseMaterialLessons.v1"', course_info)
        # create a file segment file name from segment slug
        segments_information = self.create_segment_file_name(segments_information)
        # update segment information
        updated_segments_information = list(map(functools.partial(self.allocating_weeks_in_segments,
                                                                  week_ids_dict=week_ids_dict), segments_information))
        # updating all_lessons_dict with segment information
        self.updating_all_lessons_dict_with_segments(all_lessons_dict, updated_segments_information)
        # going through all the lessons
        all_lessons = search('linked."onDemandCourseMaterialItems.v2"', course_info)
        # id = lesson url id, moduleId = weeks id, lessonId = segment id
        updated_all_lessons_information = list(map(functools.partial(
            self.updating_all_lessons_information, updated_segments_information=updated_segments_information,
            video_api_url=self.video_api_url, course_id=course_id), all_lessons))
        # get all the high res video urls and put them to the all_lessons_dict
        all_lessons_dict = self.update_all_lessons_dict_with_high_res_video_url(updated_all_lessons_information,
                                                                                all_lessons_dict)
        # creating json file
        self.creating_json(all_lessons_dict)
        # download videos to your computer
        self.download_files(all_lessons_dict, course_name)

    @staticmethod
    def get_course_name(course_slug, name_api_url):
        name_api_full_url = name_api_url.format(course_slug=course_slug)
        name_api_response = requests.get(url=name_api_full_url)
        if name_api_response:
            name_api_response_dict = json.loads(name_api_response.text)
            course_name = search("elements[0].name", name_api_response_dict)
            clean_course_name = re.sub('[?|:|>|<|*|"|,|.]', "", course_name)
            return clean_course_name
        else:
            return "course_name_not_found"

    @staticmethod
    def organize_week_information(course_info):
        all_weeks = search("elements[0].moduleIds", course_info)
        all_lessons_dict = {}
        week_ids_dict = {}
        for index, week in enumerate(all_weeks):
            week_var = "week_" + str(index + 1)
            all_lessons_dict[week_var] = {}
            week_ids_dict.update({week: week_var})
        return all_lessons_dict, week_ids_dict

    @staticmethod
    def create_segment_file_name(segments_information):
        for index, segment in enumerate(segments_information):
            segment["segment_file_name"] = str(index + 1) + "_" + segment["slug"].replace("-", "_")
        return segments_information

    @staticmethod
    def allocating_weeks_in_segments(segment, week_ids_dict):
        week_id = jmespath.search("moduleId", segment)
        segment["week"] = week_ids_dict[week_id]
        # this will be used as a key so we need to make it a string
        lessons_string = ",".join(segment["itemIds"])
        segment["lessons_string"] = lessons_string
        segment["path"] = week_ids_dict[week_id] + "/" + segment["segment_file_name"] + "/"
        # a bit of clean up
        if "trackId" in segment: del segment["trackId"]
        if "timeCommitment" in segment: del segment["timeCommitment"]
        if "elementIds" in segment: del segment["elementIds"]
        return segment

    @staticmethod
    def updating_all_lessons_dict_with_segments(all_lessons_dict, updated_segments_information):
        for item in updated_segments_information:
            week = jmespath.search("week", item)
            segment_file_name = jmespath.search("segment_file_name", item).replace("-", "_")
            all_lessons_dict[week][segment_file_name] = {}
        return all_lessons_dict

    @staticmethod
    def updating_all_lessons_information(lesson, updated_segments_information, video_api_url, course_id):
        lesson_id = lesson["id"]
        for segment in updated_segments_information:
            if lesson_id in segment["lessons_string"]:
                lesson["segment_name"] = segment["name"]
                lesson["week"] = segment["week"]
                lesson["path"] = segment["path"]
                lesson["segment_slug"] = segment["slug"]
                lesson["video_lecture"] = False
                lesson["lesson_file_name"] = lesson["slug"].replace("-", "_")
                lesson["segment_file_name"] = segment["segment_file_name"]
                # id = lesson url id, moduleId = weeks id, lessonId = segment id
                if search('contentSummary.typeName', lesson) != "lecture":
                    return lesson
                lesson["finalized_api_video_url"] = video_api_url.format(course_id=course_id, lecture_id=lesson["id"])
                lesson["video_lecture"] = True
                return lesson

    @staticmethod
    def update_all_lessons_dict_with_high_res_video_url(updated_all_lessons_information, all_lessons_dict):
        for index, lesson in enumerate(updated_all_lessons_information):
            if lesson["video_lecture"] is True:
                finalized_api_video_url = lesson["finalized_api_video_url"]
                api_response = requests.get(url=finalized_api_video_url)
                if api_response:
                    get_dict = json.loads(api_response.text)
                    # VIDEO RESOLUTION HERE
                    vid_720p_url = jmespath.search('linked."onDemandVideos.v1"[0].sources.byResolution."720p".webMVideoUrl', get_dict)
                    vid_540p_url = jmespath.search('linked."onDemandVideos.v1"[0].sources.byResolution."540p".webMVideoUrl', get_dict)
                    vid_360p_url = jmespath.search('linked."onDemandVideos.v1"[0].sources.byResolution."360p".webMVideoUrl', get_dict)
                    vid_240p_url = jmespath.search('linked."onDemandVideos.v1"[0].sources.byResolution."240p".webMVideoUrl', get_dict)
                    all_lessons_dict[lesson["week"]][lesson["segment_file_name"]].update({"item_" + str(index + 1) + "_" + lesson["lesson_file_name"]: {
                        "vid_720p_url": vid_720p_url,
                        "vid_540p_url": vid_540p_url,
                        "vid_360p_url": vid_360p_url,
                        "vid_240p_url": vid_240p_url,
                    }})
                else:
                    all_lessons_dict[lesson["week"]][lesson["segment_file_name"]].update({"item_" + str(index + 1) + "_" + lesson["lesson_file_name"]: "failed to get"})
                time.sleep(3)
        return all_lessons_dict

    @staticmethod
    def creating_json(all_lessons_dict):
        data_dict_string = json.dumps(all_lessons_dict)
        with open('all_lessons_dict.json', 'w', encoding='utf-8') as f:
            json.dump(data_dict_string, f, ensure_ascii=False, indent=4)

    @staticmethod
    def download_files(data_dict, course_name, video_quality):
        video_quality_file_name = None
        video_quality_list = ["vid_720p_url", "vid_540p_url", "vid_360p_url", "vid_240p_url"]
        for video in video_quality_list:
            if video_quality in video:
                video_quality_file_name = video
                break
        if not video_quality_file_name:
            print("wrong video format, function terminated")
            return
        os.mkdir(course_name)
        for week_name, values in data_dict.items():
            print(" *************** starting " + week_name + " ***************")
            week_directory = course_name + "/" + week_name
            os.mkdir(week_directory)
            for segment_name, lessons in values.items():
                print("--------- starting " + segment_name + " ---------")
                temp_directory = week_directory + "/" + segment_name
                os.mkdir(temp_directory)
                for video_name, video_urls in lessons.items():
                    print("! downloading video " + video_name + " !")
                    video_url = video_urls[video_quality_file_name]
                    final_video_name = video_name + "_" + str(video_quality) + "p" + ".mp4"
                    urllib.request.urlretrieve(video_url, temp_directory + "/" + final_video_name)
                    print(" !! finished video " + video_name + " !!")
                    time.sleep(10)
                print("--------- finished " + segment_name + " ---------")
            print(" *************** finished " + week_name + " ***************")
        print("@@@@@@@@@@@@@@ spider finished @@@@@@@@@@@@@@")