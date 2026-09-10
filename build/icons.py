"""Individually authored SVG artwork for the handbook landing page.

Every idea, skill, guide and investigation gets its own drawing: 19 + 4 + 13 + 3,
all distinct. Stroke-based on a 64 (ideas, skills), 32 (guides) or 160x80
(investigations) grid, drawn in currentColor and inlined into the HTML, so the
page loads nothing from the network.
"""
from math import cos, sin, pi

STROKE = 'fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"'
STROKE_SM = 'fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"'


def svg(inner, size=64, cls='icon', stroke=STROKE):
    return (f'<svg class="{cls}" viewBox="0 0 {size} {size}" aria-hidden="true" focusable="false" '
            f'{stroke}>{inner}</svg>')


def poly(cx, cy, r, n, rot=-pi / 2):
    pts = [(cx + r * cos(rot + 2 * pi * k / n), cy + r * sin(rot + 2 * pi * k / n)) for k in range(n)]
    return 'M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + 'z'


def star(cx, cy, r1, r2, n=5):
    pts = []
    for k in range(2 * n):
        r = r1 if k % 2 == 0 else r2
        a = -pi / 2 + pi * k / n
        pts.append((cx + r * cos(a), cy + r * sin(a)))
    return 'M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + 'z'


def gear(cx, cy, r=6, teeth=8):
    d = f'<circle cx="{cx}" cy="{cy}" r="{r}"/><circle cx="{cx}" cy="{cy}" r="{r*0.4:.1f}"/>'
    for k in range(teeth):
        a = 2 * pi * k / teeth
        d += (f'<path d="M{cx + (r+1)*cos(a):.1f} {cy + (r+1)*sin(a):.1f}'
              f'L{cx + (r+4)*cos(a):.1f} {cy + (r+4)*sin(a):.1f}"/>')
    return d


def dot(x, y, r=1.6):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="currentColor" stroke="none"/>'


def soft(d):
    """A translucent filled region used as a light wash behind strokes."""
    return f'<path d="{d}" fill="currentColor" fill-opacity=".12" stroke="none"/>'


