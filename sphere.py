import bisect
import math


class Sphere:
    def __init__(self, faces, radius):
        vertices = self.getVertices(faces)
        print "\nNumber of Vertices: " + str(len(vertices))
        self.faces = self.matchVerticesToFaces(vertices, faces)
        print "Number of Faces: " + str(len(self.faces)) + "\n"
        self.vertices = self.changeRadius(vertices, radius)
    def getVertices(self, faces):
        newVertices = []
        for vertices in faces:
            for vertex in vertices:
                newVertices.append(vertex)
        return sorted(set(newVertices))
    def matchVerticesToFaces(self, lookupVertices, faces):
        newFaces = []
        for vertices in faces:
            newVertices = []
            for vertex in vertices:
                newVertices.append(bisect.bisect(lookupVertices, vertex) - 1)
            newFaces.append(tuple(newVertices))
        return newFaces
    def changeRadius(self, vertices, radius):
        newVertices = []
        for x, y, z in vertices:
            newVertices.append((x * radius, y * radius, z * radius))
        return newVertices
    def save(self, fileName):
        with open(fileName, "w") as f:
            f.write("import bpy\n\n\n")
            f.write("# Total " + str(len(self.vertices)) + " vertices\n")
            f.write("vertices = []\n\n")
            for vertex in self.vertices:
                f.write("vertices.append(" + str(vertex) + ")\n")
            f.write("\n\n# Total " + str(len(self.faces)) + " faces\n")
            f.write("faces = []\n\n")
            for face in self.faces:
                f.write("faces.append(" + str(face) + ")\n")
            f.write("\n\nmesh = bpy.data.meshes.new(\"sphere\")\n")
            f.write("object = bpy.data.objects.new(\"sphere\", mesh)\n\n")
            f.write("object.location = bpy.context.scene.cursor_location\n")
            f.write("bpy.context.scene.objects.link(object)\n\n")
            f.write("mesh.from_pydata(vertices, [], faces)\n")
            f.write("mesh.update(calc_edges=True)\n")

class PlatonicSphere(Sphere):
    def __init__(self, faces, divisions, radius):
        for i in xrange(divisions):
            faces = self.divide(faces)
        Sphere.__init__(self, faces, radius)
        self.divisions = divisions
    def middle(self, v1, v2):
        x1, y1, z1 = v1
        x2, y2, z2 = v2
        xm = (x1 + x2) / 2
        ym = (y1 + y2) / 2
        zm = (z1 + z2) / 2
        size = (xm ** 2 + ym ** 2 + zm ** 2) ** 0.5
        return xm / size, ym / size, zm / size
    def divide(self, faces):
        newFaces = []
        for v1, v2, v3 in faces:
            m1 = self.middle(v1, v2)
            m2 = self.middle(v2, v3)
            m3 = self.middle(v3, v1)
            newFaces.append((v1, m1, m3))
            newFaces.append((v2, m2, m1))
            newFaces.append((v3, m3, m2))
            newFaces.append((m1, m2, m3))
        return newFaces
    def save(self, prefix):
        fileName = prefix + "Sphere " + str(self.divisions) + ".py"
        Sphere.save(self, fileName)

class OctaSphere(PlatonicSphere):
    def __init__(self, divisions, radius):
        v1 = (1.0, 0, 0)
        v2 = (0, 1.0, 0)
        v3 = (0, 0, 1.0)
        v4 = (-1.0, 0, 0)
        v5 = (0, -1.0, 0)
        v6 = (0, 0, -1.0)
        faces = []
        faces.append((v1, v2, v3))
        faces.append((v2, v4, v3))
        faces.append((v4, v5, v3))
        faces.append((v5, v1, v3))
        faces.append((v6, v2, v1))
        faces.append((v6, v4, v2))
        faces.append((v6, v5, v4))
        faces.append((v6, v1, v5))
        PlatonicSphere.__init__(self, faces, divisions, radius)
    def save(self):
        PlatonicSphere.save(self, "Octa")

