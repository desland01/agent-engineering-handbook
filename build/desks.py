"""Three empty workstations, for the page that carries the career-level claim.

The claim on that page is that building an environment where code lands well is
the skill worth having. This drawing is that claim's punchline: a streaming desk,
a course desk and an interview set, every chair pushed back and empty, while the
little robots from the home page work at the desks and the screens keep landing
green checks on their own.

Nobody is named. The stations are archetypes — the people whose public work this
handbook reads have not endorsed it, so no desk carries a name and the drawing
attributes nothing to anyone.

Continuity, as on the home page: every animation is SMIL on one shared period, so
frame t and frame t + PERIOD are identical and the loop never restarts.
"""
from robots import ROBOTS

PERIOD = 9.0                              # seconds for one pass
PANEL_W, PANEL_H, GAP = 320, 224, 28
VIEW_W = PANEL_W * 3 + GAP * 2
VIEW_H = PANEL_H + 40                     # room for the caption under each panel

FLOOR = 196                               # the line everything stands on
DESK_TOP, DESK_X, DESK_W = 140, 28, 224   # the slab, and where it starts

ACCENT = '#f37a3b'
_MONO = 'font-family="var(--font-mono, ui-monospace, SFMono-Regular, Menlo, monospace)" letter-spacing=".12em"'

STATIONS = [
    ('THE STREAM', 'ON AIR · NO', 'claude'),
    ('THE COURSE', 'RENDER · DONE', 'gemini'),
    ('THE INTERVIEW', 'GUEST · AWAY', 'kimi'),
]


def _label(x, y, text, size=13, anchor='start', cls='lbl'):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" {_MONO} '
            f'fill="currentColor">{text}</text>')


def _hair(x, y, w, h, rx=3, op='.3'):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="currentColor" '
            f'fill-opacity=".03" stroke="currentColor" stroke-opacity="{op}"/>')


def _stroke(d, op='.5', w=1.6):
    return (f'<path d="{d}" fill="none" stroke="currentColor" stroke-opacity="{op}" stroke-width="{w}" '
            'stroke-linecap="round" stroke-linejoin="round"/>')


def _floor(ox):
    return (f'<line x1="{ox + 14}" y1="{FLOOR}" x2="{ox + PANEL_W - 14}" y2="{FLOOR}" '
            'stroke="currentColor" stroke-opacity=".24"/>')


def _desk(ox):
    """A slab on two legs, standing on the floor. Everything else rests on it."""
    x, t = ox + DESK_X, DESK_TOP
    return (f'<rect x="{x}" y="{t}" width="{DESK_W}" height="7" rx="2" fill="currentColor" fill-opacity=".22"/>'
            + _stroke(f'M{x + 12} {t + 7} V{FLOOR}', op='.4')
            + _stroke(f'M{x + DESK_W - 12} {t + 7} V{FLOOR}', op='.4'))


def _robot(key, cx, w, base=DESK_TOP):
    """One of the home page's robots, standing on the slab at the keyboard.

    Drawn quieter than on the home page, and with its accent pixel dropped to the
    same ink as its body: in this picture the subject is the empty chair, so the
    robot must not be the brightest thing in the frame."""
    h = w * 28 / 40
    x, y = cx - w / 2, base - h
    svg = ROBOTS.get(key)
    if not svg:
        return (f'<g transform="translate({x},{y}) scale({w / 40})">'
                '<rect x="6" y="4" width="28" height="18" rx="2" fill="currentColor"/>'
                '<rect x="8" y="22" width="4" height="4" fill="currentColor"/>'
                '<rect x="28" y="22" width="4" height="4" fill="currentColor"/></g>')
    inner = svg[svg.index('>') + 1:svg.rindex('</svg>')]
    inner = inner.replace('var(--accent-text,#f37a3b)', 'currentColor')
    return (f'<g transform="translate({x},{y}) scale({w / 40})" fill="currentColor" '
            f'fill-opacity=".5" shape-rendering="crispEdges">{inner}</g>')


def _chair(cx, s=1.0, flip=False, turn=-8):
    """An office chair seen from the side, standing on the floor, with nobody in
    it. It is drawn turned a few degrees — the angle a chair keeps after someone
    pushes it back and walks off."""
    body = ('<g fill="none" stroke="currentColor" stroke-opacity=".85" stroke-width="1.8" '
            'stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M6 0v30a5 5 0 0 0 5 5h17"/>'          # the back, and the seat's near edge
            '<path d="M8 35h30a3 3 0 0 1 0 6H14a6 6 0 0 1-6-6z"/>'   # the seat
            '<path d="M22 41v14"/><path d="M8 58h28"/>'      # the column and the base
            '<path d="M14 55l-6 3M30 55l6 3"/>'
            '<path d="M10 6h-3M10 14h-3" stroke-opacity=".45"/></g>')
    sx = -1 if flip else 1
    return (f'<g transform="translate({cx},{FLOOR - 58 * s}) scale({sx * s},{s}) '
            f'rotate({turn} 22 30)">{body}</g>')


