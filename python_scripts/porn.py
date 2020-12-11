import threading
import requests
from queue import Queue
from threading import Thread,Lock
import re

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}
lock = Lock()
def get_pic(in_q):
    while in_q.empty() is not True:
        try:
            url = in_q.get()
            ress = requests.get(url,headers = headers)
            while url[-3:] != 'jpg':
                url = re.findall("(.*)\?\d+",url)[0]
            name = url[-21:]
            lock.acquire()
            fp = open(f"porn/{name.replace('/','_')}","wb")
            fp.write(ress.content)
            print("OK---------------------------------")
            fp.close()
            lock.release()
        except (OSError,IndexError):
            pass
    in_q.task_done()
print("开始--------")
ur = "https://raw.githubusercontent.com/vllbc/nsfw_data_scraper/master/raw_data/porn/urls_porn.txt"
res = requests.get(ur)
uu = res.text.strip().split("\n")[20:-18]


queues = Queue()
for url in uu:
    queues.put(url)
for _ in range(100):
    thread = Thread(target=get_pic,args=(queues,))
    thread.daemon = True
    thread.start()
queues.join()
