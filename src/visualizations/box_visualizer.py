import os

import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def visualize(objects, camera_calib, output_path, image=None, torch_image=None):
    """
    Visualizes 2D and 3D boxes on image and outputs as image
    Args:
        objects [List[Object]]: List of objects
        camera_calib [CameraCalib]: Camera calibration
        output_path: Path to output the visualization
        image: Image in BGR numpy format
        torch_image: Image in BGR torch format [C, H, W] normalized between 0-1
    """

    if image is None and torch_image is None:
        raise ValueError("Invalid argument: image is None and torch_image is None")

    elif image is not None and torch_image is None:
        img = image

    elif image is None and torch_image is not None:
        # Scale image between 0 and 255
        img = torch_image.numpy() * 255

        # Convert back to int
        img = img.astype(np.uint8)

        # Switch shape to shape [H, W, C]
        img = np.moveaxis(img, 0, -1)

    else:
        raise ValueError("Invalid argument: image is not None and torch_image is not None")

    # Add image to plot
    fig, axes = image_to_plot(img, subplot_rows=2)

    # Set box colors for classes
    box_colors = ["g", "c", "y"]

    # Overlay boxes on plot
    for obj in objects:
        overlay_boxes2D(axes=axes[0], obj=obj, box_colors=box_colors)
        overlay_boxes3D(axes=axes[1], obj=obj, camera_calib=camera_calib, box_colors=box_colors)

    # Output the plot as image
    output_vis(output_path)


def overlay_boxes2D(axes, obj, box_colors, line_width=3):
    """
    Overlays 2D boxes on plot
    Args:
        axes: Subplot handle
        obj [Object]: Object detection to overlay
        box_colours[List[int]]: List of box colors for each class
        line_width: Line width of the box
    """
    u, v, w, h = obj.bound_box2d.get_coords_UVWH()
    rect = patches.Rectangle((u, v),
                             w, h,
                             linewidth=line_width,
                             edgecolor=box_colors[obj.class_id],
                             facecolor='none')
    axes.add_patch(rect)


def overlay_boxes3D(axes, obj, camera_calib, box_colors,
                    show_orientation=True, line_width=3,
                    line_style="solid", double_line=True):
    """
    Overlays 3D boxes on plot
    Args:
        axes: Subplot handle
        obj [Object]: Object detection to overlay
        camera_calib [CameraCalib]: Camera calibration
        show_orientation: Draw a line showing orientation
        box_colours[List[int]]: List of box colors for each class
        line_width: Line width of the box
        line_style: Line style of the box
        double_line: Overlays a thinner line inside the box lines
    """

    # Corner indices for 3D bounding box face
    # it is converted to 4x4 matrix
    face_idx = np.array([0, 1, 5, 4,  # front face
                         1, 2, 6, 5,  # right face
                         2, 3, 7, 6,  # back face
                         3, 0, 4, 7]).reshape((4, 4))  # left face

    # Get the image locations of bounding box corners
    corners3d = obj.bound_box3d.get_corners_3d()
    corners = camera_calib.project_points3d_to_image(corners3d)

    # Draw boxes if corners are computed
    if len(corners) > 0:
        for i in range(4):
            x = np.append(corners[0, face_idx[i, ]],
                          corners[0, face_idx[i, 0]])
            y = np.append(corners[1, face_idx[i, ]],
                          corners[1, face_idx[i, 0]])

            axes.plot(x, y, linewidth=line_width,
                      color=box_colors[obj.class_id],
                      linestyle=line_style)

            # Draw a thinner second line inside
            if double_line:
                axes.plot(x, y, linewidth=line_width / 3.0, color='b')

    # TO DO:
    # if show_orientation:
        # Compute orientation 3D
        # orientation = obj_utils.compute_orientation_3d(obj, cam_p)

        # if orientation is not None:
        #     x = np.append(orientation[0, ], orientation[0, ])
        #     y = np.append(orientation[1, ], orientation[1, ])

        #     # draw the boxes
        #     ax.plot(x, y, linewidth=4, color='w')
        #     ax.plot(x, y, linewidth=2, color='k')


def output_vis(output_path):
    """
    Outputs the current plot as an image
    Args:
        output_path: Path to output the plot
    """
    # Make directory if doesn't exists
    dir_ = os.path.dirname(output_path)
    if not os.path.exists(dir_):
        os.makedirs(dir_)

    plt.savefig(output_path)
    plt.close()


def set_plot_limits(axes, image):
    """
    # Set the plot limits to the size of the image, y is inverted
    """
    axes.set_xlim(0, image.shape[1])
    axes.set_ylim(image.shape[0], 0)


def image_to_plot(img,
                  subplot_rows=1,
                  subplot_cols=1,
                  fig_size=None):
    """
    Forms the plot figure and axis for the visualization
    Args:
        img: image to plot
        subplot_rows: number of rows of the subplot grid
        subplot_cols: number of columns of the subplot grid
        fig_size: (optional) size of the figure
    """
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if fig_size is None:
        img_shape = np.shape(img)
        fig_height = img_shape[0] / 100 * subplot_rows
        fig_width = img_shape[1] / 100 * subplot_cols
        fig_size = (fig_width, fig_height)

    # Create the figure
    fig, axes = plt.subplots(subplot_rows, subplot_cols, figsize=fig_size, sharex=True)
    fig.subplots_adjust(left=0.0, bottom=0.0, right=1.0, top=1.0, hspace=0.0)

    # Plot image
    if subplot_rows == 1 and subplot_cols == 1:
        # Single axis
        axes.imshow(img)
        set_plot_limits(axes, img)
    else:
        # Multiple axes
        for idx in range(axes.size):
            axes[idx].imshow(img)
            set_plot_limits(axes[idx], img)

    return fig, axes
