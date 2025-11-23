# TODO TODO TODO TODO TODO TODO TODO #

from ultralytics import YOLO

model = YOLO("../../assets/models/yolo11n.pt", task="detect")

total_people_detected = 0
frame_count = 0

results = model.predict(
    source="это_просто_заглушка",
    classes=[0],
    save=False,  # это менять
    show=True,  # и это, остальное не менять
    verbose=False,
    stream=True,
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
    # if os.path.exists(temp_video):
    #     os.remove(temp_video)
