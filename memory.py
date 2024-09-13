from random import *
from turtle import *

from freegames import path

#crea los posibles colores y formas para los tiles
tile_formas = ["heart", "star","omega","thunder"]
tile_colores = ["red", "cyan", "green", "blue", "yellow", "purple", "orange", "pink"]

#crea una lista para todas la combinaciones de formas y colores
tiles = [(x, y) for x in tile_formas for y in tile_colores] * 2
shuffle(tiles) # mezcla todo

#Dibuja un corazon
def draw_heart(x, y, color):
    """Draw a heart with the given color at (x,y)."""
    print ("Drawing heart at", x, y, "with color", color)
    #hace los preparativos
    up()
    goto(x, y + 30)
    down()
    fillcolor(color)
    begin_fill()
    #dibuja la figura
    # Dibuja la curva izquierda del corazón
    for _ in range(200):
        right(1)
        forward(2)

    # Dibuja la curva derecha del corazón
    left(120)
    for _ in range(200):
        right(1)
        forward(2)

    #termina el dibujo
    forward(180)
    end_fill()
    setheading(0)

#dibuja un trueno
def draw_thunder(x, y, color):
    """Draw a thunder with the given color at (x,y)."""
    print ("Drawing thunder at", x, y, "with color", color)
    up()
    goto(x, y)
    down()
    fillcolor(color)
    begin_fill()
    # Dibuja la forma del trueno
    left(90)
    forward(100)
    right(120)
    forward(50)
    left(120)
    forward(50)
    right(120)
    forward(50)
    left(120)
    forward(50)
    right(120)
    forward(50)

    # Regresar al punto de inicio
    right(90)
    forward(100)

    end_fill()
    setheading(0)

#dibuja el simbolo omenga
def draw_omega(x, y, color):
    """Draw the Omega symbol with the given color at (x,y)."""
    print ("Drawing Omega at", x, y, "with color", color)
    up()
    goto(x, y + 30)
    down()
    fillcolor(color)
    begin_fill()

    # Dibuja la parte inferior de Omega
    circle(50, 180)  # Dibuja la mitad superior de un círculo
    right(90)
    forward(100)  # Línea vertical central
    left(90)
    circle(-50, 180)  # Dibuja la mitad inferior del círculo (hacia arriba)

    end_fill()
    setheading(0)

def draw_star(x, y, color):
    """Draw a star with the given color at (x, y)."""
    print("Drawing star at", x, y, "with color", color)
    up()
    goto(x, y + 30)
    down()
    fillcolor(color)
    begin_fill()
    #dibuja la figura
    for _ in range(5):
        forward(50)
        right(144)
    end_fill()




car = path('car.gif')
tiles = list(range(32)) * 2
state = {'mark': None, 'taps': 0}
hide = [True] * 64

def square(x, y):
    """Draw white square with black outline at (x, y)."""
    up()
    goto(x, y)
    down()
    color('black', 'white')
    begin_fill()
    for count in range(4):
        forward(50)
        left(90)
    end_fill()


def index(x, y):
    """Convert (x, y) coordinates to tiles index."""
    return int((x + 200) // 50 + ((y + 200) // 50) * 8)


def xy(count):
    """Convert tiles count to (x, y) coordinates."""
    return (count % 8) * 50 - 200, (count // 8) * 50 - 200


def tap(x, y):
    """Update mark and hidden tiles based on tap."""
    spot = index(x, y)
    mark = state['mark']
    state['taps'] += 1

    if mark is None or mark == spot or tiles[mark] != tiles[spot]:
        state['mark'] = spot
    else:
        hide[spot] = False
        hide[mark] = False
        state['mark'] = None


def draw():
    """Draw image and tiles."""
    clear()
    goto(0, 0)
    shape(car)
    stamp()

    for count in range(64):
        if hide[count]:
            x, y = xy(count)
            square(x, y)

    mark = state['mark']

    if mark is not None and hide[mark]:
        x, y = xy(mark)
        up()
        goto(x + 2, y)

        #dibuja las formas en ls tile
        forma_nombre, forma_color = tiles[mark]
        if forma_nombre == 'heart':
            draw_heart(x, y, forma_color)
        elif forma_nombre == 'thunder':
            draw_thunder(x, y, forma_color)
        elif forma_nombre == 'omega':
            draw_omega(x, y, forma_color)
        elif forma_nombre == 'star':
            draw_star(x, y, forma_color)

    up()
    goto(-200, 200)






    #TAPS HECHOS
    up()
    goto(0,200)
    color('blue')
    write(f"Taps: {state['taps']}", font=('comic sans',20,'normal'))

    update()
    ontimer(draw, 100)

   #IF ALL TILES ARE CONNECTED, DISPLAY WINNING  MESSAGE
   #The if checks if all values in hide (which are the tiles that hide the image) are false, if they are it means the person finished

 #   if all(not h for h in hide):
 #       up()
 #       goto(0,0)
 #       color('Blue')
 #       write(f"You won!! You did it in {state['taps']} taps", align='center',font('Arial', 40, 'bold'))

#   update()
#    ontimer(draw, 100)


shuffle(tiles)
setup(420, 420, 370, 0)
addshape(car)
hideturtle()
tracer(False)
onscreenclick(tap)
draw()
done()
