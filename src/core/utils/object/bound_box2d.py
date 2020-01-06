class BoundBox2D:
    """
    2D Bounding Box in image space
    """

    def __init__(self, u1, v1, u2, v2):
        """
        Initializes 2D Bounding Box
        Args:
            u1: Bottom left x coordinate
            v1: Bottom left y coordinate
            u2: Top right x coordinate
            v2: Top right y coordinate
        """
        self.u1 = u1
        self.v1 = v1
        self.u2 = u2
        self.v2 = v2

    def get_coords_UVUV(self):
        return self.u1, self.v1, self.u2, self.v2

    def get_coords_UVWH(self):
        w = self.u2 - self.u1
        h = self.v2 - self.v1

        return self.u1, self.v1, w, h
