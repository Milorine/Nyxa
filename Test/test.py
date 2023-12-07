import cv2
import numpy as np
import mss
import pygetwindow as gw
import pytesseract
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


def detect_text(frame, screensize):
    roi_x, roi_y, roi_w, roi_h = screensize
    croppedshot = frame[roi_y:roi_y + roi_h, roi_x:roi_x + roi_w]
    

    # Use pytesseract to perform OCR on the grayscale frame
    custom_config = r'--oem 3 --psm 6'  # You can adjust OCR settings as needed
    return pytesseract.image_to_string(croppedshot, config=custom_config)


def ping(frame):
    ping_coordinates = ((0,0), (0,0))
    ping_text = detect_text(frame, ping_coordinates)
    print("Ping Text:", ping_text)


def low_callout(health_percentage):
    if health_percentage < 30:
        print("I'm low!")



def detect_health_bar(roi_coordinates, max_hp_coordinates, missing_percentage):
    with mss.mss() as sct:

        prev_health_percentage = 0
        screensize = (0, 0, 1920, 1080)
        while True:
            # Capture a screenshot of the screen
            screenshot = sct.shot()

            # Read the screenshot using OpenCV
            frame = cv2.imread(screenshot)

            # Extract the region of interest (ROI)
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
            health_percentage = (health_white_pixel_count / total_health_pixels) * 100

            # Adjust max HP to compensate for missing percentage
            max_hp_x, max_hp_y, max_hp_w, max_hp_h = max_hp_coordinates
            max_hp_pixels = max_hp_w * max_hp_h

            # Draw a rectangle representing max HP on the frame
            cv2.rectangle(frame, (max_hp_x, max_hp_y), (max_hp_x + max_hp_w, max_hp_y + max_hp_h), (0, 0, 255), 2)

            # Print the health percentage only when it changes significantly
            if abs(health_percentage - prev_health_percentage) > 1:
                if health_percentage > 85:
                    health_percentage += missing_percentage
                    print(f"Health Percentage: {health_percentage}%")
                else:
                    print(f"Health Percentage: {health_percentage}%")
                low_callout(health_percentage)
                prev_health_percentage = health_percentage

            # Call the detect_text and ping functions with the screenshot
            detect_text(frame, screensize)  # Adjust ping region coordinates

            # Display the frame with the drawn rectangle
            cv2.imshow('Frame with Rectangle', frame)

            # Break the loop if 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Set the coordinates of the region where the health bar is expected (x, y, width, height)
    roi_coordinates = (175, 1007, 245, 13)

    # Set the coordinates of the rectangle representing max HP (x, y, width, height)
    max_hp_coordinates = (175, 1007, 245, 13)

    # Set the missing percentage due to the slant
    missing_percentage = 10.6122

    detect_health_bar(roi_coordinates, max_hp_coordinates, missing_percentage)