# ------------------------------------------------------------ 19 ideas
IDEAS = {
    # 01 Close the CI feedback loop
    '01': svg(
        '<path d="M50 32a18 18 0 1 1-6.2-13.6"/>'
        '<path d="M38.4 14.2l6.2 3.8-1.4 6.6"/>'
        + soft('M22 25h20v14H22z') +
        '<rect x="22" y="25" width="20" height="14" rx="2"/>'
        '<path d="M26 30h6"/>' + dot(35, 30) +
        '<path d="M26 34h6"/><path d="M34 34.5l1.8 1.8 3.4-3.8"/>'),
    # 02 Two-actor end-to-end test
    '02': svg(
        soft('M6 18h24v18H6z') +
        '<rect x="6" y="18" width="24" height="18" rx="2"/><path d="M6 23h24"/>'
        + dot(9, 20.5, 1) + dot(12.5, 20.5, 1) +
        '<path d="M11 29h8"/>'
        + soft('M34 28h24v18H34z') +
        '<rect x="34" y="28" width="24" height="18" rx="2"/><path d="M34 33h24"/>'
        + dot(37, 30.5, 1) + dot(40.5, 30.5, 1) +
        '<path d="M39 39h8"/><path d="M40.5 42.5l1.5 1.5 3-3.5"/>'
        '<path d="M18 40c0 9 10 9 19 6"/><path d="M34.5 43.5l3.4 2.2-1.6 3.6"/>'),
    # 03 Automation speeds up every agent
    '03': svg(
        gear(16, 32) +
        '<path d="M27 32c8 0 10-16 17-16"/><path d="M27 32h17"/><path d="M27 32c8 0 10 16 17 16"/>'
        + soft(poly(50, 16, 5.5, 6)) + f'<path d="{poly(50, 16, 5.5, 6)}"/>'
        + soft(poly(50, 32, 5.5, 6)) + f'<path d="{poly(50, 32, 5.5, 6)}"/>'
        + soft(poly(50, 48, 5.5, 6)) + f'<path d="{poly(50, 48, 5.5, 6)}"/>'),
    # 04 Preview environments
    '04': svg(
        soft('M19 30a6 6 0 0 1 1-11.9A9 9 0 0 1 37 16a7 7 0 0 1 9 6.5A5 5 0 0 1 46 32H19z') +
        '<path d="M19 30a6 6 0 0 1 1-11.9A9 9 0 0 1 37 16a7 7 0 0 1 9 6.5A5 5 0 0 1 46 32H19"/>'
        '<rect x="14" y="36" width="36" height="20" rx="2"/>'
        '<rect x="18" y="40" width="28" height="4" rx="1"/>'
        '<path d="M22 48h10"/><path d="M36 50.5l2.5 2.5 5-5.5"/>'),
    # 05 Small tool adapters
    '05': svg(
        soft('M8 26h14v12H8z') +
        '<rect x="8" y="26" width="14" height="12" rx="3"/><path d="M22 29h6M22 35h6M8 32H3"/>'
        '<path d="M28 32h9"/><path d="M34.5 29l3 3-3 3"/>'
        '<path d="M40 14h10l6 6v30H40z"/><path d="M50 14v6h6"/>'
        '<path d="M48 44V30"/><path d="M43 35l5-5 5 5"/>'),
    # 06 Authoring a small skill is a tight loop
    '06': svg(
        '<path d="M18 12h18l8 8v32H18z"/><path d="M36 12v8h8"/>'
        '<path d="M24 30h12M24 36h14M24 42h6"/>'
        '<path d="M40 48a7 7 0 1 1-2.5-5.4"/><path d="M33.5 40l4.5 1.2-1 4.4"/>'
        '<path d="M54 6v12M48 12h12"/><path d="M51 9l6 6M57 9l-6 6" stroke-width="1.2"/>'),
    # 07 Teams fund tooling time
    '07': svg(
        soft('M28 14a16 16 0 1 0 0 32 16 16 0 0 0 0-32z') +
        '<circle cx="28" cy="30" r="16"/>'
        '<path d="M28 16v3M28 41v3M14 30h3M39 30h3"/>'
        '<path d="M28 30V21"/><path d="M28 30l7 4.5"/>' + dot(28, 30, 1.6) +
        '<path d="M56 38a6 6 0 0 1-8 7l-8 8-3.5-3.5 8-8a6 6 0 0 1 7-8l-3.5 3.5 3.5 3.5z"/>'),
    # 08 Move recurring fixes into executable checks
    '08': svg(
        ''.join(f'<path d="M{x-2} {y-2}l4 4M{x+2} {y-2}l-4 4"/>' for x, y in
                [(18, 10), (30, 8), (42, 12), (24, 17), (37, 18)]) +
        soft('M12 24h40L38 37v11l-12 5V37z') +
        '<path d="M12 24h40L38 37v11l-12 5V37z"/>'
        '<path d="M52 36l7 3v6c0 5-3 8.5-7 10.5C48 53.5 45 50 45 45v-6z"/>'
        '<path d="M48.5 45.5l2.5 2.5 4.5-5"/>'),
    # 09 Custom lint rules became economical
    '09': svg(
        '<path d="M20 12c-5 0-5 4-5 9s0 7-5 9c5 2 5 4 5 9s0 9 5 9"/>'
        '<path d="M44 12c5 0 5 4 5 9s0 7 5 9c-5 2-5 4-5 9s0 9-5 9"/>'
        '<path d="M22 18h5v8h5v8h5v8h5"/><path d="M39.5 39.5l2.5 2.5 2.5-2.5"/>'
        '<circle cx="30" cy="50" r="4"/><path d="M30 47.5v5"/>'),
    # 10 Encode domain knowledge as infrastructure
    '10': svg(
        soft('M32 6a8 8 0 0 1 5 14.2c-1 1-2 2.2-2 3.8h-6c0-1.6-1-2.8-2-3.8A8 8 0 0 1 32 6z') +
        '<path d="M32 6a8 8 0 0 1 5 14.2c-1 1-2 2.2-2 3.8h-6c0-1.6-1-2.8-2-3.8A8 8 0 0 1 32 6z"/>'
        '<path d="M29 27h6"/><path d="M32 30v6"/>'
        '<rect x="14" y="36" width="36" height="6" rx="1.5"/>'
        '<rect x="14" y="45" width="36" height="6" rx="1.5"/>'
        '<rect x="14" y="54" width="36" height="6" rx="1.5"/>'
        '<path d="M19 40l2-2M22 40l2-2"/><path d="M19 49.5l2.5-1.5-2.5-1.5"/><path d="M19 57.5l1.5 1.5 3-3"/>'),
    # 11 Newcomer questions as a signal
    '11': svg(
        soft('M10 10h26a4 4 0 0 1 4 4v14a4 4 0 0 1-4 4H22l-8 7v-7h-4a4 4 0 0 1-4-4V14a4 4 0 0 1 4-4z') +
        '<path d="M10 10h26a4 4 0 0 1 4 4v14a4 4 0 0 1-4 4H22l-8 7v-7h-4a4 4 0 0 1-4-4V14a4 4 0 0 1 4-4z"/>'
        '<path d="M19.5 19.5a3.5 3.5 0 1 1 5 3.2c-1.2.6-1.5 1.3-1.5 2.3"/>' + dot(23, 28.5, 1.2) +
        '<path d="M42 40c2.5-6 5.5-6 8 0s5.5 6 8 0"/>'
        '<circle cx="52" cy="54" r="7"/><circle cx="52" cy="54" r="3"/>' + dot(52, 54, 1)),
    # 12 Write your own instruction files
    '12': svg(
        '<path d="M12 12h24l8 8v34H12z"/><path d="M36 12v8h8"/>'
        '<path d="M18 30h14M18 36h14M18 42h8"/>'
        + soft('M56 24L40 40l-6 2 2-6 16-16z') +
        '<path d="M56 24L40 40l-6 2 2-6 16-16 4 4z"/><path d="M49 25l4 4"/>'
        '<path d="M40 8c3-4 13-4 16 0c-3 4-13 4-16 0z"/>' + dot(48, 8, 1.6)),
    # 13 Steering files that say no
    '13': svg(
        '<circle cx="26" cy="36" r="16"/><circle cx="26" cy="36" r="4"/>'
        '<path d="M26 20v12M12.5 40l9.6-2.5M39.5 40l-9.6-2.5"/>'
        + soft(poly(50, 14, 9, 8, rot=pi / 8)) + f'<path d="{poly(50, 14, 9, 8, rot=pi / 8)}"/>'
        '<path d="M46 18l8-8"/>'),
    # 14 Compose layers so type safety runs end to end
    '14': svg(
        '<path d="M32 4v56" stroke-opacity=".45" stroke-width="3"/>'
        + soft('M14 8h36v12H14z') +
        '<rect x="14" y="8" width="36" height="12" rx="2"/><path d="M14 13h36"/>'
        '<rect x="14" y="26" width="36" height="12" rx="2"/><path d="M20 32h6M38 32h6"/>'
        '<path d="M18 46v8c0 2.2 6.3 4 14 4s14-1.8 14-4v-8"/>'
        '<ellipse cx="32" cy="46" rx="14" ry="4"/>'
        + dot(32, 20, 2) + dot(32, 26, 2) + dot(32, 38, 2) + dot(32, 42, 2)),
    # 15 Docs so agents work with zero prompting context
    '15': svg(
        '<rect x="40" y="6" width="18" height="24" rx="2"/>'
        + soft('M34 12h18v24H34z') +
        '<rect x="34" y="12" width="18" height="24" rx="2"/><path d="M38 18h10M38 23h10M38 28h6"/>'
        '<path d="M43 40v5H16"/><path d="M19 42l-3 3 3 3"/>'
        + soft('M6 46h34v12H6z') +
        '<rect x="6" y="46" width="34" height="12" rx="3"/><path d="M12 49.5v5"/>'),
    # 16 Calibrate from a cold start
    '16': svg(
        '<path d="M12 44a20 20 0 0 1 40 0"/>'
        + ''.join(f'<path d="M{32 + 20*cos(a):.1f} {44 + 20*sin(a):.1f}L{32 + 16.5*cos(a):.1f} {44 + 16.5*sin(a):.1f}"/>'
                  for a in [pi + pi * k / 6 for k in range(0, 7)]) +
        '<path d="M32 44L16.5 37.5"/>' + dot(32, 44, 2.5) +
        '<path d="M46 12v8M42 16h8"/><path d="M56 26v5M53.5 28.5h5"/>'),
    # 17 Instruction files should steer, not map
    '17': svg(
        '<path d="M18 46c-6-8-9-13-9-18a9 9 0 0 1 18 0c0 5-3 10-9 18z"/><circle cx="18" cy="28" r="3"/>'
        '<path d="M6 50L30 12" stroke-width="2.2"/>'
        '<path d="M34 54c8-6 8-18 18-26"/><path d="M47.5 27.5l4.5-.5-.5 4.5"/>'
        + soft(star(53, 14, 7, 3)) + f'<path d="{star(53, 14, 7, 3)}"/>'),
    # 18 Building environments is a career-level skill
    '18': svg(
        '<path d="M28 50l6-9 6 9z"/><path d="M8 56L58 34"/>'
        + soft('M46 26l6.5-3 3 6.5-6.5 3z') +
        '<path d="M46 26l6.5-3 3 6.5-6.5 3z"/><path d="M40 20l6.5-3 3 6.5-6.5 3z"/>'
        '<path d="M50 14l6.5-3 3 6.5-6.5 3z"/>'
        '<circle cx="14" cy="50" r="4.5" fill="currentColor" fill-opacity=".35"/>'),
    # 19 Solo projects beyond your comprehension
    '19': svg(
        soft('M18 40L46 8l8 16z') +
        '<circle cx="14" cy="44" r="5"/><path d="M4 60c0-8.5 20-8.5 20 0"/>'
        '<path d="M22 12h-4M26 8l-3-3M28 20l-4-1" stroke-opacity=".6"/>'
        '<path d="M40 14l12-4 4 14-10 6-8-8zM52 10l6 14M42 30l14 12"/>'
        + dot(40, 14, 2) + dot(52, 10, 2) + dot(56, 24, 2) + dot(46, 30, 2) + dot(58, 42, 2)),
}

