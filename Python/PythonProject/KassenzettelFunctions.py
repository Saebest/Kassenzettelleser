def sort_from_top(list):
    list.sort(key=get_y)

def get_y(box):
    return box[0][0][1]

def get_x(box):
    return box[0][0][0]

def same_column(box1, box2, tolerance=1):
    if isinstance(box1,tuple):
        box1 = box1[0]
    if isinstance(box2,tuple):
        box2 = box2[0]

    # box = [x1, y1, x2, y2]
    [x1_min,_], _, [x1_max,_], _ = box1
    [x2_min,_], _, [x2_max,_], _ = box2

    # Check if x ranges overlap (with optional tolerance)
    return max(x1_min, x2_min) <= min(x1_max, x2_max) + tolerance

def same_row(box1, box2):
    # box = [x1, y1, x2, y2]
    y1 = box1[0][0][1]
    y2 = box2[0][0][1]

    #half line height
    tolerance = abs( box1[0][0][1] - box1[0][2][1])/3

    # Check if y ranges overlap (with optional tolerance)
    return abs(y1 - y2) < tolerance