import sys
sys.path.append("src/connections")

from camera import Webcam

if __name__ == "__main__":
    camera = Webcam()
    camera.open(0)
    if camera.is_open():
        mat = camera.grab()
        if mat is not None:
            print(mat.shape)
        camera.close()
        

