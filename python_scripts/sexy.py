import re
import requests
from queue import Queue
from threading import Lock, Thread
lock = Lock()

def get_pic(in_q):
    while in_q.empty() is not True:
        url = in_q.get()
        res = requests.get(url)
        try:
            while url[-3:] != 'jpg':
                url = re.findall("(.*)\?\d+",url)[0]
        except IndexError:
            pass
        name = url[-11:]
        lock.acquire()
        fp = open(f"sexy/{name.replace('/','_')}",'wb')
        fp.write(res.content)
        print("ok-----------------------------")
        fp.close()
        lock.release()
    in_q.task_done()
print("开始-------------------------------")
with open('urls_sexy.txt','r') as fp:
    line = fp.read()
    lines = line.strip().split("\n")
queues = Queue()
for url in lines:
    queues.put(url)
for _ in range(100):
    thread = Thread(target=get_pic,args=(queues,))
    thread.daemon = True
    thread.start()
queues.join()