def _screen(x, y, w, h, phase, T, rows=3):
    """A screen that keeps landing checks by itself: rows of bars, and one accent
    check ticking onto the next row each beat. One accent on screen at a time."""
    out = [_hair(x, y, w, h, rx=3, op='.36'),
           f'<line x1="{x}" y1="{y + 16}" x2="{x + w}" y2="{y + 16}" stroke="currentColor" stroke-opacity=".2"/>']
    for d in range(3):
        out.append(f'<circle cx="{x + 10 + d * 7}" cy="{y + 8}" r="1.6" fill="currentColor" fill-opacity=".3"/>')
    step = (h - 26) / rows
    for i in range(rows):
        ry = y + 26 + i * step
        out.append(f'<rect x="{x + 11}" y="{ry:.1f}" width="{w - 52}" height="3.5" rx="1.75" '
                   'fill="currentColor" fill-opacity=".16"/>')
        begin = -(((i + phase) % rows) / rows) * T
        out.append(
            f'<g opacity="0"><path d="M{x + w - 30},{ry + 1.5:.1f} l3.5,3.5 l7,-8" fill="none" stroke="{ACCENT}" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.05;0.30;0.34;1" '
            f'dur="{T}s" begin="{begin:.3f}s" repeatCount="indefinite"/></g>')
    return ''.join(out)


def _stand(cx, top):
    """The neck and foot that hold a monitor on the slab."""
    return (_stroke(f'M{cx} {top} V{DESK_TOP - 4}', op='.4')
            + f'<rect x="{cx - 13}" y="{DESK_TOP - 6}" width="26" height="4" rx="2" fill="currentColor" fill-opacity=".3"/>')


def _keyboard(ox):
    return (f'<rect x="{ox + DESK_X + 118}" y="{DESK_TOP - 5}" width="56" height="4" rx="1.5" '
            'fill="currentColor" fill-opacity=".3"/>')


def _stream(ox, T, key):
    """A streaming desk. The chat keeps scrolling and the checks keep landing;
    the on-air lamp is the one thing that never comes on."""
    a = [_screen(ox + 40, 40, 134, 80, 0, T), _stand(ox + 107, 120)]
    # the chat column, still moving with nobody reading it
    a.append(_hair(ox + 182, 40, 46, 80, rx=3, op='.26'))
    for i in range(5):
        w = [26, 34, 20, 30, 24][i]
        a.append(f'<rect x="{ox + 189}" y="{52 + i * 14}" width="{w}" height="3.5" rx="1.75" '
                 f'fill="currentColor" fill-opacity=".2">'
                 f'<animate attributeName="y" values="{52 + i * 14};{38 + i * 14}" dur="{T / 5:.3f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.2;.8;1" dur="{T / 5:.3f}s" repeatCount="indefinite"/></rect>')
    # the boom arm and its microphone, swung aside, and the on-air lamp on its clip
    a.append(_stroke(f'M{ox + 262} {DESK_TOP} V72 h-22', op='.45'))
    a.append(f'<rect x="{ox + 233}" y="72" width="13" height="21" rx="6.5" fill="currentColor" fill-opacity=".1" '
             'stroke="currentColor" stroke-opacity=".45" stroke-width="1.4"/>')
    # the lamp that would say ON AIR: drawn, never lit
    a.append(f'<circle cx="{ox + 262}" cy="60" r="4.5" fill="none" stroke="currentColor" stroke-opacity=".3"/>')
    a.append(_keyboard(ox))
    a.append(_desk(ox))
    a.append(_robot(key, ox + DESK_X + 146, 44))
    a.append(_chair(ox + 190, 1.0))
    return ''.join(a)


