
import turtle



statistics = {
    "score": 0,
    "death_right": 3
}

wn = turtle.Screen()
wn.title('Ping & Pong Game')
wn.bgcolor('black')
wn.setup(width=800, height=600)
wn.tracer(0)



# User Score 





def render_comps():
    global paddle_a, paddle_b, ball
    paddle_a = turtle.Turtle()
    paddle_a.speed(0)
    paddle_a.shape('square')
    paddle_a.color('white')
    paddle_a.shapesize(stretch_wid=5, stretch_len=0.125)
    paddle_a.penup()
    paddle_a.goto(-375, 0)

    # Paddle B

    paddle_b = turtle.Turtle()
    paddle_b.speed(0)
    paddle_b.shape('square')
    paddle_b.color('white')
    paddle_b.shapesize(stretch_wid=5, stretch_len=0.125)
    paddle_b.penup()
    paddle_b.goto(375, 0)

    # Ball

    ball = turtle.Turtle()
    ball.speed(0)
    ball.shape('square')
    ball.color('white')
    ball.penup()
    ball.goto(0, 0)
    ball.dx = 0.15
    ball.dy = 0.15

render_comps()

# Back Functions

def paddle_a_up():
    global move
    y = paddle_a.ycor()
    if (y + 20) <= 255 and move == True:
        y += 30 
        paddle_a.sety(y)

def paddle_a_down():
    global move
    y = paddle_a.ycor()
    if (y - 20) > -255 and move == True:
        y -= 30 
        paddle_a.sety(y)

def paddle_b_up():
    global move
    y = paddle_b.ycor()
    if (y + 20) <= 255 and move == True:
        y += 30 
        paddle_b.sety(y)

def paddle_b_down():
    global move
    y = paddle_b.ycor()
    if (y - 20) > -255 and move == True:
        y -= 30 
        paddle_b.sety(y)

def pause_switch():
    global move 
    global paused 
    if move:
        paused = not paused 
            

# Keyboard binding

wn.listen()
wn.onkeypress(paddle_a_up, 'w')
wn.onkeypress(paddle_a_down, 's')
wn.onkeypress(paddle_b_up, 'Up')
wn.onkeypress(paddle_b_down, 'Down')
wn.onkeypress(pause_switch, 'Escape')
# Main loop

isChanged = True
move = True
paused = False

while True:
    try:
        wn.update()
        if move == True and paused == False:
            ball.setx(ball.xcor() + ball.dx)
            ball.sety(ball.ycor() + ball.dy)

        if ball.ycor() > 290:
            ball.sety(290)
            ball.dy *= -1
        if ball.ycor() < -290:
            ball.sety(-290)
            ball.dy *= -1
        
        if ball.xcor() > 390:
            ball.goto(0, 0)
            ball.dx *= -1
            statistics['death_right'] -= 1
            isChanged = True 
        
        if ball.xcor() < -390:
            ball.goto(0, 0)
            ball.dx *= -1
            statistics['death_right'] -= 1
            isChanged = True 
        
        if ball.xcor() > 340 and ball.xcor() < 350 and (ball.ycor() < paddle_b.ycor() + 40 and ball.ycor() > paddle_b.ycor() - 40):
            ball.setx(340)
            statistics['score'] += 1
            ball.dx *= -1 
            isChanged = True 
        if ball.xcor() < -340 and ball.xcor() > -350 and (ball.ycor() < paddle_a.ycor() + 40 and ball.ycor() > paddle_a.ycor() - 40):
            ball.setx(-340)
            ball.dx *= -1
            statistics['score'] += 1
            isChanged = True
        if isChanged == True:
            turtle.reset()
            score = statistics['score']
            death_right = statistics['death_right']
            if death_right >= 1:
                turtle.setposition(0, 265)
                turtle.color('whitesmoke')
                style = ('Courier', 18, 'normal')
                turtled = turtle.write(f'Score : {score} ({death_right} chances left)', font=style, align='center')
                turtle.hideturtle()
            else:
                move = False
                turtle.setposition(0, 0)
                turtle.color('red')
                style = ('Courier', 25, 'normal')
                turtled = turtle.write(f'Game Over!', font=style, align='center')
                ball.reset()
                paddle_a.reset()
                paddle_b.reset()

                turtle.hideturtle()


            isChanged = False
    except: pass