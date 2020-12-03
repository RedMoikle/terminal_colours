# terminal_colours

##Add helpful ANSI tools for printing funky text

**Author: Michael Stickler**

![Preview image](/preview.PNG)
****
###Contents:

Functions

Colour and Style Code Guide

****
##Functions

####cprint

######(message, preset=None, tx=None, bg=None, style="", br=False)

Message is required, all other params are optional and can be named.

Prints a message to the screen in a particular colour and style
    
    import terminal_colours.colours as tc
    tc.cprint('Hello', tx='r') # prints red text
    tc.cprint('Hello', tx='dg', style='bi') # prints dark green, bold italic text
    tc.cprint('Hello', preset='error') # prints text with the 'error' preset

####colour

######(message, preset=None, tx=None, bg=None, style="", br=False)

Message is required, all other params are optional and can be named.

Returns a string formatted with a specified colour and style. 
This can be used to mix styles.

    tc.colour('WARNING', preset='warning') 
    # Returns '\x1b[33;3;4mWARNING\x1b[0m'
    
    print(tc.colour('ERROR: ', preset='error') + "something went wrong!") 
    #prints an error message and the first word is highlighted
    
####new_preset

######(name, preset=None, tx=None, bg=None, style="", br=False, test=False)

name is required, all other params are optional and can be named.

Creates a new preset format that you can use with the other commands in this module.
You can also add the `test=True` parameter to have it print out an example of the preset.

    tc.new_preset("important", tx="a530", style="rb")
    #creates a new preset called "important"
    
    tc.new_preset("important", tx="a530", style="rb", test=True)
    #does the same as the last line, but also gives a sample.
    
now these presets can be used:

    print(tc.colour("ATTENTION! ", "important") + "This message is super duper important")
   
####style_code

######(tx=None, bg=None, style="", br=False, test=False)

All params are optional and can be named.

Generates a style code that can be added to text. Will also need to be surrounded by ANSI tags:
   
    message = "Red text"
    style = tc.style_code(tx = "r")
    styled_message = '\x1b[{style}m{message}\x1b[0m)'

####print_rainbow

######(message, rotations=1, style="")

Give it a try, or don't, I definitely didn't spend hours programming this, nope, not at all.

    tc.print_rainbow(f'{"~" * 10}HOLY WOW, RAINBOWS!{"~" * 10}', rotations=5, style="b")
    tc.print_rainbow(f'{" " * 120}\n' * 40, rotations=81, style="r")

##Colour/style string codes:

Use these in a string whenever a "tx" or "bg" parameter is required

## Styles

(some of these may or may not work depending on your terminal):

    b:   bold
    i:   italic
    u:   underline
    s:   strikethrough
    x:   blinking
    r:   reverse
    y:   fast blinking
    f:   faint
    h:   hide
***

## Colours

    k:   black
    r:   red
    g:   green
    y:   yellow
    b:   blue
    m:   magenta
    c:   cyan
    w:   white

***

### More colours:

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
    a225: the best blue
    a555: full white
    
s: greyscale

    0-25 brightness
    s0 :  black
    s12: middle grey
    s25: white
