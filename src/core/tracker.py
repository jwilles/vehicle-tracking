from .kf import KalmanFilter


class Tracker():
    """
        Global Tracking Manager
    """

    def __init__(self, kitti_frame_detections):
        """
        Initializes the Global Track Manager

        :param kitti_detections: kitti detections object
        """
        self.frame_detections = kitti_frame_detections
        self.num_frames = kitti_frame_detections.num_frames
        self.tracklets = []
        self.current_tracklets = []
        self.current_frame = 0

    def run(self):
        """
        Execute Tracking for each Kitti Sequence
        :return:
        """

        for i in range(self.num_frames + 1):
            self.current_frame = i
            current_object_detections = self.frame_detections[self.current_frame]

            matched_detections, unmatched_detections, \
                unmatched_tracklets = self.associate_detections(current_object_detections)

            self.update_matched_tracklets(matched_detections)
            self.destroy_unmatched_tracklets(unmatched_tracklets)
            self.create_tracklets_for_unmatched_detections(unmatched_detections)

            #object_predictions = self.get_predictions()

    def associate_detections(self, detections):
        if not self.current_tracklets:
            return [], detections, []

    def update_matched_tracklets(self, matched_detections):
        pass

    def destroy_unmatched_tracklets(self, unmatched_tracklets):
        pass

    def create_tracklets_for_unmatched_detections(self, umatched_detections):
        pass



class Tracklet():

    def __init__(self, detection, initial_frame):
        self.inital_frame = initial_frame
        self.state = [ detection ]
        self.kf = KalmanFilter()

    def get_predicted_state(self):
        pass

