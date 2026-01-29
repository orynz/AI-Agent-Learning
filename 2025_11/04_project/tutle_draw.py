# turtle_draw.py
import turtle as t

for _ in range(4):
    t.forward(100)
    t.right(90)

t.penup(); t.goto(-150, 0); t.pendown()
t.speed(10)
length = 5
for _ in range(1000):
    t.forward(length)
    t.right(84)
    length += 1

t.done()