import os
import multiprocessing
from tqdm import tqdm
import m3u8
import requests


# https://cdn20.vip-vip-yzzy.com/20231117/5322_1192b1b5/2000k/hls/25ee40729c6000146.ts
# https://cdn20.vip-vip-yzzy.com/20231117/5322_1192b1b5/2000k/hls/index.m3u8


# 下载m3u8
def get_ts_list(video_url, ts_header=''):
    resp = requests.get(video_url, headers)
    m3u8_master = m3u8.loads(resp.text)
    print(m3u8_master.data['segments'])
    ts_list = []
    for segment in m3u8_master.data['segments']:
        uri = segment['uri']
        ts_list.append(ts_header + uri)
    return ts_list


# 下载ts
def download_ts(m3u8_url, ts_header=''):
    # n = 0
    pbar = tqdm(total=len(m3u8_url))
    pbar.set_description('下载ts切片中...')
    update = lambda *args: pbar.update()
    pool = multiprocessing.Pool(50)
    for ts_slice_url in get_ts_list(m3u8_url, ts_header):
        pool.apply_async(get_ts_list, ts_slice_url, callback=update)
        # t.submit(get_ts_slices, ts_slice_url)
        print('开始下载' + ts_header + ts_slice_url)


# 下载ts视频
def get_ts_slices(slice_url: str):
    # 下载视频
    resp3 = requests.get(slice_url, headers=headers)
    slice_name = slice_url.split('/')[-1]
    with open(f"{os.curdir}/video/{slice_name}", "wb") as f:
        f.write(resp3.content)


def merge_video():
    files = os.listdir(f'video')
    for file in tqdm(files, desc="正在转换视频格式："):
        with open(f'video/{file}', 'rb') as f1:
            with open("zshz.mp4", 'ab') as f2:
                f2.write(f1.read())


def download_video(m3u8_url, ts_header=''):
    if not os.path.exists('video'):
        os.mkdir('video')
    download_ts(m3u8_url, ts_header)
    merge_video()


# url = r"https://www.d53w.com/tpsf/player/dpx2/?hls=1&url=https%3A%2F%2Fs9.fsvod1.com%2F20231116%2FuSh0HCu1%2Findex.m3u8"

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
}
url = 'https://v.cdnlz14.com/20231008/30170_e3ce21c0/2100k/hls/mixed.m3u8'
my_ts_header = 'https://v.cdnlz14.com/20231008/30170_e3ce21c0/2100k/hls/'
download_video(url, my_ts_header)
