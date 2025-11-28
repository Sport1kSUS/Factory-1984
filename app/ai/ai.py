import time
import cv2
from ultralytics import YOLO


def drawBoxes(frame, result, class_labels, class_colors, class_conf, get_count=False):# BGR
    boxes = result.boxes
    amount = dict(zip(class_labels, [0]*len(class_labels))) # словать с подсчетом объектов каждого класса

    for box in boxes:

        cls = int(box.cls[0])
        x1, y1, x2, y2 = list(map(int,box.xyxy[0]))
        conf = float(box.conf[0])
        id = int(box.id[0]) if box.id != None else "-" # айди треккинга
        if conf>=class_conf[cls]:
            amount[class_labels[cls]] += 1 # добавление найденного объекта с привязкой к классу в счётчик
            cv2.rectangle(frame, (x1, y1), (x2, y2), class_colors[cls], 2)
            cv2.putText(frame, f"{class_labels[cls]} id: {id}  {int(conf*100)}%", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, class_colors[cls], 2)

    if get_count:
        return frame, amount

    else:
        return frame


start_time = time.time()

model_ppe = YOLO("../../assets/models/ppe.pt")
model_fall = YOLO("../../assets/models/fall.pt")
model_person = YOLO("../../assets/models/yolo11n.pt")

input_video = "../../assets/test_video.mp4"
output_video = "../../assets/output_video.mp4"

cap = cv2.VideoCapture(input_video)

input_fps = cap.get(cv2.CAP_PROP_FPS)
input_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
input_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
input_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))



if input_fps>10: reduced_fps_coefficient = input_fps // 10# уменьшаем фпс ближе к 15
else: reduced_fps_coefficient=1
if input_height>=640: target_height = 640
else: target_height = input_height
if input_width>=640: target_width = 640
else: target_width = input_width

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(output_video, fourcc, 10.0, (input_width, target_height)) # сохраняем готове видео


while True:
    ret, frame = cap.read()
    if not ret:
        break

    current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    if current_frame % reduced_fps_coefficient != 0:
        continue

    resized_frame = cv2.resize(frame, (input_width, target_height))
    results_ppe = model_ppe.track(resized_frame, stream=True, verbose=False, device="cpu", conf=0.2)# , classes=[0,1,2,3,4,5,7,8,9] person --> 11n
    results_fall = model_fall.predict(resized_frame, stream=True, verbose=False, device="cpu", conf=0.2)
   # results_person = model_person.track(resized_frame, stream=True, verbose=False, device="cpu",  conf=0.2, classes=[0])
    out_frame = resized_frame
    for result_ppe in results_ppe:
        out_frame, ppe_amount = drawBoxes(out_frame,
                                            result_ppe,
                                            ["helmet","gloves","vest","boots","goggles","none", "person", "???", "???", "no_gloves"],
                                            [(255, 0, 0),(215, 0, 255), (76, 59, 255),(198, 255, 63) , (111, 53, 96),(31, 34, 30) ,(0, 255, 0) ,(0, 0, 255),(0, 0, 255),(0, 0, 255)],
                                            [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.5, 0.3, 0.3, 0.3, 0.3],True)


    for result_fall in results_fall:
        out_frame, fall_amount = drawBoxes(out_frame, result_fall, ["fall"], [(0, 0, 255)],[0.4], True)

    # for result_person in results_person:
    #     out_frame, person_amount = drawBoxes(out_frame, result_person, ["person"], [(0, 255, 0)],[0.4], True)

   # cv2.imshow("frame", out_frame)
    out.write(out_frame)
    for keys, value in ppe_amount.items():
        print("{0}: {1}".format(keys, value))
    print("\n")
    key = cv2.waitKey(1) & 0xFF
    if key == ord(" "):
        start_time = time.time()
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        break



end_time = time.time()
print("Время выполнения: ", end_time - start_time, " секунд")

cap.release()
cv2.destroyAllWindows()







# TODO
#  Обучить 1000 epochs на суперкомпьютере
#from ultralytics import YOLO
#
# # Load pretrained model
# model = YOLO("yolo11n.pt")
#
# # Train the model on Construction-PPE dataset
# model.train(data="construction-ppe.yaml", epochs=1000, imgsz=640, name="ppe")

# TODO
#  cls: tensor([0.])
#  conf: tensor([0.6620])
#  data: tensor([[558.9044, 174.6042, 647.9957, 259.9578,   1.0000,   0.6620,   0.0000]])
#  id: tensor([1.])
#  is_track: True
#  orig_shape: (640, 1280)
#  shape: torch.Size([1, 7])
#  xywh: tensor([[603.4501, 217.2810,  89.0913,  85.3535]])
#  xywhn: tensor([[0.4714, 0.3395, 0.0696, 0.1334]])
#  xyxy: tensor([[558.9044, 174.6042, 647.9957, 259.9578]])
#  xyxyn: tensor([[0.4366, 0.2728, 0.5062, 0.4062]])
#  -
#  cls: tensor([0.])
#  conf: tensor([0.6620])
#  data: tensor([[558.9044, 174.6042, 647.9957, 259.9578,   0.6620,   0.0000]])
#  id: None
#  is_track: False
#  orig_shape: (640, 1280)
#  shape: torch.Size([1, 6])
#  xywh: tensor([[603.4501, 217.2810,  89.0913,  85.3535]])
#  xywhn: tensor([[0.4714, 0.3395, 0.0696, 0.1334]])
#  xyxy: tensor([[558.9044, 174.6042, 647.9957, 259.9578]])
#  xyxyn: tensor([[0.4366, 0.2728, 0.5062, 0.4062]])



