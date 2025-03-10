from tkinter import *
import random

GAME_WIDTH = 620
GAME_HEIGHT = 620
SPEED = 120  # Start with a slower speed
SPACE_SIZE = 25
BODY_PARTS = 3
SNAKE_COLOR = "cyan"
FOOD_COLOR = "#F28500"
BACKGROUND_COLOR = "black"
POWER_UP_DURATION = 5000  # 5 seconds in milliseconds

# Global variables
score = 0
high_score = 0
direction = "down"
snake = None
food = None
power_up = None
paused = False

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self):
        self.spawn_food()

    def spawn_food(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


class PowerUp:
    def __init__(self):
        self.active = False
        self.timer = None

    def spawn(self):
        if not self.active:
            self.x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
            self.y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
            self.shape = canvas.create_rectangle(self.x, self.y, self.x + SPACE_SIZE, self.y + SPACE_SIZE, fill="red", tag="powerup")
            self.active = True
            self.timer = window.after(POWER_UP_DURATION, self.remove)

    def remove(self):
        if self.active:
            canvas.delete(self.shape)
            self.active = False

def toggle_pause():
    global paused
    paused = not paused  # Toggle between paused and unpaused states

    if paused:
        pause_button.config(text="Resume")  # Change button text to "Resume"
    else:
        pause_button.config(text="Pause")  # Change button text to "Pause"
        next_turn()  # Resume the game loop

def next_turn():
    global score, high_score, SPEED, paused
    if paused:
        return
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        label.config(text=f"Score: {score}  High Score: {high_score}")
        canvas.delete("food")
        food.spawn_food()

        if score > high_score:
            high_score = score
            label.config(text=f"Score: {score}  High Score: {high_score}")

        SPEED = max(30, SPEED - 2)

        if score >= 10 and score % 5 == 0:
            power_up.spawn()

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if power_up.active and x == power_up.x and y == power_up.y:
        power_up.remove()
        SPEED += 20

        display_power_up_message("Snake Speed Decreased!")

    if check_collisions():
        game_over()
    else:
        window.after(SPEED, next_turn)


def change_direction(new_direction):
    global direction

    if new_direction == "left" and direction != "right":
        direction = new_direction
    elif new_direction == "right" and direction != "left":
        direction = new_direction
    elif new_direction == "up" and direction != "down":
        direction = new_direction
    elif new_direction == "down" and direction != "up":
        direction = new_direction


def check_collisions():
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def display_power_up_message(message):
    """ Display a message on the canvas for 2 seconds. """
    message_id = canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 - 20, fill="yellow", font=("consolas", 20), text=message, tag="powerup_message")
    window.after(2000, lambda: canvas.delete(message_id))


def game_over():
    canvas.delete(ALL)
    # Game over text
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 - 30, text="GAME OVER", font=("consolas", 70), fill="red",
                       tag="gameover")

    # Retry button moved further down
    retry_button.place(x=(GAME_WIDTH // 2) - 100, y=(GAME_HEIGHT // 2) + 70, width=200, height=50)

    # Exit button adjusted accordingly
    exit_button.place(x=(GAME_WIDTH // 2) - 100, y=(GAME_HEIGHT // 2) + 140, width=200, height=50)

    #hide pause button
    pause_button.place_forget()


def game_over():
    canvas.delete(ALL)
    # Game over text
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 - 30, text="GAME OVER", font=("consolas", 70), fill="red",tag="gameover")
    # Retry button moved further down
    retry_button.place(x=(GAME_WIDTH // 2) - 100, y=(GAME_HEIGHT // 2) + 70, width=200, height=50)
    # Exit button adjusted accordingly
    exit_button.place(x=(GAME_WIDTH // 2) - 100, y=(GAME_HEIGHT // 2) + 140, width=200, height=50)
    #hide pause button
    pause_button.place_forget()

def start_game():
    global snake, food, score, direction, power_up, SPEED, paused
    pause_button.place(x=(GAME_WIDTH - 110), y=1, width=95, height=40)

    SPEED = 120
    score = 0
    direction = "down"
    paused = False
    label.config(text=f"Score: {score}  High Score: {high_score}")

    canvas.delete(ALL)
    snake = Snake()
    food = Food()
    power_up = PowerUp()

    # Hide all buttons related to the menu or game over
    play_button.place_forget()
    retry_button.place_forget()
    exit_button.place_forget()

    next_turn()

def show_main_menu():
    canvas.delete(ALL)
    # Add "Snake Game" title
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 - 100, text="SNAKE GAME", font=("consolas", 70), fill="cyan",tag="title")
    # Play button
    play_button.place(x=(GAME_WIDTH // 2) - 100, y=(GAME_HEIGHT // 2) + 20, width=200, height=50)
    #Exit button
    exit_button.place(x=(GAME_WIDTH // 2) - 100, y=(GAME_HEIGHT // 2) + 90, width=200, height=50)
    # Hide retry button in the main menu
    retry_button.place_forget()
    pause_button.place_forget()


def exit_game():
    window.destroy()

window = Tk()
window.title("Snake Game")
window.resizable(False, False)

label = Label(window, text=f"Score: {score}  High Score: {high_score}", font=("consolas", 20))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()


play_button = Button(window, text="Play", command=start_game, font=("consolas", 20))
exit_button = Button(window, text="Exit", command=exit_game, font=("consolas", 20))
retry_button = Button(window, text="Retry", command=start_game, font=("consolas", 20))
pause_button = Button(window, text="Pause", command=toggle_pause, font=("consolas", 20), bg="lightgray")

window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

show_main_menu()

window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))
window.bind("<w>", lambda event: change_direction("up"))
window.bind("<s>", lambda event: change_direction("down"))
window.bind("<a>", lambda event: change_direction("left"))
window.bind("<d>", lambda event: change_direction("right"))

window.mainloop()
