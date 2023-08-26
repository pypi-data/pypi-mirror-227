from mpmath import mp

def printpi():
    mp.dps = 1000  # Set the desired precision
    return str(mp.pi)