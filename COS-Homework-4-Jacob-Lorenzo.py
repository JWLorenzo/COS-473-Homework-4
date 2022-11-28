# Name: Jacob Lorenzo
# Assignment: COS-473-Homework-4
# Date: 11-28-22
# Professor: Dr. Yoo

# Import the packages used for the program
import cv2 as cv
import numpy as np

# Initializes lists that are used to store the coordinates for the homography matrix
SourceList = []
DestinationList = []

# Creates the prompts to get the strings to use for the file names
SourceImage = input("What is the name of the first image?\n")

DestinationImage = input("What is the name of the second image?\n")

# Provides instructions for what to do once the files have been found
print(
    "Good, now starting from the top left corner of the quadrat, moving clockwise, select the quadrat corners"
    "for each quadrat\n"
)

print("Once you are done, click q\n")

# Sets up the variables that read the files from the given names
# Source Image
SourceImg = cv.imread(SourceImage)
SourceImg = cv.resize(SourceImg, (500, 500), interpolation=cv.INTER_AREA)
SourceImg = cv.rotate(SourceImg, cv.ROTATE_90_COUNTERCLOCKWISE)

# Destination Image
DestinationImg = cv.imread(DestinationImage)
DestinationImg = cv.resize(DestinationImg, (500, 500), interpolation=cv.INTER_AREA)

# Source Image Transformation
TransformedSource = cv.imread(SourceImage)
TransformedSource = cv.resize(
    TransformedSource, (500, 500), interpolation=cv.INTER_AREA
)
TransformedSource = cv.rotate(TransformedSource, cv.ROTATE_90_COUNTERCLOCKWISE)

# Function for left-clicks on the source image
def LeftClickSourceFunction(event, x, y, flags, param):
    global SourceList
    # This draws circles on the point where it was clicked and stores that coordinate
    if event == cv.EVENT_LBUTTONDOWN:
        cv.circle(SourceImg, (x, y), 3, (0, 255, 0), -1)
        SourceList.append([x, y])


# Function for left-clicks on the destination image
def LeftClickDestinationFunction(click, x, y, flags, param):
    global DestinationList
    if click == cv.EVENT_LBUTTONDOWN:
        # This draws circles on the point where it was clicked and stores that coordinate
        cv.circle(DestinationImg, (x, y), 3, (0, 0, 255), -1)
        DestinationList.append([x, y])


while True:

    # Displays the source image and checks for left clicks
    cv.imshow("SourceImg", SourceImg)
    cv.setMouseCallback("SourceImg", LeftClickSourceFunction)

    # Displays the destination image and checks for left clicks
    cv.imshow("DestinationImg", DestinationImg)
    cv.setMouseCallback("DestinationImg", LeftClickDestinationFunction)

    # Once the user presses q, then it moves to the transform of the images
    if cv.waitKey(1) & 0xFF == ord("q"):
        cv.destroyAllWindows()

        # These declare that they are floats
        PointsSource = np.float32(SourceList)
        PointsDestination = np.float32(DestinationList)

        # This creates the homography matrix
        HomographyMatrix = cv.getPerspectiveTransform(PointsSource, PointsDestination)

        PerspectiveWarpResult = cv.warpPerspective(
            TransformedSource,
            HomographyMatrix,
            (int(SourceImg.shape[1]), int(SourceImg.shape[0])),
        )

        print("Once you are done viewing the PerspectiveWarpResult, press q to exit\n")

        while True:

            # Shows the transformation
            cv.imshow("perspectivee transformation", PerspectiveWarpResult)

            # User can exit program with q
            if cv.waitKey(1) & 0xFF == ord("q"):
                quit()
