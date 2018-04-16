# Brianna Brown Richardson
# Visual Data Setup Module for VBASE project
# Last Modified Date:
# CS200 - Algorithm Analysis

import shapefile
import matplotlib.pyplot as plt
import random
import numpy as np

# Constants for shape types
NULL = 0
POINT = 1
POLYLINE = 3
POLYGON = 5
MULTIPOINT = 8
POINTZ = 11
POLYLINEZ = 13
POLYGONZ = 15
MULTIPOINTZ = 18
POINTM = 21
POLYLINEM = 23
POLYGONM = 25
MULTIPOINTM = 28
MULTIPATCH = 31


class VisualSetup:
    def __init__(self, sf_reader):
        self.sf_reader = sf_reader
        self.sf_writer = shapefile.Writer()
        self.fig = plt.figure()

    def get_plt_2d(self):
        """
        Get the matplotlib figure that contains the 2D scene of selected
        shapefile
        :return: ax - figure containing visualized data
        """
        for shape in self.sf_reader.shapes():
            x = [i[0] for i in shape.points[:]]
            y = [i[1] for i in shape.points[:]]
            plt.plot(x, y)

        ax = plt.gcf()
        plt.axis('off')
        return ax

    def get_plt_3d(self):
        """
        Get the matplotlib figure that contains the 3D scene of selected
        shapefile
        :return: self.fig - figure containig visualized data
        """
        return self.fig

    def setting_shapes_to_3d(self):
        """
        Changing Shapes from a 2D file to be 3D and save as a 3D shapefile
        :return: None
        """
        shapes = self.sf_reader.shapes()
        self.sf_writer.autoBalance = 1

        for i in range(0, len(shapes), 1):

            if shapes[i].shapeType == NULL:
                pass

            elif shapes[i].shapeType == (POINT or POLYLINE or MULTIPOINT or
                                         POINTM or POLYLINEM or MULTIPOINTM or
                                         POINTZ or POLYLINEZ or
                                         MULTIPOINTZ):

                self.point_line_elevation(shapes[i], shapes[i].shapeType)

            elif shapes[i].shapeType == (POLYGON or POLYGONZ or POLYGONM):
                # go through 3d setup/3d environment
                self.polygon_to_multipatch(shapes[i])

            elif shapes[i].shapeType == MULTIPATCH:
                # go typical 3D scene setup
                self.multipatch_draw(shapes[i])

        self.sf_writer.save("3D_temp")

    def polygon_to_multipatch(self, shape):
        """
        Change polygon shape to multipatch and write to temporary 3D shapefile
        :param shape: current polygon shape
        :return: None
        """
        part = list()
        shapestype = list()
        floor = list()
        ceiling = list()
        for i in shape.points:
            floor.append([i[0], i[1], 0])
            ceiling.append([i[0], i[1], 1])

        part.append(floor)
        part.append(ceiling)
        for i in range(1, len(floor), 1):
            j = i - 1
            surface = [floor[j], floor[j + 1], ceiling[j], ceiling[j + 1]]
            part.append(surface)

        for i in range(0, len(part), 1):
            shapestype.append(POLYGON)

        self.sf_writer.poly(parts=part,
                            partTypes=shapestype,
                            shapeType=MULTIPATCH)

    def point_line_elevation(self, shape, shape_type):
        """
        Change points and lines to 3D elements and write to temporary shapefile
        :param shape: current shape
        :param shape_type: shape type of shape argument
        :return: None
        """
        if shape_type == POINT or MULTIPOINT or POINTM or MULTIPOINTM:
            for i in shape.points:
                self.sf_writer.point(i[0], i[1], 0.5, shapeType=POINTZ)

        elif shape_type == (POLYLINE or POLYLINEM):
            part = list()
            shapestype = list()
            for i in shape.points:
                part.append([i[0], i[1], 0.5])

            for i in range(0, len(part), 1):
                shapestype.append(POLYLINEZ)

            self.sf_writer.line(parts=part, shapeType=shapestype)

        elif shape_type == POINTZ or MULTIPOINTZ:
            z_coors = shape.z
            for i in range(0, len(shape.points), 1):
                self.sf_writer.point(shape.points[i][0], shape.points[i][1],
                                     z_coors[i], shapeType=POINTZ)

        elif shape_type == POLYLINEZ:
            part = list()
            shapestype = list()
            z_coors = shape.z
            for i in range(0, len(shape.points), 1):
                part.append([shape.points[i][0], shape.points[i][1],
                             z_coors[i]])

            for i in range(0, len(part), 1):
                shapestype.append(POLYLINEZ)

            self.sf_writer.line(parts=part, shapeType=shapestype)

    def draw_3d_shapes(self, xy_coors, z_part, rand_color):
        """
        Actual drawing of 3D elements to matplotlib figure
        :param xy_coors: x and y coordinates of current part
        :param z_part: z coordinates of current part
        :param rand_color: color value for a particular shape
        :return: None
        """
        # if z_coordinates are all the same value that means
        # shape is flat surface
        if all(x == z_part[0] for x in z_part) is True:
            pass

        # not a flat surface
        else:
            x_coors = list()
            y_coors = list()
            z_coors = list()
            z_floor = list()
            z_ceiling = list()
            z_ranges = list()
            for p in range(0, len(xy_coors), 1):
                x_coors.append(xy_coors[p][0])
                y_coors.append(xy_coors[p][1])
                z_coors.append(z_part[p])

            for k in range(len(z_coors)):
                z_floor.append(min(z_coors))
                z_ceiling.append(max(z_coors))

            z_ranges.append(z_floor)
            z_ranges.append(z_ceiling)
            self.fig.add_subplot(projection='3d')
            ax = self.fig.gca(projection='3d')
            ax.set_zlim(0, max(z_coors) + 5)
            ax.set_axis_off()
            x = np.array(x_coors)
            y = np.array(y_coors)
            z = np.array(z_ranges)
            ax.plot_surface(x, y, z, color=rand_color)

    def multipatch_draw(self, curr_shape):
        """
        Take a multipatch shape and draw it to a matplotlib figure
        :param curr_shape: current multipatch shape needing to be drawn
        :return: None
        """
        rand_color = [random.uniform(0, 1), random.uniform(0, 1),
                      random.uniform(0, 1)]
        for k in range(1, len(curr_shape.parts), 1):
            j = k - 1
            xy_coors = curr_shape.points[
                       curr_shape.parts[j]:curr_shape.parts[k]]
            z_part = curr_shape.z[curr_shape.parts[j]:curr_shape.parts[k]]

            self.draw_3d_shapes(xy_coors, z_part, rand_color)

        xy_coors = curr_shape.points[
                   curr_shape.parts[-1]:-1]
        z_part = curr_shape.z[curr_shape.parts[-1]:-1]
        self.draw_3d_shapes(xy_coors, z_part, rand_color)

    def setup_3d_scene(self):
        """
        Setting up the 3D scene by shape type and drawing to figure accordingly
        :return: None
        """
        r = shapefile.Reader('3D_temp')
        shapes = r.shapes()
        for i in range(0, len(shapes), 1):
            if shapes[i].shapeType == POINTZ:
                x_coors = list()
                y_coors = list()
                z_coors = shapes[i].z

                for j in shapes[i].points:
                    x_coors.append(j[0])
                    y_coors.append(j[1])

                self.fig.add_subplot(projection='3d')
                ax = self.fig.gca(projection='3d')
                ax.set_axis_off()
                ax.scatter(x_coors, y_coors, z_coors)

            elif shapes[i].shapeType == POLYLINEZ:
                x_coors = list()
                y_coors = list()
                z_coors = shapes[i].z

                for j in shapes[i].points:
                    x_coors.append(j[0])
                    y_coors.append(j[1])

                self.fig.add_subplot(projection='3d')
                ax = self.fig.gca(projection='3d')
                ax.set_axis_off()
                ax.plot(x_coors, y_coors, z_coors)

            elif shapes[i].shapeType == MULTIPATCH:
                self.multipatch_draw(shapes[i])