# ------------------------------------------------------------ 4 skills
SKILLS = {
    'agent-feedback-engineering': svg(
        soft('M14 42L24 22l10 20z') +
        '<path d="M14 42L24 22l10 20z"/><path d="M24 30v6"/>' + dot(24, 39, 1.3) +
        '<path d="M36 32h8"/><path d="M41 29l3 3-3 3"/>'
        '<path d="M52 20l8 3v8c0 6-4 10-8 12-4-2-8-6-8-12v-8z"/><path d="M48.5 31l2.5 2.5 5-6"/>'),
    'agent-ready-workspaces': svg(
        soft('M8 12h48v40H8z') +
        '<rect x="8" y="12" width="48" height="40" rx="3"/><path d="M8 20h48M20 20v32"/>'
        + dot(12, 16, 1) + dot(15.5, 16, 1) +
        '<path d="M27 30l4 3-4 3M34 36h8"/>'
        '<circle cx="48" cy="46" r="6"/><path d="M45.5 46l1.8 1.8 3.4-3.8"/>'),
    'agent-context-calibration': svg(
        '<circle cx="32" cy="30" r="14"/><circle cx="32" cy="30" r="6" stroke-opacity=".6"/>'
        '<path d="M32 10v6M32 44v6M12 30h6M46 30h6"/>' + dot(32, 30, 2) +
        '<path d="M10 58h44"/>' + '<circle cx="22" cy="58" r="3.5" fill="currentColor" fill-opacity=".35"/>'
        '<path d="M14 55v6M30 55v6M38 55v6M46 55v6" stroke-opacity=".5"/>'),
    'agent-tool-adapters': svg(
        '<path d="M4 46h16M44 46h16"/><path d="M20 46c4-14 20-14 24 0"/>'
        '<path d="M26 46v-5M32 46v-9M38 46v-5" stroke-opacity=".6"/>'
        + soft('M27 14h10v8H27z') +
        '<rect x="27" y="14" width="10" height="8" rx="2"/><path d="M30 14V9M34 14V9M32 22v10"/>'),
}

