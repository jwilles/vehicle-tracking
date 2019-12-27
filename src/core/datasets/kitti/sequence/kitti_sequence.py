import os
import cv2

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
            self.label_dir = os.path.join(self.image_dir, 'training',
                                          "label_02")
            self.calib_dir = os.path.join(self.calib_dir, 'training', 'calib')
        else:
            self.image_dir = os.path.join(self.image_dir, 'testing',
                                          "image_02", str(self.seq_id).zfill(4))
            self.label_dir = ""
            self.calib_dir = os.path.join(self.calib_dir, 'testing', 'calib')

        # Get all objects in detections file
        objects = self.get_objects(self.detection_file)

        self.num_frames = objects[-1].frame
        self.objects = [[] for _ in range(self.num_frames + 1)]

        for object_ in objects:
            self.objects[object_.frame].append(object_)

    def __len__(self):
        """
        Gets the number of frames in the sequence
        :return num_frames [int]: Number of frames in the sequence
        """
        return self.num_frames

    def __getitem__(self, frame):
        """
        Retrieves all object labels at specific frame
        :param  frame   [int] : Frame number
        :return objects [list]: List of object labels for given frame
        """
        objects = self.objects[frame]
        return objects

    def get_image(self, frame):
        """
        Retreives image at a specific frame
        """
        image_file = os.path.join(self.image_dir, str(frame).zfill(6) + ".png")
        image = cv2.imread(image_file)

        return image

    def get_objects(self, detection_file):
        """
        Get all objects in detections file
        :param  detection_file [string] : Sequence file
        :return objects [list]: List of object labels in sequence file
        """
        with open(detection_file, 'r') as file:
            lines = file.readlines()
        objects = [KittiObject(line) for line in lines]

        return objects

    def get_calib(self):
        """
        Gets calibration for sequence
        """
        # Get Calib
        calib_file = os.path.join(self.calib_dir, str(self.seq_id).zfill(4) + ".txt")
        return KittiCalib(calib_file)
