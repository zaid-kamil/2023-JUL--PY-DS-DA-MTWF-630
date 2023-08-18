import pgzrun
from random import randint

HEIGHT = 700
WIDTH = 1200
w, h = WIDTH, HEIGHT
music.play('remix')

p = Actor('ironman', (w//2, h//2))
c = Actor('coin', (w//2, h-100))

e_list = []
for i in range(10):
    e_list.append(Actor('alien', (randint(0, w), randint(0, h))))

block1 = Rect((0, 0), (w, 40))
score = 0
game_state = -1

def draw_game_level():
    screen.fill('black')
    # name of the game
    screen.draw.text('Ironman Game', (w//2, 10),
                        color='white', fontsize=50, centerx=w//2)
    screen.draw.filled_rect(block1, 'blue')
    screen.draw.text(f'Score: {score}', (10,10),
                        color='white')
    c.draw()
    p.draw()
    for e in e_list:
        e.draw()

def draw():
    if game_state == -1:
        screen.fill('yellow')
        screen.draw.text(f'Press Space to Start', color='black', fontsize=50, centery=h//2, centerx=w//2)
    if game_state == 0:
        draw_game_level()
    elif game_state == 1:
        screen.fill('black')
        screen.draw.text(f'Game Over', color='red', fontsize=100, centery=h//2, centerx=w//2)
    elif game_state == 2:
        screen.fill('black')
        screen.draw.text(f'You Win',color='green', fontsize=100, centery=h//2, centerx=w//2)

def player_update():
    if keyboard.left:
        p.x -= 10
        p.angle = 20
    elif keyboard.right:
        p.x += 10
        p.angle = -20
    elif keyboard.up:
        p.y -= 10
    elif keyboard.down:
        p.y += 10
    else:
        p.angle = 0

    # loop around the screen

    if p.x > w:
        p.x = 0
    if p.x < 0:
        p.x = w
    if p.y > h:
        p.y = 0
    if p.y < 0:
        p.y = h

def enemy_update():
    for e in e_list:
        s = randint(1, 4)
        if c.x > e.x:
            e.x += s
        if c.x < e.x:
            e.x -= s
        if c.y > e.y:
            e.y += s
        if c.y < e.y:
            e.y -= s
    # keep them from colliding together
    for e in e_list:
        for e2 in e_list:
            if e.colliderect(e2):
                if e.x > e2.x:
                    e.x += 5
                if e.x < e2.x:
                    e.x -= 5
                if e.y > e2.y:
                    e.y += 5
                if e.y < e2.y:
                    e.y -= 5

def score_update():
    global score, game_state
    if p.colliderect(c):
        score += 10
        c.x = randint(0, w)
        c.y = randint(0, h)
        sounds.action.play()
    
    for e in e_list:
        if e.colliderect(c):
            score -= 5
            c.x = randint(0, w)
            c.y = randint(0, h)
            sounds.action.play()
    if score <= -100:
        game_state = 1 # game over
    if score >= 100:
        game_state = 2 # you win
        


def update():
    global game_state
    if game_state == 0:
        enemy_update()
        player_update()
        score_update()
    if keyboard.space and game_state == -1:
        game_state = 0

pgzrun.go()