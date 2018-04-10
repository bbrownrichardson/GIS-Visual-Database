import shapefile
import os
import matplotlib.pyplot as plt
import math
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np



# Constants for ...
CHARACER = 'C'
NUMBERS = 'N'
LONGS = 'L'
MEMO = 'M'

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


def all_shapes_to_3d():
    myshp = open("CollegeCampus.shp", "rb")
    mydbf = open("CollegeCampus.dbf", "rb")
    r = shapefile.Reader(shp=myshp, dbf=mydbf)
    w = shapefile.Writer(shapeType=shapefile.MULTIPATCH)
    shapesrec = r.shapes()
    w.autoBalance = 1

    for i in range(0, len(shapesrec), 1):
        individual_shape_to_3d(shapesrec[i], w)
    w.save("3D_temp")


def individual_shape_to_3d(shape, writer):
    part = []
    shapestype = list()
    floor = list()
    ceiling = list()
    # z_coors = shape.z
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
        shapestype.append(5)

    writer.poly(parts=part,
                        partTypes=shapestype,
                        shapeType=31)


def setup_3d_scene():
    x_coors = list()
    y_coors = list()
    z_ranges = list()
    z_floor = list()
    z_flat = list()
    z_high = list()
    fig = plt.gcf() # figsize=plt.figaspect(0.5)

    r = shapefile.Reader('3D_temp')
    shapes = r.shapes()
    # print shapes[3].shapeType
    # print shapes[3].points
    shape_color = np.random.rand(3)
    for i in range(0, len(shapes), 1):
        print('SHAPE-----')
        shape_var = r.shape(i).points
        z_coors = r.shape(i).z

        for i in shape_var:
            x_coors.append(i[0])
            y_coors.append(i[1])

        z_max = max(z_coors)
        z_min = min(z_coors)

        for i in range(0, len(z_coors), 1):
            z_floor.append(0)
            z_flat.append(z_min)
            z_high.append(z_max)

        z_ranges.append(z_coors)
        z_ranges.append(z_floor)

        fig.add_subplot(projection='3d')
        ax = fig.gca(projection='3d')
        ax.set_zlim(0, z_max + 5)
        ax.set_axis_off()
        X = np.array(x_coors)
        Y = np.array(y_coors)
        Z = np.array(z_ranges)
        ax.plot_surface(X, Y, Z, facecolor=shape_color)
        verts = [zip(x_coors, y_coors, z_flat)]
        ax.add_collection3d(Poly3DCollection(verts, facecolor=shape_color))
        verts = [zip(x_coors, y_coors, z_high)]
        ax.add_collection3d(Poly3DCollection(verts, facecolor=shape_color))

        x_coors = []
        y_coors = []
        z_coors = []
        z_ranges = []
        z_floor = []
        # plt.show()

    plt.show()


