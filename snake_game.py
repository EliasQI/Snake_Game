import turtle
import time
import random

delay = 0.1
speed_snake = 0

# Pontuação
score = 0
high_score = 0

# Criando Tela
wn = turtle.Screen()
wn.title("Mr.Baem")
wn.bgcolor("#1e1e1e")
wn.setup(width=600, height=600)
wn.tracer(0)  # Desliga a atualização de tela

# Cabeça da cobra
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("#a3e635")
head.penup()
head.goto(0, 0)
head.direction = "Stop"

# Comida da Cobra
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("#ef4444")
food.penup()
food.goto(0, 100)

# Comida Venenosa
poison = turtle.Turtle()
poison.speed(0)
poison.shape("circle")
poison.color("#10b981")
poison.penup()
poison.goto(0, -100)

segments = []

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Pontos: 0  Recorde Pontos: 0", align="center", font=("Courier", 24, "normal"))

# Funções de movimento
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    
    if head.direction == "down":
        head.sety(head.ycor() - 20)
    
    if head.direction == "left":
        head.setx(head.xcor() - 20)
    
    if head.direction == "right":
        head.setx(head.xcor() + 20)

# Bindando as teclas
wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")

# Função do Menu
def menu():
    pen.clear()
    pen.goto(0, 50)
    pen.write("Bem-vindo ao Mr.Baem!", align="center", font=("Courier", 30, "bold"))
    pen.goto(0, 0)
    pen.write("Use as setas para mover a cobra", align="center", font=("Courier", 20, "normal"))
    pen.goto(0, -30)
    pen.write("Coma a comida vermelha para crescer", align="center", font=("Courier", 20, "normal"))
    pen.goto(0, -60)
    pen.write("Evite a comida verde ou você perde partes!", align="center", font=("Courier", 18, "normal"))
    pen.goto(0, -120)
    pen.write("Pressione ESPAÇO para começar", align="center", font=("Courier", 24, "bold"))
    
    wn.onkeypress(start_game, "space")

# Função para iniciar o jogo
def start_game():
    global score, delay

    # Reseta posição e direção da cobra
    head.goto(0, 0)
    head.direction = "Stop"

    # Reseta comidas
    food.goto(0, 100)
    poison.goto(0, -100)

    # Remove segmentos do corpo da cobra
    for segment in segments:
        segment.goto(1000, 1000)
    segments.clear()

    # Reseta pontuação
    score = 0
    delay = 0.1

    pen.clear()
    pen.goto(0, 260)
    pen.write(f"Pontos: {score}  Recorde Pontos: {high_score}", align="center", font=("Courier", 24, "normal"))

    # Inicia o loop do jogo
    game_loop()

# Loop do jogo
def game_loop():
    global score, high_score, delay

    wn.update()

    # Checa se a cobra bateu na borda
    if (
        head.xcor() > 290
        or head.xcor() < -290
        or head.ycor() > 290
        or head.ycor() < -290
    ):
        game_over()
        return  

    # Checa se a cobra pegou a comida
    if head.distance(food) < 20:
        food.goto(random.randint(-290, 290), random.randint(-290, 290))

        # Adiciona um pedaço para a cobra
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("#65a30d")
        new_segment.penup()
        segments.append(new_segment)

        delay *= 0.9
        delay = max(delay, 0.02)  # Impede que fique rápido demais

        score += 10
        if score > high_score:
            high_score = score

        pen.clear()
        pen.write(f"Pontos: {score}  Recorde Pontos: {high_score}", align="center", font=("Courier", 24, "normal"))

    # Checa se a cobra pegou a comida venenosa
    if head.distance(poison) < 20:
        poison.goto(random.randint(-290, 290), random.randint(-290, 290))

        if segments:
            segments[-1].goto(1000, 1000)
            segments.pop()

        if not segments:
            game_over()
            return

        score = max(0, score - 10)

        pen.clear()
        pen.write(f"Pontos: {score}  Recorde Pontos: {high_score}", align="center", font=("Courier", 24, "normal"))

    # Move o corpo da cobra
    for i in range(len(segments) - 1, 0, -1):
        segments[i].goto(segments[i - 1].xcor(), segments[i - 1].ycor())

    if segments:
        segments[0].goto(head.xcor(), head.ycor())

    move()

    # Checa colisão da cobra consigo mesma
    for segment in segments:
        if segment.distance(head) < 20:
            game_over()
            return

    wn.ontimer(game_loop, int(delay * 1000))

# Função para resetar o jogo ao morrer
def game_over():
    global score, delay
    time.sleep(1)
    menu()

# Chama a tela de menu
menu()
wn.mainloop()
