import pyautogui
import time

# Run in a circle using wasd, 0.25 seconds per direction

while True:
    pyautogui.keyUp('a')
    time.sleep(0.25)
    pyautogui.keyDown('d')

    pyautogui.keyUp('w')
    time.sleep(0.25)
    pyautogui.keyDown('s')

    pyautogui.keyUp('d')
    time.sleep(0.25)
    pyautogui.keyDown('a')

    pyautogui.keyUp('s')
    time.sleep(0.25)
    pyautogui.keyDown('w')