# ------------------------------------------------------------ 13 guides
def g(inner):
    return svg(inner, size=32, cls='glyph', stroke=STROKE_SM)


GUIDES = {
    '01': g('<path d="M16 3l10 4v8c0 7-5 12-10 14C11 27 6 22 6 15V7z"/><path d="M12 13h8M12 17h8"/>'),
    '02': g('<path d="M5 26C10 8 22 24 27 8"/>' + dot(5, 26, 2) + '<path d="M27 8V3M27 3h4l-1 1.5 1 1.5h-4"/>'),
    '03': g('<rect x="4" y="6" width="24" height="16" rx="2"/><path d="M12 27h8M16 22v5"/>'
            '<path d="M10 14c3-4 9-4 12 0c-3 4-9 4-12 0z"/>' + dot(16, 14, 1.3)),
    '04': g('<path d="M25 14a9 9 0 0 0-16-5"/><path d="M8 4v6h6"/><path d="M7 18a9 9 0 0 0 16 5"/><path d="M24 28v-6h-6"/>'),
    '05': g('<path d="M6 5h9a3 3 0 0 1 3 3v19a2 2 0 0 0-2-2H6z"/><path d="M26 5h-9a3 3 0 0 0-3 3v19a2 2 0 0 1 2-2h10z"/>'),
    '06': g('<rect x="3" y="12" width="10" height="8" rx="2"/><path d="M13 14h5M13 18h5M3 16H1"/>'
            '<rect x="21" y="10" width="8" height="12" rx="2"/><path d="M25 14v1M25 18v1"/>'),
    '07': g('<circle cx="11" cy="11" r="4"/><circle cx="21" cy="11" r="4"/><path d="M3 27c0-7 16-7 16 0M13 27c0-7 16-7 16 0"/>'),
    '08': g('<path d="M11 5c-3 0-3 3-3 5.5s0 4-3 5.5c3 1.5 3 3 3 5.5S8 27 11 27"/>'
            '<path d="M21 5c3 0 3 3 3 5.5s0 4 3 5.5c-3 1.5-3 3-3 5.5s0 5.5-3 5.5"/><path d="M13 16h6"/>'),
    '09': g(f'<path d="{poly(16, 16, 12, 12)}"/><circle cx="16" cy="16" r="8"/><path d="M11.5 16l3 3 6-6"/>'),
    '10': g('<circle cx="16" cy="16" r="12"/><path d="M21 11l-3 7-7 3 3-7z" fill="currentColor" fill-opacity=".35"/>'),
    '11': g('<path d="M4 5h16a3 3 0 0 1 3 3v8a3 3 0 0 1-3 3H12l-5 5v-5H4z"/><path d="M8 12h8"/><path d="M25 12h4" stroke-width="2.4"/>'),
    '12': g('<path d="M4 10l12-6 12 6v12l-12 6-12-6z"/><path d="M4 10l12 6 12-6M16 16v12"/><path d="M8 14v4M12 16v4" stroke-opacity=".6"/>'),
    '13': g('<path d="M16 4l12 6-12 6-12-6z"/><path d="M4 16l12 6 12-6"/><path d="M4 22l12 6 12-6"/>'),
}

