import os
import random
import turtle

window = turtle.Screen()
window.setup(1200 + 3, 800 + 3)

BASE_X, BASE_Y = 0, - 320
ENEMY_COUNT = 10

new_image = []
images ={
"pic_path": os.path.abspath("images/pig1.gif"),
"pic_path_bird": os.path.abspath("images/bird.gif"),
"pic_path_acorn": os.path.abspath("images/acorn.gif"),
"pic_path_splash": os.path.abspath("images/splash.gif"),
"ingurepic_path": os.path.abspath("images/ingurepig.gif"),
"apple_path": os.path.abspath("images/apple.gif"),
"cat_path": os.path.abspath("images/cat.gif"),
"dog_path": os.path.abspath("images/dog.gif"),
"dead_cat": os.path.abspath("images/sadcat.gif"),
"dead_dog": os.path.abspath("images/saddog.gif"),
}

for name, location in images.items():
    new_image.append(location)

for image in new_image:
    window.register_shape(image)


animals_info = {
"pig": [BASE_X, BASE_Y, images["pic_path"], images["ingurepic_path"], 2000],
"cat": [BASE_X + 300, BASE_Y, images["cat_path"], images["dead_cat"], 1000],
"dog": [BASE_X - 300, BASE_Y, images["dog_path"], images["dead_dog"], 500],
}



class Animals:
    def __init__(self, x, y, shape, shape_splash, base_health):
        self.x = x
        self.y = y
        self.shape = shape
        self.shape_splash = shape_splash

        base = turtle.Turtle()
        base.hideturtle()
        base.speed(0)
        base.penup()
        base.setpos(x=x, y=y)
        base.shape(shape)
        base.showturtle()
        self.base = base

        self.base_health = base_health
        self.base_bonus = 0

        title = turtle.Turtle(visible=False)
        title.speed(0)
        title.penup()
        title.setpos(x=self.x, y=self.y - 75)
        title.color('black')
        title.write(str(self.base_health), align="center", font=["Arial", 20, "bold"])
        self.title = title
        self.title_health = self.base_health

        title_bonus = turtle.Turtle(visible=False)
        title_bonus.speed(0)
        title_bonus.penup()
        title_bonus.setpos(x=BASE_X + 500, y=BASE_Y + 200)
        title_bonus.color('black')
        title_bonus.write(str(self.base_bonus), align="center", font=["Arial", 20, "bold"])
        self.title_bonus = title_bonus
        self.title_bonus_1 = self.base_bonus

    def draw(self):
        if self.base_bonus != self.title_bonus_1:
            self.title_bonus_1 = self.base_bonus
            self.title_bonus.clear()
            self.title_bonus.write(str(self.title_bonus_1), align="center", font=["Arial", 20, "bold"])

        if self.base_health != self.title_health:
            self.title_health = self.base_health
            self.title.clear()
            self.title.write(str(self.title_health), align="center", font=["Arial", 20, "bold"])

    def animal_health_lowering(self):
        if self.base_health <= 0:
            self.base_health = 0
        else:
            self.base_health -= 100

    def animal_bonus_increasing(self):
        self.base_bonus += 100

    def change_pic(self):
        self.base.shape(self.shape_splash)


class Missile:
    def __init__(self, x, y, shape, x2, y2, shape_splash):
        self.shape = shape
        self.shape_splash = shape_splash

        pen = turtle.Turtle(visible=False)
        pen.shape(shape)
        pen.speed(10)
        pen.penup()
        pen.setpos(x=x, y=y)
        heading = pen.towards(x=x2, y=y2)
        pen.setheading(heading)
        pen.showturtle()
        self.pen = pen

        self.target = x2, y2
        self.state = "launched"

    def step(self):
        if self.state == "launched":
            self.pen.forward(4)
            if self.pen.distance(x=self.target[0], y=self.target[1]) < 20:
                self.state = "explode"
                self.pen.shape(self.shape_splash)
        elif self.state == "explode":
            self.pen.clear()
            self.pen.hideturtle()
            self.state = "dead"
        elif self.state == "dead":
            self.pen.clear()
            self.pen.hideturtle()

    def distance(self, x, y):
        return self.pen.distance(x=x, y=y)

    def clear(self):
        self.pen.clear()
        self.pen.hideturtle()

    @property
    def x(self):
        return self.pen.xcor()

    @property
    def y(self):
        return self.pen.ycor()

