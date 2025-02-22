import dataclasses
from typing import Any, Dict, List

from qulacsvis.visualization.circuit_parser import CircuitData


def dataclasses_to_dict(circuit: CircuitData) -> List[List[Dict[str, Any]]]:
    res = []
    for gates in circuit:
        gate_dicts = []
        for gate in gates:
            gate_dicts.append(dataclasses.asdict(gate))
        res.append(gate_dicts)
    return res
