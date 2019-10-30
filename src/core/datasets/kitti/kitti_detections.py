import os

from .kitti_object import KittiObject


class KittiDetections():
    """ KITTI Object Detection Results"""

    def __init__(self, dataset_dir, split='val', class_='car'):
        """
        Loads the required KITTI Detection files
        Args:
            dataset_dir [string]: Directory to the root of the Kitti object detection dataset
            split       [string]: Detection split [val/test]
            class_      [string]: Object class [car/cyclist/pedestrian]
        """
        self.dataset_dir = os.path.expanduser(dataset_dir)
        self.split = split
        self.class_ = class_
        self.detection_dir = os.path.join(self.dataset_dir, "detections", self.split, self.class_)

        # Get detection file paths list
        self.detection_files = [file for file in os.listdir(
            self.detection_dir) if os.path.isfile(os.path.join(self.detection_dir, file))]
        self.num_samples = self.detection_files.__len__()

    def __len__(self):
        """
        Gets the size of the detection result list
        Returns:
            num_samples [int]: Number of samples in the dataset
        """
        return self.num_samples

    def __getitem__(self, idx):
        """
        Retrieves an indexed detections sample
        Args:
            idx [int]: Index of the sample
        Returns:
            detections [list]: Dataset sample with list of detections for each sequence
        """

        detections_file = os.path.join(self.detection_dir, self.detection_files[idx])
        detections = self.get_objects(detections_file)
        return detections

    @staticmethod
    def get_objects(detections_file):
        """
        Gets all object detections from a KITTI detections text file
        Args:
            detections_file [string]: Detection text file path
        Returns:
            objects [list]: All object detections within the text file
        """
        with open(detections_file, 'r') as file:
            lines = file.readlines()
        objects = [KittiObject(line) for line in lines]
        return objects
