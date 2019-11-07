class KittiBBox2D():
    """
    Kitti 2D Bounding Box
    """

    def __init__(self, x1, y1, x2, y2):
        """
        Initializes 2D Bounding Box
        :param x1: Bottom left x coordinate
        :param y1: Bottom left y coordinate
        :param x2: Top right x coordinate
        :param y2: Top right y coordinate
        """
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
