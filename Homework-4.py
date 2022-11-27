import cv2 as cv
import numpy as np

Image1 = input('What is the name of the first image?\n')

Image2 = input('What is the name of the second image?\n')

print("Good, now starting from the top left corner of the quadrat, moving clockwise, select the quadrat corners"
      "for each quadrat\n")

print("Once you are done, click q\n")

list1 = []
list2 = []

img = cv.imread(Image1)
img = cv.resize(img, (500, 500), interpolation=cv.INTER_AREA)
img = cv.rotate(img, cv.ROTATE_90_COUNTERCLOCKWISE)

img2 = cv.imread(Image2)
img2 = cv.resize(img2, (500, 500), interpolation=cv.INTER_AREA)

img3 = cv.imread(Image1)
img3 = cv.resize(img3, (500, 500), interpolation=cv.INTER_AREA)
img3 = cv.rotate(img3, cv.ROTATE_90_COUNTERCLOCKWISE)


def leftclickfn1(event, x, y, flags, param):
    global list1
    if event == cv.EVENT_LBUTTONDOWN:
        cv.circle(img, (x, y), 3, (0, 0, 255), -1)
        list1.append([x, y])


def leftclickfn2(click, x, y, flags, param):
    global list2
    if click == cv.EVENT_LBUTTONDOWN:
        cv.circle(img2, (x, y), 3, (0, 0, 255), -1)
        list2.append([x, y])


while True:
    cv.imshow('img', img)
    cv.setMouseCallback('img', leftclickfn1)

    cv.imshow('img2', img2)
    cv.setMouseCallback('img2', leftclickfn2)

    if cv.waitKey(1) & 0xFF == ord('q'):
        cv.destroyAllWindows()
        pointset1 = np.float32(list1)
        pointset2 = np.float32(list2)
        homographymatrix = cv.getPerspectiveTransform(pointset1, pointset2)

        result = cv.warpPerspective(img3, homographymatrix, (int(img.shape[1]), int(img.shape[0])))

        print("Once you are done viewing the result, press q to exit\n")

        while True:

            cv.imshow('perspectivee transformation', result)

            if cv.waitKey(1) & 0xFF == ord('q'):
                quit()
