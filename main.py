from sphere import *


def inputRadius():
    radius = float(raw_input("Radius of Sphere: "))
    return radius

def inputPlatonic():
    divisions = int(raw_input("Number of Divisions: "))
    return divisions, inputRadius()

def inputUV():
    rings = int(raw_input("Number of Rings: "))
    segments = int(raw_input("Number of Segments: "))
    return rings, segments, inputRadius()


def main():
    modes = "\tO - OctaSphere\n\tI - IcoSphere\n\tU - UVSphere\n"
    mode = raw_input("Blender 3D Sphere Generator\n" + modes + "Enter Mode: ")
    if mode.upper() in ["O", "I", "U"]:
        if mode.upper() == "O":
            divisions, radius = inputPlatonic()
            sphere = OctaSphere(divisions, radius)
        elif mode.upper() == "I":
            divisions, radius = inputPlatonic()
            sphere = IcoSphere(divisions, radius)
        else:
            rings, segments, radius = inputUV()
            sphere = UVSphere(rings, segments, radius)
        sphere.save()
        raw_input("Operation Successful")
    else:
        raw_input("\nERROR - Invalid Mode")


if __name__ == "__main__":
    main()
