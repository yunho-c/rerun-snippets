"""
This script creates 
"""

from __future__ import annotations

import math
import time
from typing import Sequence

import rerun as rr  # pip install rerun-sdk


def _build_bar_geometry(
    categories: Sequence[str],
    values: Sequence[float],
    colors: Sequence[Sequence[int]],
    *,
    spacing: float,
    bar_width: float,
) -> rr.Boxes2D:
    """Turn scalar values into Boxes2D instances that look like bars."""
    centers = []
    half_sizes = []
    labels = []
    bar_colors = []

    for index, (name, value, color) in enumerate(zip(categories, values, colors)):
        x_pos = index * spacing
        height = max(0.05, value)  # Keep a visible sliver when the signal dips.

        centers.append([x_pos, height / 2.0])
        half_sizes.append([bar_width / 2.0, height / 2.0])
        labels.append(f"{name}\n{height:.2f}")
        bar_colors.append(color)

    return rr.Boxes2D(
        centers=centers,
        half_sizes=half_sizes,
        colors=bar_colors,
        labels=labels,
        show_labels=True,
    )


def _synthetic_values(frame_idx: int, base: Sequence[float], offsets: Sequence[float]) -> list[float]:
    """Simple animated signal that keeps every bar moving independently."""
    phase = frame_idx * 0.15
    return [
        base_val + math.sin(phase + offset) * 0.9 + math.sin(phase * 0.5 + offset) * 0.4
        for base_val, offset in zip(base, offsets)
    ]


def main() -> None:
    rr.init("rerun_boxes2d_fake_barchart", spawn=True)

    categories = ["Apples", "Bananas", "Cherries", "Dates"]
    palette = [
        [255, 99, 71],   # Tomato
        [255, 206, 86],  # Golden yellow
        [75, 192, 192],  # Teal
        [153, 102, 255], # Lavender
    ]

    spacing = 1.4
    bar_width = 0.9

    # Keep the chart upright and set a simple baseline once.
    rr.log("chart", rr.ViewCoordinates.RIGHT_HAND_Y_UP, static=True)
    rr.log(
        "chart/baseline",
        rr.LineStrips2D([[[ -spacing, 0.0], [(len(categories) - 1) * spacing + spacing, 0.0]]]),
        static=True,
    )

    base_levels = [2.8, 1.9, 3.6, 2.4]
    phase_offsets = [0.0, math.pi / 2.0, math.pi, 3.0 * math.pi / 2.0]

    try:
        for frame_idx in range(600):
            rr.set_time_sequence("frame", frame_idx)

            values = _synthetic_values(frame_idx, base_levels, phase_offsets)
            bars = _build_bar_geometry(
                categories,
                values,
                palette,
                spacing=spacing,
                bar_width=bar_width,
            )
            rr.log("chart/bars", bars)

            time.sleep(0.05)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