class IcoSphere(PlatonicSphere):
    def __init__(self, divisions, radius):
        phi1 = 2 / (10 + 2 * 5 ** 0.5) ** 0.5
        phi2 = (1 + 5 ** 0.5) / (10 + 2 * 5 ** 0.5) ** 0.5
        v1 = (phi2, phi1, 0)
        v2 = (phi2, -phi1, 0)
        v3 = (-phi2, phi1, 0)
        v4 = (-phi2, -phi1, 0)
        v5 = (0, phi2, phi1)
        v6 = (0, phi2, -phi1)
        v7 = (0, -phi2, phi1)
        v8 = (0, -phi2, -phi1)
        v9 = (phi1, 0, phi2)
        v10 = (-phi1, 0, phi2)
        v11 = (phi1, 0, -phi2)
        v12 = (-phi1, 0, -phi2)
        faces = []
        faces.append((v3, v10, v5))
        faces.append((v11, v8, v12))
        faces.append((v1, v11, v6))
        faces.append((v10, v7, v9))
        faces.append((v9, v2, v1))
        faces.append((v4, v8, v7))
        faces.append((v1, v2, v11))
        faces.append((v4, v3, v12))
        faces.append((v6, v12, v3))
        faces.append((v10, v3, v4))
        faces.append((v2, v7, v8))
        faces.append((v12, v6, v11))
        faces.append((v8, v11, v2))
        faces.append((v6, v5, v1))
        faces.append((v4, v12, v8))
        faces.append((v9, v5, v10))
        faces.append((v7, v10, v4))
        faces.append((v2, v9, v7))
        faces.append((v5, v6, v3))
        faces.append((v5, v9, v1))
        PlatonicSphere.__init__(self, faces, divisions, radius)
    def save(self):
        PlatonicSphere.save(self, "Ico")

class UVSphere(Sphere):
    def __init__(self, rings, segments, radius):
        faces = []
        phiTop = math.pi - math.pi / rings
        v1 = self.unitCartesian(math.pi, 0)
        for j in xrange(segments - 1):
            thetaCurrent = 2 * j * math.pi / segments
            thetaNext = 2 * (j + 1) * math.pi / segments
            v2 = self.unitCartesian(phiTop, thetaNext)
            v3 = self.unitCartesian(phiTop, thetaCurrent)
            faces.append((v1, v2, v3))
        thetaLast = 2 * (segments - 1) * math.pi / segments
        v2 = self.unitCartesian(phiTop, 0)
        v3 = self.unitCartesian(phiTop, thetaLast)
        faces.append((v1, v2, v3))
        for i in xrange(1, rings - 1):
            phiBottom = math.pi - i * math.pi / rings
            phiTop = math.pi - (i + 1) * math.pi / rings
            for j in xrange(segments - 1):
                thetaCurrent = 2 * j * math.pi / segments
                thetaNext = 2 * (j + 1) * math.pi / segments
                v1 = self.unitCartesian(phiBottom, thetaCurrent)
                v2 = self.unitCartesian(phiBottom, thetaNext)
                v3 = self.unitCartesian(phiTop, thetaNext)
                v4 = self.unitCartesian(phiTop, thetaCurrent)
                faces.append((v1, v2, v3, v4))
            thetaLast = 2 * (segments - 1) * math.pi / segments
            v1 = self.unitCartesian(phiBottom, thetaLast)
            v2 = self.unitCartesian(phiBottom, 0)
            v3 = self.unitCartesian(phiTop, 0)
            v4 = self.unitCartesian(phiTop, thetaLast)
            faces.append((v1, v2, v3, v4))
        phiBottom = math.pi - (rings - 1) * math.pi / rings
        v1 = self.unitCartesian(0, 0)
        for j in xrange(segments - 1):
            thetaCurrent = 2 * j * math.pi / segments
            thetaNext = 2 * (j + 1) * math.pi / segments
            v2 = self.unitCartesian(phiBottom, thetaCurrent)
            v3 = self.unitCartesian(phiBottom, thetaNext)
            faces.append((v1, v2, v3))
        thetaLast = 2 * (segments - 1) * math.pi / segments
        v2 = self.unitCartesian(phiBottom, thetaLast)
        v3 = self.unitCartesian(phiBottom, 0)
        faces.append((v1, v2, v3))
        Sphere.__init__(self, faces, radius)
        self.rings = rings
        self.segments = segments
    def unitCartesian(self, phi, theta):
        x = math.sin(phi) * math.cos(theta)
        y = math.sin(phi) * math.sin(theta)
        z = math.cos(phi)
        return x, y, z
    def save(self):
        fileName = "UVSphere " + str(self.rings) + "R "
        fileName += str(self.segments) + "S.py"
        Sphere.save(self, fileName)
