#! python3
"""
Add helpful ANSI tools for printing funky text
# Author: Michael Stickler

Examples:
cprint('Hello', tx='r') # prints red text
cprint('Hello', tx='dg', style='bi') # prints dark green, bold italic text
cprint('Hello', preset='error') # prints text with the 'error' preset

print(colour('ERROR: ', preset='error') + "something went wrong!") 
#prints an error message and the first word is highlighted

new_preset("important", tx="a530", style="rb", test=True)
#creates a new preset called "important" and gives a sample.

print_rainbow(f'{"~" * 10}HOLY WOW, RAINBOWS!{"~" * 10}', rotations=5, style="b")
print_rainbow(f'{" " * 120}\n' * 40, rotations=81, style="r")

List of styles:
    b   bold
    i   italic
    u   underline
    s   strikethrough
    x   blinking
    r   reverse
    y   fast blinking
    f   faint
    h   hide

List of colours (for tx and bg):
    k   black
    r   red
    g   green
    y   yellow
    b   blue
    m   magenta
    c   cyan
    w   white

more colours:
prefix with the following:
l: light colour codes (light and dark may be inverted in dark mode)
    lk: light black
    lr: red
    lg: green
    ly: yellow
    lb: blue
    lm: magenta
    lc: cyan
    lw: white
d: dark colour codes (light and dark may be inverted in dark mode)
    dk: black
    dr: tan
    dg: green
    dy: brown
    db: blue
    dm: purple
    dc: cyan
    dw: light grey
a: rgb values in 3 base 6 digits
    0-5 digits for r then g then b values
    e.g:
    a000: black
    a520: orange
    a022: sea green
s: greyscale
    0-25 brightness
    s0: black
    s12: middle grey
"""
from math import sin, pi, ceil
from typing import List

BRIGHT_ALLOWED = True
COLCODE = {
    'k': 0,  # black
    'r': 1,  # red
    'g': 2,  # green
    'y': 3,  # yellow
    'b': 4,  # blue
    'm': 5,  # magenta
    'c': 6,  # cyan
    'w': 7  # white
}

FMTCODE = {
    'b': 1,  # bold
    'f': 2,  # faint
    'i': 3,  # italic
    'u': 4,  # underline
    'x': 5,  # blinking
    'y': 6,  # fast blinking
    'r': 7,  # reverse
    'h': 8,  # hide
    's': 9,  # strikethrough
}
PRESETS = {}


def cprint(message, preset=None, tx=None, bg=None, style="", br=False, *args, **kwargs):
    """print a string with a particular colour/style"""
    print(colour(message, preset, tx, bg, style, br), *args, **kwargs)


def colour(message, preset=None, tx=None, bg=None, style="", br=False, skip_break=True) -> str:
    """return a string with a particular colour/style, useful for mixing styles"""
    if skip_break:
        m_lines = str(message).split("\n")
    else:
        m_lines = [str(message)]
    if preset is None:
        prop_str = style_code(tx, bg, style, br)
    else:
        prop_str = PRESETS[preset]
    if prop_str:
        # if \n in message, skip formatting on them
        return "\n".join([f"\x1b[{prop_str}m{line}\x1b[0m" for line in m_lines])
    else:
        return message


def new_preset(name, tx=None, bg=None, style="", br=False, test=False):
    """Saves a preset ANSI code under a name for easy reference"""
    preset = style_code(tx, bg, style, br)
    PRESETS[name] = preset
    if test:
        cprint(f"Test message using the new style preset: ({name}) {preset}", name)


def style_code(tx=None, bg=None, style="", br=False) -> str:
    """Generates and returns a ANSI code sequence as a string."""
    properties: List[str] = []
    if tx is not None:
        properties.append(f"3{get_colour_code(tx)}")
    if bg is not None:
        properties.append(f"4{get_colour_code(bg)}")
    if br and tx is not None or bg is not None:
        properties.append("1")
    properties += [str(FMTCODE[s]) for s in style]
    return ";".join(properties)


def get_colour_code(code="") -> str:
    """
    Returns ANSI colour code
    full list of values in module docstring
    Args:
        code (str):
            SIMPLE:
            string containing colour code
                k   black
                r   red
                ...
            ADVANCED:
            prefix with the following:
            l: light colour codes (light and dark may be inverted in dark mode)
                lk: light black
                lr: red
                ...
            d: dark colour codes (light and dark may be inverted in dark mode)
                dk: black
                dr: tan
                ...

            a: rgb values in 3 base 6 digits
                0-5 digits for r then g then b values
                e.g:
                a000: black
                a520: orange
                a022: sea green
            s: greyscale
                s0-23 brightness
                s0: black
                s11: middle grey
    """
    if code.startswith("l"):
        return f"8;5;{COLCODE[code[1]]}"
    if code.startswith("d"):
        return f"8;5;{COLCODE[code[1]] + 8}"
    if code.startswith("a"):
        return f"8;5;{16 + int(code[1:], 6)}"
    if code.startswith("s"):
        if int(code[1:]) > 23:
            raise ValueError("Greyscale colours must be between 0 and 23")
        return f"8;5;{232 + int(code[1:])}"
    return f"{COLCODE[code]}"


