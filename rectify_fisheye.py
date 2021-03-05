import numpy as np
import cv2
import math
import yaml

def load_calib(calib_file):
    with open(calib_file) as f:
        doc= yaml.full_load(f)
    xi = doc["mirror_parameters"]["xi"]
    fx = doc["projection_parameters"]["gamma1"]
    fy = doc["projection_parameters"]["gamma2"]
    cx = doc["projection_parameters"]["u0"]
    cy = doc["projection_parameters"]["v0"]
    k1 = doc["distortion_parameters"]["k1"]
    k2 = doc["distortion_parameters"]["k2"]
    p1 = doc["distortion_parameters"]["p1"]
    p2 = doc["distortion_parameters"]["p2"]

    K = np.matrix([[fx, 0, cx], [0, fy, cy], [0, 0, 1]], dtype=float)
    return K, xi, k1, k2


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser("Rectify fisheye image to get side rectified image")
    parser.add_argument("--front_img", type=str, required=True, help='target image')
    parser.add_argument("--back_img", type=str, required=True, help='target image')
    parser.add_argument("--front_calib", type=str, required=True, help="camera calibration file for mei camera model")
    parser.add_argument("--back_calib", type=str, required=True, help="camera calibration file for mei camera model")

    args = parser.parse_args()

    K_front, xi_front, k1_front, k2_front = load_calib(args.front_calib)
    K_back, xi_back, k1_back, k2_back = load_calib(args.back_calib)

    # define image spec to be generated
    w_sp = 1000
    h_sp = 500

    rot = np.matrix([[math.cos(math.pi), 0, math.sin(math.pi)], [0, 1, 0], [-math.sin(math.pi), 0, math.cos(math.pi)]], dtype=float)

    frame_front = cv2.imread(args.front_img)
    frame_back = cv2.imread(args.back_img)
    h, w, c = frame_front.shape

    frame_sp = np.zeros((h_sp, w_sp, c), dtype=frame_front.dtype)

    # build conversion map
    convert_map = dict()
    for i in range(h_sp):
        for j in range(w_sp):
            theta = (-180.0+360.0/w_sp*j)*math.pi/180.0;
            phi = (-90.0+180.0/h_sp*i)*math.pi/180.0;
            r = 1.0

            xs = np.matrix([r*math.cos(phi)*math.sin(theta), r*math.sin(phi), r*math.cos(phi)*math.cos(theta)], dtype=float).transpose()
            if xs[2] >= 0:
                K = K_front
                k1 = k1_front
                k2 = k2_front
                xi = xi_front
                is_front = True
            else:
                K = K_back
                k1 = k1_back
                k2 = k2_back
                xi = xi_back
                is_front = False

            xs /= np.linalg.norm(xs)
            if not is_front:
                xs = rot*xs

            norm_xs = math.sqrt(math.pow(xs[0], 2) + math.pow(xs[1], 2) + math.pow(xs[2], 2))
            m = np.transpose(np.matrix([xs[0, 0]/(xs[2, 0]+xi*norm_xs), xs[1, 0]/(xs[2, 0]+xi*norm_xs), 1.0], dtype=float))
            r = math.sqrt(m[0, 0]*m[0, 0] + m[1, 0]*m[1, 0])
            d = (1.0+k1*math.pow(r, 2)+k2*math.pow(r, 4))
            m[0, 0] = m[0, 0]*d
            m[1, 0] = m[1, 0]*d
            m_proj = K*m
            u = int(round(m_proj[0, 0]/ m_proj[2, 0]))
            v = int(round(m_proj[1, 0]/ m_proj[2, 0]))

            convert_map[(i, j)] = (v, u, is_front)

    # assign pixel value to image
    for i in range(h_sp):
        for j in range(w_sp):
            v, u, is_front = convert_map[(i, j)]
            if u < 0 or u > w-1 or v < 0 or v > h-1:
                continue
            if is_front:
                frame_sp[i, j, :] = frame_front[v, u, :]
            else:
                frame_sp[i, j, :] = frame_back[v, u, :]

    cv2.imshow("Front Image", frame_front)
    cv2.imshow("Back Image", frame_back)
    cv2.imshow("sp Image", frame_sp)
    cv2.imwrite("spherical_image.jpg", frame_sp)
    key = cv2.waitKey(0)

