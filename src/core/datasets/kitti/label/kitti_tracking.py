from .kitti_label import KittiLabel
from ..boundbox.kitti_bbox2d import KittiBBox2D
from ..boundbox.kitti_bbox3d import KittiBBox3D

# TO DO: Remove this, add to KittiObject


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
        params = {}
        params["frame"] = int(label[0])
        params["type"] = label[2]

        # 2D bounding box in pixel coordinates [px]
        params["bbox2d"] = KittiBBox2D(x1=float(label[6]), y1=float(label[7]),
                                       x2=float(label[8]), y2=float(label[9]))

        # 3D bounding box in camera coordinates [m,rad]
        params["bbox3d"] = KittiBBox3D(x=float(label[13]),
                                       y=float(label[14]),
                                       z=float(label[15]),
                                       length=float(label[12]),
                                       width=float(label[11]),
                                       height=float(label[10]),
                                       theta=float(label[16]))

        params["alpha"] = float(label[5])
        params["score"] = float(label[17]) if label.__len__() == 18 else -1.0
        super(KittiTracking, self).__init__(params)

        self.track_id = int(label[1])
        self.truncated = float(label[3])
        self.occluded = float(label[4])
