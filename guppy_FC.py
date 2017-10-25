# -*- coding: utf-8 -*-
"""
Created on 24-8-2017

This class provides 2 functions: capture() which returns a numpy array and
stream() which opens a live stream in a seperate window.
Currently assumes a single camera attached.

@author: RCole
v0.1
"""

# from __future__ import absolute_import, print_function, division
from pymba import *
import numpy as np
import cv2
import time
import datetime
import uuid
import logging

unique_filename = str(uuid.uuid4().hex[0:7])
log_name = 'guppy_{}.log'.format(unique_filename)
logging.basicConfig(filename=log_name,level=logging.DEBUG)
print("Logging to %s" % log_name)


class guppy_cam():
    def __init__(self):
        self.created = self.now()

    def now(self):
        now = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        return now

    def live(self):
        """Starts a live stream in a window."""
        message = 'Camera live stream started at %s' % self.now()
        print(message)
        logging.info(message)
        with Vimba() as vimba:
            system = vimba.getSystem()
            system.runFeatureCommand("GeVDiscoveryAllOnce")
            time.sleep(0.2)
            self.camera_id = vimba.getCameraIds()[0]

            c0 = vimba.getCamera(self.camera_id)
            c0.openCamera()
            c0.PixelFormat="Mono8"
            frame = c0.getFrame()
            frame.announceFrame()

            c0.startCapture()
            framecount = 0
            droppedframes = []

            while True:
                try:
                    frame.queueFrameCapture()
                    success = True
                except:
                    droppedframes.append(framecount)
                    success = False

                c0.runFeatureCommand("AcquisitionStart")
                c0.runFeatureCommand("AcquisitionStop")
                frame.waitFrameCapture(1000)
                frame_data = frame.getBufferByteData()

                if success:
                    img = np.ndarray(buffer=frame_data,
                                    dtype=np.uint8,
                                    shape=(frame.height,frame.width,1))
                    cv2.imshow("Press Esc to quit",img)

                framecount+=1
                k = cv2.waitKey(1)
                if k == 0x1b:
                    cv2.destroyAllWindows()
                    break

            c0.endCapture()
            c0.revokeAllFrames()
            c0.closeCamera()
            message = 'Camera live stream terminated at %s' % self.now()
            print(message)
            logging.info(message)

    def still(self):
        """"Capture and save a still and return the numpy array"""

        with Vimba() as vimba:
            system = vimba.getSystem()
            system.runFeatureCommand("GeVDiscoveryAllOnce")
            time.sleep(0.2)
            self.camera_id = vimba.getCameraIds()[0]

            c0 = vimba.getCamera(self.camera_id)
            c0.openCamera()
            c0.AcquisitionMode = 'SingleFrame'

            frame0 = c0.getFrame()    # creates a frame
            frame1 = c0.getFrame()    # creates a second frame
            frame0.announceFrame()

            c0.startCapture()
            frame0.queueFrameCapture()
            c0.runFeatureCommand('AcquisitionStart')
            c0.runFeatureCommand('AcquisitionStop')
            frame0.waitFrameCapture()

            # get image data...
            imgData = frame0.getBufferByteData()

            moreUsefulImgData = np.ndarray(buffer = frame0.getBufferByteData(),
                                           dtype = np.uint8,
                                           shape = (frame0.height,frame0.width,
                                           1))

            rgb = cv2.cvtColor(moreUsefulImgData, cv2.COLOR_BAYER_RG2RGB)
            save_name = make_filename()
            cv2.imwrite(save_name, rgb)
            c0.endCapture()
            c0.revokeAllFrames()
            c0.closeCamera()
            message = "Image %s saved" % save_name
            logging.info(message)
            print(message)

        return moreUsefulImgData[:,:,0] # this is only the red channel?


def make_filename():
    """"This functions creates a unique filename."""
    unique_filename = time.strftime("%Y%m%d-%H%M%S")
    #unique_filename = str(uuid.uuid1())
    #unique_filename = str(uuid.uuid1().hex[0:7])
    save_name = 'capture_ferhat_{}.png'.format(unique_filename)
    return(save_name)