def _course(ox, T, key):
    """A course desk. The playhead crosses the timeline and the render completes
    whether or not anyone is watching it."""
    a = [_screen(ox + 40, 36, 152, 74, 1, T), _stand(ox + 116, 110)]
    # the edit timeline under the screen: clips, and a playhead crossing once a pass
    for bx, bw in [(0, 30), (36, 20), (62, 42), (110, 26), (142, 10)]:
        a.append(f'<rect x="{ox + 46 + bx}" y="118" width="{bw}" height="8" rx="2" '
                 'fill="currentColor" fill-opacity=".18"/>')
    a.append(f'<rect x="{ox + 46}" y="115" width="1.6" height="14" fill="{ACCENT}">'
             f'<animate attributeName="x" values="{ox + 46};{ox + 198};{ox + 198}" keyTimes="0;.85;1" '
             f'dur="{T}s" repeatCount="indefinite"/></rect>')
    # the camera on its tripod, standing on the floor beside the desk
    a.append(f'<rect x="{ox + 232}" y="78" width="34" height="22" rx="3" fill="currentColor" fill-opacity=".06" '
             'stroke="currentColor" stroke-opacity=".5" stroke-width="1.6"/>')
    a.append(_stroke(f'M{ox + 266} 84 l10 -5 v16 l-10 -5z', op='.5'))
    a.append(f'<circle cx="{ox + 243}" cy="89" r="4.5" fill="none" stroke="currentColor" stroke-opacity=".45"/>')
    a.append(_stroke(f'M{ox + 249} 100 V{FLOOR - 20} M{ox + 249} {FLOOR - 20} l-12 20 M{ox + 249} {FLOOR - 20} l12 20', op='.45'))
    a.append(_keyboard(ox))
    a.append(_desk(ox))
    a.append(_robot(key, ox + DESK_X + 146, 44))
    a.append(_chair(ox + 186, 1.0))
    return ''.join(a)


def _interview(ox, T, key):
    """An interview set: two chairs turned towards each other with a microphone
    between them, and nobody in either one."""
    a = []
    # the standing lamp, the one light left on
    a.append(_stroke(f'M{ox + 44} 58 l26 0 l9 20 h-44z', op='.45'))
    a.append(_stroke(f'M{ox + 57} 78 V{FLOOR} M{ox + 44} {FLOOR} h26', op='.45'))
    for i in range(3):
        a.append(f'<path d="M{ox + 42 + i * 13} 86 l-5 11" stroke="{ACCENT}" stroke-width="1.4" '
                 'stroke-linecap="round" opacity=".45"/>')
    # the screen on a stand at the side, still landing checks
    a.append(_screen(ox + 204, 74, 92, 52, 2, T, rows=2))
    a.append(_stroke(f'M{ox + 250} 126 V{FLOOR} M{ox + 236} {FLOOR} h28', op='.4'))
    # the two chairs, turned towards each other across the microphone
    a.append(_chair(ox + 96, 0.95, turn=-8))
    a.append(_chair(ox + 206, 0.95, flip=True, turn=-8))
    # the microphone on its stand, between them
    a.append(f'<rect x="{ox + 150}" y="{FLOOR - 80}" width="14" height="22" rx="7" fill="currentColor" '
             'fill-opacity=".1" stroke="currentColor" stroke-opacity=".5" stroke-width="1.4"/>')
    a.append(_stroke(f'M{ox + 157} {FLOOR - 58} V{FLOOR} M{ox + 143} {FLOOR} h28', op='.5'))
    a.append(_robot(key, ox + 262, 40, base=FLOOR))
    return ''.join(a)


def _station(i, T):
    name, status, key = STATIONS[i]
    build = (_stream, _course, _interview)[i]
    return (f'<svg class="desks-loop" viewBox="0 0 {PANEL_W} {VIEW_H}" role="img" aria-label="{ALT[i]}">'
            '<defs><pattern id="desks-dots-' + str(i) + '" width="24" height="24" patternUnits="userSpaceOnUse">'
            '<circle cx="1" cy="1" r="1" fill="currentColor" fill-opacity=".12"/></pattern></defs>'
            f'<rect width="{PANEL_W}" height="{VIEW_H}" fill="url(#desks-dots-{i})"/>'
            + _hair(0, 0, PANEL_W, PANEL_H, rx=4, op='.18')
            + _floor(0) + build(0, T, key)
            + _label(18, PANEL_H + 26, name)
            + _label(PANEL_W - 18, PANEL_H + 26, status, size=11, anchor='end', cls='lbl sub')
            + '</svg>')


ALT = [
    'A streaming desk with the chair pushed back and nobody in it. A small robot works at '
    'the keyboard, the chat column keeps scrolling and the screen keeps landing green checks; '
    'the on-air lamp is dark.',
    'A course desk with the chair pushed back and nobody in it. A small robot works at the '
    'keyboard while the playhead crosses the edit timeline and the screen lands green checks.',
    'An interview set: two chairs turned towards each other across a microphone, both empty, '
    'a lamp still on, and a screen at the side still landing green checks.',
]


def desks():
    """The three stations, as three drawings in one scrolling row. They are separate
    so each is a scroll-snap target on a phone; they share one period, and each
    starts its own SMIL clock at page load, so they stay in step."""
    return ('<div class="desks-row" tabindex="0" role="group" '
            'aria-label="Three empty workstations">'
            + ''.join(_station(i, PERIOD) for i in range(3))
            + '</div>')


if __name__ == '__main__':
    print(desks())
