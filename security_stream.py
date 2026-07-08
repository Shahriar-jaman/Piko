import cv2
import numpy as np
import urllib.request
import time
import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# ==================== CONFIG ====================
ESP32_IP = "192.168.0.221" 
# We use the snapshot URL now (mid resolution is best for speed/quality balance)
URL = f"http://{ESP32_IP}:80/cam-hi.jpg"

# YOLO Config
CONFIG_FILE = "yolov3.cfg"
WEIGHTS_FILE = "yolov3.weights"
NAMES_FILE = "coco.names"

CONF_THRESHOLD = 0.5
NMS_THRESHOLD = 0.4
HARMFUL = ['knife', 'scissors', 'gun', 'pistol', 'rifle']

# Email Config
SEND_EMAIL = True
EMAIL = 'mdsakibsarker52@gmail.com'
PASS = 'acav iegp join llfe'
TO = 'shahriarnayem001@gmail.com'
# ===============================================

print("\n--- SYSTEM STARTING (SNAPSHOT MODE) ---")

# Load YOLO
print("1. Loading YOLOv3...")
try:
    with open(NAMES_FILE, 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    net = cv2.dnn.readNetFromDarknet(CONFIG_FILE, WEIGHTS_FILE)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
except Exception as e:
    print(f"❌ Error loading YOLO: {e}")
    exit()

print(f"2. Target URL: {URL}")
print("   (Press 'q' to quit)")

last_email_time = 0
COOLDOWN = 60

while True:
    try:
        # --- MANUAL IMAGE FETCH (Replaces VideoCapture) ---
        # Timeout set to 5 seconds to prevent freezing
        img_resp = urllib.request.urlopen(URL, timeout=5)
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        frame = cv2.imdecode(imgnp, -1)
        # --------------------------------------------------

        if frame is None:
            print("⚠️ Empty frame received.")
            continue

        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)
        outs = net.forward(net.getUnconnectedOutLayersNames())

        boxes = []
        confidences = []
        class_ids = []
        alert_triggered = False
        detected_label = ""

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > CONF_THRESHOLD:
                    cx, cy = int(detection[0] * w), int(detection[1] * h)
                    bw, bh = int(detection[2] * w), int(detection[3] * h)
                    x, y = int(cx - bw / 2), int(cy - bh / 2)
                    boxes.append([x, y, bw, bh])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, CONF_THRESHOLD, NMS_THRESHOLD)
        
        if len(indexes) > 0:
            for i in indexes.flatten():
                x, y, w, h = boxes[i]
                label = classes[class_ids[i]]
                conf = confidences[i]
                
                color = (0, 0, 255) if label in HARMFUL else (0, 255, 255)
                
                if label == 'person' or label in HARMFUL:
                    alert_triggered = True
                    detected_label = label
                    text = f"ALERT: {label} {conf:.2f}"
                else:
                    text = f"{label} {conf:.2f}"

                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # Email Logic
        if alert_triggered and (time.time() - last_email_time > COOLDOWN):
            print(f"🚨 Intruder ({detected_label}) Detected! Sending Email...")
            filename = f"ALERT_{datetime.now().strftime('%H%M%S')}.jpg"
            cv2.imwrite(filename, frame)
            
            if SEND_EMAIL:
                try:
                    msg = MIMEMultipart()
                    msg['From'] = EMAIL
                    msg['To'] = TO
                    msg['Subject'] = f'SECURITY ALERT: {detected_label.upper()} DETECTED'
                    msg.attach(MIMEText('Camera detected suspicious activity.', 'plain'))
                    
                    with open(filename, 'rb') as f:
                        img = MIMEImage(f.read())
                        img.add_header('Content-Disposition', 'attachment', filename=filename)
                        msg.attach(img)

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(EMAIL, PASS)
                    server.sendmail(EMAIL, TO, msg.as_string())
                    server.quit()
                    print("✅ Email Sent.")
                    last_email_time = time.time()
                except Exception as e:
                    print(f"❌ Email Failed: {e}")
            
            if os.path.exists(filename):
                os.remove(filename)

        cv2.imshow("ESP32 Security (Snapshot Mode)", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    except Exception as e:
        print(f"⚠️ Connection error: {e}")
        print("Retrying in 1 second...")
        time.sleep(1)

cv2.destroyAllWindows()