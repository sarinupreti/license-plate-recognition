# Main.py

import os
from builtins import int, round, tuple, len, float

import cv2
# from flask import Flask, render_template
# app = Flask(__name__)


import DetectCharactersHelper
import DetectPlatesHelper


#
# @app.route('/<numberplate>')
# def index(licPlate):
#    return render_template("index.html", numberplate = licPlate)
#
# if __name__ == "__main__":
#     app.run()

SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = False


def main():
    dataTraining = DetectCharactersHelper.loadDataAndTrain()  # attempt KNN training

    if dataTraining == False:  # if KNN training was not successful
        print("\n error: KNN-traning was not successful\n")  # show error message
        return  # and exit program
    # end if

    originalImage = cv2.imread("0.jpg")  # open image

    if originalImage is None:  # if image was not read successfully
        print("\n ERROR:: image not read from the picture \n\n")
        os.system("pause")  # pauses the code so error can be checked
        return  # and exit program
    # end if

    listOfPossiblePlates = DetectPlatesHelper.detectPlatesInScene(originalImage)  # detect plates

    listOfPossiblePlates = DetectCharactersHelper.detectCharsInPlates(listOfPossiblePlates)  # detect chars in plates

    cv2.imshow("Original_Image", originalImage)  # show scene image

    if len(listOfPossiblePlates) == 0:  # if no plates were found
        print("\n ERROR:: no license plates were detected\n")  # print user no plates were found
    else:

        # sort the list of possible plates in DESCENDING order (most number of chars to least number of chars)
        listOfPossiblePlates.sort(key=lambda possiblePlate: len(possiblePlate.strChars), reverse=True)

        # suppose the plate with the most recognized chars (the first plate in sorted by string length descending order) is the actual plate
        licPlate = listOfPossiblePlates[0]

        cv2.imshow("Plate_image", licPlate.imgPlate)  # show crop of plate and threshold of plate
        cv2.imshow("Threshold_image", licPlate.imgThresh)

        if len(licPlate.strChars) == 0:  # if no chars were found in the plate
            print("\n ERROR :: no characters were detected\n\n")  # show message
            return  # and exit program
        # end if

        # draw red rectangle around plate
        drawRedRectangleAroundPlate(originalImage, licPlate)

        print("------------------DETECTED-NUMBER PLATE FROM IMAGE----------------------")
        print("\n " + licPlate.strChars + "\n")

        print("----------------------------------------")

        writeLicensePlateCharsOnImage(originalImage, licPlate)  # write license plate text on the image

        cv2.imshow("final_image", originalImage)  # showing image again from image comparision

        cv2.imwrite("original_Image.png", originalImage)  # write image out to file

    # end if else

    cv2.waitKey(0)  # hold windows open until user presses a key

    return


# end main


def drawRedRectangleAroundPlate(imgOriginalScene, licPlate):
    p2fRectPoints = cv2.boxPoints(licPlate.rrLocationOfPlateInScene)  # four sides of rotated rectangle plate

    cv2.line(imgOriginalScene, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), SCALAR_RED, 2)  # draw 4 red lines
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), SCALAR_RED, 2)


# end function

###################################################################################################
def writeLicensePlateCharsOnImage(imgOriginalScene, licPlate):
    ptCenterOfTextAreaX = 0  # this will be the center of the area the text will be written to
    ptCenterOfTextAreaY = 0

    BottomLowerLeftTextFromNumberPlateX = 0  # this will be the bottom left of the area that the text will be written to
    BottomLowerLeftTextFromNumberPlateY = 0

    sceneHeight, sceneWidth, sceneNumChannels = imgOriginalScene.shape
    plateHeight, plateWidth, plateNumChannels = licPlate.imgPlate.shape

    intFontFace = cv2.FONT_HERSHEY_SIMPLEX  # choose a plain jane font
    fltFontScale = float(plateHeight) / 30.0  # base font scale on height of plate area
    intFontThickness = int(round(fltFontScale * 1))  # base font thickness on font scale

    textSize, baseline = cv2.getTextSize(licPlate.strChars, intFontFace, fltFontScale,
                                         intFontThickness)  # call getTextSize

    # unpack roatated rect into center point, width and height, and angle
    ((intPlateCenterX, intPlateCenterY), (intPlateWidth, intPlateHeight),
     fltCorrectionAngleInDeg) = licPlate.rrLocationOfPlateInScene

    intPlateCenterX = int(intPlateCenterX)  # make sure center is an integer
    intPlateCenterY = int(intPlateCenterY)

    ptCenterOfTextAreaX = int(intPlateCenterX)  # the horizontal location of the text area is the same as the plate

    if intPlateCenterY < (sceneHeight * 0.75):  # if the license plate is in the upper 3/4 of the image
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) + int(
            round(plateHeight * 1.6))  # write the chars in below the plate
    else:  # else if the license plate is in the lower 1/4 of the image
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) - int(
            round(plateHeight * 1.6))  # write the chars in above the plate
    # end if

    textSizeWidth, textSizeHeight = textSize  # unpack text size width and height

    BottomLowerLeftTextFromNumberPlateX = int(
        ptCenterOfTextAreaX - (textSizeWidth / 2))  # calculate the lower left origin of the text area
    BottomLowerLeftTextFromNumberPlateY = int(
        ptCenterOfTextAreaY + (textSizeHeight / 2))  # based on the text area center, width, and height

    # write the text on the image
    cv2.putText(imgOriginalScene, licPlate.strChars,
                (BottomLowerLeftTextFromNumberPlateX, BottomLowerLeftTextFromNumberPlateY), intFontFace, fltFontScale,
                SCALAR_YELLOW, intFontThickness)


# end function

if __name__ == "__main__":
    main()
