#!/usr/bin/env python3
import logging

logging.basicConfig(filename='vc.log',
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)-8s - %(message)s",
                    datefmt='%m/%d/%Y %I:%M:%S %p')
import ctypes
import queue
import sounddevice as sd

import numpy as np
import time
from multiprocessing import Process
from multiprocessing import Queue
from multiprocessing import Value
from threading import Thread

from infer.utils import get_time_dif
from infer.model import Model


class Application:
    def __init__(self):
        """
        initialize the application
        """
        self.model = Model()
        self.flag = Value(ctypes.c_bool, False)
        self.speaker = None
        self.audio = np.zeros(
            shape=(24000,
                   1))  # add zero-filled buffer to promote the performance
        self.ini_sd()
        logging.info('Application has been initialized.')

    def ini_sd(self):
        """
        init sounddevice
        """
        # enable to detect bluetooth devices, if and only if the devices are paired
        sd._terminate()
        sd._initialize()
        sd.default.reset()
        # set input and output devices
        sd.default.device = 1, 5
        sd.default.samplerate = 24000  # set sample rate
        sd.default.channels = 1, 2  # one input channel, two output channel
        logging.info('sounddevice has been initialized.')

    def stream(self):
        """
        this function tends to capture the audio, which is enabled by start function and terminated by stop function
        """
        q = queue.Queue()

        def callback(in_data, frames, time, status):
            q.put(in_data.copy())
            
        with sd.InputStream(samplerate=24000,
                            device=sd.default.device[0],
                            dtype='float32',
                            channels=1,
                            callback=callback):
            logging.info('Begin to record.')

            while self.flag.value:
                packet = q.get()
                self.audio = np.append(self.audio, packet, axis=0)
                logging.info(len(self.audio))
            logging.info("input stream exit.")

    def start(self):
        self.flag.value = True
        self.audio = np.zeros(shape=(24000,
                                     1))  # init the audio for a new start
        self.p = Thread(target=self.stream)
        self.p.start()
        start_time = time.time()

        def timer_stop():
            while self.flag.value:
                time.sleep(1)
                if time.time() - start_time > 5 * 60:
                    self.flag.value = False
                    break

        self.t = Thread(target=timer_stop)
        self.t.setDaemon(True)
        self.t.start()
        logging.info('begin recording.')

    def stop(self):
        self.flag.value = False
        logging.info('end recording.')
        self.t.join()
        self.p.join()

    def verify_speaker(self, speaker):
        # speaker is int instead of string
        if speaker not in self.model.speakers.keys():
            logging.info('\tIncorrect speaker.')
            return False
        else:
            logging.info('\tThe target speaker is {}. {}'.format(
                speaker, self.model.speakers[speaker]))
            return True

    def infer(self):
        # pre-process audio
        logging.info(self.audio.shape, self.audio)
        self.audio = self.audio / np.max(np.abs(self.audio))
        self.audio = self.audio.flatten()  # flatten the 2D numpy array
        # convert audio to target speaker tone
        start_time = time.time()
        converted_audio = self.model.infer(self.audio, self.speaker)
        logging.info('VC costs {:.4} s'.format(get_time_dif(start_time)))
        start_time = time.time()
        sd.play(converted_audio, 24000)
        sd.wait()  # wait to playing
        logging.info('Playing costs {:.4} s'.format(get_time_dif(start_time)))


if __name__ == '__main__':
    app = Application()
    app.ini_sd()
    app.speaker = 1  # Hua_Chunying
    app.verify_speaker(app.speaker)

    app.start()
    print('开始录音')
    time.sleep(10)
    app.stop()
    print('结束录音')

    app.infer()
