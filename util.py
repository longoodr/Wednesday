import numpy as np

def get_min_max_tuple(data):
    lo = np.amin(data)
    hi = np.amax(data)
    return lo, hi

def get_scaled_num(num, min_, max_):
    return (num - min_) / (max_ - min_)

# Scales point to have coords lie within [0, 1].
def get_scaled_pt(txy_pt, max_t, min_x, max_x, min_y, max_y):
    gsn = get_scaled_num
    (t, (x, y)) = txy_pt
    return (gsn(t, 0, max_t), (gsn(x, min_x, max_x), gsn(y, min_y, max_y)))

# Takes normalized point and upscales it to given bounds,where 0 is min and 1 is max.
def get_upscaled_pt(xy_pt, x0, x1, y0, y1):
    return ( x0 + xy_pt[0] * (x1 - x0), y0 + xy_pt[1] * (y1 - y0) )

def norm_to_pixel_space(xy_pt, size):
    (w, h) = size
    return (xy_pt[0] * w, xy_pt[1] * h)

def flip_pt_vertically(xy_pt):
    return (xy_pt[0], 1 - xy_pt[1])

def flip_pt_horizontally(xy_pt):
    return (1 - xy_pt[0], xy_pt[1])