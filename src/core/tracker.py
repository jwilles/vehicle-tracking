
class Tracker():
    """
        Global Tracking Manager
    """

    def __init__(self, kitti_detections):
        """
        Initializes the Global Track Manager

        :param kitti_detections: kitti detections object
        """
        self.detections = kitti_detections

    def run(self):
        """
        Execute Tracking for each Kitti Sequence

        :return:
        """
        


class Tracklet():

    def __init__(self):