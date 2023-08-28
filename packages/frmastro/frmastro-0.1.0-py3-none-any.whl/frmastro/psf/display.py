import matplotlib.pyplot as plt
import matplotlib.colors as mcolor
import numpy as np


def disp(img, norm=None, pct=.5):
    """Display an image"""

    vmin, vmax = np.percentile(img.flatten(), [pct, 100-pct])
    norm = norm or mcolor.Normalize(vmin, vmax)

    plt.imshow(
        img,
        cmap=plt.cm.YlGnBu_r,
        origin="lower",
        interpolation="nearest",
        norm = norm,
    )


