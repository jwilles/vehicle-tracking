import numpy as np
from .tracklet import Tracklet
from .associator import TrackletAssociator

class Tracker():
    """ Global Tracking Manager """

    def __init__(self, kitti_frame_detections):
        """
        Initializes the Global Track Manager

        :param kitti_detections: kitti detections object
        """
        self.frame_detections = kitti_frame_detections
        self.num_frames = kitti_frame_detections.num_frames
        self.tracklet_history = []
        self.current_detections = []
        self.current_tracklets = []
        self.current_frame_idx = 0
        self.tracklet_associator = TrackletAssociator()

    def run(self):
        """
        Execute Tracking for each Kitti Sequence
        :return:
        """

        for i in range(2): #range(self.num_frames + 1):
            self.current_frame_idx = i
            self.get_current_detections()
            self.propogate_tracklets()

            self.tracklet_associator.associate_detections(self.current_detections, self.current_tracklets)

            self.destroy_unmatched_tracklets(self.tracklet_associator.unmatched_tracklets)
            self.update_matched_tracklets(self.tracklet_associator.matched_detections)
            self.create_tracklets_for_unmatched_detections(self.tracklet_associator.unmatched_detections)

            #print(self.current_tracklets)

    def get_current_detections(self):
        self.current_detections = self.frame_detections[self.current_frame_idx]

    def propogate_tracklets(self):
        for tracklet in self.current_tracklets:
            tracklet.update_prediction()

    def update_matched_tracklets(self, matched_detections):
        print(matched_detections)
        
    def destroy_unmatched_tracklets(self, unmatched_tracklets):
        for tracklet in unmatched_tracklets:
            self.tracklet_history.append(tracklet)
            self.current_tracklets = [x for x in self.current_tracklets if x.id != tracklet.id]

    def create_tracklets_for_unmatched_detections(self, unmatched_detections):
        for detection in unmatched_detections:
            self.current_tracklets.append(Tracklet(detection, self.current_frame_idx))
