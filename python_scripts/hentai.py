import requests
from queue import Queue
from threading import Thread,Lock
lock = Lock()
def get_pic(in_q):
    while in_q.empty() is not True:
        ur = in_q.get()
        ress = requests.get(ur)
        name = ur[-10:]
        lock.acquire()
        fp = open(f"hentai/{name.replace('/','_')}",'wb')
        fp.write(ress.content)
        print("OK---------------------------------------")
        fp.close()
        lock.release()
    in_q.task_done()
print("开始----------")
urls = "https://raw.githubusercontent.com/vllbc/nsfw_data_scraper/master/raw_data/hentai/urls_hentai.txt"
res = requests.get(urls)
queues = Queue()
for url in res.text.strip().split("\n"):
    if "https://hentaiprn.com" in url:
        continue
    queues.put(url)

for _ in range(100):
    thread = Thread(target=get_pic,args=(queues,))
    thread.daemon = True
    thread.start()
queues.join()