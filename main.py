import requests
import bs4
import json
import re
from collections import namedtuple

Video = namedtuple('Video', 'video_url subtitle_url')


def soupify(url: str):
    html = requests.get(url).text
    soup = bs4.BeautifulSoup(html, 'html.parser')
    return soup


def extract_video(page_url: str):
    soup = soupify(page_url)
    video_url = 'http:' + soup.select_one('.mediaInfo .download').attrs['href']
    mediaobj_helper_json = soup.select_one('.mediaLink').attrs['data-extension']
    mediaobj_helper_url = json.loads(mediaobj_helper_json)['mediaObj']['url']
    mediaobj_js = requests.get(mediaobj_helper_url).text
    mediaobj_json = (mediaobj_js
                     .replace('$mediaObject.jsonpHelper.storeAndPlay(', '')
                     .replace(');', ''))
    mediaobj = json.loads(mediaobj_json)
    srt_url = 'https:' + mediaobj['mediaResource']['captionsHash']['srt']
    return Video(video_url=video_url, subtitle_url=srt_url)


if __name__ == '__main__':
    page_url = input('Type in WRD url\n')
    video = extract_video(page_url)
    print(video.video_url)
    print(video.subtitle_url)
