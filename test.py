import requests

url = 'https://player.ikmz.cc/yinhua/?url=MCZY-6edclJXcfk78YtI7W2hsPW38HtOrB_yPDq_F7Kl4LWw6cs5AEHi9W5AEKMkGNIH2OXJhjkUC_JW3sol2ioI1w_7InKGxFjzlC5ZyjIK6uBlUNhCqaQ&next=https://www.yinhuadm.cc/p/11034-1-3.html&title=%E9%97%B4%E8%B0%8D%E8%BF%87%E5%AE%B6%E5%AE%B6%20%E7%AC%AC%E4%BA%8C%E5%AD%A3%20%E7%AC%AC02%E9%9B%86%E5%9C%A8%E7%BA%BF%E6%92%AD%E6%94%BE'
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
}
response = requests.get(url,headers)
print(response.text)
