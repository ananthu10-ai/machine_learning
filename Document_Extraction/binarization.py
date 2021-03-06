import numpy as np 
from PIL import Image 
import cv2
from scipy.ndimage import filters,interpolation,morphology

def pil2array(im):
    a= np.array(im)
    return a

def array2pil(im):
    return Image.fromarray(im)

def nlbin(im, threshold=0.5, zoom=0.5, escale=1.0, border=0.1, perc=80,
          range=20, low=5, high=90):
    """
    Performs binarization using non-linear processing.

    Args:
        im (PIL.Image):
        threshold (float):
        zoom (float): Zoom for background page estimation
        escale (float): Scale for estimating a mask over the text region
        border (float): Ignore this much of the border
        perc (int): Percentage for filters
        range (int): Range for filters
        low (int): Percentile for black estimation
        high (int): Percentile for white estimation

    Returns:
        PIL.Image containing the binarized image
    """
    raw = pil2array(im)
    # rescale image to between -1 or 0 and 1
    raw = raw/np.float(np.iinfo(raw.dtype).max)
    image = raw-np.amin(raw)
    image /= np.amax(image)

    m = interpolation.zoom(image, zoom)
    m = filters.percentile_filter(m, perc, size=(range, 2))
    m = filters.percentile_filter(m, perc, size=(2, range))
    m = interpolation.zoom(m, 1.0/zoom)
    w, h = np.minimum(np.array(image.shape), np.array(m.shape))
    flat = np.clip(image[:w, :h]-m[:w, :h]+1, 0, 1)

    # estimate low and high thresholds
    d0, d1 = flat.shape
    o0, o1 = int(border*d0), int(border*d1)
    est = flat[o0:d0-o0, o1:d1-o1]
    # by default, we use only regions that contain
    # significant variance; this makes the percentile
    # based low and high estimates more reliable
    v = est-filters.gaussian_filter(est, escale*20.0)
    v = filters.gaussian_filter(v**2, escale*20.0)**0.5
    v = (v > 0.3*np.amax(v))
    v = morphology.binary_dilation(v, structure=np.ones((int(escale * 50), 1)))
    v = morphology.binary_dilation(v, structure=np.ones((1, int(escale * 50))))
    est = est[v]
    lo = np.percentile(est.ravel(), low)
    hi = np.percentile(est.ravel(), high)

    flat -= lo
    flat /= (hi-lo)
    flat = np.clip(flat, 0, 1)
    bin = np.array(255*(flat > threshold), 'B')
    return array2pil(bin)
