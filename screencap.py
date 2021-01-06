import threading
import tempfile
from datetime import datetime
import time
from os import listdir, system
from os.path import exists, splitext, basename, join,dirname
from PIL import ImageGrab
from pynput import keyboard
from moviepy.video.io import ImageSequenceClip


def record_screen():
    global index
    while continue_record:
        ImageGrab.grab().save(f'{pic_dir}\\{index}.jpg', quality=95)
        time.sleep(sleep_time)
        index += 1
        if index > total_pic:
            index = 1


def stop_record(key):
    if key== keyboard.Key.esc:
        global continue_record
        continue_record = False
        return False


if __name__ == '__main__':
    continue_record = True
    cap_sec = 5
    sleep_time = 0.02
    index = 1

    temp_dir_obj = tempfile.TemporaryDirectory()
    pic_dir = temp_dir_obj.name
    video_dir = 'D:\\'
    file_name = join(video_dir, str(datetime.now())[:19].replace(':', '_') + '.avi')
    sec_a = time.time()
    ImageGrab.grab().save(f'{pic_dir}\\1.jpg', quality=95)
    time.sleep(sleep_time)
    sec_b = time.time()
    FPS = 1/(sec_b - sec_a)
    total_pic = int(FPS * cap_sec)
    t1 = threading.Timer(3, record_screen)
    t1.start()
    with keyboard.Listener(on_press=stop_record) as listener:
        listener.join()
    t1.join()
    pic_files = [join(pic_dir, fn) for fn in listdir(pic_dir) if fn.endswith('.jpg')]
    pic_files.sort(key=lambda fn: int(splitext(basename(fn))[0]))
    print(len(pic_files))
    if exists(f'{pic_dir}\\{index}.jpg'):
        pic_files = pic_files[index - 1:] + pic_files[0:index - 1]
    image_clip = ImageSequenceClip.ImageSequenceClip(pic_files, fps=FPS)
    image_clip.write_videofile(file_name, codec='png')
    del temp_dir_obj
    system(f'explorer {dirname(file_name)}')
