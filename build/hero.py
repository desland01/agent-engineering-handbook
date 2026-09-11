"""The home page hero: one drawn system loop, animated without a seam.

What the handbook is about, at a glance. On the left, the codebase as a stack of
hairline cells — checks, instructions, skills, code — the places the video says to
put what you keep repeating. On the right, five terminal windows, one per coding agent. Between them one closed track: changes leave the agents, pass a
check gate, and land in the codebase; the codebase hands context back along the
bottom. The agents are little robots that walk the track, each carrying a change. On its lap
one robot's parcel is a mistake: orange with an ×. The gate catches it, a new rule
writes itself into CHECKS, and the parcel carries on as an ivory check — a correction
you made once becoming a rule that catches it forever. The mistake passes from robot
to robot, so the full cycle is five laps; every animation shares that period.

Continuity: every animation is SMIL on one shared period (``PERIOD`` seconds), on a
closed path, with negative ``begin`` offsets, so frame t and frame t + PERIOD are
identical and the loop never restarts. ``handbook.js`` pauses the SVG under
``prefers-reduced-motion: reduce``; at rest it is the same drawing.

The robots come from ``robots.py`` (drawn by a delegated worker); without that
file each agent gets a plain pixel body so the page still builds.
"""
import re
from math import pi, cos, sin

try:
    from robots import ROBOTS
except ImportError:  # the delegated drawings are not in yet
    ROBOTS = {}

PERIOD = 12.0            # seconds for one lap of the loop
LAPS = 5                 # the mistake rotates through the five agents, one per lap
N = 5                    # one robot per agent on the track

# Geometry, in the 1040 x 640 viewBox.
TRACK_TOP, TRACK_BOTTOM = 92, 560
TRACK_LEFT, TRACK_RIGHT = 318, 828       # inside the codebase's right edge / agents centre
R_CORNER = 28
GATE_X = 512
CODE_X, CODE_Y, CODE_W, CODE_H = 64, 148, 300, 356
AGENT_X, AGENT_W, AGENT_H, AGENT_GAP = 672, 312, 66, 12
AGENTS = [('claude', 'Claude'), ('codex', 'Codex'), ('gemini', 'Gemini'), ('kimi', 'Kimi'), ('zai', 'Z.ai')]
AGENT_Y0 = 142
AGENT_YS = [AGENT_Y0 + i * (AGENT_H + AGENT_GAP) for i in range(len(AGENTS))]

ACCENT = '#f37a3b'
IVORY = '#f7f3ef'
_MONO = 'font-family="var(--font-mono, ui-monospace, SFMono-Regular, Menlo, monospace)" letter-spacing=".12em"'


def _label(x, y, text, size=15, anchor='start', cls='lbl'):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" {_MONO} '
            f'fill="currentColor">{text}</text>')


def _loop_path():
    r = R_CORNER
    return (f'M{TRACK_RIGHT},{TRACK_TOP} H{TRACK_LEFT + r} a{r},{r} 0 0 0 -{r},{r} '
            f'V{TRACK_BOTTOM - r} a{r},{r} 0 0 0 {r},{r} H{TRACK_RIGHT - r} a{r},{r} 0 0 0 {r},-{r} '
            f'V{TRACK_TOP + r} a{r},{r} 0 0 0 -{r},-{r} Z')


def _fractions():
    """Where the gate, the codebase and the agents sit along the closed path, as
    fractions of its length, so colour changes and pulses line up with the motion."""
    r = R_CORNER
    straight_h = (TRACK_RIGHT - TRACK_LEFT) - r
    straight_v = (TRACK_BOTTOM - TRACK_TOP) - 2 * r
    arc = pi * r / 2
    total = 2 * straight_h + 2 * straight_v + 4 * arc
    d_gate = TRACK_RIGHT - GATE_X
    d_code_top = straight_h + arc + (CODE_Y - (TRACK_TOP + r))
    d_agents = 2 * straight_h + straight_v + 3 * arc + (TRACK_BOTTOM - r - (AGENT_YS[-1] + AGENT_H))
    cells = [(d_code_top + i * CODE_H / 4) / total for i in range(4)]
    return d_gate / total, d_code_top / total, d_agents / total, cells


