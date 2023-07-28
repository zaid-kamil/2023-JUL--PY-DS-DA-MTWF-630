from turtle import *
pensize(3)
speed('fastest')
bgcolor('black')
pencolor('yellow')
for i in range(6):
    lt(60)
    fd(100)
    for i in range(4):
        lt(90)
        fd(50)
        circle(100, 270)
        for i in range(6):
            lt(60)
            fd(25)

hideturtle()
mainloop()