import os
import sys
import uuid
import threading
import socket
import numpy as np
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QMainWindow, QPushButton
from PyQt5.QtGui import QImage, QPixmap, QPainter
from PyQt5.QtCore import QTimer
import cv2
import time
import multiprocessing

id = uuid.uuid4()



face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)


def save_face_data(veri_sayisi=500, data_file="yuz_verisi.txt"):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    
    if os.path.exists(data_file):
        os.remove(data_file)
    
    sayac = 0
    
    with open(data_file, "w") as f:
        while sayac < veri_sayisi:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  

            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            
            for (x, y, w, h) in faces:
                def save():
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                        
                    face = gray[y:y+h, x:x+w]
                    face = cv2.resize(face, (300, 300))
                        
                    face_list = face.flatten().tolist()
                    f.write(str(face_list) + "\n")
                    multiprocessing.Process(target=save, args=(face_list,)).start()

                threading.Thread(target=save).start()

                sayac += 1
                if sayac >= veri_sayisi:
                    break

    
    cap.release()
    cv2.destroyAllWindows()

def update_frame():
    ret, frame = cap.read()

    if ret:
        color_frame = frame.copy() 
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        faces = face_cascade.detectMultiScale(grey, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

        for (x, y, w, h) in faces:
            cv2.rectangle(color_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        color_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2RGB)

        h, w, ch = color_frame.shape
        bytes_per_line = ch * w

        q_img = QImage(color_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

        pixmap = QPixmap.fromImage(q_img)
        label.setPixmap(pixmap)

def start_thread():
    threading.Thread(target=save_face_data).start()
    time.sleep(5)


app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle("Yüz Tespiti")
window.setFixedSize(1250,600)

button = QPushButton('Taramayı Başlat', window)
button.setStyleSheet("""
    background-color: #4CAF50;
    color: white;
    font-size: 20px;
    border-radius: 30px;
    padding: 30px 30px;
    border: none;
""")
button.raise_()
button.setGeometry(300,350,200,100)
button.move(790,45)
button.clicked.connect(start_thread)


layout = QVBoxLayout()
label = QLabel(window)
layout.addWidget(label)

window.setGeometry(100,500,1100,500)

widget = QWidget()
widget.setLayout(layout)
window.setCentralWidget(widget)

if not cap.isOpened():
    print("Kamera açılamadı!")
    sys.exit()

timer = QTimer()
timer.timeout.connect(update_frame)
timer.start(30)

window.show()
button.show()

def close_event(event):
    cap.release()

window.closeEvent = close_event

sys.exit(app.exec_())


