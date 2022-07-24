import PIL.Image as img
import cv2
import numpy as np

import sim
from lyb import connector, address, commandList


class DetectionSystem(object):
    socket = connector.MySocket(address.addr_DS)
    socket.sock.settimeout(1)

    def __init__(self):
        self.clientID = 0
        self.color = 0
        self.o_s = None
        self.camera = None
        self.time_start_frame = 0
        self.time_end_frame = 0
        self.px = 128


def processThePicture():
    res, resolv, image = sim.simxGetVisionSensorImage(detection_system.clientID, detection_system.camera,
                                                      detection_system.color, sim.simx_opmode_buffer)

    if (res == sim.simx_return_ok) and (resolv[0] > 0) and (resolv[1] > 0):
        im_t = []
        for i in range(len(image)):
            if image[i] < 0:
                im_t.append(image[i] + 256)
            else:
                im_t.append(image[i])
        im_t.reverse()
        im = img.frombuffer("RGB", resolv, bytes(im_t), "raw", "RGB", 0, 1)
        image_cv = np.asarray(im)
        cv2.flip(image_cv, 1, image_cv)

        # Threshold the HSV image to get only green colors

        median = cv2.medianBlur(image_cv, 1)
        blur_median = cv2.GaussianBlur(median, (7, 7), 1)
        blur_median_hcv = cv2.cvtColor(blur_median, cv2.COLOR_BGR2HSV)
        # lower_red = np.array([0, 50, 50])  # example value
        # upper_red = np.array([10, 255, 255])  # example value
        mask1 = cv2.inRange(blur_median_hcv, (0, 70, 30), (5, 255, 255))
        mask2 = cv2.inRange(blur_median_hcv, (175, 50, 20), (180, 255, 255))
        blur_median_mask = cv2.bitwise_or(mask1, mask2)

        moments = cv2.moments(blur_median_mask)
        dM01 = moments['m01']
        dM10 = moments['m10']
        dArea = moments['m00']

        if dArea > 100:
            cx = int(dM10 / dArea)
            cy = int(dM01 / dArea)

            C = (cx, cy)
            cv2.circle(median, C, 8, (0, 0, 255), 2)
            x = -(int(cx) - (detection_system.px / 2)) / (detection_system.px / 2)
            y = (int(cy) - (detection_system.px / 2)) / (detection_system.px / 2)
            print(11111)
            detection_system.socket.send_com(commandList.EVENT_OBJ(x, y), address.addr_M)

        img_scale = cv2.resize(median, None, fx=6, fy=6, interpolation=cv2.INTER_CUBIC)
        cv2.imshow("cam", img_scale)

        try:
            cv2.waitKey(1)
        except:
            print("ok")


detection_system = DetectionSystem()
