import os
import cv2
import numpy as np

from core.datasets.kitti.label.kitti_object import KittiObject
from core.datasets.kitti.kitti_calib import KittiCalib


class KittiSequence():
    """ KITTI Sequence for 3D Multi Object Tracking"""

    def __init__(self, detections_dir, dataset_dir, seq_id, split='val', class_="car"):
        """
        Loads the KITTI Sequence
        :param detections_dir [string]: Directory to the root of the detections on Kitti dataset
        :param dataset_dir [string]: Directory to the root of the Kitti dataset
        :param seq_id [int]: Sequence ID (corresponds with file name)
        :param format [string]: Format of labels [detection/trackingGT]
        """
        self.detections_dir = os.path.expanduser(detections_dir)
        self.dataset_dir = os.path.expanduser(dataset_dir)
        self.seq_id = seq_id
        self.split = split
        self.class_ = class_

        self.detection_file = os.path.join(
            self.detections_dir, self.split, self.class_, str(seq_id).zfill(4) + ".txt")

        # Get dataset directories
        self.image_dir = os.path.join(self.dataset_dir, "data_tracking_image_2")
        self.label_dir = os.path.join(self.dataset_dir, "data_tracking_label_2")
        self.calib_dir = os.path.join(self.dataset_dir, "data_tracking_calib")

        if self.split != 'test':
            self.image_dir = os.path.join(self.image_dir, 'training',
                                          "image_02", str(self.seq_id).zfill(4))
            self.label_dir = os.path.join(self.label_dir, 'training',
                                          "label_02")
            self.calib_dir = os.path.join(self.calib_dir, 'training', 'calib')
        else:
            self.image_dir = os.path.join(self.image_dir, 'testing',
                                          "image_02", str(self.seq_id).zfill(4))
            self.label_dir = ""
            self.calib_dir = os.path.join(self.calib_dir, 'testing', 'calib')

        # Get all objects in detections file
        detections = self.get_objects(self.detection_file)

        self.num_frames = detections[-1].frame
        self.detections = [[] for _ in range(self.num_frames + 1)]

        for detection in detections:
            self.detections[detection.frame].append(detection)

    def __len__(self):
        """
        Gets the number of frames in the sequence
        :return num_frames [int]: Number of frames in the sequence
        """
        return self.num_frames

    def __getitem__(self, frame):
        """
        Retrieves all detections at specific frame
        :param  frame   [int] : Frame number
        :return detections [list]: List of object detections for given frame
        """
        detections = self.detections[frame]
        return detections

    def get_image(self, frame):
        """
        Retreives image at a specific frame
        """
        image_file = os.path.join(self.image_dir, str(frame).zfill(6) + ".png")
        image = cv2.imread(image_file)

        return image

    def get_objects(self, objects_file, format_="detection"):
        """
        Get all objects in file
        :param  objects_file [string] : Sequence file
        :return objects [list]: List of object labels in sequence file
        """
        with open(objects_file, 'r') as file:
            lines = file.readlines()
        objects = [KittiObject(line, format_) for line in lines]

        return objects

    def get_track(self, track_id):
        """
        Gets track from labels
        """
        label_file = os.path.join(self.label_dir, str(self.seq_id).zfill(4) + ".txt")
        objects = self.get_objects(label_file, format_="track")
        track = np.empty((7, 0))

        for object_ in objects:
            if object_.track_id == track_id:
                state = np.array([object_.bound_box3d.x,
                                  object_.bound_box3d.y,
                                  object_.bound_box3d.z,
                                  object_.bound_box3d.theta,
                                  object_.bound_box3d.x_dim,
                                  object_.bound_box3d.y_dim,
                                  object_.bound_box3d.z_dim])
                state = state.reshape((7, 1))
                track = np.append(track, state, axis=1)

        return track

    def get_calib(self):
        """
        Gets calibration for sequence
        """
        # Get Calib
        calib_file = os.path.join(self.calib_dir, str(self.seq_id).zfill(4) + ".txt")
        return KittiCalib(calib_file)
