import turtle
import time
import math
import random

# Function to create custom shapes
def create_shapes():
    # Player spaceship shape
    player_shape = (
        (-20, 0), (10, 10), (5, 5), (10, 5),
        (10, -5), (5, -5), (10, -10)
    )
    turtle.register_shape("player_spaceship", player_shape)


   # Alien spaceship shape
    alien_shape = (
       (-10, 15), (-15, 10), (-10, 5), (-15, 0),
       (-10, -5), (-15, -10), (-10, -15), (10, 0)
    )
    turtle.register_shape("alien_spaceship", alien_shape)


   # Boss spaceship shape
    boss_shape = (
       (-30, 0), (-20, 20), (-10, 0), (-20, -20),
       (20, -20), (10, 0), (20, 20), (30, 0)
    )
    turtle.register_shape("boss_spaceship", boss_shape)




# Create custom shapes
create_shapes()

class GameObject:
    def __init__(self, shape, color, x, y):
        self.turtle = turtle.Turtle()
        self.turtle.shape(shape)
        self.turtle.color(color)
        self.turtle.penup()
        self.turtle.goto(x, y)
        self.alive = True


    def move(self, dx, dy):
        if self.alive:
            self.turtle.setx(self.turtle.xcor() + dx)
            self.turtle.sety(self.turtle.ycor() + dy)
    
    def destroy(self):
        self.alive = False
        self.turtle.hideturtle()
        self.turtle.clear()


class PlayerSpaceship(GameObject):
    def __init__(self, x, y):
        super().__init__('player_spaceship', 'blue', x, y)

    def move_left(self):
        if self.turtle.xcor() > -380:
            self.move(-15, 0)

    def move_right(self):
        if self.turtle.xcor() < 380:
            self.move(15, 0)


class AlienSpaceship(GameObject):
    def __init__(self, x, y):
        super().__init__('alien_spaceship', 'purple', x, y)

    def move_down(self):
        self.move(0, -20)

class BossAlien(GameObject):
    def __init__(self, x, y):
        super().__init__('boss_spaceship', 'red', x, y)
        self.health = 10  # Boss has more health
       
class Bullet(GameObject):
    def __init__(self, x, y, color, heading, curve_probability=0.1):
        super().__init__('square', color, x, y)
        self.turtle.shapesize(stretch_wid=0.2, stretch_len=0.8)
        self.turtle.setheading(heading)
        self.speed = 20 if color == 'red' else 5  # Player bullets are faster
        self.curve_probability = curve_probability
        self.curving = False
        self.curve_initiated = False
        self.initial_heading = heading
        self.max_total_turn = 45  # Max total angle bullet can turn


    def move_forward(self, target_x=None, target_y=None):
       # Decide whether to curve only once per bullet
        if not self.curve_initiated and self.curve_probability > 0:
            if random.random() < self.curve_probability:
                self.curving = True
                self.turtle.color('red')  # Change to red when it starts curving
            self.curve_initiated = True


        if self.curving and target_x is not None and target_y is not None:
            dx = target_x - self.turtle.xcor()
            dy = target_y - self.turtle.ycor()
            angle_to_target = math.degrees(math.atan2(dy, dx))


            angle_difference = (angle_to_target - self.initial_heading + 360) % 360
            if angle_difference > 180:
                angle_difference -= 360


            angle_difference = max(-self.max_total_turn, min(self.max_total_turn, angle_difference))
            desired_heading = self.initial_heading + angle_difference


            current_heading = self.turtle.heading()
            angle_diff_current = (desired_heading - current_heading + 360) % 360
            if angle_diff_current > 180:
                angle_diff_current -= 360


            max_turn_angle = 2
            turn_angle = max(-max_turn_angle, min(max_turn_angle, angle_diff_current))
            new_heading = current_heading + turn_angle
            self.turtle.setheading(new_heading)
        self.turtle.forward(self.speed)


class PowerUp(GameObject):
    def __init__(self, x, y, powerup_type):
        color_map = {
            'faster_fire': 'orange',
            'double_bullets': 'cyan',
            'extra_life': 'pink',
            'score_multiplier': 'yellow'
        }
        super().__init__('circle', color_map[powerup_type], x, y)
        self.powerup_type = powerup_type
        self.turtle.shapesize(stretch_wid=1, stretch_len=1)
        self.spawn_time = time.time()




def is_collision(obj1, obj2):
    if obj1.alive and obj2.alive:
        distance = math.hypot(
            obj1.turtle.xcor() - obj2.turtle.xcor(),
            obj1.turtle.ycor() - obj2.turtle.ycor()
        )
        return distance < 20  # Collision threshold
    return False




