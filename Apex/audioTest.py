import cv2
import numpy as np
import mss
import pygetwindow as gw
import pytesseract
from playsound import playsound
import time
from pathlib import Path
import random


def low_callout():
    directory = Path(fr'mio_voice\attackhere')
    audio_file = random.choice(list(directory.glob('**/*'))).__str__()
    playsound(audio_file)
    time.sleep(2)


while True:
    low_callout()