def main():
    # myshp = open("Shapefiles\CollegeCampus.shp", "rb")
    # mydbf = open("Shapefiles\CollegeCampus.dbf", "rb")
    # sf = shapefile.Reader(shp=myshp, dbf=mydbf)
    # w = shapefile.Writer(shapefile.POLYGONZ)
    # w.autoBalance = 1

    # vertices = [-81.9336023, 40.8134129, -81.9333167, 40.8135786,
    #             -81.9333188, 40.8134627, -81.9336303, 40.8134555,
    #             -81.9337162, 40.8133967, -81.9337162, 40.8132444,
    #             -81.9338552, 40.8132444, -81.9338879, 40.8132444,
    #             -81.9338878, 40.8135327, -81.9338616, 40.813551,
    #             -81.9338181, 40.8135814, -81.9333555, 40.8135788,
    #             -81.9333167, 40.8135786]
    #
    # x_coor = list()
    # y_coor = list()
    #
    # for i in range(0, len(vertices), 1):
    #     if i % 2 == 0:
    #         x_coor.append(vertices[i])
    #     else:
    #         y_coor.append(vertices[i])
    #
    # print(x_coor)
    # x_sort = sorted(x_coor)
    # print(x_sort)
    #
    # print('\n\n\n')
    #
    # print(y_coor)
    # y_sort = sorted(y_coor)
    # print(y_sort)

    # vertices = [(-81.9336023, 40.8134129), (-81.9333167, 40.8135786),
    #             (-81.9333188, 40.8134627), (-81.9336303, 40.8134555),
    #             (-81.9337162, 40.8133967), (-81.9337162, 40.8132444),
    #             (-81.9338552, 40.8132444), (-81.9338879, 40.8132444),
    #             (-81.9338878, 40.8135327), (-81.9338616, 40.813551),
    #             (-81.9338181, 40.8135814), (-81.9333555, 40.8135788),
    #             (-81.9333167, 40.8135786)]
    #
    # print(sorted(vertices))
    # print(len(vertices))
    #
    # for i in range(1, len(vertices), 1):
    #     j = i - 1
    #     # dist = math.hypot(x2 - x1, y2 - y1)
    #     # print(math.hypot())
    #     print(math.hypot(vertices[i][0] - vertices[j][0],
    #                      vertices[i][1] - vertices[j][1]) * 100000)

    # mpl.rcParams['legend.fontsize'] = 10
    #
    # fig = plt.figure()
    # ax = fig.gca(projection='3d')
    # theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
    # z = np.linspace(-2, 2, 100)
    # r = z ** 2 + 1
    # x = r * np.sin(theta)
    # y = r * np.cos(theta)
    # ax.plot(x, y, z, label='parametric curve')
    # ax.legend()

    # w = shapefile.Writer(shapeType=shapefile.POLYGONZ)
    # # OR you can type
    # # w = shapefile.Writer(shapeType=15)
    # w.poly([[[-89.0, 33, 12], [-90, 31, 11], [-91, 30, 12]]], shapeType=15)
    # w.field("NAME")
    # w.record("PolyZTest")
    # w.save("MyPolyZ")


    # /******************/
    # myshp = open("Shapefiles\MyPolyZ.shp", "rb")
    # r = shapefile.Reader(shp=myshp)
    # print(r.shapes()[0].points)
    # print(r.shapes()[0].z)
    # x_coors = []
    # y_coors = []
    # z_coors = []
    # for i in r.shapes():
    #     print(i.points)
    #     for j in i.points:
    #         x_coors.append(j[0])
    #         y_coors.append(j[1])
    #
    # for i in range(0, len(r.shapes()), 1):
    #     print(r.shapes()[i].z)

    # print(x_coors)
    # print(y_coors)

    # fig = plt.figure()
    # ax = fig.gca(projection='3d')
    # ax.scatter(x_coors, y_coors, r.shapes()[0].z)
    # plt.show()

    """
    MOTHERFUCKING WORKIN BITCH!!
    """
    # /******THIS CREATES 3D Objects WORKING TESTED IN ARCSCENE *********/

    # myshp = open("Shapefiles\CollegeCampus.shp", "rb")
    # mydbf = open("Shapefiles\CollegeCampus.dbf", "rb")
    # r = shapefile.Reader(shp=myshp, dbf=mydbf)
    # part = []
    # shapestype = list()
    # shapesrec = r.shapes()
    # # print(shapesrec[0].points)
    # floor = list()
    # ceiling = list()
    # for i in shapesrec[0].points:
    #     floor.append([i[0], i[1], 0])
    #     ceiling.append([i[0], i[1], 1])
    #
    # part.append(floor)
    # part.append(ceiling)
    # for i in range(1, len(floor), 1):
    #     j = i - 1
    #     surface = [floor[j], floor[j+1], ceiling[j], ceiling[j+1]]
    #     part.append(surface)
    #
    # for i in range(0, len(part), 1):
    #     shapestype.append(5)
    #
    # w = shapefile.Writer(shapeType=shapefile.MULTIPATCH)
    # w.autoBalance = 1
    # w.poly(parts=part,
    #     partTypes=shapestype,
    #     shapeType=31)
    # # w.field("NAME")
    # # w.record("CamZTest")
    # w.save("MyCampus")


    # *************************

    # # all_shapes_to_3d()
    # myshp = open(r"3D_temp.shp", "rb")
    # mydbf = open(r"3D_temp.dbf", "rb")
    # r = shapefile.Reader(shp=myshp, dbf=mydbf)
    #
    # # print(len(r.shapes()))
    # print(r.shapes()[0].points)

    # *******************************************************************
    # for shape in r.iterShapeRecords():
    #     print('SHAPE-----')
    #     temp = shape.shape.points[:]
    #     for i in temp:
    #         print([i[0], i[1], 5.0, 0.0])
    #         coors.extend([i[0], i[1], 5.0, 0.0])
    #         part.append([i[0], i[1], 5.0, 0.0])
    #         # temp = [i[0], i[1], 5]
    #         # all_shapes_z.append(temp)
    #         # all_shapes_z.append(temp)
    #         # temp = []
    #     # all_shapes_z.append(parts)
    #     # parts = []
    # print(part)
    # print(coors)
    # w.poly(parts=[part], shapeType=shapefile.POLYGONZ)
    # for i in coors:
    #     w.record(i)
    # w.poly(all_shapes_z, shapeType=15)
    #
    # # print(all_shapes_z)
    # # w.poly(all_shapes_z)
    # # w.field("NAME")
    # # w.record("PolyZTest")
    # w.save("CollegeCampusZ")


    #/******************/
    # x_coors = list()
    # y_coors = list()
    # z_ranges = list()
    # z_floor = list()
    #
    # r = shapefile.Reader('3D_temp')
    # # print(len(r.shapes()))
    # # for shape in r.shapes():
    # #     print('SHAPE-----')
    # #     for i in shape.points:
    # #         print(i)
    # #         x_coors.append(i[0])
    # #         y_coors.append(i[1])
    #
    # shape_var = r.shapes()[1].points
    #
    # for i in shape_var:
    #     x_coors.append(i[0])
    #     y_coors.append(i[1])
    #
    # for i in range(0, len(r.shapes()[1].z), 1):
    #     z_floor.append(0)
    #
    # z_ranges.append(r.shapes()[1].z)
    # z_ranges.append(z_floor)
    #
    # # ***WORKING FUNCTION ***
    # fig = plt.figure()
    # ax = fig.gca(projection='3d')
    # X = np.array(x_coors)
    # Y = np.array(y_coors)
    # Z = np.array(z_ranges)
    # ax.plot_surface(X, Y, Z, color='b')
    # plt.show()

    # all_shapes_to_3d()
    # setup_3d_scene()
    fig = plt.figure(figsize=plt.figaspect(0.5))
    ax = fig.gca(projection='3d')
    myshp = open("3D_temp.shp", "rb")
    mydbf = open("3D_temp.dbf", "rb")
    r = shapefile.Reader(shp=myshp, dbf=mydbf)
    shapes = r.shapes()
    # for i in range(0, len(shapes), 1):
    #     print shapes[i].shapeType

    # vart = r.shapes()[5]
    # flat_z_surfaces = list()
    # flat_xy_surfaces = list()
    # print len(vart.parts)
    # for i in range(1, len(vart.parts), 1):
    #     j = i - 1
    #     print "SECTION_____" + str(j)
    #     print vart.parts[j]
    #     xy_coors = vart.points[vart.parts[j]:vart.parts[i]]
    #     z_it = vart.z[vart.parts[j]:vart.parts[i]]
    #
    #     if all(x==z_it[0] for x in z_it) is True:
    #         flat_z_surfaces.append(z_it)
    #         flat_xy_surfaces.append(xy_coors)
    #
    #     else:
    #         pass
    #         # not flat surface
    #         x_coors = list()
    #         y_coors = list()
    #         z_coors = list()
    #         z_floor = list()
    #         z_ceiling = list()
    #         z_ranges = list()
    #         for i in range(0, len(xy_coors), 1):
    #             x_coors.append(xy_coors[i][0])
    #             y_coors.append(xy_coors[i][1])
    #             z_coors.append(z_it[i])
    #
    #         for k in range(len(z_coors)):
    #             z_floor.append(min(z_coors))
    #             z_ceiling.append(max(z_coors))
    #
    #         z_ranges.append(z_floor)
    #         z_ranges.append(z_ceiling)
    #         # fig.add_subplot(projection='3d')
    #         x = np.array(x_coors)
    #         y = np.array(y_coors)
    #         z = np.array(z_ranges)
    #         ax.plot_surface(x, y, z)

        # for k in range(0, len(flat_z_surfaces), 1):
        #     x_coors = list()
        #     y_coors = list()
        #     z_coors = list()
        #
        #     for i in range(0, len(flat_xy_surfaces[k]), 1):
        #         x_coors.append(flat_xy_surfaces[k][i][0])
        #         y_coors.append(flat_xy_surfaces[k][i][1])
        #         z_coors.append(flat_z_surfaces[k][i])
        #
        #     verts = [zip(x_coors, y_coors, z_coors)]
        #     # ax.add_collection3d(Poly3DCollection(verts))

    # plt.show()


if __name__ == '__main__':
    main()

# w = shapefile.Writer(shapeType=shapefile.MULTIPATCH)
# w.poly(parts=[
# [[0,0,0], [0,1,0], [0,1,1], [0,0,1], [0,0,0]],
# [[0,0,0], [0,0,1], [1,0,1], [1,0,0], [0,0,0]],
# [[1,1,0], [1,1,1], [0,1,1], [0,1,0], [1,1,0]],
# [[1,0,0], [1,0,1], [1,1,1], [1,1,0], [1,0,0]],
# [[0,0,1], [0,1,1], [1,1,1], [1,0,1], [0,0,1]],
# [[0,0,0], [0,1,0], [1,1,0], [1,0,0], [0,0,0]]
# ],
#         partTypes=[5,5,5,5,5,5],
#         shapeType=31)
# w.field("NAME")
# w.record("PolyZTest")
# w.save("MyPolyS")
