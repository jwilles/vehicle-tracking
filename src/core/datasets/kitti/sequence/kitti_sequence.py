import os

from ..label.kitti_object import KittiObject


class KittiSequence():
    """ KITTI Sequence for 3D Multi Object Tracking"""

    def __init__(self, seq_dir, seq_id):
        """
        Loads the KITTI Sequence
        :param seq_path [string]: Directory the sequence file is located
        :param seq_id   [int]   : Sequence ID (corresponds with file name)
        """
        self.seq_dir = os.path.expanduser(seq_dir)
        self.seq_id = seq_id
        self.seq_file = os.path.join(
            self.seq_dir, str(seq_id).zfill(4) + ".txt")

        # Get all objects in sequence file
        objects = self.get_objects(self.seq_file)

        # Create 2D list for objects where: [frame_no][detection_no]
        self.num_frames = objects[-1].frame
        self.objects = [[] for _ in range(self.num_frames + 1)]
        for object_ in objects:
            self.objects[object_.frame].append(object_)

        self.num_frames = self.objects.__len__()

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
