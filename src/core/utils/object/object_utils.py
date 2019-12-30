def object_to_text_line(frame, object_):
    """
    Converts an object to a text line in KITTI format
    """

    bit_size = 32
    track_id = object_.track_id.int >> bit_size

    # String class label
    if object_.class_id == 1:
        class_ = "Pedestrian"
    elif object_.class_id == 2:
        class_ = "Car"
    elif object_.class_id == 3:
        class_ = "Cyclist"
    else:
        class_ = "DontCare"

    # Form list
    label = [frame,
             track_id,
             class_,
             -1,
             -1,
             -10,
             object_.bound_box2d.u1,
             object_.bound_box2d.v1,
             object_.bound_box2d.u2,
             object_.bound_box2d.v2,
             object_.bound_box3d.y_dim,
             object_.bound_box3d.z_dim,
             object_.bound_box3d.x_dim,
             object_.bound_box3d.x,
             object_.bound_box3d.y,
             object_.bound_box3d.z,
             object_.bound_box3d.theta,
             object_.score]

    # Covert list to a line
    line = "{0:d} {1:d} {2} {3:d} {4:d} {5:d} {6:.6f} {7:.6f} {8:.6f} {9:.6f} {10:.6f} {11:.6f} {12:.6f} {13:.6f} {14:.6f} {15:.6f} {16:.6f} {17:.6f}\n".format(
        *label)
    return line


def objects_to_text_lines(frame, objects):
    """
    Outputs list of objects as text lines
    Args:
        objects [list[Object]]: List of objects
    Returns
        lines [list[string]]: List of text lines
    """

    # Convert objects to KITTI tracking labels text format

    lines = [object_to_text_line(frame, object_) for object_ in objects]
    return lines
