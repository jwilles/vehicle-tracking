import os

from kitti_object import KittiObject


class KittiSequence():
    """ KITTI Sequence for 3D Multi Object Tracking"""

    def __init__(self, dataset_dir, split='val', class_='car', seq_id):
        """
        Loads the KITTI Sequence
        :param dataset_dir [string]: Directory to the root of the Kitti object detection dataset
        :param split       [string]: Detection split [val/test]
        :param class_      [string]: Object class [car/cyclist/pedestrian]
        :param seq_id      [int]   : Sequence ID (corresponds with file name)
        """
        self.dataset_dir = os.path.expanduser(dataset_dir)
        self.split = split
        self.class_ = class_
        self.seq_id = seq_id
        self.sequence_file = os.path.join(
            self.dataset_dir, "detections", self.split, self.class_, str(seq_id).zfill(4) + ".txt")

        # Get all objects in sequence file
        with open(self.sequence_file, 'r') as file:
            lines = file.readlines()
        objects = [KittiObject(line) for line in lines]

        # Create 2D list for objects where: [frame_no][detection_no]
        self.objects = [[]]
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
