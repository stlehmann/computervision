"""Computervision utility functions."""

from collections import namedtuple
from typing import List, Union, Tuple

Rect = namedtuple("Rect", "x y w h")
RectUnion = Union[Tuple[int, int, int, int], Rect]


def rects_overlap(r1: Rect, r2: Rect, g: int = 0) -> bool:
    """Check if two rectangles overlap / touch each other.

    :param r1: first rectangle
    :param r2: second rectangle
    :param g: maximum gap between rectangles
    :return: True if rectangles overlap or border each other

    """
    x00, y00, x01, y01 = r1.x, r1.y, r1.x + r1.w, r1.y + r1.h
    x10, y10, x11, y11 = r2.x, r2.y, r2.x + r2.w, r2.y + r2.h

    return (
            x10 - x01 <= g and x00 - x11 <= g and y10 - y01 <= g and y00 - y11 <= g
    )


def combine_rects(rects: List[RectUnion], gap: int = 0) -> List[Rect]:
    """Combine overlapping and adjacent rectangles to bigger rectangles.

    :param rects: List of rectangles
    :param gap: Maximum gap between rectangles for combining
    :return: List of combined rectangles

    """
    overlapping_rects = set()
    res: List[Rect] = []

    # find overlapping rects
    for i0, (x0, y0, w0, h0) in enumerate(rects):
        overlaps = False
        for i1, (x1, y1, w1, h1) in enumerate(rects):
            if i0 == i1:
                continue
            r0 = Rect(x0, y0, w0, h0)
            r1 = Rect(x1, y1, w1, h1)

            if rects_overlap(r0, r1, g=gap):
                overlaps = True
                overlapping_rects.add((min(i0, i1), max(i0, i1)))

        if not overlaps:
            res.append((x0, y0, w0, h0))

    for i0, i1 in overlapping_rects:
        x0, y0, w0, h0 = rects[i0]
        x1, y1, w1, h1 = rects[i1]
        new_x0, new_y0 = min(x0, x1), min(y0, y1)
        new_x1, new_y1 = max(x0 + w0, x1 + w1), max(y0 + h0, y1 + h1)
        res.append(Rect(new_x0, new_y0, new_x1 - new_x0, new_y1 - new_y0))

    return res
