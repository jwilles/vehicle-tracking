import numpy as np
from bbox import BBox2D, BBox3D, XYXY

from kitti_label import KittiLabel


class KittiTracking(KittiLabel):
    """ Kitti 3D Multi Object Tracking Label """

    def __init__(self, line):
        """
        Converts a line from the KITTI labels text file into the KittiTracking format.
        Same as KittiObject format with additional attributes for occluded, truncated, and track_id
        See https://github.com/pratikac/kitti/blob/master/readme.tracking.txt
        :param line [string]: Line in the KITTI object tracking text file
        """
        label = line.strip().split(' ')
        params["frame"] = int(label[0])
        params["type"] = label[2]

        # 2D bounding box in pixel coordinates [px]
        params["bbox2d"] = BBox2D([float(label[6]), float(label[7]),
                                   float(label[8]), float(label[9])], mode=XYXY)

        # 3D bounding box in camera coordinates [m,rad]
        params["bbox3d"] = BBox3D(x=float(label[13]),
                                  y=float(label[14]),
                                  z=float(label[15]),
                                  length=float(label[12]),
                                  width=float(label[11]),
                                  height=float(label[10]),
                                  euler_angles=[0, float(label[16]), 0])

        params["alpha"] = float(label[5])
        params["score"] = float(label[17])
        super(KittiTracking, self).init(params)

        self.track_id = int(label[1])
        self.truncated = float(label[3])
        self.occluded = float(label[4])
