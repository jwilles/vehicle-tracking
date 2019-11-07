import os

from kitti_sequence import KittiSequence
from label.kitti_tracking import KittiTracking


class KittiTrackingGT(KittiSequence):
    """ KITTI Ground Truth for 3D Multi Object Tracking"""

    def __init__(self, dataset_dir,  split='val', seq_id):
        """
        Loads the KITTI Sequence
        :param dataset_dir [string]: Directory to the root of the Kitti object detection dataset
        :param type_       [string]: Type of sequence [detections/tracking_GT]
        :param split       [string]: Datset split [val/test]
        :param seq_id      [int]   : Sequence ID (corresponds with file name)
        """
        self.dataset_dir = dataset_dir
        self.split = split
        seq_dir = os.path.join(
            self.dataset_dir, "tracking_GT", self.split)

        super(KittiTracking, self).init(seq_dir, seq_id)

    def get_objects(self, seq_file):
        """
        Get all objects in sequence file
        :param  seq_file [string] : Sequence file
        :return objects [list]: List of object labels in sequence file
        """
        with open(sequence_file, 'r') as file:
            lines = file.readlines()
        objects = [KittiTracking(line) for line in lines]

        return objects
