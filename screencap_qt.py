import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from screen_qt import Ui_MainWindow
import threading
import tempfile
import time
from os import listdir, system
from os.path import exists, splitext, basename, join, dirname
from PIL import ImageGrab
from pynput import keyboard
from moviepy.video.io import ImageSequenceClip


class MyMainWindow(QMainWindow, Ui_MainWindow):
    video_fn = ''
    record_sec = 5
    interval_sec = 0.02
    continue_record = True
    cap_sec = 5
    sleep_time = 0.02
    index = 1
    temp_dir_obj = tempfile.TemporaryDirectory()
    pic_dir = temp_dir_obj.name
    total_pic = 0

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.lineEdit_3.setDisabled(True)
        self.pushButton.clicked.connect(self.getfile)
        self.pushButton_2.clicked.connect(self.start_record)

    def getfile(self):
        self.video_fn, _ = QtWidgets.QFileDialog.getSaveFileName(filter='avi文件(*.avi)')
        self.lineEdit_3.setText(self.video_fn)
        # if len(self.video_fn):
        #     self.pushButton.setDisabled(True)
        # print(self.video_fn)

    def start_record(self):
        error_msg = []
        self.record_sec = self.lineEdit.text()
        try:
            float(self.record_sec) + 1
        except:
            error_msg.append('录屏时长输入错误，请输入大于0的数字')
        else:
            if float(self.record_sec) <= 0:
                error_msg.append('录屏时长输入错误，请输入大于0的数字')
        self.interval_sec = self.lineEdit_2.text()
        try:
            float(self.interval_sec) + 1
        except:
            error_msg.append('截屏间隔输入错误，请输入大于等于0的数字')
        else:
            if float(self.interval_sec) < 0:
                error_msg.append('截屏间隔输入错误，请输入大于等于0的数字')
        if not len(self.video_fn):
            error_msg.append('请选择保存文件的位置')
        if len(error_msg):
            # print(error_msg)
            warning_msg = '\n'.join(error_msg)
            QtWidgets.QMessageBox.warning(self, '参数输入错误', warning_msg)
        else:
            self.lineEdit.setDisabled(True)
            self.lineEdit_2.setDisabled(True)
            self.pushButton_2.setDisabled(True)
            self.pushButton.setDisabled(True)
            self.showMinimized()
            threading.Thread(target=self.record_screen).start()

    def record_screen(self):
        sec_a = time.time()
        ImageGrab.grab().save(f'{self.pic_dir}\\1.jpg', quality=95)
        time.sleep(float(self.interval_sec))
        sec_b = time.time()
        fps = 1 / (sec_b - sec_a)
        self.total_pic = int(fps * float(self.record_sec))
        t1 = threading.Timer(3, self.grab_pic)
        t1.start()
        with keyboard.Listener(on_press=self.stop_record) as listener:
            listener.join()
        t1.join()
        pic_files = [join(self.pic_dir, fn) for fn in listdir(self.pic_dir) if fn.endswith('.jpg')]
        pic_files.sort(key=lambda fn: int(splitext(basename(fn))[0]))
        if exists(f'{self.pic_dir}\\{self.index}.jpg'):
            pic_files = pic_files[self.index - 1:] + pic_files[0:self.index - 1]
        image_clip = ImageSequenceClip.ImageSequenceClip(pic_files, fps=fps)
        self.showNormal()
        self.label.setText("正在生成视频文件")
        image_clip.write_videofile(self.video_fn, codec='png')
        open_dir = self.video_fn.replace('/', '\\')
        system(f'explorer /select,/n,{open_dir}')
        self.reset()

    def reset(self):
        self.lineEdit.setDisabled(False)
        self.lineEdit_2.setDisabled(False)
        self.pushButton_2.setDisabled(False)
        self.pushButton.setDisabled(False)
        self.label.setText("点击[开始录制]后3s开始录制")


    def stop_record(self, key):
        if key == keyboard.Key.esc:
            self.continue_record = False
            return False

    def grab_pic(self):
        while self.continue_record:
            ImageGrab.grab().save(f'{self.pic_dir}\\{self.index}.jpg', quality=95)
            time.sleep(float(self.interval_sec))
            self.index += 1
            if self.index > self.total_pic:
                self.index = 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = MyMainWindow()
    MainWindow.show()
    sys.exit(app.exec_())