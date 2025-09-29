import cv2
import numpy as np
def sort_from_top(list):
    return list.sort(key=get_y)

def get_y(item):
    return int(item[0][0][1])

def get_x(item):
    return item[0][0][0]

def get_height(item):
    # [[top-left], [top-right], [bottom-right], [bottom-left]]
    y_top = item[0][0][1]
    y_bot = item[0][3][1]
    return abs(y_bot-y_top)

def same_column(item1, item2, tolerance=1):
    if isinstance(item1,tuple):
        item1 = item1[0]
    if isinstance(item2,tuple):
        item2 = item2[0]

    # box = [x1, y1, x2, y2]
    [x1_min,_], _, [x1_max,_], _ = item1
    [x2_min,_], _, [x2_max,_], _ = item2

    # Check if x ranges overlap (with optional tolerance)
    return max(x1_min, x2_min) <= min(x1_max, x2_max) + tolerance

def same_row(item1, item2) :
   # [[top-left], [top-right], [bottom-right], [bottom-left]]
    y1 = item1[0][0][1]
    y2 = item2[0][0][1]

    tolerance = abs(item1[0][0][1] - item1[0][3][1])/2

    # Check if y ranges overlap (with optional tolerance)
    return abs(y1 - y2) < tolerance

def other_items_within_range(list,item,range):
    indexOfItem = list.index(item)
    i = indexOfItem-range
    output=[]
    while i <= (indexOfItem + range):
        if 0 <= i < len(list) and not i == indexOfItem:
            output.append(list[i])

        i += 1
    return output

def resize_image(image,max_size = False):
    new_width = min(max_size, image.shape[1]) if max_size else image.shape[1]
    ratio = new_width / image.shape[1]
    new_height = int(image.shape[0] * ratio)
    return cv2.resize(image, (new_width, new_height))

def make_image_better(img):
    # --- Step 1: Normalize blue background to white ---
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    img[mask_blue > 0] = (255, 255, 255)

    # --- Step 2: Grayscale ---
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # --- Step 3: Adaptive threshold (works locally, not globally) ---
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 10
    )
    # Invert: text = white, background = black (needed for connectedComponents)
    thresh_inv = cv2.bitwise_not(thresh)

    # Connected component analysis
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh_inv, connectivity=8)

    # Create mask keeping components larger than a threshold
    clean_mask = np.zeros_like(thresh_inv)

    for i in range(1, num_labels):  # skip background
        if stats[i, cv2.CC_STAT_AREA] > 30:  # tweak this value
            clean_mask[labels == i] = 255

    # Invert back to text = black, background = white
    clean = cv2.bitwise_not(clean_mask)
    cv2.imwrite("cleaned.png", clean)
    clean = cv2.bitwise_not(thresh)
    return clean
