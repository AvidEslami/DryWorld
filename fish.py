import mss
import pyautogui
import time

pyautogui.FAILSAFE = True

# Your exact target data
TARGET_X = 973
TARGET_Y = 399

TARGET_R = 234
TARGET_G = 199
TARGET_B = 44

SECOND_TARGET_R = 223
SECOND_TARGET_G = 225
SECOND_TARGET_B = 234

THIRD_TARGET_R = 128
THIRD_TARGET_G = 135
THIRD_TARGET_B = 158

# A tiny tolerance for slight lighting variations
TOLERANCE = 1

def exact_pixel_bot():
    # Define a 1x1 pixel bounding box
    # region = {"top": TARGET_Y-1, "left": TARGET_X-1, "width": 2, "height": 2}
    region = {"top": TARGET_Y-0, "left": TARGET_X-0, "width": 1, "height": 1}
    
    with mss.mss() as sct:
        print(f"Scanning exactly at X: {TARGET_X}, Y: {TARGET_Y}...")
        print("Bot active. Move physical mouse to a corner to abort.")
        
        while True:
            # Grab just that single pixel
            img = sct.grab(region)
            
            # mss has a built-in method to get the RGB of a pixel in the grabbed region
            # Since our region is 1x1, the coordinates inside it are just (0, 0)
            for x in range(region["width"]):
                for y in range(region["height"]):

                    r, g, b = img.pixel(x, y)
                    # print(f"Scanned color: ({r}, {g}, {b})")
                    # Check if the colors match
                    if (abs(r - TARGET_R) <= TOLERANCE and 
                        abs(g - TARGET_G) <= TOLERANCE and 
                        abs(b - TARGET_B) <= TOLERANCE):
                        
                        print(f"Found color ({r}, {g}, {b})! Right-clicking.")
                        pyautogui.rightClick()
                        time.sleep(1) # Sleep for a second so it doesn't click multiple times immediately
                        pyautogui.rightClick()
                        # Sleep for a second so it doesn't
                    elif (abs(r - SECOND_TARGET_R) <= TOLERANCE and 
                        abs(g - SECOND_TARGET_G) <= TOLERANCE and 
                        abs(b - SECOND_TARGET_B) <= TOLERANCE):
                        
                        print(f"Found color ({r}, {g}, {b})! Right-clicking.")
                        pyautogui.rightClick()
                        time.sleep(1) # Sleep for a second so it doesn't click multiple times immediately
                        pyautogui.rightClick()
                        # Sleep for a second so it doesn't
                    elif (abs(r - THIRD_TARGET_R) <= TOLERANCE and
                        abs(g - THIRD_TARGET_G) <= TOLERANCE and 
                        abs(b - THIRD_TARGET_B) <= TOLERANCE):
                        
                        print(f"Found color ({r}, {g}, {b})! Right-clicking.")
                        pyautogui.rightClick()
                        time.sleep(1) # Sleep for a second so it doesn't click multiple times immediately
                        pyautogui.rightClick()
                        # Sleep for a second so it doesn't
                    # sleep briefly to minimize cpu strain
            time.sleep(0.1)

if "__main__" == __name__:
    exact_pixel_bot()