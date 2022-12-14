# Name: Jacob Lorenzo
# Assignment: COS-473-Homework-4
# Date: 11-28-22
# Professor: Dr. Yoo

# Import the packages used for the program
import cv2 as cv
import numpy as np

# Initializes lists that are used to store the coordinates for the homography matrix
SourceList = []
DestinationList = [[0, 0], [750, 0], [750, 750], [0, 750]]

# Creates the prompts to get the strings to use for the file names
SourceImage = input("What is the name of the image?\n")

# Provides instructions for what to do once the files have been found
print("Good, now rotate the image so its in the proper orientation by pressing r\n")

print("Once you are done, click q\n")

# Sets up the variables that read the files from the given names
# Source Image
SourceImg = cv.imread(SourceImage)
SourceImg = cv.resize(SourceImg, (750, 750), interpolation=cv.INTER_AREA)

# Source Image Transformation
TransformedSource = cv.imread(SourceImage)
TransformedSource = cv.resize(
    TransformedSource, (750, 750), interpolation=cv.INTER_AREA
)

# Function for left-clicks on the source image
def LeftClickSourceFunction(event, x, y, flags, param):
    global SourceList

    # This draws circles on the point where it was clicked and stores that coordinate
    if event == cv.EVENT_LBUTTONDOWN:
        cv.circle(SourceImg, (x, y), 3, (0, 0, 255), -1)
        SourceList.append([x, y])


while True:

    # Displays the image
    cv.imshow("SourceImg", SourceImg)

    # Checks the keypressed for rotation and exit purposes
    pressedKey = cv.waitKey(1) & 0xFF

    # Checks if r is pressed to rotate the image
    if pressedKey == ord("r"):
        cv.destroyAllWindows()
        SourceImg = cv.rotate(SourceImg, cv.ROTATE_90_COUNTERCLOCKWISE)
        TransformedSource = cv.rotate(TransformedSource, cv.ROTATE_90_COUNTERCLOCKWISE)
        cv.imshow("SourceImg", SourceImg)

    # Checks if q is pressed to continue
    elif pressedKey == ord("q"):
        cv.destroyAllWindows()
        print(
            "Good, now starting with the top left corner, going clockwise, select the four corners of the quadrat, press q once you are done"
            "\n"
        )
        while True:
            # Displays the source image and checks for left clicks
            cv.imshow("SourceImg", SourceImg)
            cv.setMouseCallback("SourceImg", LeftClickSourceFunction)

            # Once the user presses q, then it moves to the transform of the images
            if cv.waitKey(1) & 0xFF == ord("q"):
                cv.destroyAllWindows()

                # These declare that they are floats
                PointsSource = np.float32(SourceList)
                PointsDestination = np.float32(DestinationList)

                # This creates the homography matrix
                HomographyMatrix = cv.getPerspectiveTransform(
                    PointsSource, PointsDestination
                )

                # This warps the perspective
                PerspectiveWarpResult = cv.warpPerspective(
                    TransformedSource,
                    HomographyMatrix,
                    (int(SourceImg.shape[1]), int(SourceImg.shape[0])),
                )

                print(
                    "Once you are done viewing the PerspectiveWarpResult, press q to exit\n"
                )

                while True:

                    # Shows the transformation
                    cv.imshow("perspective transformation", PerspectiveWarpResult)

                    # User can exit program with q
                    if cv.waitKey(1) & 0xFF == ord("q"):
                        quit()
