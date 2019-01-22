import os
import _thread
import threading

import math
import wget

class_names = [
    "neutral",
    "drawings",
    "sexy",
    "porn",
    "hentai"
]

def download_worker( files , images_dir , i , cname ):
    for img in files:
        img = img.replace("\n", "")
        try:
            wget.download(img,images_dir)
        except Exception as e:
            print('failed:', e)
        else:
            print(cname+'-thread:' + str(i) + ',' + 'file:' + img + ', downloaded')


for cname in class_names:
    urls_file = '../raw_data/{cname}/urls_{cname}.txt'
    images_dir = '../raw_data/{cname}/IMAGES'
    urls_file = urls_file.format(cname=cname)
    images_dir = images_dir.format(cname=cname)
    if os.path.isdir(images_dir):
        print('exist:' + urls_file)
        pass
    else:
        print(images_dir)
        os.mkdir(images_dir,0o777)
        print('created:' + urls_file)
    file = open(urls_file)
    lines = file.readlines()
    # set your thread count here , default 8 worker 
    worker_count = 8
    img_count = len(lines)
    pre_thread_img_count = math.floor(img_count / worker_count);

    if img_count % worker_count == 0:
        last_thread_img_count = pre_thread_img_count;
    else:
        last_thread_img_count = pre_thread_img_count + (img_count % worker_count);

    print('img_count:' + str(img_count))
    thread_list = []

    for i in range(1, worker_count + 1):
        if i != worker_count:
            start = pre_thread_img_count * (i - 1);
            end = pre_thread_img_count * (i) - 1;
        else:
            start = pre_thread_img_count * (i - 1);
            end = start + last_thread_img_count - 1;
        print('thread' + str(i) + ':' + str(start) + '-' + str(end))
        thread = threading.Thread(target=download_worker, args=(lines[start:end], images_dir, i, cname))
        thread.start()
        thread_list.append(thread)
