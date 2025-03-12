import turtle
import time
import random

delay = 0.1

speed_snake = 0

#Pontuação
score = 0
high_score = 0

#Criando Tela
wn = turtle.Screen()
wn.title("Mr.Baem")
wn.bgcolor("#1e1e1e")
wn.setup(width = 600, height = 600)
wn.tracer(0) #Desliga a atualização de tela

#Cabeça da cobra
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("#a3e635")
head.penup()
head.goto(0, 0) #goto() seta as coordenadas do ponto
head.direction = "Stop"

#Comida da Cobra
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("#ef4444")
food.penup()
food.goto(0, 100)

#Comida Venenosa
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

#Funções
def efeito_comer():
    head.color("#fbbf24")  # Muda para amarelo rapidamente
    wn.update()
    time.sleep(0.02)
    head.color("#a3e635")  # Volta para verde

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
        y = head.ycor()
        head.sety(y + 20)
    
    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)
    
    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)
    
    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

#Bindando as teclas
wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")

#Loop do jogo
while True:
    wn.update()

    #Checa de a cobra bateu na borda
    if (
        head.xcor() > 290
        or head.xcor() < -290
        or head.ycor() > 290
        or head.ycor() < -290
    ):
        for _ in range(3):
            pen.clear()
            pen.write("Game Over!", align="center", font=("Courier", 30, "bold"))
            time.sleep(0.5)
            pen.clear()
            time.sleep(0.5)

        #Esconde o corpo da cobra
        for segment in segments:
            segment.goto(1000, 1000)
        
        #Limpa o corpo da cobra
        segments.clear()

        #Reinicia o score
        score = 0

        #Reinicia o delay
        delay = 0.1

        pen.clear()
        pen.write("Pontos: {}  Recorde Pontos: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

    #Checa se a cobra pegou a comida
    if head.distance(food) < 20:
        #Muda a comida de lugar para um aleatório
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x, y)
        efeito_comer()

        #Adiciona um pedaço para a cobra
        cores = ["#65a30d", "#a3e635"]  # Alterna entre verde escuro e verde claro
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color(cores[len(segments) % 2])  # Alterna entre verde escuro e verde claro
        new_segment.penup()
        segments.append(new_segment)

        #Diminui o delay
        delay *= 0.9

        if delay < 0.02:  # Limite mínimo para a velocidade
            delay = 0.02

        #Aumenta os pontos
        score += 10

        #Aumenta a velocidade
        speed_snake += 1000
        head.speed(speed_snake)

        if score > high_score:
            high_score = score

        pen.clear()
        pen.write("Pontos: {}  Recorde Pontos: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

        
    #Checa se a cobra pegou a comida venenosa
    if head.distance(poison) < 20:
        #Muda a comida de lugar para um aleatório
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        poison.goto(x, y)

        #Remove um pedaço do corpo ao comer uma comida venenosa
        if len(segments) > 0:
            segments[-1].goto(1000, 1000)  # Manda para longe para "sumir"
            segments.pop() 
        
        # Checa se a cobra está só com a cabeça (sem pedaços)
        if len(segments) == 0:
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "Stop"
        
        score -= 10
        if score < 0:
            score = 0

        pen.clear()
        pen.write("Pontos: {}  Recorde Pontos: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

    #Inverte o corpo da cobra
    for index in range(len(segments) -1, 0, -1):
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)

    #Move o primeiro pedaço do corpo para onde a cabeça tá
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    move()
    #Checa a colisão da cabeça da cobra com o próprio corpo
    for segment in segments:
        if segment.distance(head) < 20:
            for _ in range(3):
                pen.clear()
                pen.write("Game Over!", align="center", font=("Courier", 30, "bold"))
                time.sleep(0.5)
                pen.clear()
                time.sleep(0.5)

            #Esconde o corpo
            for segment in segments:
                segment.goto(1000, 1000)

            #Limpa o corpo
            segments.clear()

            #Reinicia o score
            score = 0

            #Rseeta o delay
            delay = 0.1

            pen.clear()
            pen.write("Pontos: {}  Recorde Pontos: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))
    time.sleep(delay)
