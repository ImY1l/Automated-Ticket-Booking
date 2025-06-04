# 🎫 Automated Ticket Booking
This Python script automates the process of selecting seats on a web-based seat map by detecting seat colors using OpenCV and PyAutoGUI. It is highly customizable—just update the color ranges to match your seat map!

## ⚙️ Usage
Use this script when you are trying to buy tickets for high-demand events where seats sell out within seconds. The script will automatically and instantly select available seats as soon as they appear, giving you a better chance to secure tickets faster than manual clicking. The script captures a the seat map and converts it to HSV color space. It then applies predefined HSV ranges to create masks for the target seat colors.

## 🔧 Prerequisites
- OpenCV `pip install opencv-python`
- NumPy `pip install numpy`
- PyAutoGUI `pip install pyautogui`
- Pillow `pip install pillow`

## 🚀 Run Locally
1- Clone the repository
```bash
git clone https://github.com/ImY1l/Automated-Ticket-Booking.git
cd Automated-Ticket-Booking
```
2- Configure Color Ranges
```python
# If your sampled HSV is (62, 150, 163):
lower = np.array([60, 135, 140])
upper = np.array([65, 170, 180])
```
  > you can add more then one range
3- Run
```bash
python webook.py
```