def fire_bullet():
    global last_bullet_time
    current_time = time.time()
    if current_time - last_bullet_time >= bullet_cooldown:
        if double_bullets:
            bullet1 = Bullet(player.turtle.xcor() - 10, player.turtle.ycor() + 20, 'red', 90)
            bullet2 = Bullet(player.turtle.xcor() + 10, player.turtle.ycor() + 20, 'red', 90)
            player_bullets.extend([bullet1, bullet2])
        else:
            bullet = Bullet(player.turtle.xcor(), player.turtle.ycor() + 20, 'red', 90)
            player_bullets.append(bullet)
        last_bullet_time = current_time

def update_score_display():
    score_display.clear()
    active_powerups = ' | '.join(active_powerup_names())
    score_display.write(
        f"Score: {score}  Lives: {lives}  Wave: {wave_number}\nActive Power-Ups: {active_powerups}",
        align="center",
        font=("Arial", 16, "normal")
    )


def active_powerup_names():
    names = []
    for effect in powerup_end_times.keys():
        if effect == 'faster_fire':
            names.append('Faster Fire')
        elif effect == 'double_bullets':
            names.append('Double Bullets')
        elif effect == 'score_multiplier':
            names.append('Score x2')
    return names

def display_wave_message(wave_number):
    message_turtle = turtle.Turtle()
    message_turtle.hideturtle()
    message_turtle.color("white")
    message_turtle.penup()
    message_turtle.goto(0, 0)
    if wave_number % 3 == 0:
        message_turtle.write(f"Wave {wave_number} - Boss Wave!\nGood luck!", align="center",
                                font=("Arial", 24, "normal"))
    else:
        message_turtle.write(f"Wave {wave_number}\nGood luck!", align="center", font=("Arial", 24, "normal"))
    screen.update()
    time.sleep(2)  # Pause for 2 seconds
    message_turtle.clear()
    message_turtle.hideturtle()


def apply_powerup(powerup_type):
    global bullet_cooldown, double_bullets, lives, powerup_end_times, score_multiplier
    current_time = time.time()
    if powerup_type == 'faster_fire':
        bullet_cooldown = 0.1
        powerup_end_times['faster_fire'] = current_time + powerup_duration
    elif powerup_type == 'double_bullets':
        double_bullets = True
        powerup_end_times['double_bullets'] = current_time + powerup_duration
    elif powerup_type == 'extra_life':
        lives += 1
        update_score_display()


    elif powerup_type == 'score_multiplier':
        score_multiplier = 2
        powerup_end_times['score_multiplier'] = current_time + powerup_duration




def reset_powerups():
    global bullet_cooldown, double_bullets, powerup_end_times, score_multiplier
    bullet_cooldown = 0.3
    double_bullets = False
    score_multiplier = 1
    powerup_end_times.clear()
    update_score_display()


def update_boss_health_bar():
    boss_health_bar.clear()
    if boss_alien and boss_alien.alive:
        boss_health_bar.showturtle()
        boss_health_bar.penup()


        # Position the health bar relative to the boss's current position
        boss_x = boss_alien.turtle.xcor()
        boss_y = boss_alien.turtle.ycor()


        # Adjust the offset as needed (e.g., 40 pixels below the boss)
        x = boss_x - 100  # Starting 100 pixels to the left of the boss
        y = boss_y - 40  # 40 pixels below the boss


        boss_health_bar.goto(x, y)
        boss_health_bar.color("red")
        boss_health_bar.width(3)
        boss_health_bar.setheading(0)
        boss_health_bar.pendown()


        max_health = 10
        health_ratio = boss_alien.health / max_health
        # 200 pixels wide at full health
        boss_health_bar.forward(200 * health_ratio)


        boss_health_bar.penup()
    else:
        # No boss -> clear and hide
        boss_health_bar.clear()
        boss_health_bar.hideturtle()


 

def reset_game():
    global aliens, boss_alien, alien_bullets, player_bullets, power_ups, alien_speed
    global score, lives, alien_direction, last_bullet_time, player, score_display
    global game_start_time, wave_number, last_powerup_time, powerup_spawn_interval
    global bullet_cooldown, double_bullets, powerup_end_times, score_multiplier


    screen.clearscreen()
    screen.bgcolor("black")
    screen.title("Space Invaders")
    screen.tracer(0)


    # Re-register custom shapes after clearing the screen
    create_shapes()


    aliens = []
    boss_alien = None
    alien_bullets.clear()
    player_bullets.clear()
    power_ups.clear()
    alien_speed = 2
    score = 0
    lives = 3
    alien_direction = 2
    last_bullet_time = 0
    wave_number = 1


    bullet_cooldown = 0.3
    double_bullets = False
    powerup_duration = 10
    powerup_end_times = {}
    score_multiplier = 1


    global next_powerup_index
    last_powerup_time = time.time()
    powerup_spawn_interval = random.randint(10, 20)
    next_powerup_index = 0


    player.__init__(0, -250)

    score_display.clear()
    score_display.hideturtle()
    score_display.goto(0, 260)
    update_score_display()


    screen.onkeypress(lambda: keys_pressed.update({"Left": True}), "Left")
    screen.onkeyrelease(lambda: keys_pressed.update({"Left": False}), "Left")
    screen.onkeypress(lambda: keys_pressed.update({"Right": True}), "Right")
    screen.onkeyrelease(lambda: keys_pressed.update({"Right": False}), "Right")
    screen.onkey(fire_bullet, "space")
    screen.onkey(restart_game, "r")
    screen.listen()


    game_start_time = time.time()
    start_new_wave()
    start_game()




