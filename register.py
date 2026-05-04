import cv2
import os

# user input
name = input("Enter Name: ")
user_id = input("Enter ID: ")

folder_name = f"{name}_{user_id}"
dataset_path = "dataset"
path = os.path.join(dataset_path, folder_name)

# create dataset folder if not exists
if not os.path.exists(dataset_path):
    os.makedirs(dataset_path)

# create user folder
if not os.path.exists(path):
    os.makedirs(path)

# start camera
cap = cv2.VideoCapture(0)

print("📸 Press 'c' to capture image")
print("❌ Press 'q' to quit")

count = 0

while True:
    ret, frame = cap.read()

    if not ret:
        print("Camera not working")
        break

    cv2.imshow("Register Face", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('c'):
        img_path = os.path.join(path, f"{count}.jpg")
        cv2.imwrite(img_path, frame)
        print(f"Captured image {count}")
        count += 1

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print("✅ Registration complete!")