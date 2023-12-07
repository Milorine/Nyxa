import cv2
import numpy as np
import mss
import pygetwindow as gw
import pytesseract
from playsound import playsound
import time
from pathlib import Path
import random
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

prev_health_percentage = 0
username = 'PAIN'
lowhp = False
isdead = False
pings_speech = ['AVOID THIS AREA', 'ENEMY AUDIO', 'LOOTING THIS AREA', 'ATTACK HERE', "REGROUP HERE", 'DEFEND', 'WATCHING HERE', "SOMEONE'S BEEN HERE", 'You pinged a care package.', 'You - Ok.', 'NICE']
ping_speech_file = ['avoidThisArea', 'enemyAudio', 'lootingThisArea', 'attackHere', 'regroupHere', 'defendHere', 'watchingHere', "someone'sBeenHere", "supply", "okay", 'praise']
def resize_img(img, scale):

    width = int(img.shape[1] * scale / 100)
    height = int(img.shape[0] * scale / 100)

    dsize = (width, height)
    
    return cv2.resize(img, dsize=dsize)
    
def detect_text(frame, screensize):
    roi_x, roi_y, roi_w, roi_h = screensize
    croppedshot = frame[roi_y:roi_y + roi_h, roi_x:roi_x + roi_w]
    
    # Use pytesseract to perform OCR on the grayscale frame

    return pytesseract.image_to_string(croppedshot, lang='eng', config='--psm 6').strip()

def ping(frame):
    ping_coordinates = (830, 410, 260, 50)
    ping_text = detect_text(frame, ping_coordinates)
    if ping_text in pings_speech:
        speak_ping(ping_text)

def speak_ping(ping_text):
    index = pings_speech.index(ping_text)
    directory = Path(fr'mio_voice\{ping_speech_file[index]}')
    audio_file = random.choice(list(directory.glob('**/*'))).__str__()
    playsound(audio_file)
    time.sleep(2)

def playing(frame):
    username_coordinates = (182, 969, 40, 14)
    username_text = detect_text(frame, username_coordinates)
    return username_text == username

def spectate(frame):
    spectate_coordinates = (440, 20, 475, 60)
    spectate_text = detect_text(frame, spectate_coordinates)
    if 'SPECTATE' in spectate_text:  
        return True


def capture_screen():
    with mss.mss() as sct:
        # Capture a screenshot of the entire screen
        screenshot = sct.shot(output='numpy')

        # Read the screenshot using OpenCV
        frame = cv2.imread(screenshot)

        return frame


def dead_callout():
    global isdead
    if spectate(frame) and not isdead:
        directory = Path(fr'mio_voice\dead')
        audio_file = random.choice(list(directory.glob('**/*'))).__str__()
        playsound(audio_file)
        isdead = True
        time.sleep(5)

def low_callout():
    directory = Path(fr'mio_voice\lowhealth')
    audio_file = random.choice(list(directory.glob('**/*'))).__str__()
    playsound(audio_file)
    time.sleep(5)

def heald_callout():
    directory = Path(fr'mio_voice\healed')
    audio_file = random.choice(list(directory.glob('**/*'))).__str__()
    playsound(audio_file)
    time.sleep(5)

def detect_health_bar():
    global prev_health_percentage  # Use the global variable
    global lowhp
    global isdead

    # Extract the region of interest (ROI)

    roi_coordinates = (175, 1007, 245, 13)

    # Set the coordinates of the rectangle representing max HP (x, y, width, height)
    max_hp_coordinates = (175, 1007, 245, 13)

    # Set the missing percentage due to the slant
    missing_percentage = 10.6122
    roi_x, roi_y, roi_w, roi_h = roi_coordinates
    roi = frame[roi_y:roi_y + roi_h, roi_x:roi_x + roi_w]

    # Convert the ROI to grayscale
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to identify white regions
    _, thresholded_roi = cv2.threshold(gray_roi, 200, 255, cv2.THRESH_BINARY)

    # Count the number of white pixels in the health bar
    health_white_pixel_count = np.sum(thresholded_roi == 255)

    # Calculate the total number of pixels in the health bar
    total_health_pixels = roi_w * roi_h

    # Calculate the health percentage based on the number of white pixels
    health_percentage = (health_white_pixel_count / total_health_pixels) * 100 + missing_percentage

    # Adjust max HP to compensate for missing percentage
    max_hp_x, max_hp_y, max_hp_w, max_hp_h = max_hp_coordinates
    max_hp_pixels = max_hp_w * max_hp_h

    # Print the health percentage only when it changes significantly
    if abs(health_percentage - prev_health_percentage) > 1:
        if health_percentage < 60 and not lowhp:
            print(f"Health Percentage: {health_percentage}%")
            low_callout()
            prev_health_percentage = health_percentage
            lowhp = True
        elif health_percentage > 70 and lowhp:
            print(f"Health Percentage: {health_percentage}%")
            prev_health_percentage = health_percentage
            lowhp = False
    if health_percentage > 90:
        isdead = False
# Example usage:

while True:
    frame = capture_screen()
    playing(frame)
    if playing(frame):
        screensize = (0, 0, 1920, 1080)
        detect_health_bar()

        detect_text(frame, screensize)

        ping(frame)

        # Do something with the captured frame (e.g., display it)
    spectate(frame)
    dead_callout()
    cv2.imshow('Captured Screen', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
