from pathlib import Path
from typing import TextIO

import click


def validate_file(ctx: click.Context, param: click.Parameter, path: Path) -> Path:
    """Callback for file validation"""
    with open(path) as file:
        if is_valid(file):
            return path
        else:
            raise click.BadParameter("invalid file format")


def is_valid(file: TextIO) -> bool:
    """
    Validates file according to format:

        <number of nodes>
        <id of node>
        ...
        <id of node>
        <number of edges>
        <from node id> <to node id> <length in meters>
        ...
        <from node id> <to node id> <length in meters>
    """
    nodes_count = next(file).rstrip()
    if not nodes_count.isdigit():
        return False

    for _ in range(int(nodes_count)):
        nodes_per_line = next(file).split()
        if len(nodes_per_line) != 1:
            return False

    edges_count = next(file).rstrip()
    if not edges_count.isdigit():
        return False

    for _ in range(int(edges_count)):
        edge = next(file).split()
        if len(edge) != 3:
            return False

        *_, weight = edge
        if weight.isdigit() and int(weight) < 0:
            return False

    return True
