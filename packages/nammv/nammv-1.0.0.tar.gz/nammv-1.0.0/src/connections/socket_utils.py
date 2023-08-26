from io import BytesIO
import numpy as np

TXT_STARTBYTES = b':text:'
IM_STARTBYTES = b':image:'

def mat2buffer(array:np.ndarray):
    f = BytesIO()
    np.savez(f, frame=array)
    packet_size = len(f.getvalue())
    header = f'{packet_size}{IM_STARTBYTES.decode()}'
    out = bytearray()
    out += header.encode()
    f.seek(0)
    out += f.read()
    return out

def text2buffer(text:str):
    out = bytearray()
    text = text.encode()
    packet_size = len(text)
    header = f'{packet_size}{TXT_STARTBYTES.decode()}'
    out += header.encode()
    out += text
    return out

def buffer2mat(buffer:bytes):
    return np.load(BytesIO(buffer), allow_pickle=True)['frame']

def buffer2text(buffer:bytes):
    return buffer.decode()

def send_image(socket, mat:np.ndarray):
    buffer = mat2buffer(mat)
    socket.sendall(buffer)

def send_text(socket, text:str):
    buffer = text2buffer(text)
    socket.sendall(buffer)