def _keyed(attr, points, T, begin=0.0, discrete=True):
    """An <animate> values/keyTimes pair from (fraction, value) points."""
    pts = sorted(dict(points).items())
    kt = ';'.join(f'{t:.4f}' for t, _ in pts)
    vals = ';'.join(str(v) for _, v in pts)
    mode = ' calcMode="discrete"' if discrete else ''
    b = f' begin="{begin:.3f}s"' if begin else ''
    return f'<animate attributeName="{attr}" values="{vals}" keyTimes="{kt}"{mode} dur="{T}s"{b} repeatCount="indefinite"/>'


def _pulse_points(centres, rise=0.004, fall=0.06, peak='1'):
    """Opacity points for a flash at each centre fraction, zero elsewhere."""
    pts = {0.0: '0', 1.0: '0'}
    for c in centres:
        for dt, v in ((-rise, '0'), (0.0, peak), (fall, '0')):
            pts[min(max(c + dt, 0.0), 1.0)] = v
    return list(pts.items())


def _step_points(base, hits, hold, value):
    """Discrete points: `base` everywhere, `value` from each hit for `hold`."""
    pts = {0.0: base, 1.0: base}
    for h in hits:
        pts[h] = value
        pts[min(h + hold, 0.999)] = base
    return list(pts.items())


def _robot(key, x, y, w, chest=None):
    """The robot at (x, y), w wide. With `chest`, the brand mark is removed and the
    given markup (drawn around the chest centre, in the robot's 40x28 units) sits
    in its place."""
    svg = ROBOTS.get(key)
    if not svg:
        inner = ('<rect x="6" y="4" width="28" height="18" rx="2" fill="currentColor"/>'
                 '<rect x="12" y="9" width="4" height="5" fill="var(--bg,#0b0b0c)"/><rect x="24" y="9" width="4" height="5" fill="var(--bg,#0b0b0c)"/>'
                 '<rect x="8" y="22" width="4" height="4" fill="currentColor"/><rect x="28" y="22" width="4" height="4" fill="currentColor"/>'
                 f'<rect x="2" y="10" width="4" height="6" fill="currentColor"/><rect x="34" y="10" width="4" height="6" fill="{ACCENT}"/>')
        cx, cy = 20, 15
    else:
        inner = svg[svg.index('>') + 1:svg.rindex('</svg>')]
        m = re.search(r'<g transform="translate\(15 ([\d.]+)\) scale\([\d.]+\)"[^>]*>.*?</g>', inner, re.S)
        cx, cy = 20, (float(m.group(1)) + 5 if m else 15)
        if chest is not None and m:
            inner = inner[:m.start()] + inner[m.end():]
    if chest is not None:
        inner += f'<g transform="translate({cx:.1f},{cy:.1f})">{chest}</g>'
    return f'<g transform="translate({x},{y}) scale({w / 40})" fill="currentColor" shape-rendering="crispEdges">{inner}</g>'


