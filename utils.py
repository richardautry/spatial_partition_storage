"""
Utility functions primarily for graphing objects in jupyter notebook
"""

import plotly.graph_objects as go
import numpy as np
import random
from typing import List
from itertools import product


def get_box_min_max(box_range: List[int]):
    """
    Get random min/max values for a given range.
    Ensures that max is always larger than min.
    :param box_range:
    :return:
    """
    if not box_range:
        raise Exception("'box_range' with length > 0 required.")

    if len(box_range) == 1:
        return box_range[0], box_range[0]

    index_range = list(range(len(box_range)))
    # Min value cannot be the last element in the range
    min_index = random.choice(index_range[:-1])
    # Max value must be larger than min, and min value cannot be a candidate
    max_index = random.choice(index_range[min_index + 1:])

    return box_range[min_index], box_range[max_index]


def get_box_points_array(x_min, x_max, y_min, y_max, z_min, z_max):
    return np.array([
        [x_min, x_min, x_max, x_max, x_min, x_min, x_max, x_max, ],
        [y_min, y_max, y_max, y_min, y_min, y_max, y_max, y_min, ],
        [z_min, z_min, z_min, z_min, z_max, z_max, z_max, z_max, ]
    ])


def generate_box(**kwargs):
    default_values = {
        "min": 0,
        "max": 1
    }
    x_range_min = kwargs.get("x", default_values).get("min")
    x_range_max = kwargs.get("x", default_values).get("max")
    y_range_min = kwargs.get("y", default_values).get("min")
    y_range_max = kwargs.get("y", default_values).get("max")
    z_range_min = kwargs.get("z", default_values).get("min")
    z_range_max = kwargs.get("z", default_values).get("max")

    x_min, x_max = get_box_min_max(list(range(x_range_min, x_range_max)))
    y_min, y_max = get_box_min_max(list(range(y_range_min, y_range_max)))
    z_min, z_max = get_box_min_max(list(range(z_range_min, z_range_max)))

    return get_box_points_array(x_min, x_max, y_min, y_max, z_min, z_max)


def get_box_arg_name(dimension: str, range_type: str):
    if range_type not in ["min", "max"]:
        raise Exception("Unknown 'range_type'")
    return f"{dimension}_range_{range_type}"


def generate_box_per_partition(min_range: int, max_range: int, partition_size: int, dimensions: List[str]):
    def get_dimension_args(dimension_name, range_min, range_max, step):
        return [{dimension_name: {"min": i, "max": i + step}} for i in range(range_min, range_max, step)]

    # Prep box kwargs with default values
    # for i in range(min_range, max_range, partition_size):
    #     for dimension in dimensions:
    #         for j in range(min_range, max_range, partition_size):
    #             box_kwargs = {dimension: {"min": i, "max": i + partition_size} for dimension in dimensions}
    #             for key_dimension, _ in box_kwargs.items():
    #                 if key_dimension != dimension:
    #                     box_kwargs[key_dimension]["min"] = j
    #                     box_kwargs[key_dimension]["max"] = j + partition_size
    #             yield box_kwargs
    dimension_args = [get_dimension_args(dimension, min_range, max_range, partition_size) for dimension in dimensions]
    all_args = product(*dimension_args)
    for args_output in all_args:
        yield_args = {}
        for args_dict in args_output:
            yield_args.update(args_dict)
        yield yield_args


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
