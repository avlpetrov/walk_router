from math import isinf
from pathlib import Path

import click

from src.graph import NodeID, UndirectedGraph
from src.utils import validate_file


@click.command()
@click.argument("path", type=click.Path(exists=True), callback=validate_file)
@click.argument("from_node_id")
@click.argument("to_node_id")
def main(path: Path, from_node_id: NodeID, to_node_id: NodeID) -> None:
    """Finds shortest distance between nodes in graph if path exists."""
    graph = UndirectedGraph.build_from_file(path)
    shortest_distance = graph.find_shortest_distance(from_node_id, to_node_id)
    if isinf(shortest_distance):
        print("No path between nodes")
    else:
        print(shortest_distance)


if __name__ == "__main__":
    main()
