import face_recognition as fr
import cv2
from Database import *

pathFaceRecFile = 'C:/Users/Korisnik/Desktop/faks/face_recognition_images'


class FaceRecog:
    def __init__(self):
        a = 1
        res = getAllUsernames()
        self.known_face_encondings = []
        self.known_face_names = []
        if res is None:
            return

        for username in res:
            image = fr.load_image_file(f"{pathFaceRecFile}/{username}.jpg")
            image_encoding = fr.face_encodings(image)[0]

            self.known_face_encondings.append(image_encoding)
            self.known_face_names.append(username)






    def regRun(self, name):
        self.video_capture = cv2.VideoCapture(0)

        while True:
            ret, frame = self.video_capture.read()
            cv2.imshow('Webcam_facerecognition', frame)
            img_counter = 0
            if cv2.waitKey(1) & 0xFF == ord('q'):
                img_name = "{}.jpg".format(name)
                cv2.imwrite(f"{pathFaceRecFile}\{img_name}", frame)
                print("{} written!".format(img_name))
                img_counter += 1

                break

        self.video_capture.release()
        cv2.destroyAllWindows()

    def run(self):
        self.matchedFace = False
        self.video_capture = cv2.VideoCapture(0)
        self.matchedUsername = ""
        while True:
            ret, frame = self.video_capture.read()

            rgb_frame = frame[:, :, ::-1]

            face_locations = fr.face_locations(rgb_frame)
            face_encodings = fr.face_encodings(rgb_frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

                matches = fr.compare_faces(self.known_face_encondings, face_encoding, tolerance=0.5)

                name = "Unknown"

                face_distances = fr.face_distance(self.known_face_encondings, face_encoding)

                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
                    self.matchedFace = True
                    self.matchedUsername = name



                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            cv2.imshow('Webcam_facerecognition', frame)
            img_counter = 0
            if cv2.waitKey(1) & 0xFF == ord('q'):

                if self.matchedFace is True:
                    self.video_capture.release()
                    cv2.destroyAllWindows()
                    return self.matchedUsername
                else :
                    self.video_capture.release()
                    cv2.destroyAllWindows()
                    return ""



        self.video_capture.release()
        cv2.destroyAllWindows()