def hero():
    f_gate, f_in, f_agents, f_cells = _fractions()
    T = PERIOD
    parts = []
    a = parts.append
    TT = T * LAPS          # the full cycle: each robot takes the mistake on one lap
    # robot k starts at lap-fraction k/N along the path (begin = -k/N * T); its mistake
    # lap is lap k. In cycle fractions (0..1 over TT): a point at lap-fraction f on lap j
    # of robot k happens at ((j + f - k/N) mod LAPS) / LAPS.
    def when(k, lap, f):
        return ((lap + f - k / N) % LAPS) / LAPS
    catch_times = sorted(when(k, k, f_gate) for k in range(N))
    file_times = sorted(when(k, k, f_in) for k in range(N))

    a('<svg class="hero-loop" viewBox="0 0 1040 640" role="img" '
      'aria-label="A drawn loop: changes leave five coding agents, pass a check, and land in a codebase drawn as a stack of checks, instructions, skills and code; the codebase hands context back to the agents. Mistakes are caught at the check and written into the checks.">')
    a('<defs>'
      '<pattern id="hero-dots" width="24" height="24" patternUnits="userSpaceOnUse">'
      '<circle cx="1" cy="1" r="1" fill="currentColor" fill-opacity=".14"/></pattern>'
      f'<path id="hero-track" d="{_loop_path()}"/>'
      '</defs>')
    a('<rect width="1040" height="640" fill="url(#hero-dots)"/>')

    # ---- the track: a dashed drafting guide with a slow dash flow, and its two captions
    a('<use href="#hero-track" fill="none" stroke="currentColor" stroke-opacity=".4" stroke-width="1.2" stroke-dasharray="4 7">'
      f'<animate attributeName="stroke-dashoffset" from="0" to="-11" dur="{T/12:.3f}s" repeatCount="indefinite"/></use>')
    a(_label(TRACK_RIGHT - 24, TRACK_TOP - 14, '← PULL REQUESTS', anchor='end', cls='lbl track'))
    a(_label(TRACK_RIGHT - 60, TRACK_BOTTOM + 30, 'CONTEXT · WHAT THE AGENT READS →', anchor='end', cls='lbl track'))

    # ---- the codebase: four hairline cells, labelled with what the video says to put there
    a('<g class="codebase">')
    a(f'<rect x="{CODE_X}" y="{CODE_Y}" width="{CODE_W}" height="{CODE_H}" rx="4" fill="currentColor" fill-opacity=".03" stroke="currentColor" stroke-opacity=".28"/>')
    cells = [('CHECKS', 'CI · LINT RULES · TESTS'), ('INSTRUCTIONS', 'CLAUDE.md · AGENTS.md'),
             ('SKILLS', 'TOOLS THE AGENT CAN CALL'), ('CODE', 'PREVIEWS · TYPES · DOCS')]
    ch = CODE_H / 4
    for i, (name, sub) in enumerate(cells):
        y = CODE_Y + i * ch
        if i:
            a(f'<line x1="{CODE_X}" y1="{y:.0f}" x2="{CODE_X + CODE_W}" y2="{y:.0f}" stroke="currentColor" stroke-opacity=".2"/>')
        a(_label(CODE_X + 16, y + 26, name, cls='lbl cell'))
        a(_label(CODE_X + 16, y + 45, sub, size=12.5, cls='lbl sub'))
        bars = {0: [(0, 64), (0, 40), (0, 52)], 1: [(0, 110), (0, 86)], 2: [(0, 46), (56, 46), (112, 46)], 3: [(0, 130), (0, 96), (0, 72)]}[i]
        by = y + 58
        for j, (bx, bw) in enumerate(bars):
            yy = by + (j * 11 if i != 2 else 0)
            a(f'<rect x="{CODE_X + 16 + bx}" y="{yy:.0f}" width="{bw}" height="4" rx="2" fill="currentColor" fill-opacity=".22"/>')
        # each layer brightens for a moment as a change reaches it - the codebase being written to
        layer_hits = [((k / N) + f_cells[i]) % 1.0 for k in range(N)]
        a(f'<rect x="{CODE_X}" y="{y:.0f}" width="{CODE_W}" height="{ch:.0f}" fill="currentColor" opacity="0">'
          + _keyed('opacity', _pulse_points(layer_hits, rise=0.003, fall=0.035, peak='.06'), T, discrete=False) + '</rect>')
    # the CHECKS cell: when a caught mistake is filed, the border flashes and a new rule bar
    # writes itself in orange, settles to ivory, and fades before the lap ends
    a(f'<rect x="{CODE_X}" y="{CODE_Y}" width="{CODE_W}" height="{ch:.0f}" rx="4" fill="none" stroke="{ACCENT}" stroke-width="1.5" opacity="0">'
      + _keyed('opacity', _pulse_points(file_times, fall=0.03, peak='.9'), TT, discrete=False) + '</rect>')
    for j, t0 in enumerate(file_times):
        bx, by = CODE_X + 16 + 96, CODE_Y + 58 + j * 11
        t_settle, t_end = min(t0 + 0.03, 0.998), min(t0 + 0.16, 0.999)
        a(f'<rect x="{bx}" y="{by:.0f}" width="0" height="4" rx="2" fill="{IVORY}" opacity="0">'
          + _keyed('opacity', [(0.0, '0'), (t0, '1'), (t_end, '0'), (1.0, '0')], TT)
          + _keyed('fill', [(0.0, IVORY), (t0, ACCENT), (t_settle, IVORY), (1.0, IVORY)], TT)
          + f'<animate attributeName="width" values="0;0;72;72;72" keyTimes="0;{t0:.4f};{min(t0 + 0.012, 0.998):.4f};0.999;1" dur="{TT}s" repeatCount="indefinite"/></rect>')
    # a CI status light in the CHECKS cell: orange while a mistake is being caught
    a(f'<circle cx="{CODE_X + CODE_W - 22}" cy="{CODE_Y + 22}" r="4" fill="{IVORY}">'
      + _keyed('fill', _step_points(IVORY, catch_times, 0.03, ACCENT), TT) + '</circle>')
    a(_label(CODE_X + CODE_W - 34, CODE_Y + 26, 'CI', size=11, anchor='end', cls='lbl sub ci'))
    a(_label(CODE_X, CODE_Y - 16, 'THE CODEBASE'))
    a('</g>')

    # ---- the gate: a square on the track with a check; it pulses and throws a ring of dots on every catch
    gx, gy, gs = GATE_X, TRACK_TOP, 76
    a('<g class="gate">')
    a(f'<rect x="{gx - gs/2}" y="{gy - gs/2}" width="{gs}" height="{gs}" rx="3" fill="var(--bg,#0b0b0c)" stroke="currentColor" stroke-opacity=".7" stroke-width="1.4"/>')
    a(f'<path d="M{gx - 30},{gy - 22} l6,6 l12,-13" fill="none" stroke="{IVORY}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">'
      + _keyed('stroke', _step_points(IVORY, catch_times, 0.012, ACCENT), TT) + '</path>')
    a(f'<rect x="{gx - gs/2 - 7}" y="{gy - gs/2 - 7}" width="{gs + 14}" height="{gs + 14}" rx="6" fill="none" stroke="{ACCENT}" stroke-width="1.5" opacity="0">'
      + _keyed('opacity', _pulse_points(catch_times, rise=0.001, fall=0.012), TT, discrete=False) + '</rect>')
    # the dot burst: twelve dots that fly out from the gate and fade, once per catch
    for d in range(12):
        ang = 2 * pi * d / 12
        dx, dy = cos(ang), sin(ang)
        tr = {0.0: '0 0', 1.0: '0 0'}
        for c in catch_times:
            tr[max(c - 0.0005, 0.0)] = '0 0'
            tr[min(c + 0.015, 0.999)] = f'{dx*18:.1f} {dy*18:.1f}'
            tr[min(c + 0.0152, 0.9995)] = '0 0'
        trs = sorted(tr.items())
        a(f'<circle cx="{gx + dx * 46:.1f}" cy="{gy + dy * 46:.1f}" r="2" fill="{ACCENT}" opacity="0">'
          + _keyed('opacity', _pulse_points(catch_times, rise=0.0005, fall=0.015, peak='.9'), TT, discrete=False)
          + f'<animateTransform attributeName="transform" type="translate" values="{";".join(v for _, v in trs)}" '
            f'keyTimes="{";".join(f"{t:.4f}" for t, _ in trs)}" dur="{TT}s" repeatCount="indefinite"/></circle>')
    a(_label(gx, gy + gs / 2 + 26, 'THE CHECK', anchor='middle'))
    a('</g>')

    # ---- the agents: five little robots in terminal windows, each typing and blinking
    a('<g class="agents">')
    for i, (key, name) in enumerate(AGENTS):
        y = AGENT_YS[i]
        a(f'<rect x="{AGENT_X}" y="{y}" width="{AGENT_W}" height="{AGENT_H}" rx="4" fill="currentColor" fill-opacity=".03" stroke="currentColor" stroke-opacity=".28"/>')
        a(f'<line x1="{AGENT_X}" y1="{y + 24}" x2="{AGENT_X + AGENT_W}" y2="{y + 24}" stroke="currentColor" stroke-opacity=".2"/>')
        for d in range(3):
            a(f'<circle cx="{AGENT_X + 14 + d * 10}" cy="{y + 12}" r="2.2" fill="currentColor" fill-opacity=".35"/>')
        a(_label(AGENT_X + AGENT_W - 14, y + 17, name.upper(), size=12, anchor='end', cls='lbl name'))
        a(f'<text x="{AGENT_X + 16}" y="{y + 52}" font-size="14" {_MONO} fill="currentColor" fill-opacity=".8">&#8811;</text>')
        # the prompt line types itself out over the lap, at a different phase per agent, and clears
        w = [150, 118, 176, 132, 160][i]
        ph = i / len(AGENTS)
        a(f'<rect x="{AGENT_X + 36}" y="{y + 44}" width="0" height="5" rx="2.5" fill="currentColor" fill-opacity=".55">'
          f'<animate attributeName="width" values="0;{w};{w};0;0" keyTimes="0;.55;.9;.9;1" dur="{T}s" begin="-{ph * T:.3f}s" repeatCount="indefinite"/></rect>')
        a(f'<rect x="{AGENT_X + 38}" y="{y + 41}" width="7" height="11" fill="{ACCENT}">'
          f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="{T/12:.3f}s" begin="-{i * 0.2:.2f}s" repeatCount="indefinite"/>'
          f'<animate attributeName="x" values="{AGENT_X + 38};{AGENT_X + 38 + w};{AGENT_X + 38 + w};{AGENT_X + 38};{AGENT_X + 38}" keyTimes="0;.55;.9;.9;1" dur="{T}s" begin="-{ph * T:.3f}s" repeatCount="indefinite"/></rect>')
    a(_label(AGENT_X, AGENT_Y0 - 16, 'THE AGENTS'))
    a('</g>')

    # ---- the agents on the track: five robots, each carrying a change. On lap k
    # robot k's parcel is the mistake: orange with an x from the agents to the gate,
    # then an ivory check round to the agents. Every other lap it is a plain change.
    a('<g class="changes">')
    for k, (key, _name) in enumerate(AGENTS):
        begin = -(k / N) * T
        # parcel state over the full cycle, in cycle fractions, relative to this robot's own clock
        # (its animate begins at the same offset as its motion, so lap j runs j/LAPS .. (j+1)/LAPS)
        lap = k
        t_orange_on = ((lap - 1 + f_agents) % LAPS) / LAPS      # leaving the agents on the lap before
        t_catch = (lap + f_gate) / LAPS
        t_check_off = ((lap + f_agents) % LAPS) / LAPS           # back at the agents
        pts_fill = {0.0: IVORY, 1.0: IVORY, t_orange_on: ACCENT, t_catch: IVORY}
        pts_x = {0.0: '0', 1.0: '0', t_orange_on: '1', t_catch: '0'}
        pts_ok = {0.0: '0', 1.0: '0', t_catch: '1', t_check_off: '0'}
        if t_orange_on > t_catch:  # the orange stretch wraps the cycle boundary
            pts_fill[0.0] = ACCENT; pts_x[0.0] = '1'
        if t_check_off < t_catch:
            pts_ok[0.0] = '1'
        dark = 'var(--bg,#0b0b0c)'
        chest = (f'<path d="M-3.5,-3.5 L3.5,3.5 M3.5,-3.5 L-3.5,3.5" stroke="{dark}" stroke-width="2" stroke-linecap="square" opacity="0">'
                 + _keyed('opacity', list(pts_x.items()), T * LAPS, begin=begin) + '</path>'
                 f'<path d="M-4.5,0 l3,3 l6,-6.5" fill="none" stroke="{dark}" stroke-width="2" stroke-linecap="square" stroke-linejoin="miter" opacity="0">'
                 + _keyed('opacity', list(pts_ok.items()), T * LAPS, begin=begin) + '</path>')
        body = _robot(key, -24, -17, 48, chest=chest)
        # the whole robot changes colour: orange while it carries the mistake, ivory otherwise
        body = body.replace('fill="currentColor" shape-rendering="crispEdges">', f'fill="{IVORY}" shape-rendering="crispEdges">'
                            + _keyed('fill', list(pts_fill.items()), T * LAPS, begin=begin), 1)
        a(f'<g>{body}<animateMotion dur="{T}s" begin="{begin:.3f}s" repeatCount="indefinite" calcMode="linear"><mpath href="#hero-track"/></animateMotion></g>')
    a('</g>')
    a('</svg>')
    return ''.join(parts)


if __name__ == '__main__':
    print(hero())
