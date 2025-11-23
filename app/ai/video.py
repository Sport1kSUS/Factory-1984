import cv2

input_video = "../../assets/test_video.mp4"
temp_video = "../../temp/processed_video.mp4"

cap = cv2.VideoCapture(input_video)

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
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