def firemissile(x, y):
    info = Missile(x=BASE_X, y=BASE_Y, shape = images["pic_path_acorn"], x2=x, y2=y, shape_splash = images["pic_path_splash"])
    our_missiles.append(info)

def enemy_firemissile():
    enemy_base_x = random.randint(-600, 600)
    enemy_base_y = random.randint(400, 800)
    aim_x = random.randint(-400, 400)
    info = Missile(x=enemy_base_x, y=enemy_base_y, shape = images["pic_path_bird"], x2=aim_x, y2=BASE_Y, shape_splash = images["pic_path_splash"])
    enemy_missiles.append(info)

def apples_fall():
    apple_base_x = random.randint(-600, 600)
    apple_base_y = random.randint(400, 800)
    aim_x = random.randint(-400, 400)
    info = Missile(x=apple_base_x, y=apple_base_y, shape = images["apple_path"], x2=aim_x, y2=BASE_Y, shape_splash = None)
    apples.append(info)

def move_missiles(missiles):
    for missile in missiles:
        missile.step()

        dead_missiles = [missile for missile in missiles if missile.state == "dead"]
        for dead in dead_missiles:
            missiles.remove(dead)

def check_enemy_count():
    if len(enemy_missiles) < ENEMY_COUNT:
        enemy_firemissile()
        apples_fall()

def check_interceptions():
    for our_missile in our_missiles:
        if our_missile.state != "explode":
            continue
        for enemy_missile in enemy_missiles:
            if enemy_missile.distance(x=our_missile.x, y=our_missile.y) < 50:
                enemy_missile.state = "dead"
                enemy_missile.clear()
        for apple_missile in apples:
            if apple_missile.distance(x=our_missile.x, y=our_missile.y) < 50:
                apple_missile.state = "dead"
                apple_missile.clear()


def game_over():
    return pig.base_health <= 0

def check_impakt():
    for enemy_missile in enemy_missiles:
        if enemy_missile.state != "explode":
            continue
        for animal in animals:
            if enemy_missile.distance(animal.x, animal.y) < 100:
                animal.animal_health_lowering()
                enemy_missile.state = "dead"
                enemy_missile.clear()
        print("base_health", pig.base_health, "cat_base_health", cat.base_health, "dog_base_health", dog.base_health)

    for apple_missile in apples:
        if apple_missile.state != "explode":
            continue
        if apple_missile.distance(BASE_X, BASE_Y) < 50:
            pig.animal_bonus_increasing()
            apple_missile.state = "dead"
            apple_missile.clear()
            print("bonus:", pig.base_bonus)

def draw_animals():
    for animal in animals:
        animal.draw()

def check_health():
    for animal in animals:
        if animal.base_health <= 0:
            animal.change_pic()


def game():
    window.clear()
    global enemy_missiles, our_missiles, apples, animals, pig, cat, dog
    window.bgpic(os.path.abspath("images/background.png"))
    window.tracer(n=2)
    window.onclick(firemissile)

    our_missiles = []
    enemy_missiles = []
    apples = []
    animals = []

    for animal, animal_info in animals_info.items():
        animal = Animals(x=animal_info[0], y=animal_info[1], shape=animal_info[2], shape_splash=animal_info[3],
                         base_health=animal_info[4])
        animals.append(animal)

    pig = animals[0]
    cat = animals[1]
    dog = animals[2]


    while True:
        window.update()
        if game_over():
            break
        else:
            draw_animals()
            check_impakt()
            check_enemy_count()
            check_interceptions()
            check_health()
            move_missiles(missiles=our_missiles)
            move_missiles(missiles=enemy_missiles)
            move_missiles(missiles=apples)

    pen = turtle.Turtle(visible=False)
    pen.speed(0)
    pen.penup()
    pen.color("red")
    pen.write("Game over", align="center", font=["Arial", 80, "bold"])

while True:
    game()
    answer = window.textinput(title="Привет!", prompt="Хотите сыграть еще?")
    if answer.lower() not in ('д', 'да', 'y', 'yes'):
        break
