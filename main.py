import cv2
from ultralytics import YOLO
class Video:
    def __init__(self, video_source="", saved_video_source=""):

        if saved_video_source != "":
            self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.out = cv2.VideoWriter('output.mp4', self.fourcc, 25.0, (1920, 1080))

        if video_source == "":
            self.cap = cv2.VideoCapture(0)
        else:
            self.cap = cv2.VideoCapture(video_source)

    def getFrame(self):
        ret, frame = self.cap.read()
        return ret, frame

    def getVideoInfo(self):
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        return {
            "fps": fps,
            "width": width,
            "height": height,
        }

    def saveFrame(self, frame):
        self.out.write(frame)


    def showFrame(self, frame):
        cv2.imshow("zavod", frame)

    def releaseVideo(self):
        self.cap.release()

    def releaseSavedVideo(self):
        self.out.release()

class Detector:
    def __init__(self):
        self.model = YOLO("yolov8x.pt") #n, s, m, l, x по возрастанию n-самая маленькая x-самая большая
    def detectPeople(self, frame):
        results = self.model(frame, verbose=False)
        people = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                if int(box.cls[0]) == 0:
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    confidence = float(box.conf[0])
                    person_info = {"bbox": [int(x1), int(y1), int(x2), int(y2)],
                                   "confidence": confidence}
                    people.append(person_info)
        return people
    def drawBoxes(self, frame, people):
        for person in people:
            x1, y1, x2, y2 = person["bbox"]
            conf = person["confidence"]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            conf = int(conf*100)
            label = f"Person {conf}%"
            cv2.putText(frame,label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        return frame

class SafetyDetector():

    def __init__(self):
        self.person_model = YOLO("yolov8x.pt")

vid = Video("456315_Laundry_Wash_1920x1080.mp4", "---")
detector = Detector() #n s m(50mb) l(90mb) x(130mb) - model_size
print(vid.getVideoInfo())
while True:
    ret,frame = vid.getFrame()
    frame = detector.drawBoxes(frame, detector.detectPeople(frame))
    if not(ret):
        vid.releaseVideo()
        vid.releaseSavedVideo()
        cv2.destroyAllWindows()
        break
    vid.showFrame(frame)
    vid.saveFrame(frame)

    if cv2.waitKey(1) & 0xFF == ord(' '):
        vid.releaseVideo()
        cv2.destroyAllWindows()
        break