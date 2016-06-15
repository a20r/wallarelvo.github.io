
import cv2
import numpy as np
import numpy.linalg as lin
import scipy.interpolate as interp
import scipy.signal as sig
import scipy.io as sio
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from itertools import product


def derivative(im1, im2):
    fx, fy = np.gradient(im2)
    ft = im2 - im1
    return fx, fy, ft


def warp_flow(im, u, v):
    height, width = im.shape
    xx, yy = np.meshgrid(np.arange(width), np.arange(height))
    warped = np.zeros_like(im)
    pts = np.array(list(product(range(height), range(width))))
    warped[:, :] = interp.griddata(
        pts, im[:, :].flatten(), (yy + u, xx + v), method="cubic")
    return warped


def lk_pw(fx, fy, ft, i, j, ws):
    wfx = fx[i - ws:i + ws, j - ws:j + ws]
    wfy = fy[i - ws:i + ws, j - ws:j + ws]
    wft = ft[i - ws:i + ws, j - ws:j + ws]
    A = np.vstack((wfx.flatten(), wfy.flatten())).T
    b = -wft.flatten()
    try:
        return np.dot(np.dot(lin.inv(np.dot(A.T, A)), A.T), b)
    except:
        return np.zeros((2, 1))


def lk(im1, im2, ws=15, ms=15, N=3, u=None, v=None):
    height, width = im1.shape
    if u is None or v is None:
        u = np.zeros((height, width))
        v = np.zeros((height, width))
    im2w = im2.copy()
    for n in xrange(N):
        print n
        fx, fy, ft = derivative(im1, im2w)
        fx = cv2.blur(fx, (3, 3))
        fy = cv2.blur(fy, (3, 3))
        ft = cv2.blur(ft, (3, 3))
        for i in xrange(ws + 1, height - ws - 1):
            for j in xrange(ws + 1, width - ws - 1):
                V = lk_pw(fx, fy, ft, i, j, ws)
                u[i, j] = u[i, j] + V[0]
                v[i, j] = v[i, j] + V[1]
        im2w = warp_flow(im2w, u, v)
    u = sig.medfilt2d(u, ms)
    v = sig.medfilt2d(v, ms)
    return u, v, im2w


def build_pyramid(im, n_levels=4):
    cim = im.copy()
    ims = list()
    for n in xrange(n_levels):
        ims.append(cim.copy())
        cim = cv2.pyrDown(cim)
    return ims


def lk_pyr(im1, im2, n_levels=4, ws=15, ms=15, N=3):
    pyr1 = build_pyramid(im1, n_levels=n_levels)
    pyr2 = build_pyramid(im2, n_levels=n_levels)
    k = len(pyr1) - 1
    u = np.zeros_like(pyr1[k])
    v = np.zeros_like(pyr1[k])
    for i in xrange(len(pyr1)):
        u, v, im2w = lk(pyr1[k - i], pyr2[k - i],
                        N=N, ms=ms, ws=ws, u=u, v=v)
        u = cv2.pyrUp(u)
        v = cv2.pyrUp(v)
    return u, v, im2w


if __name__ == "__main__":
    im1 = cv2.imread("ps3_motion/car1.jpg", 0)
    im2 = cv2.imread("ps3_motion/car2.jpg", 0)
    im1 = cv2.resize(im1, None, fx=0.5, fy=0.5).astype("f")
    im2 = cv2.resize(im2, None, fx=0.5, fy=0.5).astype("f")
    u, v, im2w = lk_pyr(im1, im2, n_levels=4, ws=15, ms=11, N=2)
    plt.imshow(im2w, cmap=cm.gray)
    plt.show()
    sio.savemat("uv.mat", {"u": u, "v": v})
