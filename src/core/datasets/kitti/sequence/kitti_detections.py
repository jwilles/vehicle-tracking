import os

from kitti_sequence import KittiSequence


class KittiDetections(KittiSequence):
    """ KITTI Detections for 3D Multi Object Tracking"""

    def __init__(self, dataset_dir,  split='val', class_='car', seq_id):
        """
        Loads the KITTI Sequence
        :param dataset_dir [string]: Directory to the root of the Kitti object detection dataset
        :param split       [string]: Datset split [val/test]
        :param class_      [string]: Object class [car/cyclist/pedestrian]
        :param seq_id      [int]   : Sequence ID (corresponds with file name)
        """
        self.dataset_dir = dataset_dir
        self.split = split
        self.class_ = class_
        seq_dir = os.path.join(
            self.dataset_dir, "detections", self.split, self.class_)

        super(KittiDetections, self).init(seq_dir, seq_id)
