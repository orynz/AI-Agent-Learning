# turtle_draw.py
import turtle as t

for _ in range(12):
    t.forward(50)
    t.right(30)

t.penup(); t.goto(-300, 0); t.pendown()
t.speed(0)
length = 3
for _ in range(200):
    t.forward(length)
    t.right(89)
    length += 5

t.done()