def restart_game():
    reset_game()

def start_new_wave():
    global aliens, boss_alien, alien_speed, alien_direction, game_start_time, wave_number


    reset_powerups()
    player.turtle.goto(0, -250)


    for bullet in alien_bullets[:]:
        bullet.destroy()
        alien_bullets.remove(bullet)
    for bullet in player_bullets[:]:
        bullet.destroy()
        player_bullets.remove(bullet)


    aliens.clear()
    boss_alien = None
    alien_speed += 0.5
    alien_direction = alien_speed if alien_direction > 0 else -alien_speed


    display_wave_message(wave_number)


    if wave_number % 3 == 0:
        # Boss wave
        boss_alien = BossAlien(0, 250)
        boss_alien_speed = alien_speed + 0.5
        update_boss_health_bar()  # Draw initial health bar
    else:
        boss_alien_speed = None
        for row in range(5):
            for col in range(10):
                alien = AlienSpaceship(-225 + col * 50, 250 - row * 50)
                aliens.append(alien)


    game_start_time = time.time()
    update_score_display()

def start_game():
    global running, last_alien_fire_time, alien_direction, alien_speed
    global score, lives, wave_number, last_powerup_time, powerup_spawn_interval, score_multiplier
    global boss_alien


    running = True
    last_alien_fire_time = time.time()


    # boss_alien_speed is already set in start_new_wave


    while running:
        screen.update()


        if keys_pressed["Left"]:
            player.move_left()
        if keys_pressed["Right"]:
            player.move_right()


        current_time = time.time()


        # Spawn power-ups randomly
        if current_time - last_powerup_time >= powerup_spawn_interval:
            global next_powerup_index
            powerup_sequence = ['faster_fire', 'double_bullets', 'extra_life', 'score_multiplier']
            powerup_type = powerup_sequence[next_powerup_index % len(powerup_sequence)]
            next_powerup_index += 1
            powerup_x = random.randint(-350, 350)
            powerup = PowerUp(powerup_x, -250, powerup_type)
            power_ups.append(powerup)
            last_powerup_time = current_time
            powerup_spawn_interval = random.randint(10, 20)

        for powerup in power_ups[:]:
            if is_collision(player, powerup):
                apply_powerup(powerup.powerup_type)
                powerup.destroy()
                power_ups.remove(powerup)
                update_score_display()
            elif current_time - powerup.spawn_time >= powerup_duration:
                powerup.destroy()
                power_ups.remove(powerup)


        for effect in list(powerup_end_times.keys()):
            if current_time >= powerup_end_times[effect]:
                if effect == 'faster_fire':
                    bullet_cooldown = 0.3
                elif effect == 'double_bullets':
                    double_bullets = False
                elif effect == 'score_multiplier':
                    score_multiplier = 1
                del powerup_end_times[effect]
                update_score_display()


        # Move player bullets
        for bullet in player_bullets[:]:
            bullet.move_forward()
            if bullet.turtle.ycor() > 300:
                bullet.destroy()
                player_bullets.remove(bullet)
            
            
        # Alien/Boss firing logic
        if current_time - last_alien_fire_time >= alien_fire_cooldown:
            if boss_alien and boss_alien.alive:
                fire_probability = 0.8
                if random.random() < fire_probability:
                    alien_bullet = Bullet(
                        boss_alien.turtle.xcor(),
                        boss_alien.turtle.ycor() - 20,
                        'red',
                        270,
                        curve_probability=1.0
                    )
                    alien_bullets.append(alien_bullet)
                last_alien_fire_time = current_time - (alien_fire_cooldown / 2)
            else:
                fire_probability = 0.1 + (wave_number * 0.01)
                fire_probability = min(fire_probability, 0.5)
                for alien in aliens:
                    if random.random() < fire_probability:
                        alien_bullet = Bullet(alien.turtle.xcor(), alien.turtle.ycor() - 20, 'yellow', 270)
                        alien_bullets.append(alien_bullet)
                last_alien_fire_time = current_time


        # Move alien bullets
        for bullet in alien_bullets[:]:
            if bullet.curve_probability > 0:
                bullet.move_forward(player.turtle.xcor(), player.turtle.ycor())
            else:
                bullet.move_forward()
            if bullet.turtle.ycor() < -300 or bullet.turtle.xcor() < -400 or bullet.turtle.xcor() > 400:
                bullet.destroy()
                alien_bullets.remove(bullet)
            elif is_collision(bullet, player):
                bullet.destroy()
                alien_bullets.remove(bullet)
                lives -= 1
                update_score_display()
                if lives == 0:
                    running = False
                    display_message("GAME OVER\nPress 'R' to Restart")
                    
                    
            # Move aliens or boss
        if boss_alien and boss_alien.alive:
            boss_alien.move(alien_direction * alien_speed, 0)
            if boss_alien.turtle.xcor() > 380 or boss_alien.turtle.xcor() < -380:
                alien_direction *= -1
            update_boss_health_bar()  # Update health bar if boss is alive
        elif aliens:
            leftmost_x = min(alien.turtle.xcor() for alien in aliens)
            rightmost_x = max(alien.turtle.xcor() for alien in aliens)
            if rightmost_x >= 380 or leftmost_x <= -380:
                alien_direction *= -1
                for alien in aliens:
                    alien.move_down()
            for alien in aliens:
                alien.move(alien_direction, 0)
                if alien.turtle.ycor() < -280:
                    alien.turtle.sety(300)



            # Check for collisions between player bullets and aliens/boss
        for bullet in player_bullets[:]:
            if boss_alien and boss_alien.alive and is_collision(bullet, boss_alien):
                bullet.destroy()
                player_bullets.remove(bullet)
                boss_alien.health -= 1
                if boss_alien.health <= 0:
                    boss_alien.destroy()
                    boss_alien = None
                    # Call update to clear the health bar immediately
                    update_boss_health_bar()
                    score += 50 * score_multiplier
                    update_score_display()
                else:
                    update_boss_health_bar()  # Boss hit, update health bar
            else:
                for alien in aliens[:]:
                    if is_collision(bullet, alien):
                        bullet.destroy()
                        alien.destroy()
                        player_bullets.remove(bullet)
                        aliens.remove(alien)
                        score += 1 * score_multiplier
                        update_score_display()
                        break
                        
                        
            # Start new wave if all aliens and boss are destroyed
        if not aliens and (boss_alien is None or not boss_alien.alive):
            wave_number += 1
            update_score_display()
            start_new_wave()


        time.sleep(0.02)




