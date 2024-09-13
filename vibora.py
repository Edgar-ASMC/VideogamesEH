from random import randrange
from random import choice
from random import randint
from turtle import *

from freegames import square, vector

food = vector(0, 0)
snake = [vector(10, 0)]
aim = vector(0, -10)
M = 0

#Randomize colors for snake and fruit using choice()
colors = ['cornflower blue','deep pink','gold','orange','orchid','medium spring green',"medium slate blue"]
snakeColor = choice(colors)
colors.remove(snakeColor)
fruitColor = choice(colors)

def change(x, y):
    """Change snake direction."""
    aim.x = x
    aim.y = y

def inside(head):
    """Return True if head inside boundaries."""
    return -200 < head.x < 190 and -200 < head.y < 190

def move():
    """Move snake forward one segment."""
    head = snake[-1].copy()
    head.move(aim)

    if not inside(head) or head in snake:
        square(head.x, head.y, 9, 'red')
        update()
        return

    snake.append(head)

    food.x = food.x + randint(-1,1)
    food.y = food.y + randint(-1,1)


    if (abs(head.x - food.x) < 7) and (abs(head.y - food.y) < 7):
        print('Snake:', len(snake))
        food.x = randrange(-15, 15) * 10
        food.y = randrange(-15, 15) * 10
        # aumento la variable
        global M
        M = M+1
    else:
        snake.pop(0)

    clear()


    for body in snake:
        square(body.x, body.y, 9, snakeColor)

    square(food.x, food.y, 9, fruitColor)
    update()
    #aumenta el movimiento
    ontimer(move, 100-M)

setup(420, 420, 370, 0)
hideturtle()
tracer(False)
listen()
onkey(lambda: change(10, 0), 'Right')
onkey(lambda: change(-10, 0), 'Left')
onkey(lambda: change(0, 10), 'Up')
onkey(lambda: change(0, -10), 'Down')
move()
done()

