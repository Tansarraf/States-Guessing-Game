import turtle
import pandas as pd
import time
import random 

# Creating the screen
screen = turtle.Screen()
screen.title("Indian States Game")
screen.setup(width=630,height=685)
screen.tracer(0)

# Loading the image
image = "map.gif" 
screen.addshape(image)
turtle.shape(image)

# Scoreboard
score = turtle.Turtle()
score.hideturtle()
score.penup()
score.goto(50,150)

# Timer
timer = turtle.Turtle()
timer.hideturtle()
timer.penup()
timer.goto(50,175)

# Reading the file
data = pd.read_csv("indian_states.csv")
all_states = data.state.to_list()

guessed_states = []
colors = ["red","green","blue","purple","brown","black"]

def difficulty():
    level = screen.textinput("Choose Your Difficulty" , "Easy / Medium / Hard").lower()
    if level == "easy":
        return 420  # 7 minutes
    elif level == "medium":
        return 300  # 5 minutes
    elif level == "hard":
        return 180  # 3 minutes
    else:
        return difficulty() 

time_left = difficulty()

def update_score():
    score.clear()
    score.write(f"Score: {len(guessed_states)}/29", font=("Times New Roman", 16, "bold"))
    screen.update()

def update_timer():
    global time_left
    timer.clear()
    if time_left > 0:
        timer.write(f"Time: {time_left}s", font=("Times New Roman", 16, "bold"))
        time_left -= 1
        screen.update()
        screen.ontimer(update_timer, 1000)
    else:
        timer.write("Time Over", font=("Times New Roman", 16, "bold"))
        end_game()

def states(state_name):
  t=turtle.Turtle()
  t.hideturtle()
  t.penup()
  t.color(random.choice(colors))
  state_data = data[data.state==state_name]
  t.goto(state_data.x.item(),state_data.y.item())
  t.write(state_name,align="left",font=("Times New Roman",12,"bold"))
  screen.update()

def start_game():
    update_score()
    update_timer()

    while len(guessed_states) < 29 and time_left > 0:
      answer_state = screen.textinput(title=f"{len(guessed_states)}/29 States correct",prompt="Make a guess?").title()

      if answer_state == "Exit":
        end_game()
        break

      if answer_state in all_states and answer_state not in guessed_states:
        guessed_states.append(answer_state)
        states(answer_state)
        update_score()

      if len(guessed_states) == 29:
        victory()
        return

def end_game():
    missing_states = [state for state in all_states if state not in guessed_states]
    pd.DataFrame(missing_states).to_csv("states_not_guessed.csv")
    
    end_msg = turtle.Turtle()
    end_msg.hideturtle()
    end_msg.penup()
    end_msg.goto(102.5, 200)
    end_msg.write("Game Over!", align="center", font=("Times New Roman", 16, "bold"))
    screen.update()
    time.sleep(5)
    screen.bye()

def victory():
    celebrate = turtle.Turtle()
    celebrate.hideturtle()
    celebrate.penup()
    celebrate.goto(120, 200)
    celebrate.write("Congratulations!\n You've guessed all states correctly 🎉", align="center", font=("Times New Roman", 14, "bold"))
    screen.update()
    time.sleep(5)
    screen.bye()

start_game()
screen.mainloop()