#GlowScript 1.1 VPython
# Converted from the VPython program MandelbrotOrbits3D
'''
    MandelbrotOrbits3D.py     Copyright (C) 2015 Alan Richmond (Tuxar.uk, FractalArt.Gallery)
    =====================     MIT License
'''
from visual import *
import random as Math       # comment out for Glowscript
#width,height=1920,1080     # my left monitor
#width,height=1280,1024     # my right monitor
#width,height=1280,720      # YouTube HD
#width,height=1152,870
width,height=1024,768
#width,height=800,600

#   Major parameters
sidey=2**6                  # samples from Mandelbrot set, vertically
maxit=64                    # maximum iterations per point
flipx=False                 # flipx means: flip the x-coordinate up into z
tt=0.002                    # trail thickness
grid=4                      # how often to show orbit
gofx=0                      # grid offset, x
gofy=0                      # grid offset, y
radius=1.2/sidey            # size of balls indicating sample point

#   Complex plane
xmin = -2.25
xmax = 0.75
ymax = 1.25
ymin = -ymax

#   Scaling
xd = xmax - xmin
yd = ymax - ymin
sidex=int(sidey*xd/yd)
xscale = xd / sidex
yscale = yd / sidey

#   Stars
spacesize = xmax*4
nstars = 2**9
starsz=radius/1.7
radius2 = Math.random()*starsz
d=0
def Setup():
    global d
    title="The Orbits of Starship Mandelbrot in 3D"
    d=display(title=title,width=width,height=height)
    d.range=1.5
    d.autoscale=False
    d.center=vector(-0.75,0,0)
    d.autocenter=False
#   Following code can be uncommented for Glowscript.org
#    $('<button />').text("FlipY").appendTo(d.title).click( def ():
#    global change, flipx
#    flipx= !flipx
#    if flipx:   $(this).text("FlipX")
#    else:       $(this).text("FlipY")
#    change=True
#)
#    prompt = $("<p>Grid frequency (red balls): </p>").appendTo(d.title)
#    s  = "<option select=selected>4</option><option>2</option><option>3</option><option>5</option><option>6</option><option>7</option><option>8</option><option>9</option>"
#    $('<select/>').html(s).css(font="sans").change(def ():
#    global grid, change
#    grid=int($(this).val())
#    change=True
#).appendTo(prompt)
#    prompt = $("<p>Grid offset x: </p>").appendTo(d.title)
#    s  = "<option select=selected>0</option><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option><option>6</option><option>7</option><option>8</option"
#    $('<select/>').html(s).css(font="sans").change(def ():
#    global gofx, change
#    gofx=int($(this).val())
#    change=True
#).appendTo(prompt)
#    prompt = $("<p>Grid offset y: </p>").appendTo(d.title)
#    s  = "<option select=selected>0</option><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option><option>6</option><option>7</option><option>8</option"
#    $('<select/>').html(s).css(font="sans").change(def ():
#    global gofy, change
#    gofy=int($(this).val())
#    change=True
#).appendTo(prompt)
    return

def mandel(ix, iy):

    xp=x=xscale * ix + xmin
    yp=y=-yscale * iy + ymax
    store=[(x,y)]
    trail = curve(pos=vector(x, y, 0),radius=tt)
    trail.visible = False

    for it in range(maxit):

        xt=x*x-y*y+xp
        y=2*x*y+yp
        x=xt
        z=(x,y)
        bc=vector(1,1,1)
        col=color.hsv_to_rgb(vector(it*1.0/maxit,1,1))

        if (ix+gofx)%grid==0 and (iy+gofy)%grid==0:
            bc=vector(1,0,0)
            if flipx:
                zo = x - xp
                trail.append(pos=vector(xp, y, zo),color=col)
            else:
                zo = y - yp
                trail.append(pos=vector(x, yp, zo),color=col)

        if x*x+y*y>4: return it
        z=(x,y)
        if z in store: break    # completed orbit
        store.append(z)
        
    trail.visible = True
    ball = sphere(pos=vector(xp, yp, 0), radius=radius,color=bc)
    return it

#   Stars from
#   http://vpython.org/contents/contributed/vspace.py

def randpoint_onsphere(radius):
    """ Generate a random point on the outside of a sphere.
    """
    theta = Math.random() * ( 2 * pi )
    u = Math.random() * 2 - 1
    x = radius * sqrt(  1 - u**2) * cos(theta)
    y = radius * sqrt(  1 - u**2) * sin(theta)
    z = radius * u
    return vector(x,y,z)

def rand_3tuple(min=0, max=1):
    """ Generate a random 3 item tuple between min & max
    """
    m = max-min
    r = m * Math.random() + min
    b = m * Math.random() + min
    g = m * Math.random() + min
    return vector(r,g,b)

def Stars():
    for n in range(nstars):
        pos = randpoint_onsphere(spacesize)
        col = rand_3tuple(.3, .7)
        sphere( pos=pos, radius=radius2, color=col)

def Mandelbrot():
    for ix in range(sidex):
        for iy in range(sidey):
                mandel(ix,iy)

def Show():
    for obj in d.objects:
        obj.visible=False
    Stars()
    Mandelbrot()

Setup()
change=True
while True:
    rate(60)
    if change:
        change=False
        Show()

#   Rudimentary panning
#    dist=0.1
#    event=d.waitfor('keydown')
#    key = event.which 
#    if key=='left': d.center-=vector(dist,0,0)
#    elif key=='right': d.center+=vector(dist,0,0)
#    elif key=='up': d.center+=vector(0,dist,0)
#    elif key=='down': d.center-=vector(0,dist,0)
#   Earlier attempt to get number from user
#    d.caption.text("Vary the sampling frequency (red balls): ")
#    def setfreq():
#        global freq
#        freq = $("#freq_slider").slider("value")
#    $('<div id="freq_slider"></div>').appendTo(d.title).css(width="350px")
#    $(def ():
#        $("#freq_slider").slider(value=8, min=1, max=10, range="min", slide=setfreq, change=setfreq)
#)