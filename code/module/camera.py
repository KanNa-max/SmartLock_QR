import cv2

path = "./image/pic_test.jpg"

def take_pic():   
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    # key = cv2.waitKey(1)
    cv2.imwrite(path, frame)
    cap.release()
    cv2.destroyAllWindows()

# take_pic()
