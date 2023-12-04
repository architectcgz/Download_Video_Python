import os
from tqdm import tqdm
import m3u8
import requests
from concurrent.futures import ThreadPoolExecutor

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
}

# 下载m3u8
def getTsList(video_url, ts_header=''):
    resp = requests.get(video_url, headers)
    m3u8_master = m3u8.loads(resp.text)
    print(m3u8_master.data['segments'])
    ts_list = []
    for segment in m3u8_master.data['segments']:
        uri = segment['uri']
        ts_list.append(ts_header + uri)
    return ts_list


# 下载ts
def downloadTsSlices(m3u8_url, ts_header=''):
    ts_list = getTsList(m3u8_url, ts_header)

    with ThreadPoolExecutor(max_workers=50) as t:
        # 创建一个进度条
        pbar = tqdm(total=len(ts_list))
        pbar.set_description('下载ts切片中...')
        # 创建一个列表来保存所有的任务
        all_task = []
        for ts_slice_url in ts_list:
            # 提交每个任务到线程池
            task = t.submit(getTsSlices, ts_slice_url)
            # 当任务完成时，更新进度条
            task.add_done_callback(lambda p: pbar.update())
            # 将任务添加到任务列表中
            all_task.append(task)
        # 等待所有任务完成
        for task in all_task:
            task.result()
        # 关闭进度条
        pbar.close()


# 下载ts视频
def getTsSlices(slice_url: str):
    # 下载视频
    resp3 = requests.get(slice_url, headers=headers)
    slice_name = slice_url.split('/')[-1]
    with open(f"{os.curdir}/video/{slice_name}", "wb") as f:
        f.write(resp3.content)


def mergeTsVideos(video_name):
    files = os.listdir(f'video')
    for file in tqdm(files, desc="正在转换视频格式："):
        with open(f'video/{file}', 'rb') as f1:
            with open(f"{video_name}.mp4", 'ab') as f2:
                f2.write(f1.read())


def downloadVideo(video_name: str, m3u8_url, ts_header=''):
    if not os.path.exists('video'):
        os.mkdir('video')
    downloadTsSlices(m3u8_url, ts_header)
    mergeTsVideos(video_name)
    # 删除所有无用的ts文件
    for root, dirs, files in os.walk('video', topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))


# url = r"https://www.d53w.com/tpsf/player/dpx2/?hls=1&url=https%3A%2F%2Fs9.fsvod1.com%2F20231116%2FuSh0HCu1%2Findex.m3u8"
# url = 'https://v.cdnlz14.com/20231008/30170_e3ce21c0/2100k/hls/mixed.m3u8'
# url = 'https://v.cdnlz14.com/20231202/32243_abd8b538/2100k/hls/mixed.m3u8'
# my_ts_header = 'https://v.cdnlz14.com/20231008/30170_e3ce21c0/2100k/hls/'
url = 'https://v.cdnlz14.com/20231201/32168_06c4d934/2100k/hls/mixed.m3u8'
my_ts_header = url[0:url.rfind('/') + 1]
downloadVideo('咒术回战第19集', url, my_ts_header)
