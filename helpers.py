import threading

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def rgbTohue(r, g, b):
    X = 0.412453 * r + 0.357580 * g + 0.180423 * b
    Y = 0.212671 * r + 0.715160 * g + 0.072169 * b
    Z = 0.019334 * r + 0.119193 * g + 0.950227 * b
    x = X / (X + Y + Z)
    y = Y / (X + Y + Z)
    return [x, y]


def getValue(x):
    if x > 100:
        x = 100
    if x < 0:
        x = 0
    return int(254 * x / 100)
