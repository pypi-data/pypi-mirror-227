from ultralytics import YOLO
import torch
import numpy as np
from collections import namedtuple

DetResult = namedtuple("DetectionResult", ["bnd_box", "class_index", "class_name", "score"])
ClsResult = namedtuple("ClassifyResult", ["class_index", "class_name", "score"])

def load_model(path):
    model = YOLO(path)
    x = np.random.randint(0, 255, (320, 320, 3), np.uint8)
    x = np.transpose(x, (2, 0, 1))
    x = np.expand_dims(x, 0)
    x = torch.tensor(x)
    model(x)
    return model

def det_predict(model, mat, imgsz=320, conf=0.5):
    results = model.predict(mat, imgsz=imgsz, conf=conf)

    preds = []
    for result in results:
        data = result.boxes
        cnf = data.conf.cpu().numpy()
        cls = data.cls.cpu().numpy()
        box = data.xywh.cpu().numpy()

        for score, i, b in zip(cnf, cls, box):
            i = int(i)
            cx, cy, w, h = list(map(int, b))
            x = cx - w//2
            y = cy - h//2
            preds.append(DetResult([x, y, w, h], i, result.names[i], score))
    return preds

def cls_predict(model, mat, imgsz=320, conf=0.5):
    results = model.predict(mat, imgsz=imgsz, conf=conf, device='cpu')

    preds = []
    for result in results:
        probs = result.probs
        class_index = probs.top1
        class_name = result.names[class_index]
        score = float(probs.top1conf.cpu().numpy())
        # name = 
        preds.append(ClsResult(class_index, class_name, score))

    return preds



if __name__ == "__main__":
    import cv2
    # cap = cv2.VideoCapture("rtsp://192.168.2.9:554/live/ch00_0", cv2.CAP_DSHOW)
    # print(cap.isOpened())

    mat = cv2.imread("lion.jpg")
    
    # model = YOLO("yolov8n-cls.pt")
    # print(cls_predict(model, mat))

    model = YOLO("yolov8n.pt")
    # print(det_predict(model, mat))

    cv2.namedWindow("YOLOV8", cv2.WINDOW_FREERATIO)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while True:

        ret, mat = cap.read()

        dets = det_predict(model, mat)

        for result in dets:
            x, y, w, h = result.bnd_box
            cv2.rectangle(mat, (x, y), (x + w, y +h), (255, 255, 255), 2)
            cv2.putText(mat, result.class_name, (x, y), 1, 1, (255, 255, 255), 1)
        
        cv2.imshow("YOLOV8", mat)
        cv2.waitKey(1)