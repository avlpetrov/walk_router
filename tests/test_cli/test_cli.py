import subprocess

import pytest

from src.graph import NodeID


@pytest.mark.parametrize(
    "path, from_node_id, to_node_id, expected_code",
    # fmt: off
    [
        # Path exists in a graph.
        ("./tests/test_cli/sample_graph", "A", "C", 0),

        # Path doesn't exist in a graph.
        ("./tests/test_cli/sample_graph", "X", "Y", 0),

        # Invalid parameters.
        ("./tests/test_cli/sample_graph", "X", "", 2),
        ("./tests/test_cli/sample_graph", "", "Y", 2),
        ("./tests/test_cli/sample_graph", "", "", 2),
        ("file_that_doesnt_exist", "A", "B", 2),
    ]
    # fmt: on
)
def test_run_script(
    path: str, from_node_id: NodeID, to_node_id: NodeID, expected_code: int
) -> None:
    result = subprocess.run(f"./run.sh {path} {from_node_id} {to_node_id}", shell=True)
    assert result.returncode == expected_code
