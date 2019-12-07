class Object():
    """
    Object for 3D object detection
    """

    def __init__(self, class_id, bound_box2d, bound_box3d, track_id, score):
        """
        Initializes Object
        Args:
            class_id [int]: Object class ID
            bound_box2d [BoundBox2D]: 2D bounding box in pixel coordinates
            bound_box3d [BoundBox3D]: 3D bounding box in camera coordinates
            score [float]: Confidence score
        """
        self.class_id = class_id
        self.track_id = track_id
        self.bound_box2d = bound_box2d
        self.bound_box3d = bound_box3d
        self.score = score
