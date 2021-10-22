from typing import List, Optional, Tuple

from matplotlib import patches
from matplotlib import pyplot as plt
from qulacs import QuantumCircuit
from typing_extensions import Final, TypedDict

GATE_DEFAULT_WIDTH = 1
GATE_DEFAULT_HEIGHT = 1
GATE_MARGIN_RIGHT = 0.5


GateData = TypedDict(
    "GateData",
    {
        "text": str,
        "width": float,
        "height": float,
        "raw_text": str,
        "control_bit": Optional[List[int]],
        "size": int,
    },
)
CircuitData = List[List[GateData]]

PORDER_GATE: Final[int] = 5
PORDER_LINE: Final[int] = 3
PORDER_REGLINE: Final[int] = 2
PORDER_GRAY: Final[int] = 3
PORDER_TEXT: Final[int] = 6


class MPLCircuitlDrawer:
    def __init__(self, circuit: QuantumCircuit):
        self._figure = plt.figure()
        self._ax = self._figure.add_subplot(111)
        self._ax.axis("on")
        self._ax.grid()
        self._ax.set_aspect("equal")
        self._figure.set_size_inches(18.5, 10.5)

        self._circuit = circuit
        self._circuit_data = parse_circuit(self._circuit)

    def draw(self):  # type: ignore
        self._ax.set_xlim(-3, 15)
        self._ax.set_ylim(15, -1)  # (max, min)にすると吊り下げになる

        # for col in range(10):
        #     for row in range(10):
        #         self._gate(col,row,0)
        GATE_RIGHT_MARGIN = 0.5
        max_line_length = (
            max([len(line) for line in self._circuit_data])
            * (GATE_DEFAULT_WIDTH + GATE_RIGHT_MARGIN)
            - GATE_RIGHT_MARGIN
        )
        for i, line in enumerate(self._circuit_data):
            line_ypos = i * (GATE_DEFAULT_HEIGHT + GATE_RIGHT_MARGIN)
            self._text(
                -2,
                line_ypos,
                "$q_{" + str(i) + "}$",
                fontsize=20,
            )

            self._line(
                (-1, line_ypos),
                (
                    max_line_length,
                    line_ypos,
                ),
            )

            for j, gate in enumerate(line):
                if gate["raw_text"] == "CNOT":
                    self._cnot(gate, i, j)
                elif gate["raw_text"] == "ghost":
                    continue
                elif gate["size"] > 1:
                    self._multi_gate(gate, i, j)
                else:
                    self._gate(gate, i, j)

        return self._figure

    def _line(
        self,
        from_xy: Tuple[float, float],
        to_xy: Tuple[float, float],
        lc: str = "k",
        ls: str = "-",
        lw: float = 3.0,
        zorder: int = PORDER_LINE,
    ) -> None:
        from_x, from_y = from_xy
        to_x, to_y = to_xy
        self._ax.plot(
            [from_x, to_x],
            [from_y, to_y],
            color=lc,
            linestyle=ls,
            linewidth=lw,
            zorder=zorder,
        )

    def _text(
        self,
        x: float,
        y: float,
        text: str,
        horizontalalignment: str = "center",
        verticalalignment: str = "center",
        fontsize: int = 13,
        color: str = "r",
        clip_on: bool = True,
        zorder: int = PORDER_TEXT,
    ) -> None:
        self._ax.text(
            x,
            y,
            text,
            horizontalalignment=horizontalalignment,
            verticalalignment=verticalalignment,
            fontsize=fontsize,
            color=color,
            clip_on=clip_on,
            zorder=zorder,
        )

    def _gate(self, gate: GateData, col: int, row: int) -> None:
        ypos, xpos = col * (GATE_DEFAULT_HEIGHT + GATE_MARGIN_RIGHT), row * (
            GATE_DEFAULT_WIDTH + GATE_MARGIN_RIGHT
        )
        box = patches.Rectangle(
            xy=(xpos - 0.5 * gate["width"], ypos - 0.5 * gate["height"]),
            width=gate["width"],
            height=gate["height"],
            facecolor="b",  # 塗りつぶし色
            edgecolor="g",  # 辺の色
            linewidth=3,
            zorder=PORDER_GATE,
        )
        self._ax.add_patch(box)

        self._text(xpos, ypos, gate["text"])

    def _multi_gate(self, gate: GateData, col: int, row: int) -> None:
        multi_gate_size = gate["size"]

        ypos = (
            col * (GATE_DEFAULT_HEIGHT + GATE_MARGIN_RIGHT)
            + (col + multi_gate_size - 1) * (GATE_DEFAULT_HEIGHT + GATE_MARGIN_RIGHT)
        ) * 0.5
        xpos = row * (GATE_DEFAULT_WIDTH + GATE_MARGIN_RIGHT)
        multi_gate_height = gate["height"] * multi_gate_size + GATE_MARGIN_RIGHT * (
            multi_gate_size - 1
        )
        box = patches.Rectangle(
            xy=(xpos - 0.5 * gate["width"], ypos - 0.5 * multi_gate_height),
            width=gate["width"],
            height=multi_gate_height,
            facecolor="b",  # 塗りつぶし色
            edgecolor="g",  # 辺の色
            linewidth=3,
            zorder=PORDER_GATE,
        )
        self._ax.add_patch(box)

        self._text(xpos, ypos, gate["text"])

    def _cnot(self, gate: GateData, col: int, row: int) -> None:
        ypos, xpos = col * (GATE_DEFAULT_HEIGHT + GATE_MARGIN_RIGHT), row * (
            GATE_DEFAULT_WIDTH + GATE_MARGIN_RIGHT
        )

        if gate["control_bit"] is None:
            raise ValueError("control_bit is None")
        elif gate["control_bit"] == []:
            raise ValueError("control_bit is empty")

        target = patches.Circle(
            xy=(xpos, ypos), radius=0.4, fc="w", ec="g", zorder=PORDER_GATE
        )
        self._ax.add_patch(target)
        self._ax.plot(
            xpos,
            ypos,
            marker="+",
            color="r",
            markersize=10,
            markeredgewidth=3,
            zorder=PORDER_TEXT,
        )

        for control_bit in gate["control_bit"]:
            to_ypos = control_bit * (GATE_DEFAULT_HEIGHT + GATE_MARGIN_RIGHT)
            self._line(
                (xpos, ypos),
                (xpos, to_ypos),
                lc="r",
            )
            ctl = patches.Circle(
                xy=(xpos, to_ypos), radius=0.2, fc="g", ec="r", zorder=PORDER_GATE
            )
            self._ax.add_patch(ctl)


