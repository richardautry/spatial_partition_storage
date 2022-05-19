"""
Utility functions primarily for graphing objects in jupyter notebook
"""

import plotly.graph_objects as go
import numpy as np
import random
from typing import List


def get_box_min_max(box_range: List[int]):
    index_range = list(range(len(box_range)))
    min_index = random.choice(index_range)
    del index_range[min_index]
    max_index = random.choice(index_range)

    return box_range[min_index], box_range[max_index]


def get_box_points_array(x_min, x_max, y_min, y_max, z_min, z_max):
    return np.array([
        [x_min, x_min, x_max, x_max, x_min, x_min, x_max, x_max, ],
        [y_min, y_max, y_max, y_min, y_min, y_max, y_max, y_min, ],
        [z_min, z_min, z_min, z_min, z_max, z_max, z_max, z_max, ]
    ])


def generate_box(range_min, range_max):
    box_range = list(range(range_min, range_max))

    x_min, x_max = get_box_min_max(box_range)
    y_min, y_max = get_box_min_max(box_range)
    z_min, z_max = get_box_min_max(box_range)

    return get_box_points_array(x_min, x_max, y_min, y_max, z_min, z_max)


def add_3d_line(fig, coordinates: np.array):
    fig.add_trace(
        go.Scatter3d(
            x=coordinates[0],
            y=coordinates[1],
            z=coordinates[2],
            marker={
                "size": 4,
                "color": [0, 1],
                "colorscale": "Bluyl"
            }
))


def add_mesh_3d(fig, coordinates: np.array, name=None):
    fig.add_trace(
        go.Mesh3d(
            # 8 vertices of a cube
            x=coordinates[0],
            y=coordinates[1],
            z=coordinates[2],
            colorbar_title='z',
            colorscale=[[0, 'gold'],
                        [0.5, 'mediumturquoise'],
                        [1, 'magenta']],
            # Intensity of each vertex, which will be interpolated and color-coded
            intensity = np.linspace(0, 1, 8, endpoint=True),
            # i, j and k give the vertices of triangles
            i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
            j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
            k = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
            name=name,
            flatshading=True
        )
    )
