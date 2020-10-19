from math import inf

import pytest

from src.graph import Distance, NodeID, UndirectedGraph


@pytest.fixture(scope="module")
def fixtured_graph() -> UndirectedGraph:
    graph = UndirectedGraph()
    graph.add_edge("A", "B", weight=2)
    graph.add_edge("A", "C", weight=4)
    graph.add_edge("B", "C", weight=1)
    graph.add_edge("C", "D", weight=3)
    graph.add_edge("B", "D", weight=5)
    graph.add_edge("D", "E", weight=6)
    graph.add_edge("D", "F", weight=8)
    return graph


@pytest.mark.parametrize(
    "from_node_id, to_node_id, expected_distance",
    # fmt: off
    [
        ("A", "A", 0),
        ("A", "F", 14),
        ("F", "A", 14),
        ("B", "E", 10),
        ("A", "Z", inf),
        ("X", "Y", inf),
    ]
    # fmt: on
)
def test_find_shortest_distance(
    from_node_id: NodeID,
    to_node_id: NodeID,
    expected_distance: Distance,
    fixtured_graph: UndirectedGraph,
) -> None:
    shortest_distance = fixtured_graph.find_shortest_distance(from_node_id, to_node_id)
    assert shortest_distance == expected_distance
