import pgzrun
from random import randint
from dataclasses import dataclass

# create a data class to store game configuration
@dataclass
class GameConfig:
    # define the fields using type annotations and default values
    HEIGHT: int = 700
    WIDTH: int = 1024
    BG_WIDTH: int = 1000
    SCORE_LIMIT: int = 100
    FONT_SIZE: int = 50

    # optionally, add some methods or properties if needed
    def screen_size(self) -> tuple:
        # return a tuple of screen width and height
        return (self.WIDTH, self.HEIGHT)

# create an instance of GameConfig
config = GameConfig()
WIDTH = config.WIDTH
HEIGHT = config.HEIGHT

screen_width, screen_height = config.screen_size()
music.play('remix')

player = Actor('ironman', (screen_width//2, screen_height//2))
coin = Actor('coin', (screen_width//2, screen_height-100))
backgrounds = []
for i in range(10):
    backgrounds.append(Actor('bg', (i*config.BG_WIDTH, screen_height//2)))

# use a list comprehension to create the enemy list
enemies = [Actor('alien', (randint(0, screen_width), randint(0, screen_height))) for i in range(10)]

particle = Rect((0, 0), (5, 5))    

blue_rect = Rect((0, 0), (screen_width, 40))
score = 0
game_state = -1
game_over = False # use a variable to store the game state of 1 or 2

# use a function to generate a random position
def randomize_position():
    return (randint(100, screen_width-100), randint(100, screen_height-100))

def scroll_bacground():
    for bg in backgrounds:
        bg.x -= 1
        if bg.x < -config.BG_WIDTH:
            bg.x = screen_width


def draw_game_level():
    screen.fill('black')
    for bg in backgrounds:
        bg.draw()
    # name of the game
    screen.draw.text('Ironman Game', (screen_width//2, 10),
                        color='white', fontsize=config.FONT_SIZE, centerx=screen_width//2)
    screen.draw.filled_rect(blue_rect, 'blue')
    screen.draw.text(f'Score: {score}', (10,10),
                        color='white')
    coin.draw()
    player.draw()
    for e in enemies:
        # randomize the alien size
        e.draw()

def draw():
    if game_state == -1:
        screen.fill('yellow')
        screen.draw.text(f'Press Space to Start', color='black', fontsize=config.FONT_SIZE, centery=screen_height//2, centerx=screen_width//2)
    if game_state == 0:
        draw_game_level()
    elif game_state == 1 or game_state == 2:
        screen.fill('black')
        # use the game_over variable to display the appropriate message
        screen.draw.text(f'Game Over' if game_over else f'You Win', color='red' if game_over else 'green', fontsize=config.FONT_SIZE, centery=screen_height//2, centerx=screen_width//2)

def player_update():
    if player.x > screen_width:
        player.x = 0
    if player.x < 0:
        player.x = screen_width
    if player.y > screen_height:
        player.y = 0
    if player.y < 0:
        player.y = screen_height

def on_mouse_move(pos):
    # animate the player movement
    animate(player, pos=pos, duration=0.3)
    
def enemy_update():
    for e in enemies:
        speed = randint(1, 4)
        if coin.x > e.x:
            e.x += speed
        if coin.x < e.x:
            e.x -= speed
        if coin.y > e.y:
            e.y += speed
        if coin.y < e.y:
            e.y -= speed
    # keep them from colliding together
    for e in enemies:
        for e2 in enemies:
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
    global score, game_state, game_over
    if player.colliderect(coin):
        score += 10
        # use the randomize_position function to set the coin position
        coin.pos = randomize_position()
        sounds.action.play()
    
    for e in enemies:
        if e.colliderect(coin):
            score -= 5
            # use the randomize_position function to set the coin position
            coin.pos = randomize_position()
            sounds.action.play()
    if score <= -config.SCORE_LIMIT:
        game_state = 1 # game over
        game_over = True # set the game_over variable to True
    if score >= config.SCORE_LIMIT:
        game_state = 2 # you win
        game_over = False # set the game_over variable to False
        


def update():
    global game_state
    if game_state == 0:
        scroll_bacground()
        enemy_update()
        player_update()
        score_update()
    if keyboard.space and game_state == -1:
        game_state = 0

pgzrun.go()
