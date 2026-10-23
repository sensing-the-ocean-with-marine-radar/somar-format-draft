#!/usr/bin/env python3
"""Draw the figure of the time-bounded grids on the Georeferencing page.

The figure is drawn to scale for a platform moving at SPEED along a gently
curving track, a radar footprint of RADIUS, and measurement periods of
DURATION, during which the platform moves SPEED * DURATION (1.2 km). Each
grid is the bounding box of the footprints at the start and at the end of its
period, so that the first lies in its lower left corner and the second in its
upper right corner, and has its origin at the radar antenna at the start. Of
the periods along the track, one per STRIDE is shown, in groups named after
their start times from START; dots on the track stand for those in between.

Usage: python3 scripts/time_bounded_grids_figure.py [OUTPUT]

OUTPUT defaults to assets/images/time_bounded_grids.svg.
"""

import datetime
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = os.path.join(ROOT, "assets", "images", "time_bounded_grids.svg")

SPEED = 5.0          # m s-1, typical transit speed of the platform
RADIUS = 5000.0      # m, typical radius of the radar footprint
DURATION = 240.0     # s, length of a measurement period
STRIDE = 3600.0      # s, between the starts of the periods shown
PERIODS = 3          # number of periods shown
START = datetime.datetime(2025, 1, 15, 11, 0, 31)
GAP = 2200.0         # m of track left out on either side of the dots

SCALE = 14.0 / 1000  # px per m
ORIGIN = (140.0, 420.0)  # px of the track at the start of the first period
WIDTH, HEIGHT = 900, 690

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
MONO = "SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
TRACK, FOOTPRINT, GRID, AXIS, TEXT = "#1f5f8b", "#2a7f86", "#a0522d", "#888888", "#27262b"


def heading(s):
    """Direction of travel at s meters along the track, in degrees counterclockwise from east."""
    return 22 + 18 * math.sin(math.pi * s / 40000)


def position(s, steps=400):
    """Position in meters east and north of the start of the first period, s meters along the track."""
    x = y = 0.0
    for i in range(steps):
        angle = math.radians(heading(s * (i + 0.5) / steps))
        x += math.cos(angle) * s / steps
        y += math.sin(angle) * s / steps
    return x, y


def pixels(point):
    return ORIGIN[0] + point[0] * SCALE, ORIGIN[1] - point[1] * SCALE


def track_path(s_from, s_to, steps=60):
    points = [pixels(position(s_from + (s_to - s_from) * i / steps)) for i in range(steps + 1)]
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in points)


