def sort_from_top(list):
    list.sort(key=get_y)

def get_y(box):
    return box[0][0][1]

def get_x(box):
    return box[0][0][0]

def same_column(box1, box2, tolerance=10):
    if isinstance(box1,tuple):
        box1 = box1[0]
    if isinstance(box2,tuple):
        box2 = box2[0]

    # box = [x1, y1, x2, y2]
    [x1_min,_], _, [x1_max,_], _ = box1
    [x2_min,_], _, [x2_max,_], _ = box2

    # Check if x ranges overlap (with optional tolerance)
    return max(x1_min, x2_min) <= min(x1_max, x2_max) + tolerance

def same_row(box1, box2, tolerance=10):
    # box = [x1, y1, x2, y2]
    _, y1_min, _, y1_max= box1
    _, y2_min, _, y2_max= box2

    # Check if y ranges overlap (with optional tolerance)
    return max(y1_min, y2_min) <= min(y1_max, y2_max) + tolerance