import sys
sys.path.append("src/connections")

import time
import socket

from socket_utils import *


def test_encode_decode():
    import numpy as np
    mat = np.random.randint(0, 256, (320, 240, 3), np.uint8)

    sb = b'hello'
    buffer = mat2buffer(mat, sb)

    length, _, buffer = buffer.partition(sb)
    mat1 = buffer2mat(buffer)
    assert np.array_equal(mat, mat1)

    buffer = encode_array(mat)
    mat2 = buffer2mat(buffer)
    assert np.array_equal(mat, mat2)


def test_sending_text():
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.connect(("localhost", 5001))

    msg = time.strftime("Client sent %H:%M:%S\n")
    send_text(sk, msg)


def test_sending_image():
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.connect(("localhost", 5001))
    import numpy as np
    mat = np.random.randint(0, 256, (320, 240, 3), np.uint8)
    buffer = mat2buffer(mat)
    send_image(sk, buffer) 

