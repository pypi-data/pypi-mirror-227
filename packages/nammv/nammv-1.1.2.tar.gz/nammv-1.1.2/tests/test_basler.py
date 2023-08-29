import sys
sys.path.append("src/connections")

from camera import Basler


def test_find_devices():
    devs = Basler.get_devices()
    assert len(devs) == 1
    assert '40044700' in devs

def test_open_cam():
    camera = Basler()
    camera.open(0)
    if camera.is_open():
        camera.start_grabbing()
        mat = camera.grab()
        if mat is not None:
            print(mat.shape)
        camera.close()
        

