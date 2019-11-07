class KittiLabel():
    """ Kitti 3D Object Detection Label """

    def __init__(self, params):
        """
        Initializes parameters
        """
        self.frame = params["frame"]
        self.type = params["type"]
        self.bbox2d = params["bbox2d"]  # 2D bounding box in pixel coordinates [px]
        self.bbox3d = params["bbox3d"]  # 3D bounding box in camera coordinates [m,rad]
        self.alpha = params["alpha"]
        self.score = params["score"]
