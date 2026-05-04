import cv2
import os
import pandas as pd
from datetime import datetime
from deepface import DeepFace

dataset_path = "dataset"

def mark_attendance(name):
    file = "attendance.csv"

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    if os.path.exists(file):
        df = pd.read_csv(file)
    else:
        df = pd.DataFrame(columns=["Name", "Date", "Time"])

    # check duplicate
    if not ((df["Name"] == name) & (df["Date"] == date)).any():
        new_row = {"Name": name, "Date": date, "Time": time}

        # ✅ NEW METHOD (no append)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        df.to_csv(file, index=False)
        print(f"Attendance marked for {name}")
    else:
        print(f"{name} already marked today")


cap = cv2.VideoCapture(0)

print("Press 'q' to exit")

while True:
    ret, frame = cap.read()

    try:
        for person in os.listdir(dataset_path):
            person_path = os.path.join(dataset_path, person)

            for img in os.listdir(person_path):
                img_path = os.path.join(person_path, img)

                result = DeepFace.verify(frame, img_path, enforce_detection=False)

                if result["verified"]:
                    name = person
                    mark_attendance(name)

                    cv2.putText(frame, name, (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0,255,0), 2)
                    break

    except Exception as e:
        print("Error:", e)

    cv2.imshow("Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()