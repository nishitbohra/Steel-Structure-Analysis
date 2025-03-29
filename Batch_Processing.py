import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

output_folder = "C:/Users/Kanchan/Desktop/Steel Analysis/processed_images"
os.makedirs(output_folder, exist_ok=True)

image_paths = [
    "C:/Users/Kanchan/Desktop/Steel Analysis/Dataset/np/IMG20240615103626.jpg",
    "C:/Users/Kanchan/Desktop/Steel Analysis/Dataset/np/IMG20240615103628.jpg",
    "C:/Users/Kanchan/Desktop/Steel Analysis/Dataset/np/IMG20240615103634.jpg",
    "C:/Users/Kanchan/Desktop/Steel Analysis/Dataset/np/IMG20240615103636.jpg",
    "C:/Users/Kanchan/Desktop/Steel Analysis/Dataset/np/IMG20240615103644.jpg",
    "C:/Users/Kanchan/Desktop/Steel Analysis/Dataset/np/IMG20240615103646.jpg",
    "C:/Users/Kanchan/Desktop/Steel Analysis/Dataset/np/IMG20240615103650.jpg",
    "C:/Users/Kanchan/Desktop/Steel Analysis/Dataset/np/IMG20240615103719.jpg",
    "C:/Users/Kanchan/Desktop/Steel Analysis/Dataset/np/IMG20240615103722.jpg",
    "C:/Users/Kanchan/Desktop/Steel Analysis/Dataset/np/IMG20240615103732.jpg"
]

for image_path in image_paths:

    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced_gray = clahe.apply(gray)

    thresh = cv2.adaptiveThreshold(
        enhanced_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 31, 5  
    )

    kernel = np.ones((3, 3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filtered_contours = [cnt for cnt in contours if 30 < cv2.contourArea(cnt) < 1000]

    mask = np.zeros_like(gray)
    cv2.drawContours(mask, filtered_contours, -1, (255), thickness=cv2.FILLED)

    output = image.copy()
    output[mask == 255] = [0, 255, 0]  

    filename = os.path.basename(image_path)
    output_path = os.path.join(output_folder, f"processed_{filename}")
    cv2.imwrite(output_path, output)

    print(f"Processed image saved: {output_path}")

plt.figure(figsize=(6, 6))
plt.imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
plt.title("Processed Image (Last in Batch)")
plt.axis("off")
plt.show()