# ------------------------------------------------------------ 3 investigations (wide diagrams)
def wide(inner):
    return (f'<svg class="diagram" viewBox="0 0 160 80" aria-hidden="true" focusable="false" {STROKE}>{inner}</svg>')


INVESTIGATIONS = {
    'github-inspection.md': wide(
        '<path d="M10 56h140" stroke-opacity=".5"/>'
        + ''.join(dot(x, 56, 3) for x in (24, 52, 80, 108, 136)) +
        '<path d="M52 56c10-20 20-30 40-30h30"/>'
        + ''.join(f'<circle cx="{x}" cy="26" r="3"/>' for x in (92, 106, 120)) +
        '<path d="M122 26c8 0 10 12 14 30"/>'
        + soft('M126 8h24v14h-24z') + '<rect x="126" y="8" width="24" height="14" rx="2"/><path d="M132 15l3 3 6-6"/>'),
    'matt-pocock-inspection.md': wide(
        '<rect x="8" y="24" width="40" height="32" rx="2"/><path d="M8 32h40M8 48h40"/>'
        + ''.join(f'<path d="M{x} 24v8M{x} 48v8"/>' for x in (18, 28, 38)) +
        '<path d="M52 40h28"/><path d="M76 36l4 4-4 4"/>'
        '<rect x="84" y="30" width="28" height="20" rx="10"/><path d="M92 40h12"/>'
        '<path d="M116 40h12"/><path d="M124 36l4 4-4 4"/>'
        + soft('M132 22h20v36h-20z') + '<rect x="132" y="22" width="20" height="36" rx="2"/><path d="M137 32h10M137 40h10M137 48h6"/>'),
    'boris-cherny-inspection.md': wide(
        ''.join(f'<path d="M4 {y}h14"/><path d="M15 {y-3}l3 3-3 3"/>' for y in (28, 40, 52)) +
        ''.join(soft(f'M{x} 26h30v28H{x}z') + f'<rect x="{x}" y="26" width="30" height="28" rx="2"/>' for x in (22, 64, 106)) +
        '<path d="M52 40h12M94 40h12"/><path d="M60 36l4 4-4 4M102 36l4 4-4 4"/>'
        '<path d="M30 36h14M30 42h10M72 36h14M72 42h10M114 36h14M114 42h10" stroke-opacity=".6"/>'
        '<path d="M140 40h8"/><circle cx="152" cy="40" r="5"/><path d="M149.5 40l1.8 1.8 3.4-3.8"/>'),
}