def parse_circuit(circuit: QuantumCircuit) -> CircuitData:
    arr: CircuitData = [
        [
            {
                "text": r"$I$",
                "width": GATE_DEFAULT_WIDTH,
                "height": GATE_DEFAULT_HEIGHT,
                "raw_text": "I",
                "control_bit": None,
                "size": 1,
            },
            {
                "text": r"$X$",
                "width": GATE_DEFAULT_WIDTH,
                "height": GATE_DEFAULT_HEIGHT,
                "raw_text": "X",
                "control_bit": None,
                "size": 1,
            },
            {
                "text": r"$Y$",
                "width": GATE_DEFAULT_WIDTH,
                "height": GATE_DEFAULT_HEIGHT,
                "raw_text": "Y",
                "control_bit": None,
                "size": 1,
            },
            {
                "text": r"$Z$",
                "width": GATE_DEFAULT_WIDTH,
                "height": GATE_DEFAULT_HEIGHT,
                "raw_text": "Z",
                "control_bit": None,
                "size": 1,
            },
            {
                "text": r"$H$",
                "width": GATE_DEFAULT_WIDTH,
                "height": GATE_DEFAULT_HEIGHT,
                "raw_text": "H",
                "control_bit": None,
                "size": 1,
            },
            {
                "text": r"$S$",
                "width": GATE_DEFAULT_WIDTH,
                "height": GATE_DEFAULT_HEIGHT,
                "raw_text": "S",
                "control_bit": None,
                "size": 1,
            },
        ],
        [
            {
                "text": r"$S^\dagger$",
                "width": GATE_DEFAULT_WIDTH,
                "height": GATE_DEFAULT_HEIGHT,
                "raw_text": "Sdag",
                "control_bit": None,
                "size": 1,
            },
            {
                "text": r"$T$",
                "width": GATE_DEFAULT_WIDTH,
                "height": GATE_DEFAULT_HEIGHT,
                "raw_text": "T",
                "control_bit": None,
                "size": 1,
            },
            {
                "text": r"$T^\dagger$",
                "width": GATE_DEFAULT_WIDTH,
                "height": GATE_DEFAULT_HEIGHT,
                "raw_text": "X",
                "control_bit": None,
                "size": 1,
            },
        ],
        [
            {
                "text": r"$CNOT$",
                "width": GATE_DEFAULT_WIDTH,
                "height": GATE_DEFAULT_HEIGHT,
                "raw_text": "CNOT",
                "control_bit": [3, 4],
                "size": 1,
            },
            {
                "text": r"$ghost$",
                "width": GATE_DEFAULT_WIDTH,
                "height": GATE_DEFAULT_HEIGHT,
                "raw_text": "ghost",
                "control_bit": None,
                "size": 1,
            },
            {
                "text": r"$DeM$",
                "width": GATE_DEFAULT_WIDTH,
                "height": GATE_DEFAULT_HEIGHT,
                "raw_text": "DenseMatrix",
                "control_bit": None,
                "size": 3,
            },
        ],
        [
            {
                "text": r"$ghost$",
                "width": GATE_DEFAULT_WIDTH,
                "height": GATE_DEFAULT_HEIGHT,
                "raw_text": "ghost",
                "control_bit": None,
                "size": 1,
            },
            {
                "text": r"$CNOT$",
                "width": GATE_DEFAULT_WIDTH,
                "height": GATE_DEFAULT_HEIGHT,
                "raw_text": "CNOT",
                "control_bit": [2, 4],
                "size": 1,
            },
        ],
        [],
    ]
    return arr
