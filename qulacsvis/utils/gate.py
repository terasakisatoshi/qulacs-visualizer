__TO_LATEX_STYLE_GATESTR_MAP = {
    "": "",
    "I": "I",
    "X": "X",
    "Y": "Y",
    "Z": "Z",
    "H": "H",
    "S": "S",
    "Sdag": r"S^\dag",
    "T": "T",
    "Tdag": r"T^\dag",
    "sqrtX": r"\sqrt{X}",
    "sqrtXdag": r"\sqrt{X^\dag}",
    "sqrtY": r"\sqrt{Y}",
    "sqrtYdag": r"\sqrt{Y^\dag}",
    "Projection-0": "P0",
    "Projection-1": "P1",
    "U1": "U1",
    "U2": "U2",
    "U3": "U3",
    "X-rotation": "RX",
    "Y-rotation": "RY",
    "Z-rotation": "RZ",
    "Pauli": "Pauli",
    "Pauli-rotation": "PR",
    "CZ": "CZ",
    "CNOT": r"\targ",
    "SWAP": "SWAP",
    "Reflection": "Ref",
    "ReversibleBoolean": "ReB",
    "DenseMatrix": "DeM",
    "DinagonalMatrix": "DiM",
    "SparseMatrix": "SpM",
    "Generic gate": "GeG",
    "ParametricRX": "pRX",
    "ParametricRY": "pRY",
    "ParametricRZ": "pRZ",
    "ParametricPauliRotation": "pPR",
}


def to_latex_style(gate_name: str) -> str:
    """Get string for latex from gate name.

    Parameters
    ----------
    gate_name : str
        Gate name.

    Returns
    -------
    str
        string for LaTex.

    Raises
    ------
    KeyError
        If gate name is not found.
    """
    return __TO_LATEX_STYLE_GATESTR_MAP[gate_name]
