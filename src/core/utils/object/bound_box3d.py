import numpy as np


class BoundBox3D:
    """
    3D Bounding Box in world space
    """

    def __init__(self, x, y, z, x_dim, y_dim, z_dim, theta):
        """
        Initializes 3D Bounding Box.
        Note:
            Reference frame follows KITTI convention, with reference point centered on bottom
            face of the box. x - Right, y - Down, Z - forward.
        Args:
            x: X coordinate
            y: Y coordainate
            z: Z coordinate
            x_dim: Box dimension in x axis
            y_dim: Box dimension in y axis
            z_dim: Box dimenxion in z axis
            theta: Orientation heading about the Y axis
        """
        self.x = x
        self.y = y
        self.z = z
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.z_dim = z_dim
        self.theta = theta

    def get_corners_3d(self):
        """
        Gets the 3D corners in world space
        """

        # 3D Bounding Box corners according to KITTI convention
        x_corners = self.x_dim * \
            np.array([1 / 2, 1 / 2, -1 / 2, -1 / 2, 1 / 2, 1 / 2, -1 / 2, -1 / 2])
        y_corners = self.y_dim * np.array([0, 0, 0, 0, -1, -1, -1, -1])
        z_corners = self.z_dim * \
            np.array([1 / 2, -1 / 2, -1 / 2, 1 / 2, 1 / 2, -1 / 2, -1 / 2, 1 / 2])
        ones = np.ones(8)

        # compute transformation matrix
        trans = np.array([[+np.cos(self.theta), 0, +np.sin(self.theta), self.x],
                          [0, 1, 0, self.y],
                          [-np.sin(self.theta), 0, +np.cos(self.theta), self.z],
                          [0, 0, 0, 1]])

        # Apply transformation
        corners_3d = np.dot(trans, np.array([x_corners, y_corners, z_corners, ones]))

        # Remove padding row
        return corners_3d[0:-1, :]