def display_message(message):
    screen.clear()
    screen.bgcolor("black")
    message_text = turtle.Turtle()
    message_text.color("white")
    message_text.hideturtle()
    message_text.penup()
    message_text.goto(0, 0)
    message_text.write(message, align="center", font=("Arial", 24, "normal"))
    screen.onkey(restart_game, "r")
    screen.listen()
    while True:
        screen.update()
        time.sleep(0.1)


# Initialize the screen
screen = turtle.Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("Space Invaders")
screen.tracer(0)


# Initialize game variables
aliens = []
boss_alien = None
alien_bullets = []
player_bullets = []
power_ups = []
alien_speed = 2
alien_fire_cooldown = 1
last_alien_fire_time = time.time()
score = 0
lives = 3
alien_direction = 2
last_bullet_time = 0
game_start_time = time.time()
wave_number = 1


bullet_cooldown = 0.3
double_bullets = False
powerup_duration = 10
powerup_end_times = {}
score_multiplier = 1


last_powerup_time = time.time()
powerup_spawn_interval = random.randint(10, 20)
next_powerup_index = 0


player = PlayerSpaceship(0, -250)
keys_pressed = {"Left": False, "Right": False}


screen.onkeypress(lambda: keys_pressed.update({"Left": True}), "Left")
screen.onkeyrelease(lambda: keys_pressed.update({"Left": False}), "Left")
screen.onkeypress(lambda: keys_pressed.update({"Right": True}), "Right")
screen.onkeyrelease(lambda: keys_pressed.update({"Right": False}), "Right")
screen.onkey(fire_bullet, "space")
screen.onkey(restart_game, "r")
screen.listen()


# Create the boss health bar turtle
boss_health_bar = turtle.Turtle()
boss_health_bar.hideturtle()
boss_health_bar.speed(0)
boss_health_bar.penup()


score_display = turtle.Turtle()
score_display.hideturtle()
score_display.color("white")
score_display.penup()
score_display.goto(0, 260)


reset_game()
turtle.done()
