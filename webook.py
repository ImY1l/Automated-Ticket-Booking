import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab
import time

# === CONFIGURATION ===
COLOR_RANGES = [
    # Color 1 range (blueish)
    (np.array([100, 120, 40]), np.array([115, 255, 200])),
    # Color 2 range (red/pink)
    (np.array([160, 200, 50]), np.array([170, 255, 255])),
    # Color 3 range (yellow/orange)
    (np.array([20, 150, 0]), np.array([35, 255, 230])),
    # Color 4 range (green)
    (np.array([45, 100, 30]), np.array([75, 255, 180])),
]

CHECK_INTERVAL = 0.2
ZOOM_DELAY = 0.2
DIST_THRESHOLD = 20
SEATS_TO_SELECT = 3
NO_SEAT_TIMEOUT = 2.0

print("Move your mouse to the TOP-LEFT corner of the seat map and press Enter.")
input()
x1, y1 = pyautogui.position()
print(f"Top-left: {x1}, {y1}")

print("Move your mouse to the BOTTOM-RIGHT corner of the seat map and press Enter.")
input()
x2, y2 = pyautogui.position()
print(f"Bottom-right: {x2}, {y2}")

print("Move your mouse over the 'Next: checkout' button and press Enter.")
input()
btn_x, btn_y = pyautogui.position()
print(f"'Next: checkout' button at: {btn_x}, {btn_y}")

print(f"Starting live seat sniping for up to {SEATS_TO_SELECT} tickets of any of the 4 colors. Press Ctrl+C to stop.")

def find_seats(exclude_list=[]):
    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    img_np = np.array(img)
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    mask_total = np.zeros(img_hsv.shape[:2], dtype=np.uint8)
    for lower, upper in COLOR_RANGES:
        mask = cv2.inRange(img_hsv, lower, upper)
        mask_total = cv2.bitwise_or(mask_total, mask)
    contours, _ = cv2.findContours(mask_total, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    seat_positions = []
    for cnt in sorted(contours, key=lambda c: (cv2.boundingRect(c)[1], cv2.boundingRect(c)[0])):
        (x, y, w, h) = cv2.boundingRect(cnt)
        cx = x + w // 2
        cy = y + h // 2
        screen_x = x1 + cx
        screen_y = y1 + cy
        if all((screen_x - ex[0])**2 + (screen_y - ex[1])**2 > DIST_THRESHOLD**2 for ex in exclude_list):
            seat_positions.append((screen_x, screen_y))
    return seat_positions

try:
    selected_seats = []
    seats_selected = 0

    # --- FIRST SEAT: double-click (zoom + confirm) ---
    while True:
        seats = find_seats(selected_seats)
        if seats:
            first_seat = seats[0]
            print(f"First seat at {first_seat}, clicking to zoom...")
            pyautogui.moveTo(first_seat[0], first_seat[1], duration=0.1)
            pyautogui.click()
            time.sleep(ZOOM_DELAY)
            seats_zoomed = find_seats(selected_seats)
            if seats_zoomed:
                confirm_seat = min(seats_zoomed, key=lambda p: (p[0]-first_seat[0])**2 + (p[1]-first_seat[1])**2)
                print(f"Confirming first seat at {confirm_seat}...")
                pyautogui.moveTo(confirm_seat[0], confirm_seat[1], duration=0.1)
                pyautogui.click()
                selected_seats.append(confirm_seat)
                seats_selected += 1
                print("First seat selected and confirmed.")
                time.sleep(0.2)
                break
            else:
                print("Could not confirm first seat after zoom. Retrying...")
                time.sleep(CHECK_INTERVAL)
        else:
            print("No seat found. Waiting...")
            time.sleep(CHECK_INTERVAL)

    # --- SECOND AND THIRD SEATS: single click ---
    no_seat_start = time.time()
    while seats_selected < SEATS_TO_SELECT:
        seats = find_seats(selected_seats)
        if seats:
            next_seat = seats[0]
            print(f"Seat at {next_seat}, clicking to select...")
            pyautogui.moveTo(next_seat[0], next_seat[1], duration=0.1)
            pyautogui.click()
            selected_seats.append(next_seat)
            seats_selected += 1
            print(f"Seat {seats_selected} selected.")
            time.sleep(0.2)
            no_seat_start = time.time()
        else:
            print("No more seats found. Waiting...")
            time.sleep(CHECK_INTERVAL)
            if time.time() - no_seat_start > NO_SEAT_TIMEOUT:
                print(f"No new seat found for {NO_SEAT_TIMEOUT} seconds. Proceeding to checkout.")
                break

    # --- CHECKOUT ---
    pyautogui.moveTo(btn_x, btn_y, duration=0.2)
    pyautogui.click()
    print("Clicked 'Next: checkout' button.")

except KeyboardInterrupt:
    print("Stopped by user.")

print("Automation complete. Please check your browser.")
