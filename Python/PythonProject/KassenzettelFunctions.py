import cv2
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