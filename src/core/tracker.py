
class Tracker():
    """
        Global Tracking Manager
    """

    def __init__(self, kitti_frame_detections):
        """
        Initializes the Global Track Manager

        :param kitti_detections: kitti detections object
        """
        self.frame_detections = kitti_detections
        self.max_frame = length(kitti_detections)
        self.tracklets = []
        self.current_tracklets = []

    def run(self):
        """
        Execute Tracking for each Kitti Sequence
        :return:
        """

        for i in range(self.max_frame):
            current_object_detections = self.detections[i]

            matched_detections, unmatched_detections, unmatched_tracklets = associate_detections(current_object_detections)

            s



            object_predictions = self.get_predictions()

    def associate_detections(self, detections):


    def get_predictions(self):
        return [ tracklet.get_predicted_state for tracklet in self.current_tracklets ]
        for tracklet in self.current_tracklets:
            tracklet.get_predicted_state


class Tracklet():

    def __init__(self):
        pass

    def get_predicted_state(self):
