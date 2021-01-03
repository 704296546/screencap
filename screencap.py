import threading
from datetime import datetime
import time
from shutil import rmtree
from os import mkdir, listdir
from os.path import exists, splitext, basename, join
from PIL import ImageGrab
from moviepy.editor import *
continueRecord = True
cap_sec = 5
sleep_time = 0.02
index = 1


def record_screen():
    global index
    while continueRecord:
        ImageGrab.grab().save(f'{pic_dir}\\{index}.jpg', quality=95)
        time.sleep(sleep_time)
        index += 1
        if index > total_pic:
            index = 1


pic_dir = 'D:\\pyscreencap'
video_dir = 'D:'
file_name = join(video_dir, str(datetime.now())[:19].replace(':', '_') + '.avi')
if not exists(pic_dir):
    mkdir(pic_dir)
sec_a = time.time()
ImageGrab.grab().save(f'{pic_dir}\\1.jpg', quality=95)
time.sleep(sleep_time)
sec_b = time.time()
FPS = 1/(sec_b - sec_a)
total_pic = int(FPS * cap_sec)
t1 = threading.Timer(3, record_screen)
t1.start()
while input() != 'q':
    pass
continueRecord = False
t1.join()
pic_files = [join(pic_dir, fn) for fn in listdir(pic_dir) if fn.endswith('.jpg')]
pic_files.sort(key=lambda fn: int(splitext(basename(fn))[0]))
print(len(pic_files))
if exists(f'{pic_dir}\\{index}.jpg'):
    pic_files = pic_files[index - 1:] + pic_files[0:index - 1]
image_clips = []
for pic in pic_files:
    image_clips.append(ImageClip(pic, duration=(1/FPS)))
video = concatenate_videoclips(image_clips)
video.write_videofile(file_name, codec='png', fps=FPS)
rmtree(pic_dir)
