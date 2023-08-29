from pypylon import pylon, genicam
import numpy as np
import cv2
import logging
logging.basicConfig(format='%(message)s',
                    level=logging.DEBUG)

class Webcam():
    def __init__(self) -> None:
        self._camera:cv2.VideoCapture = None
        self._is_open = False

    def open(self, source) -> bool:
        '''
        @params
        @source: int or str
            - int: index of camera
            - str: rtsp stream link of camera
        return bool
        '''
        error = ""
        self._is_open = False
        try:
            self._camera = cv2.VideoCapture(source, cv2.CAP_DSHOW)
        except Exception as ex:
            error = str(ex)
            logging.error(error)
    
        if not error:
            logging.info("Camera open sucess")
            self._is_open = True
        else:            
            self._camera = None

        return self._is_open

    def close(self) -> bool:
        try:
            self._camera.release()
            logging.info("Camera closed")
            return True
        except Exception as ex:
            error = str(ex) 
            logging.error(error)
            return False

    def grab(self) -> np.ndarray:
        ret, mat = self._camera.read()
        if ret:
            return mat
        else:
            return None

    def get_camera(self):
        return self._camera
    
    def is_open(self):
        return self._is_open

    @staticmethod
    def get_devices() -> dict:
        dict_devives = {}
        return dict_devives

class Basler():
    def __init__(self, color='m') -> None:
        self._camera:pylon.InstantCamera = None
        self._converter:pylon.ImageFormatConverter = None
        self.init_color_converter()
        self._is_open = False

    def open(self, camera_info=None) -> bool:
        '''
        @params
        @camera_info: int or str
            - int: index of camera
            - str: serinumber of camera
            - None: open first device
        return bool
        '''
        error = ""
        self._is_open = False
        basler_devices = Basler.get_devices()

        if not len(basler_devices):
            error = "Do not found Basler device"
            logging.error(error)
        else:
            if isinstance(camera_info, str):
                try:
                    dev = basler_devices[camera_info]
                    self._camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateDevice(dev))
                except KeyError as ex:
                    error = "Camera serinumber not found"
                    logging.error(error)
                except Exception as ex:
                    error = str(ex)
                    logging.error(error)
            elif isinstance(camera_info, int):
                try:
                    key = list(basler_devices.keys())[camera_info]
                    dev = basler_devices[key]
                    self._camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateDevice(dev))
                except IndexError as ex:
                    error = "Camera index out of range"
                    logging.error(error)
                except Exception as ex:
                    error = str(ex)
                    logging.error(error)
            elif camera_info is None:
                try:
                    self._camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
                except Exception as ex:
                    error = str(ex)
                    logging.error(error)
            else:
                error = "camera_info must be index(int), or serinumber(str) or None(first device)"
                logging.error(error)

            try:
                self._camera.Open()
            except Exception as ex:
                error = str(ex) 
                logging.error(error)

        if not error:
            logging.info("Camera open success")
            self._is_open = True
        else:
            logging.error("Camera open failed")
            self._camera = None

        logging.debug("Open camera done")
        return self._is_open

    def close(self) -> bool:
        try:
            self._camera.Close()
            logging.info("Camera closed")
            return True
        except Exception as ex:
            error = str(ex) 
            logging.error(error)
            return False

    def grab(self) -> np.ndarray:
        # start grabbing first
        if not self._camera.IsGrabbing():
            self.start_grabbing()
        # grab image
        self._grab_result = self._camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        if self._grab_result.GrabSucceeded():
            if self._converter:
                image = self._converter.Convert(self._grab_result)
                return image.GetArray()
            else:
                return self._grab_result.Array
        else:
            return None

    def load_features(self, path):
        try:
            pylon.FeaturePersistence.Load(path, self._camera.GetNodeMap(), True)
        except FileNotFoundError as ex:
            error = f"{path}: file not found, load features failed"
            logging.error(error)
        except Exception as ex:
            error = str(ex)
            logging.error(error)

    def init_color_converter(self, color='m'):
        if color != 'm':
            self._converter = pylon.ImageFormatConverter()
            self._converter.OutputPixelFormat = pylon.PixelType_BGR8packed
            self._converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

    def start_grabbing(self):
        self._camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

    def stopp_grabbing(self):
        self._camera.StopGrabbing()

    def get_camera(self):
        return self._camera
    
    def is_open(self):
        return self._is_open

    @staticmethod
    def get_devices() -> dict:
        dict_devives = {}
        devices = pylon.TlFactory.GetInstance().EnumerateDevices()
        for dev in devices:
            dict_devives[dev.GetSerialNumber()] = dev
        return dict_devives
    
