import numpy as np


class CameraCalib:
    """
    Camera Calibration
    Fields:
        p: (3, 4) Camera P matrix. Contains extrinsic and intrinsic parameters.
    """

    def __init__(self, p):
        self.p = p

    def project_points3d_to_image(self, points3d):
        """Projects set of 3D points to 2D points in image space

        Args:
            points3d: (3, N) 3D points

        Returns:
            pts_2d: (2, N) projected coordinates [u, v] of the 3D points in image space
        """
        pc_padded = np.append(points3d, np.ones((1, points3d.shape[1])), axis=0)
        pts_2d = np.dot(self.p, pc_padded)

        pts_2d[0:2] = pts_2d[0:2] / pts_2d[2]
        return pts_2d[0:2]
