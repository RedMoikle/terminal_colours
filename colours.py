#! python3
"""
Add helpful ANSI tools for printing funky text
# Author: Michael Stickler

Examples:
cprint('Hello', fg='r') # prints red text
cprint('Hello', fg='dg', style='bi') # prints dark green, bold italic text
cprint('Hello', preset='error') # prints text with the 'error' preset

print(colour('ERROR: ', preset='error') + "something went wrong!") 
#prints an error message and the first word is highlighted

new_preset("important", fg="a530", style="rb", test=True)
#creates a new preset called "important" and gives a sample.

print_rainbow(f'{"~" * 10}HOLY WOW, RAINBOWS!{"~" * 10}', rotations=5, style="b")
print_rainbow(f'{" " * 120}\n' * 40, rotations=81, style="r")

List of colours (for fg and bg):
    k   black
    r   red
    g   green
    y   yellow
    b   blue
    m   magenta
    c   cyan
    w   white

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
g: greyscale
    0-25 brightness
    g0: black
    g12: middle grey
"""
from math import sin, pi
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
    'w': 7   # white
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


def cprint(message, preset=None, fg=None, bg=None, style="", br=False, *args, **kwargs):
    """print a string with a particular colour/style"""
    print(colour(message, preset, fg, bg, style, br), *args, **kwargs)


def colour(message, preset=None, fg=None, bg=None, style="", br=False, ) -> str:
    """return a string with a particular colour/style, useful for mixing styles"""
    if preset is None:
        prop_str = style_code(fg, bg, style, br)
    else:
        prop_str = PRESETS[preset]
    if prop_str:
        # TODO: if \n in message, skip formatting on them
        return f"\x1b[{prop_str}m{message}\x1b[0m"
    else:
        return message


def new_preset(name, fg=None, bg=None, style="", br=False, test=False):
    """Saves a preset ANSI code under a name for easy reference"""
    preset = style_code(fg, bg, style, br)
    PRESETS[name] = preset
    if test:
        cprint(f"Test message using the new style preset: ({name}) {preset}", name)


def style_code(fg=None, bg=None, style="", br=False) -> str:
    """Generates and returns a ANSI code sequence as a string."""
    properties: List[str] = []
    if fg is not None:
        properties.append(f"3{get_colour_code(fg)}")
    if bg is not None:
        properties.append(f"4{get_colour_code(bg)}")
    if br and fg is not None or bg is not None:
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
            g: greyscale
                0-25 brightness
                g0: black
                g12: middle grey
    """
    if code.startswith("l"):
        return f"8;5;{COLCODE[code[1]]}"
    if code.startswith("d"):
        return f"8;5;{COLCODE[code[1]] + 8}"
    if code.startswith("a"):
        return f"8;5;{16 + int(code[1:], 6)}"
    if code.startswith("g"):
        if code[1:] == "0":
            return f"8;5;0"
        if code[1:] == "25":
            return f"8;5;25"
        return f"8;5;{233 + int(code[1:])}"
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
        if char == "\n":
            print("".join([colour(char, fg=f"a{r}{g}{b}", style=style)
                           for char, r, g, b in rgb]))
            rgb = []
            continue
        rgb.append([char] + rainbow_nums(frequency, i))
        # [max(0, min(5, int(6 * (sin(2 * pi * (frequency * i + 0.333 * channel)) / 2 + 0.5))))
        # for channel in range(1, 4)])
    print("".join([colour(char, fg=f"a{r}{g}{b}", style=style)
                   for char, r, g, b in rgb]))


# default presets
testing = __name__ == '__main__'
new_preset("info", fg="lc", style="i", test=testing)
new_preset("debug", fg="lm", style="i", test=testing)
new_preset("warning", fg="y", br=True, style="iu", test=testing)
new_preset("error", fg="r", br=True, style="bu", test=testing)
new_preset("critical", fg="dr", style="rbu", test=testing)
if __name__ == '__main__':
    print_rainbow(f'{" " * 120}\n' * 4, rotations=11.5, style="r")
    print_rainbow(f'{"~" * 10}HOLY WOW, RAINBOWS!{"~" * 10}'.center(120), rotations=5, style="b")
