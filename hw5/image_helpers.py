"""
CMSC 14100
Winter 2023

Functions for reading and writing images in PPM P3 format.
"""

import os
import sys

def load_image(filename):
    """
    Load a file that is formatted using PPM P3 format.

    Input:
        filename (string): the name of the file containing the image

    Returns: list of lists of colors
    """
    try:
        f = os.path.exists(filename)
    except OSError:
        print(f"Cannot open {filename}")
        sys.exit(1)

    f = open(filename, "r")

    ppm_type = f.readline().strip()
    if ppm_type != "P3":
        print("Wrong file type. This function only loads P3 PPMs\n",
              file=sys.stderr)
        sys.exit(1)

    width, height = (int(x) for x in f.readline().strip().split())
    # We have no use for the max color
    _ = int(f.readline())

    rgbs = [int(x) for x in f.read().split()]
    assert len(rgbs) == height*width*3

    img = []
    rgbs_index = 0
    for _ in range(height):
        row = []
        for _ in range(width):
            row.append(tuple(rgbs[rgbs_index:rgbs_index + 3]))
            rgbs_index += 3
        img.append(row)

    f.close()
    return img


def write_image(filename, img):
    """
    Write an image to a file in P3 PPM format

    Input:
        filename (string): the name of the file to write
        image (list of lists of colors): the image to write to the file
    """
    try:
        f = open(filename, "w")
    except OSError:
        print(f"Cannot open {filename}")
        sys.exit(1)

    print("P3", file=f)
    # output width height
    print(f"{len(img[0])} {len(img)}", file=f)
    print("255", file=f)
    for row in img:
        flatten = []
        for color in row:
            flatten.extend([str(c) for c in color])
        print(" ".join(flatten), file=f)
    f.close()
