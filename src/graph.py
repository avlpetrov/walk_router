from collections import defaultdict
from dataclasses import dataclass, field
from math import inf
from pathlib import Path
from queue import PriorityQueue
from typing import Any, Dict, Union

Distance = Union[int, float]
NodeID = str


class UndirectedGraph:
    def __init__(self) -> None:
        self.nodes: Dict[NodeID, GraphNode] = {}

    def add_node(self, id_: NodeID) -> None:
        self.nodes[id_] = GraphNode(id_)

    def has_node(self, id_: NodeID) -> bool:
        return id_ in self.nodes

    def add_edge(self, from_node_id: NodeID, to_node_id: NodeID, weight: int) -> None:
        if from_node_id not in self.nodes:
            self.add_node(from_node_id)

        if to_node_id not in self.nodes:
            self.add_node(to_node_id)

        self.nodes[from_node_id].add_edge(to_node_id, weight)
        self.nodes[to_node_id].add_edge(from_node_id, weight)

    def find_shortest_distance(
        self, from_node_id: NodeID, to_node_id: NodeID
    ) -> Distance:
        """
        Finds shortest distance between nodes if path exists,
        returns infinity otherwise.

        Args:
            from_node_id: Node to start search from.
            to_node_id: Node to find shortest path to.

        Returns:
            shortest_distance or inf
        """
        if self.has_node(from_node_id) and self.has_node(to_node_id):
            distances = self._dijkstra_shortest_distance(from_node_id, to_node_id)
            shortest_distance = distances[to_node_id]
            return shortest_distance

        return inf

    def _dijkstra_shortest_distance(
        self, from_node_id: NodeID, to_node_id: NodeID
    ) -> Dict[NodeID, Distance]:
        """
        Implementation of Dijkstra single-destination shortest path search.
        Search stops once target node is reached.

        Returns a mapping of node id to it's shortest distance.
        """
        node_id_to_distance: Dict[NodeID, Distance] = defaultdict(lambda: inf)
        node_id_to_distance[from_node_id] = 0
        visited_nodes_ids = set()

        pqueue: PriorityQueue[PrioritizedNode] = PriorityQueue()
        pqueue.put(PrioritizedNode(priority=0, node=self.nodes[from_node_id]))

        while not pqueue.empty():
            current = pqueue.get()
            if current.node.id not in visited_nodes_ids:
                visited_nodes_ids.add(current.node.id)

                if current.node.id == to_node_id:
                    break

                for adjacent_id, weight in current.node.adjacent_to_weight.items():
                    if adjacent_id not in visited_nodes_ids:
                        new_distance = node_id_to_distance[current.node.id] + weight
                        if new_distance < node_id_to_distance[adjacent_id]:
                            node_id_to_distance[adjacent_id] = new_distance

                            pqueue.put(
                                PrioritizedNode(
                                    priority=new_distance, node=self.nodes[adjacent_id]
                                )
                            )

        return node_id_to_distance

    @classmethod
    def build_from_file(cls, path: Path) -> "UndirectedGraph":
        """
        Builds undirected graph from specified file.

        Expected file format:

            <number of nodes>
            <id of node>
            ...
            <id of node>
            <number of edges>
            <from node id> <to node id> <length in meters>
            ...
            <from node id> <to node id> <length in meters>

        Args:
            path: Path to file representation of graph.

        Returns:
            graph: Undirected graph with non-negative weights.
        """
        graph = UndirectedGraph()
        with open(path) as file:
            nodes_count = next(file)
            for _ in range(int(nodes_count)):
                node_id = next(file).rstrip()
                graph.add_node(node_id)

            edges_count = next(file)
            for _ in range(int(edges_count)):
                from_node_id, to_node_id, length = next(file).split()
                graph.add_edge(from_node_id, to_node_id, weight=int(length))

        return graph


class GraphNode:
    def __init__(self, id_: NodeID) -> None:
        self.id = id_
        self.adjacent_to_weight: Dict[NodeID, int] = {}

    def add_edge(self, to_node_id: NodeID, weight: int) -> None:
        self.adjacent_to_weight[to_node_id] = weight


@dataclass(order=True)
class PrioritizedNode:
    priority: int
    node: Any = field(compare=False)
