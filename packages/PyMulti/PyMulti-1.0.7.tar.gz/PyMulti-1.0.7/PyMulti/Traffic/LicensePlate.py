# PyMulti (Traffic) - License Plate

''' This is the "LicensePlate" module. '''

'''
Copyright 2023 Aniketh Chavare

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

# Imports
import os
import cv2
import imutils
import mimetypes
import numpy as np
import pytesseract

# Sample Media
SampleImage1 = os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/") + "/assets/sample_media/LicensePlate/images/1.jpg"
SampleImage2 = os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/") + "/assets/sample_media/LicensePlate/images/2.jpg"
SampleImage3 = os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/") + "/assets/sample_media/LicensePlate/images/3.jpg"
SampleImage4 = os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/") + "/assets/sample_media/LicensePlate/images/4.jpg"
SampleImage5 = os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/") + "/assets/sample_media/LicensePlate/images/5.jpg"
SampleImage6 = os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/") + "/assets/sample_media/LicensePlate/images/6.jpg"
SampleImage7 = os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/") + "/assets/sample_media/LicensePlate/images/7.jpg"
SampleImage8 = os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/") + "/assets/sample_media/LicensePlate/images/8.jpg"

# Class 1 - License Plate
class LicensePlate:
    # Function 1 - Init
    def __init__(self, file_path, tesseract_path=None):
        # Checking if File Path Exists
        if (os.path.exists(file_path)):
            # Assigning the Variable "file_path"
            self.file_path = file_path

            # Checking the File Type
            mimetypes.init()
            file_type = mimetypes.guess_type(file_path)[0].split("/")[0]

            if (file_type in ["image"]):
                # Assigning the Variable "file_type"
                self.file_type = file_type
            else:
                raise Exception("The file provided must be an image.")

            # Checking if Tesseract Path Exists
            if (tesseract_path != None):
                if (os.path.exists(tesseract_path)):
                    # Assigning the Variable "tesseract_path"
                    self.tesseract_path = tesseract_path
                else:
                    raise Exception("The 'tesseract_path' argument must point to a valid 'tesseract.exe' file. If Tesseract-OCR is not functioning properly or not installed on your computer, get it from https://github.com/UB-Mannheim/tesseract/wiki.")
        else:
            raise FileNotFoundError("The file path doesn't exist.")

    # Function 2 - Get
    def get(self):
        # Checking the File Type
        if (self.file_type == "image"):
            # Connecting to Tesseract-OCR
            try:
                pytesseract.pytesseract.tesseract_cmd = self.tesseract_path
            except:
                raise Exception("The 'tesseract_path' argument (during initialization) must point to a valid 'tesseract.exe' file. If Tesseract-OCR is not functioning properly or not installed on your computer, get it from https://github.com/UB-Mannheim/tesseract/wiki.")

            # Reading the Image
            img = cv2.imread(self.file_path, cv2.IMREAD_COLOR)
            img = cv2.resize(img, (600,400))

            # Converting the Image to Grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.bilateralFilter(gray, 13, 15, 15)

            # Finding & Counting the Contours
            edged = cv2.Canny(gray, 30, 200)
            contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(contours)
            contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
            screenCount = None

            for c in contours:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.018 * peri, True)

                if len(approx) == 4:
                    screenCount = approx
                    break

            # Drawing the Contours
            if (screenCount is not None):
                cv2.drawContours(img, [screenCount], -1, (0, 0, 255), 3)

            mask = np.zeros(gray.shape, np.uint8)
            new_image = cv2.drawContours(mask, [screenCount], 0,255, -1,)
            new_image = cv2.bitwise_and(img, img, mask=mask)

            (x, y) = np.where(mask == 255)
            (topx, topy) = (np.min(x), np.min(y))
            (bottomx, bottomy) = (np.max(x), np.max(y))
            Cropped = gray[topx:bottomx+1, topy:bottomy+1]

            # Fetching the License Plate Number
            try:
                text = pytesseract.image_to_string(Cropped, config="--psm 11")
            except:
                raise Exception("The 'tesseract_path' argument (during initialization) must point to a valid 'tesseract.exe' file. If Tesseract-OCR is not functioning properly or not installed on your computer, get it from https://github.com/UB-Mannheim/tesseract/wiki.")

            # Stopping OpenCV
            cv2.destroyAllWindows()

            # Returning the License Plate Number
            if ((text[-1] == " ") or (text[-1] == "") or (text[-1] == "\n")):
                return text.replace(text[-1], "")
            else:
                return text
        else:
            raise Exception("An error occurred. Please try again.")

    # Function 3 - Show
    def show(self):
        # Checking the File Type
        if (self.file_type == "image"):
            # Reading the Image
            img = cv2.imread(self.file_path)

            # Converting the Image to Grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Finding the Plates
            plates = cv2.CascadeClassifier(os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/") + "/assets/models/haarcascade_russian_plate_number.xml").detectMultiScale(gray, 1.2, 5)

            # Displaying Each License Plate
            for (x,y,w,h) in plates:
                cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
                gray_plates = gray[y:y+h, x:x+w]
                color_plates = img[y:y+h, x:x+w]

                cv2.imshow("Vehicle", img)
                cv2.imshow("License Plate", gray_plates)
                cv2.waitKey(0)
        else:
            raise Exception("An error occurred. Please try again.")