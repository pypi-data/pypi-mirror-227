import sys
sys.path.append("src/connections")

from basler import Basler

if __name__ == "__main__":
    camera = Basler()
    print(camera.get_devices())
    camera.open(0)
    if camera.is_open():
        camera.start_grabbing()
        mat = camera.grab()
        if mat is not None:
            print(mat.shape)
        camera.close()
        