def rainbow_nums(freq, i):
    """create rgb values for part of a rainbow"""
    rgb = []
    for channel in range(3):
        rgb.append(max(0, min(5, int(6 * (sin(2 * pi * (freq * i + 0.333 * channel)) / 2 + 0.5)))))
    return rgb


def print_rainbow(message, rotations=1.5, style=""):
    """
    MAGIC :D
    """
    frequency = rotations / len(message)
    rgb = []
    char_iter = iter(enumerate(message))
    for i, char in char_iter:
        rgb.append([char] + rainbow_nums(frequency, i))
        # [max(0, min(5, int(6 * (sin(2 * pi * (frequency * i + 0.333 * channel)) / 2 + 0.5))))
        # for channel in range(1, 4)])
    print("".join([colour(char, tx=f"a{r}{g}{b}", style=style)
                   for char, r, g, b in rgb]))


def readable(message="", col="", background=False, cancel=False, style="", br=False):
    """Formats the string to make sure it is readable"""
    if col in COLCODE:
        if col == "w":
            contrast = "lk"
        else:
            contrast = "dw"
    elif col[0] in ["l", "d"]:
        if col in ["dy", "dc"]:
            contrast = "s0"
        elif col in ["dw", "lw", "dk"]:
            contrast = "lk"
        else:
            contrast = "dw"
    elif col.startswith("a") and int(col[1]) / 2 + int(col[2]) > 2:
        contrast = "s0"
    elif col.startswith("s") and int(col[1:]) > 11:
        contrast = "s0"
    else:
        contrast = "s23"
    if cancel:
        contrast = None
    if background:
        return colour(message, tx=contrast, bg=col, style=style, br=br)
    return colour(message, tx=col, bg=contrast, style=style, br=br)


def test_pattern(bg=True, contrast=True, style=""):
    cancel = not contrast
    print("Simple colours: colour initial")
    print("       " + "".join([readable(f" {c}  ", c,
                                        background=bg,
                                        cancel=cancel,
                                        style=style)
                               for c in COLCODE]) + "\n")

    print("Colour shades: prefix colour initial with l for light or d for dark")
    print("Light: " + "".join([readable(f"l{c} ", f"l{c}",
                                        background=bg,
                                        cancel=cancel,
                                        style=style)
                               for c in COLCODE]))
    print("Dark:  " + "".join([readable(f"d{c} ", f"d{c}",
                                        background=bg,
                                        cancel=cancel,
                                        style=style)
                               for c in COLCODE]) + "\n")

    print("Advanced 256 bit RGB: prefix 3 ints 0-5 with a (a050: green, a210: brown)")
    columns = 2
    rows = ceil(6 / columns)

    for r_row in range(rows):
        for g in range(6):
            print("       ", end="")
            for r in range(r_row * columns, r_row * columns + columns):
                if r < 6:
                    print("".join([readable(f" {r}{g}{b}", f"a{r}{g}{b}", background=bg, cancel=cancel, style=style)
                                   for b in range(6)]),
                          end=" " * 4)
            print("")
        print("")

    print("Greyscale: prefix int 0-23 with s (s0: black, s23: white, s11: 50%grey)")
    print("       " + "".join([readable(f"s{i}".rjust(4), f"s{i}", background=bg, cancel=cancel, style=style)
                               for i in range(0, 12)]) + "")
    print("       " + "".join([readable(f"s{i}".rjust(4), f"s{i}", background=bg, cancel=cancel, style=style)
                               for i in range(12, 24)]) + "\n")


# default presets
testing = __name__ == '__main__'
new_preset("info", tx="lc", style="i", test=testing)
new_preset("debug", tx="lm", style="i", test=testing)
new_preset("warning", tx="y", br=True, style="iu", test=testing)
new_preset("error", tx="r", br=True, style="bu", test=testing)
new_preset("critical", tx="dr", style="rbu", test=testing)
if __name__ == '__main__':
    test_pattern(bg=True)
    print_rainbow(f'{" " * 120}\n' * 4, rotations=11.5, style="r")
    print_rainbow(f'{"~" * 10}HOLY WOW, RAINBOWS!{"~" * 10}'.center(120), rotations=5, style="b")
