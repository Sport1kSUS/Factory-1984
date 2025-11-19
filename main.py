import threading
import cv2
from ultralytics import YOLO
import time

class Video:
    def __init__(self, video_source="", save_video=False):

        if save_video:
            self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.out = cv2.VideoWriter('output.mp4', self.fourcc, 25.0, (1920, 1080))

        if video_source == "":
            self.cap = cv2.VideoCapture(0)
        else:
            self.cap = cv2.VideoCapture(video_source)

    def getFrame(self):
        ret, frame = self.cap.read()
        return ret, frame

    def setVideoInfo(self, fps, width, height):
        self.cap.set(cv2.CAP_PROP_FPS, fps)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def getVideoInfo(self):
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        length = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        if fps!=0:
            length = length/fps
        else:
            length = 0
        return {
            "fps": fps,
            "width": width,
            "height": height,
            "time": length,
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
        self.model = YOLO("yolov8x.pt") # yolov8x.pt 200+sec
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

class Stopwatch:
    def __init__(self):
        self.start_time = 0
        self.elapsed_time = 0
        self.is_running = False
        self.thread = None

    def start(self):
        if not self.is_running:
            self.start_time = time.time() - self.elapsed_time
            self.is_running = True
            self.thread = threading.Thread(target=self._run)
            self.thread.start()

    def stop(self):
        if self.is_running:
            self.is_running = False
            self.elapsed_time = time.time() - self.start_time
            self.thread.join()

    def reset(self):
        self.elapsed_time = 0
        self.is_running = False
        self.start_time = 0

    def get_time(self):
        if self.is_running:
            return time.time() - self.start_time
        else:
            return self.elapsed_time

    def _run(self):
        while self.is_running:
            time.sleep(0.1)



sourceChange = input("change source? (y/skip)")
if sourceChange == "y":
    source = r"".join(input("file source:"))
else:
    source = r"D:\Program Files\PyCharm\PythonProjects\Factory1984\456315_Laundry_Wash_1920x1080.mp4"


vid = Video(source, True)
detector = Detector()
vidStopWatch = Stopwatch()

paramsChange = input("change resolution? (y/skip)")
if paramsChange == "y":
    vidParams = input("video parameters (or press ENTER for 20FPS 1280x720):")
    if vidParams != "":
        fps, width, height = list(map(int,vidParams.split(" ")))
    else:
        fps, width, height = 20, 1280, 720
    vid.setVideoInfo(fps, width, height)

print(vid.getVideoInfo())

while True:
    vidStopWatch.start()
    ret,frame = vid.getFrame()
    frame = detector.drawBoxes(frame, detector.detectPeople(frame))
    if not(ret):
        vid.releaseVideo()
        vid.releaseSavedVideo()
        cv2.destroyAllWindows()
        vidStopWatch.stop()
        print("time: ",vidStopWatch.get_time())
        break
    vid.showFrame(frame)
    vid.saveFrame(frame)

    if cv2.waitKey(1) & 0xFF == ord(' '):
        vid.releaseVideo()
        cv2.destroyAllWindows()
        vidStopWatch.stop()
        break


