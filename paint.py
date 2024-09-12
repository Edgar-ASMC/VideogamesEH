#mi vercion E
from turtle import *
from freegames import vector


def line(start, end):
    """Draw line from start to end."""
    up()
    goto(start.x, start.y)
    down()
    goto(end.x, end.y)


def square(start, end):
    """Draw square from start to end."""
    up()
    goto(start.x, start.y)
    down()
    begin_fill()

    for count in range(4):
        forward(end.x - start.x)
        left(90)

    end_fill()


def circleDraw(start, end):
    """Draw circle from start to end."""
    penup()
    goto(start.x, start.y)
    goto(end.x, end.y)
    begin_fill()

    pendown()
    xbase= (end.x-start.x)
    ybase= (end.y-start.y)
    r=(xbase + ybase)**1/2
    circle(r)
    end_fill()

def rectangle(start, end):
    #empieza a dibujar con el lapiz
    up()
    goto(start.x, start.y)
    down()
    begin_fill()

    for count in range(2):
	#dibuja la primera linea (chiquita)
       forward(end.x - start.x)
       left(90)
       #dibuja la segunda linea (la grande)
       forward((end.x - start.x)+35)
       left(90)

    end_fill()




def triangle(start, end):
    """Draw triangle from start to end."""
    up()
    goto(start.x, start.y)
    down()
    begin_fill()

    for count in range(2):
	#dibuja la liena y se mueve 60 grados
        forward(end.x - start.x)
        left(120)

    end_fill()



def tap(x, y):
    """Store start g point or draw shape."""
    start = state['start']

    if start is None:
        state['start'] = vector(x, y)
    else:
        shape = state['shape']
        end = vector(x, y)
        shape(start, end)
        state['start'] = None


def store(key, value):
    """Store value in state at key."""
    state[key] = value


state = {'start': None, 'shape': line}
setup(420, 420, 370, 0)
onscreenclick(tap)
listen()

#COLORS
onkey(undo, 'u')
onkey(lambda: color('black'), 'K')
onkey(lambda: color('white'), 'W')
onkey(lambda: color('green'), 'G')
onkey(lambda: color('blue'), 'B')
onkey(lambda: color('red'), 'R')
onkey(lambda: color ('pink'), 'P')
onkey(lambda: color('yellow'), 'Y')

#SHAPES
onkey(lambda: store('shape', line), 'l')
onkey(lambda: store('shape', square), 's')
onkey(lambda: store('shape', circleDraw), 'c')
onkey(lambda: store('shape', rectangle), 'r')
onkey(lambda: store('shape', triangle), 't')
done()

#DEF
#ONKEY- Activa algo si se presiona una tecla especifica
#goto- va de un punto a otro
