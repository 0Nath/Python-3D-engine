import numpy
from stl import mesh
from math import cos, sin,radians


def load_stl(filename, color):
    stl = mesh.Mesh.from_file(filename)
    converted = [[[], []], color]
    points_dict = {}  
    points_list = []
    size = len(stl.points)

    print("Loading points")
    for j, i in enumerate(stl.points):

        coords = [
            (float(i[0]), float(i[1]), float(i[2])),
            (float(i[3]), float(i[4]), float(i[5])),
            (float(i[6]), float(i[7]), float(i[8]))
        ]


        for coord in coords:
            if coord not in points_dict:
                points_dict[coord] = len(points_list)
                points_list.append(coord)

        if j % 100 == 0:
            print(round(j * 100 / size), "%", end="\r", flush=True)

    print("\npoints loaded\n")
    converted[0][0] = points_list

    print("Loading triangles")
    for j, i in enumerate(stl.points):

        coords = [
            (float(i[0]), float(i[1]), float(i[2])),
            (float(i[3]), float(i[4]), float(i[5])),
            (float(i[6]), float(i[7]), float(i[8]))
        ]


        indices = [points_dict[coord] for coord in coords]
        converted[0][1].append(indices)

        if j % 100 == 0:
            print(round(j * 100 / size), "%", end="\r", flush=True)

    print("\ntriangles loaded")
    return converted


class Mesh_from_stl:

    def __init__(self, filename, color):
        mesh = load_stl(filename,color)

        self.points = mesh[0]
        print(len(self.points[1]),"points loaded")
        self.color = mesh[1]
        self.Z = radians(90)
        m1 = numpy.array([[cos(self.Z), 0, -sin(self.Z)], [0, 1, 0], [sin(self.Z), 0, cos(self.Z)]])
        r = []
        for p in self.points[0]:
            rot = numpy.dot(m1, numpy.array([[p[0]], [p[1]], [p[2]]]))
            r.append((rot[0][0], rot[1][0], rot[2][0]))
        self.points[0] = r

    def get_points(self):
        return self.points

    def get_color(self):
        return self.color

    def give_coordinates(self, coords):
        pass
