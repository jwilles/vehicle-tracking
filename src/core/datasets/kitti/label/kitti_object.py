import numpy as np
from bbox import BBox2D, BBox3D, XYXY

from kitti_label import KittiLabel


class KittiObject(KittiLabel):
    """ Kitti 3D Object Label """

    def __init__(self, line):
        """
        Converts a line from the KITTI labels text file into the KittiObject format.
        See https://github.com/xinshuoweng/AB3DMOT/blob/master/README.md for more details
        Args:
            line [string]: Line in the KITTI object detection text file
        """
        label = line.strip().split(',')
        params["frame"] = int(label[0])
        params["type"] = int(label[1])

        # 2D bounding box in pixel coordinates [px]
        params["bbox2d"] = BBox2D([float(label[2]), float(label[3]),
                                   float(label[4]), float(label[5])], mode=XYXY)

        # 3D bounding box in camera coordinates [m,rad]
        params["bbox3d"] = BBox3D(x=float(label[10]),
                                  y=float(label[11]),
                                  z=float(label[12]),
                                  length=float(label[9]),
                                  width=float(label[8]),
                                  height=float(label[7]),
                                  euler_angles=[0, float(label[13]), 0])

        params["alpha"] = float(label[14])
        params["score"] = float(label[6])
        super(KittiObject, self).init(params)
