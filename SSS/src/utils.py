import glob
from ase.io import read, write
from ase.geometry import cellpar_to_cell
import numpy as np
import os
from collections import defaultdict


def load_structures(xyz_path):
    return read(xyz_path, index=":")


def make_output_dir(base, split_name):
    path = f"{base}_{split_name}"
    os.makedirs(path, exist_ok=True)
    return path


def grid_select(projections: np.ndarray, divisions: int, seed: int):
    mins, maxs = projections.min(0), projections.max(0)
    sizes = (maxs - mins) / divisions
    grid = defaultdict(list)
    for idx, (x, y) in enumerate(projections):
        i = int((x - mins[0]) // sizes[0])
        j = int((y - mins[1]) // sizes[1])
        grid[(i, j)].append(idx)
    np.random.seed(seed)
    selected = sorted(np.random.choice(vals, 1)[0] for vals in grid.values())
    return selected
