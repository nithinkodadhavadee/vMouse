import pyautogui
import time

# pyautogui.click(1000, 100)
pyautogui.moveTo(1930, 100)
time.sleep(1)
pyautogui.moveRel(100, 10)  # move mouse 10 pixels down
# pyautogui.dragTo(1930, 150)
# pyautogui.dragRel(0, 10)  # drag mouse 10 pixels down
wScr, hScr = pyautogui.size()
print(wScr, hScr)