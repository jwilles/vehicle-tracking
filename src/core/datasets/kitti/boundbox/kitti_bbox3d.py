class KittiBBox3D():
    """
    Kitti 3D Bounding Box
    """

    def __init__(self, x, y, z, length, width, height, theta):
        """
        Initializes 3D Bounding Box
        :param x: Centroid x coordinate
        :param y: Centroid y coordinate
        :param z: Centroid z coordinate
        :param length: Z axis dimension of the bounding box
        :param width: X axis dimension of the bounding box
        :param height: Y axis dimension of the bounding box
        :param theta: Orientation heading about the Y axis
        """
        self.x = x
        self.y = y
        self.z = z
        self.length = length
        self.width = width
        self.height = height
        self.theta = theta
