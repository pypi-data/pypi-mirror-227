# PyMulti (Traffic) - Vehicle Detection

''' This is the "VehicleDetection" module. '''

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
import time
import mimetypes
import numpy as np
from PIL import Image

# Sample Media
SampleImage1 = os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/") + "/assets/sample_media/VehicleDetection/images/1.jpg"
SampleImage2 = os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/") + "/assets/sample_media/VehicleDetection/images/2.jpg"
SampleImage3 = os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/") + "/assets/sample_media/VehicleDetection/images/3.jpg"
SampleImage4 = os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/") + "/assets/sample_media/VehicleDetection/images/4.jpg"
SampleImage5 = os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/") + "/assets/sample_media/VehicleDetection/images/5.jpg"
SampleImage6 = os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/") + "/assets/sample_media/VehicleDetection/images/6.jpg"
SampleImage7 = os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/") + "/assets/sample_media/VehicleDetection/images/7.jpg"
SampleImage8 = os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/") + "/assets/sample_media/VehicleDetection/images/8.jpg"
SampleImage9 = os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/") + "/assets/sample_media/VehicleDetection/images/9.jpg"
SampleImage10 = os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/") + "/assets/sample_media/VehicleDetection/images/10.jpg"

SampleVideo1 = os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/") + "/assets/sample_media/VehicleDetection/videos/1.mp4"











# Class 1 - Vehicle Detection
class VehicleDetection:
    # Function 1 - Init
    def __init__(self, file_path, function=None, quit=None):
        # Checking if File Path Exists
        if (os.path.exists(file_path)):
            # Assigning the Variable "file_path"
            self.file_path = file_path

            # Checking the File Type
            mimetypes.init()
            file_type = mimetypes.guess_type(file_path)[0].split("/")[0]

            if (file_type in ["image", "video"]):
                # Assigning the Variable "file_type"
                self.file_type = file_type
            else:
                raise Exception("The file provided must be an image or a video.")

            # Checking if "function" is Valid
            if ((function != None) and (callable(function))):
                # Assigning the Variable "function"
                self.function = function
            if (isinstance(quit, str) and len(quit) == 1 and quit.isalpha() and quit != None):
                # Assigning the Variable "quit"
                self.quit = quit
            else:
                raise TypeError("The 'quit' argument must be an alphabet of length 1.")
        else:
            raise FileNotFoundError("The file path doesn't exist.")

    # Function 2 - Get
    def get(self):
        # Checking the File Type
        if (self.file_type == "image"):
            # Connecting to Tesseract-OCR
            pytesseract.pytesseract.tesseract_cmd = self.tesseract_path

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
                raise Exception("The 'tesseract_path' argument must point to a valid 'tesseract.exe' file. If Tesseract-OCR is not functioning properly or not installed on your computer, get it from https://github.com/UB-Mannheim/tesseract/wiki.")

            # Stopping OpenCV
            cv2.destroyAllWindows()

            # Returning the License Plate Number
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





a = VehicleDetection(SampleImage1)
















# Function 1 - Get Cars
def get_cars(file_path, function=None):
    # Checking if Path Exists
    if (os.path.exists(file_path)):
        # Checking the File Type
        mimetypes.init()
        fileType = mimetypes.guess_type(file_path)[0].split("/")[0]

        if (fileType == "image"): # Image
            # Opening the Image
            image = Image.open(file_path)
            image = image.resize((450, 250))
            image_arr = np.array(image)

            # Converting Image to Greyscale
            grey = cv2.cvtColor(image_arr, cv2.COLOR_BGR2GRAY)
            Image.fromarray(grey)

            # Blurring the Image
            blur = cv2.GaussianBlur(grey, (5,5), 0)
            Image.fromarray(blur)

            # Dilating the Image
            dilated = cv2.dilate(blur, np.ones((3,3)))
            Image.fromarray(dilated)

            # Morphology
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
            closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel) 
            Image.fromarray(closing)

            # Identifying the Cars
            cars = cv2.CascadeClassifier(os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/") + "/assets/models/haarcascade_car.xml").detectMultiScale(closing, 1.1, 1)

            # Counting the Cars
            count = 0

            for (x, y, w, h) in cars:
                cv2.rectangle(image_arr,(x,y),(x+w,y+h),(255,0,0),2)
                count += 1

                # Performing the User Function
                if ((function is not None) and (callable(function))):
                    function()

            # Stopping OpenCV
            cv2.destroyAllWindows()

            # Returning the Count
            return count
        else:
            raise Exception("The file provided must be an image.")
    else:
        raise FileNotFoundError("The file path doesn't exist.")

# Function 2 - Show Cars
def show_cars(file_path, function=None, quit=None):
    # Checking if Path Exists
    if (os.path.exists(file_path)):
        # Checking the File Type
        mimetypes.init()
        fileType = mimetypes.guess_type(file_path)[0].split("/")[0]

        if (fileType == "image"): # Image
            # Opening the Image
            image = Image.open(file_path)
            image = image.resize((450, 250))
            image_arr = np.array(image)

            # Converting Image to Greyscale
            grey = cv2.cvtColor(image_arr, cv2.COLOR_BGR2GRAY)
            Image.fromarray(grey)

            # Blurring the Image
            blur = cv2.GaussianBlur(grey, (5,5), 0)
            Image.fromarray(blur)

            # Dilating the Image
            dilated = cv2.dilate(blur, np.ones((3,3)))
            Image.fromarray(dilated)

            # Morphology
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
            closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel) 
            Image.fromarray(closing)

            # Identifying the Cars
            cars = cv2.CascadeClassifier(os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/") + "/assets/models/haarcascade_car.xml").detectMultiScale(closing, 1.1, 1)

            for (x, y, w, h) in cars:
                cv2.rectangle(image_arr,(x,y),(x+w,y+h),(255,0,0),2)

                # Performing the User Function
                if ((function is not None) and (callable(function))):
                    function()

            # Displaying the Image
            cv2.imshow("Vehicle Detection - Cars", image_arr)
            cv2.waitKey(0)
        elif (fileType == "video"): # Video
            # Checking the Data Type, Length, and Content of "quit"
            if ((isinstance(quit, str) and len(quit) == 1 and quit.isalpha()) or (quit == None)):
                # Opening the Video
                video = cv2.VideoCapture(file_path)

                # Opening the Video and Processing
                while video.isOpened():
                    time.sleep(.05)

                    # Reading the First Frame
                    ret, frame = video.read()
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    # Identifying the Cars
                    cars = cv2.CascadeClassifier(os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/") + "/assets/models/haarcascade_car.xml").detectMultiScale(gray, 1.4, 2)

                    for (x,y,w,h) in cars:
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
                        cv2.imshow("Vehicle Detection - Cars", frame)

                        # Performing the User Function
                        if ((function is not None) and (callable(function))):
                            function()

                    # Closing the Video
                    if (quit == None):
                        # Clicking "q" Closes the Video
                        if cv2.waitKey(1) == ord("q"):
                            break
                    else:
                        # Clicking "quit" Closes the Video
                        if cv2.waitKey(1) == ord(quit):
                            break

                # Stopping OpenCV
                video.release()
                cv2.destroyAllWindows()
            else:
                raise TypeError("The 'quit' argument must be an alphabet of only length 1.")
        else:
            raise Exception("The file provided must be an image or a video.")
    else:
        raise FileNotFoundError("The file path doesn't exist.")