def figure():
    out = []
    w = out.append
    w(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" font-family="{SANS}" font-size="15" fill="{TEXT}">')
    w('<title>Time-bounded local grids from a moving platform</title>')
    w('<defs>')
    for name, color in (("ax", AXIS), ("tr", TRACK), ("k", TEXT)):
        w(f'<marker id="a-{name}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{color}"/></marker>')
    w('</defs>')
    w(f'<rect width="{WIDTH}" height="{HEIGHT}" fill="#ffffff"/>')
    w(f'<line x1="40" y1="500" x2="840" y2="500" stroke="{AXIS}" stroke-width="1.5" marker-end="url(#a-ax)"/>')
    w(f'<line x1="50" y1="510" x2="50" y2="30" stroke="{AXIS}" stroke-width="1.5" marker-end="url(#a-ax)"/>')
    w(f'<text x="840" y="525" text-anchor="end" fill="{AXIS}">longitude</text>')
    w(f'<text x="62" y="38" fill="{AXIS}">latitude</text>')

    periods = []
    for k in range(PERIODS):
        t = k * STRIDE
        periods.append((START + datetime.timedelta(seconds=t),
                        pixels(position(SPEED * t)), pixels(position(SPEED * (t + DURATION)))))
    r = RADIUS * SCALE

    # Grids: the bounding box of the footprints at the start and at the end of the period, with a lattice of 1 km.
    for when, (x0, y0), (x1, y1) in periods:
        left, right, top, bottom = min(x0, x1) - r, max(x0, x1) + r, min(y0, y1) - r, max(y0, y1) + r
        step = 1000 * SCALE
        w(f'<g stroke="{GRID}">')
        w(f'<rect x="{left:.1f}" y="{top:.1f}" width="{right-left:.1f}" height="{bottom-top:.1f}" fill="{GRID}" fill-opacity="0.04" stroke-width="1.5"/>')
        x = left + step
        while x < right - 1:
            w(f'<line x1="{x:.1f}" y1="{top:.1f}" x2="{x:.1f}" y2="{bottom:.1f}" stroke-opacity="0.18" stroke-width="0.8"/>')
            x += step
        y = top + step
        while y < bottom - 1:
            w(f'<line x1="{left:.1f}" y1="{y:.1f}" x2="{right:.1f}" y2="{y:.1f}" stroke-opacity="0.18" stroke-width="0.8"/>')
            y += step
        w('</g>')
        w(f'<text x="{left:.1f}" y="{top-7:.1f}" font-family="{MONO}" font-size="13" fill="{GRID}">time_{when:%Y%m%d%H%M%S}</text>')

    # Track: drawn through the periods shown, and broken by dots halfway between them.
    segments, cuts = [], []
    for k in range(PERIODS):
        end_of_period = SPEED * (k * STRIDE + DURATION)
        start = -5000.0 if k == 0 else cuts[-1] + GAP
        if k < PERIODS - 1:
            cuts.append((end_of_period + SPEED * (k + 1) * STRIDE) / 2)
            segments.append((start, cuts[-1] - GAP))
        else:
            segments.append((start, end_of_period + 9000.0))
    for i, (s_from, s_to) in enumerate(segments):
        arrow = ' marker-end="url(#a-tr)"' if i == len(segments) - 1 else ""
        w(f'<path d="{track_path(s_from, s_to)}" fill="none" stroke="{TRACK}" stroke-width="3"{arrow}/>')
    for s in cuts:
        angle, (x, y) = math.radians(heading(s)), pixels(position(s))
        for d in (-10, 0, 10):
            w(f'<circle cx="{x + d*math.cos(angle):.1f}" cy="{y - d*math.sin(angle):.1f}" r="2.6" fill="{TRACK}"/>')
    x, y = pixels(position(segments[-1][1]))
    w(f'<text x="{x+10:.1f}" y="{y-2:.1f}" font-weight="bold" fill="{TRACK}">platform</text>')
    w(f'<text x="{x+10:.1f}" y="{y+16:.1f}" font-weight="bold" fill="{TRACK}">track</text>')

    # Footprints, and the origin of each grid with its axes.
    for when, (x0, y0), (x1, y1) in periods:
        w(f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="{r:.1f}" fill="none" stroke="{FOOTPRINT}" stroke-width="1.5" stroke-dasharray="5 4"/>')
        w(f'<circle cx="{x0:.1f}" cy="{y0:.1f}" r="{r:.1f}" fill="none" stroke="{FOOTPRINT}" stroke-width="1.5"/>')
        length = 30
        w(f'<g stroke="{TEXT}" stroke-width="2"><line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x0+length:.1f}" y2="{y0:.1f}" marker-end="url(#a-k)"/>'
          f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x0:.1f}" y2="{y0-length:.1f}" marker-end="url(#a-k)"/></g>')
        w(f'<circle cx="{x0:.1f}" cy="{y0:.1f}" r="3.5" fill="{TEXT}"/>')
        w(f'<text x="{x0+length+4:.1f}" y="{y0+5:.1f}" font-family="{MONO}" font-size="14">x</text>')
        w(f'<text x="{x0:.1f}" y="{y0-length-6:.1f}" font-family="{MONO}" font-size="14" text-anchor="middle">y</text>')

    # Key
    def code(name):
        return f'<tspan font-family="{MONO}">{name}</tspan>'

    def label(y, text):
        w(f'<text x="{kx+40}" y="{y+5}">{text}</text>')

    ky, kx = 556, 60
    w(f'<circle cx="{kx}" cy="{ky}" r="11" fill="none" stroke="{FOOTPRINT}" stroke-width="1.5"/>')
    label(ky, f'radar footprint at {code("time")}, the start of the measurement period or averaging window')
    w(f'<circle cx="{kx}" cy="{ky+30}" r="11" fill="none" stroke="{FOOTPRINT}" stroke-width="1.5" stroke-dasharray="4 3"/>')
    label(ky + 30, f'radar footprint at its end, {code("measurement_duration")} or {code("averaging_duration")} later')
    y = ky + 60
    w(f'<g stroke="{TEXT}" stroke-width="2"><line x1="{kx-8}" y1="{y+7}" x2="{kx+12}" y2="{y+7}" marker-end="url(#a-k)"/><line x1="{kx-8}" y1="{y+7}" x2="{kx-8}" y2="{y-13}" marker-end="url(#a-k)"/></g><circle cx="{kx-8}" cy="{y+7}" r="2.5" fill="{TEXT}"/>')
    label(y, f'grid origin at the radar antenna at {code("time")}, with {code("x")} east and {code("y")} north')
    y = ky + 90
    w(f'<rect x="{kx-11}" y="{y-8}" width="22" height="16" fill="{GRID}" fill-opacity="0.04" stroke="{GRID}" stroke-width="1.5"/>')
    label(y, f'time-bounded grid, one group {code("time_&lt;YYYYMMDDHHMMSS&gt;")} per measurement period or averaging window')
    y = ky + 120
    for d in (-9, 0, 9):
        w(f'<circle cx="{kx+d}" cy="{y}" r="2.6" fill="{TRACK}"/>')
    label(y, 'further periods or windows along the track, not shown')
    w('</svg>')
    return "\n".join(out) + "\n"


def main():
    output = sys.argv[1] if len(sys.argv) > 1 else OUTPUT
    with open(output, "w", encoding="utf-8") as f:
        f.write(figure())


if __name__ == "__main__":
    main()
