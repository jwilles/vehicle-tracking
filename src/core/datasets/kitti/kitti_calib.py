import numpy as np

from src.core.utils.calib.camera_calib import CameraCalib


class KittiCalib:
    """Kitti Calibration

    Fields:
        p0-p3: (3, 4) Camera calibration parameters. Contains extrinsic and intrinsic parameters.
        r0_rect: (3, 3) Rectification matrix
        velo_to_cam: (3, 4) Transformation matrix from velodyne to cam coordinate
            Point_Camera = P_cam * R0_rect * Tr_velo_to_cam * Point_Velodyne
    """

    def __init__(self, calib_file):
        """
        Initializes calibration from a file path
        Args:
            calib_file: Calibration file path
        """
        self.r0_rect = []
        self.velo_to_cam = []

        # Read file
        with open(calib_file, 'r') as file:
            lines = file.readlines()

        p_all = []
        for i in range(4):
            p = lines[i].strip().split(' ')
            p = p[1:]
            p = [float(p[i]) for i in range(len(p))]
            p = np.reshape(p, (3, 4))
            p_all.append(p)

        self.p0 = CameraCalib(p_all[0])
        self.p1 = CameraCalib(p_all[1])
        self.p2 = CameraCalib(p_all[2])
        self.p3 = CameraCalib(p_all[3])

        # Read in rectification matrix
        tr_rect = lines[4].strip().split(' ')
        tr_rect = tr_rect[1:]
        tr_rect = [float(tr_rect[i]) for i in range(len(tr_rect))]
        self.r0_rect = np.reshape(tr_rect, (3, 3))

        # Read in velodyne to cam matrix
        tr_v2c = lines[5].strip().split(' ')
        tr_v2c = tr_v2c[1:]
        tr_v2c = [float(tr_v2c[i]) for i in range(len(tr_v2c))]
        self.velo_to_cam = np.reshape(tr_v2c, (3, 4))
