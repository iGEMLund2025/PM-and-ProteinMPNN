#Description:
#Extracts the coordinates of a box around a selection of residues

from pymol import cmd
from pymol.cgo import BEGIN, LINES, COLOR, VERTEX, END

def draw_bounding_box(selection="known_binding_site"):
    # Step 1: Get extent (bounding box corners)
    min_coords, max_coords = cmd.get_extent(selection)

    print("Bounding Box:")
    print(f"  Min coords: {min_coords}")
    print(f"  Max coords: {max_coords}")

    # Step 2: Compute center and size
    center = [(min_coords[i] + max_coords[i]) / 2.0 for i in range(3)]
    size = [max_coords[i] - min_coords[i] for i in range(3)]

    print("\nUse these for docking:")
    print(f"  Center     = {center}")
    print(f"  Box size   = {size}")

    # Step 3: Draw box using CGO
    x0, y0, z0 = min_coords
    x1, y1, z1 = max_coords

    edges = [
        (x0, y0, z0, x1, y0, z0),
        (x0, y0, z0, x0, y1, z0),
        (x0, y0, z0, x0, y0, z1),
        (x1, y1, z1, x0, y1, z1),
        (x1, y1, z1, x1, y0, z1),
        (x1, y1, z1, x1, y1, z0),
        (x0, y1, z0, x1, y1, z0),
        (x0, y1, z0, x0, y1, z1),
        (x0, y0, z1, x1, y0, z1),
        (x0, y0, z1, x0, y1, z1),
        (x1, y0, z0, x1, y1, z0),
        (x1, y0, z0, x1, y0, z1),
    ]

    box_obj = [BEGIN, LINES, COLOR, 1.0, 1.0, 1.0]  # White box
    for e in edges:
        box_obj.extend([VERTEX, *e[:3], VERTEX, *e[3:]])
    box_obj.append(END)

    cmd.load_cgo(box_obj, "bounding_box")

# Run the function on 'known_binding_site'
draw_bounding_box()