import os

from ..label.kitti_object import KittiObject


class KittiSequence():
    """ KITTI Sequence for 3D Multi Object Tracking"""

    def __init__(self, dataset_dir, seq_id, format_, split='val', class_="car"):
        """
        Loads the KITTI Sequence
        :param dataset_dir [string]: Directory to the root of the Kitti dataset
        :param seq_id [int]: Sequence ID (corresponds with file name)
        :param format [string]: Format of labels [detection/trackingGT]
        """
        self.dataset_dir = os.path.expanduser(dataset_dir)
        self.seq_id = seq_id
        self.split = split
        self.class_ = class_
        self.format_ = format_

        if self.format_ == "detections":
            self.seq_file = os.path.join(
                self.dataset_dir, self.format_, self.split, self.class_, str(seq_id).zfill(4) + ".txt")

        # TO DO
        # elif format_ == "trackingGT":

        # Get all objects in sequence file
        objects = self.get_objects(self.seq_file)

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

    def get_objects(self, seq_file):
        """
        Get all objects in sequence file
        :param  seq_file [string] : Sequence file
        :return objects [list]: List of object labels in sequence file
        """
        with open(seq_file, 'r') as file:
            lines = file.readlines()
        objects = [KittiObject(line) for line in lines]

        return objects
