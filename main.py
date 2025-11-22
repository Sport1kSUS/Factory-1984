from ultralytics import YOLO

import cv2

import time
import os


#------------------------------------------------
# нужен именно детект      VVVVVVVVVVVVV
model = YOLO("yolo11n.pt", task='detect')

# Недо-бенчмаркинг
start_time = time.time()


# специально делаю промежуточный видос
# c оптимизациями и именно его NN анализирует
input_video = "zov.mp4"
temp_video = "temp_processed_video.mp4"

#------------------------------------------------

cap = cv2.VideoCapture(input_video)

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# я тут уменьшаю до 20 т.к знаю что исходный видос 60, по сути
# надо сделать это статическим параметром типа reduced_fps = fps / 3
out = cv2.VideoWriter(temp_video, fourcc, 20, (width, 640)) 


# тут недо-оптимизации видоса, пока что тупо скип кадров
processed_frames_count = 0
original_frames_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    original_frames_count += 1
    
    if original_frames_count % 3 == 0 or original_frames_count % 2 == 0:
        continue
    
    # разрешение yf Native_widthx640
    resized_frame = cv2.resize(frame, (width, 640))
    
    out.write(resized_frame)
    processed_frames_count += 1

cap.release()
out.release()

total_people_detected = 0
frame_count = 0

results = model.predict(
    source=temp_video,
    classes=[0],
    save=False, # это менять
    show=True, # и это, остальное не менять
    verbose=False,
    stream=True
)

for frame_idx, result in enumerate(results):
    frame_count += 1
    boxes = result.boxes
    if boxes is not None:
        people_in_frame = len(boxes)
        total_people_detected += people_in_frame
        print(f"Кадр {frame_idx + 1} | {people_in_frame} человек")
    else:
        print(f"Кадр {frame_idx + 1} | 0")




# очистка этого времнного видоса
if os.path.exists(temp_video):
    os.remove(temp_video)

end_time = time.time()
execution_time = end_time - start_time

print(f"Время выполнения: {execution_time:.2f} секунд")
print(f"Исходных кадров: {original_frames_count}")
print(f"Обработанных кадров: {processed_frames_count}")
print(f"Пропущено кадров: {original_frames_count - processed_frames_count}")
print(f"Общее количество обнаружений людей: {total_people_detected}")
print(f"Скорость обработки: {processed_frames_count/execution_time:.2f} кадров/секунду")
