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
        for i in range(self.num_frames + 1): #range(2): #range(self.num_frames + 1):
            self.current_frame_idx = i
            self._get_current_detections()
            self._propogate_tracklets()

            self.tracklet_associator.associate_detections(self.current_detections, self.current_tracklets)

            # print('-'*40)
            # print(i)
            # print("detections: ", self.current_detections)
            # print("unmatched detections: ", self.tracklet_associator.unmatched_detections)
            # print("matched detections: ", self.tracklet_associator.matched_detections)
            # print("unmatched tracklets: ", self.tracklet_associator.unmatched_tracklets)

            self._destroy_unmatched_tracklets(self.tracklet_associator.unmatched_tracklets)
            self._update_matched_tracklets(self.tracklet_associator.matched_detections)
            self._create_tracklets_for_unmatched_detections(self.tracklet_associator.unmatched_detections)

        self.tracklet_history.extend(self.current_tracklets)

       #print(self.tracklet_history)

    def get_tracks_by_frame(self):
        sequence_frame_tracks = []
        for i in range(self.num_frames + 1):
            frame_tracks = []
            for track in self.tracklet_history:
                if track.exists_for_frame(i):
                    frame_tracks.append(track.get_track_frame(i))
            sequence_frame_tracks.append(frame_tracks)
                    
    def _get_current_detections(self):
        self.current_detections = self.frame_detections[self.current_frame_idx]

    def _propogate_tracklets(self):
        for tracklet in self.current_tracklets:
            tracklet.update_prediction()

    def _update_matched_tracklets(self, matched_detections):
        for match in matched_detections:
            match[0].update_correction(match[1])

        updated_tracklets = [ match[0] for match in matched_detections]
        self.current_tracklets = updated_tracklets
        
    def _destroy_unmatched_tracklets(self, unmatched_tracklets):
        for tracklet in unmatched_tracklets:
            self.tracklet_history.append(tracklet)
            self.current_tracklets = [x for x in self.current_tracklets if x.id != tracklet.id]

    def _create_tracklets_for_unmatched_detections(self, unmatched_detections):
        for detection in unmatched_detections:
            self.current_tracklets.append(Tracklet(detection, self.current_frame_idx))
