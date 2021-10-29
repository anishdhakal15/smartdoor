from face_recognition import load_image_file,face_encodings,compare_faces
from face_recognition import face_locations as fl
from cv2 import VideoCapture,CAP_V4L2
from time import sleep
from os import listdir,path
from django.conf import settings
from threading import Thread
# https://github.com/intel-iot-devkit/sample-videos/raw/master/car-detection.mp4
# https://github.com/intel-iot-devkit/sample-videos/raw/master/face-demographics-walking-and-pause.mp4
class machine():
    def __init__(self):
        self.loop = True
        self.KNOWN_FACES_DIR = path.join(settings.MEDIA_ROOT,'known_faces')
        self.TOLERANCE = 0.6
        self.FRAME_THICKNESS = 3
        self.FONT_THICKNESS = 2
        self.MODEL = 'cnn'
        self.known_faces = []
        self.known_names = []
        self.lastSeen = 'Nobody'
        self.mainloop = None
        self.door = 'Closed'
    def dooropen(self):
        print('door opened')
    def doorclose(self):
        print('door closed')
    def loaddata(self):
        while(self.loop):
            for name in listdir(self.KNOWN_FACES_DIR):
                for filename in listdir(f'{self.KNOWN_FACES_DIR}/{name}'):
                    image = load_image_file(f'{self.KNOWN_FACES_DIR}/{name}/{filename}')
                    encoding = face_encodings(image)[0]
                    self.known_faces.append(encoding)
                    self.known_names.append(name)
                    sleep(5)
    def startCompare(self):
        datastart= Thread(target=self.loaddata)
        video_capture = VideoCapture('face-demographics-walking.mp4',CAP_V4L2) #face-demographics-walking.mp4  car-detection.mp4
        face_locations = []
        datastart.start()
        def compare(self):
            ret, frame = video_capture.read()
            print(ret)
            rgb_frame = frame[:, :, ::-1]
            face_locations = fl(rgb_frame)
            encodings = face_encodings(rgb_frame, face_locations)
            for face_encoding, face_location in zip(encodings, face_locations):
                results = compare_faces(self.known_faces, face_encoding, self.TOLERANCE)
                match = None
                if True in results:
                    self.lastSeen = self.known_names[results.index(True)]
                    return self.lastSeen
                sleep(0.2)
        matchaa=None
        while self.loop:
            matchaa=compare(self)
            if matchaa !=None:
                self.door = 'Open'
                print(matchaa,"dooropen")
                sleep(6)
                self.door = 'Closed'
                print("doorclosed")
                matchaa=None
        datastart.join()
        video_capture.release()
    def start(self):
        self.loop = True
        self.mainloop= Thread(target=self.startCompare)
        self.mainloop.start()
    def stop(self):
        self.loop = False
        self.mainloop.join()




# if __name__ == "__main__":
#     main = machine()
#     mainloop= threading.Thread(target=main.startCompare)
#     mainloop.start()