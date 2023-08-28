# -*- coding: utf-8 -*-
from bilibili_beauty.config import video_urls, url_video_root
import argparse
import random


def get_random_id():
    len_url = len(video_urls)
    rand_int = random.randint(1, len_url)
    return video_urls.get(rand_int, "BV1S14y1C7Px")


def get_id_by_num(num):
    nums = video_urls.keys()
    if num not in video_urls.keys():
        error = f"{num} not in range, range: {min(nums)} ~ {max(nums)}"
        raise Exception(error)

    return video_urls.get(num)


def get_args():
    desc = (
        "get bilibili url.\n"
        "1. get random url, e.g.: bb;\n"
        "2. get url by number, e.g.: bb -n 5"
    )
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-n", "--number", type=int, help="get url by number")
    args = parser.parse_args()
    return args


def run():
    args = get_args()

    number = args.number
    if number:
        video_id = get_id_by_num(number)
    else:
        video_id = get_random_id()

    url = "".join([url_video_root, video_id])
    print(url)


def main():
    run()
