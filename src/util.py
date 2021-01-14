import numpy as np

def get_scaled_num(num, min_, max_):
    return (num - min_) / (max_ - min_)

def get_scaled_pt(datapoint, max_t, min_x, max_x, min_y, max_y):
    gsn = get_scaled_num
    (t, (x, y)) = datapoint
    return (gsn(t, 0, max_t), (gsn(x, min_x, max_x), gsn(y, min_y, max_y)))

def get_min_max_tuple(data):
    lo = np.amin(data)
    hi = np.amax(data)
    return lo, hi