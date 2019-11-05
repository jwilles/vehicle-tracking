from src.core.datasets.kitti import kitti_detections


class Tracker():
    """
        Global Tracking Manager
    """

    def __init__(self, kitti_detections):
        