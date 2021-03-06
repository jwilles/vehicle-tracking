from core.utils.object.object import Object
from core.utils.object.bound_box2d import BoundBox2D
from core.utils.object.bound_box3d import BoundBox3D


class KittiObject(Object):
    """ Kitti 3D Object Label """

    def __init__(self, line, format_="detection"):
        """
        Converts a line from the KITTI labels text file into the KittiObject format.
        See https://github.com/xinshuoweng/AB3DMOT/blob/master/README.md for more details
        Args:
            line [string]: Line in the KITTI object detection text file
        """

        if format_ == "detection":
            label = line.strip().split(',')
            self.frame = int(label[0])
            class_id = int(label[1])

            # 2D bounding box in pixel coordinates [px]
            bound_box2d = BoundBox2D(u1=float(label[2]), v1=float(label[3]),
                                     u2=float(label[4]), v2=float(label[5]))

            # 3D bounding box in camera coordinates [m,rad]
            bound_box3d = BoundBox3D(x=float(label[10]),
                                     y=float(label[11]),
                                     z=float(label[12]),
                                     x_dim=float(label[9]),
                                     z_dim=float(label[8]),
                                     y_dim=float(label[7]),
                                     theta=float(label[13]))

            self.alpha = float(label[14])
            score = float(label[6])
            track_id = None

        elif format_ == "track":
            label = line.strip().split(' ')
            self.frame = int(label[0])
            class_ = label[2]

            # String class label
            if class_ == "Pedestrian":
                class_id = 1
            elif class_ == "Car":
                class_id = 2
            elif class_ == "Cyclist":
                class_id = 3
            else:
                class_id = -1

            # 2D bounding box in pixel coordinates [px]
            bound_box2d = BoundBox2D(u1=float(label[6]), v1=float(label[7]),
                                     u2=float(label[8]), v2=float(label[9]))

            # 3D bounding box in camera coordinates [m,rad]
            bound_box3d = BoundBox3D(x=float(label[13]),
                                     y=float(label[14]),
                                     z=float(label[15]),
                                     x_dim=float(label[12]),
                                     z_dim=float(label[11]),
                                     y_dim=float(label[10]),
                                     theta=float(label[16]))

            self.alpha = float(label[5])
            score = float(label[17]) if label.__len__() == 18 else -1.0
            track_id = int(label[1])
            self.truncated = float(label[3])
            self.occluded = float(label[4])

        # Parent class initialization
        super(KittiObject, self).__init__(class_id, bound_box2d, bound_box3d, track_id, score)
