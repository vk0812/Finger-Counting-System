import cv2
import mediapipe as mp
import time


class Detector():
    # See Mediapipe Github Repo for Parameters
    def __init__(self, mode=False, maxHands=2, detecionConf=0.5, trackConf=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionConf = detecionConf
        self.trackConf = trackConf
     
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode, max_num_hands=self.maxHands,
                                        min_detection_confidence=self.detectionConf,
                                        min_tracking_confidence=self.trackConf)

        self.mpDraw = mp.solutions.drawing_utils 

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # RGB has to be sent to self.hands
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:  # if true
            for hand_landmark in self.results.multi_hand_landmarks:  # for each hand
                if(draw):
                    self.mpDraw.draw_landmarks(
                        img, hand_landmark, self.mpHands.HAND_CONNECTIONS) # to connect dots between 21 points on hand

        return img

    def findPosition(self, img, handNum=0):
        id_pos = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNum]

            # Total 21 features with x,y,z as landmarks
            for id, landmarks in enumerate(myHand.landmark):

                # print(id,landmarks) landmarks.x,y,z is ratio by total image and in decimal
                h, w, c = img.shape  # finding height, width and channels of our image
                # finding true pixel value for point
                cx, cy = int(landmarks.x * w), int(landmarks.y * h)

                id_pos.append([id, cx, cy])
                # we do not want to draw on RGB image but on the image we are displaying

        return id_pos


def main():
    cam = cv2.VideoCapture(0)

    prev = 0
    curr = 0

    detector = Detector()

    while True:
        res, img = cam.read()
        img = detector.findHands(img)
        id_pos = detector.findPosition(img)
        if(len(is_pos) != 0):
            print(len(id_pos))

        curr = time.time()
        fps = 1/(curr-prev)
        prev = curr
        cv2.putText(img, str(int(fps)), (10, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 3)

        cv2.imshow("Hand Tracking", img)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
