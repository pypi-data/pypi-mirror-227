import sys
sys.path.append("src/connections")

import time

from socket_utils import send_text

if __name__ == "__main__":
    import socket

    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.connect(("localhost", 5001))

    msg = time.strftime("Client sent %H:%M:%S\n")
    send_text(sk, msg) 

