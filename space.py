from pygame import *
#import os
import random

# add root dir
#script_dir = os.path.dirname(__file__)
#print("ini direktori awal == ",script_dir)

#background music
mixer.init()
mixer.music.load('krusty.ogg')
mixer.music.play()
fire_sound = mixer.Sound('keren2.ogg')

#fonts and labels
font.init()
font2 = font.Font(None, 36)
win = font2.render('YOU WON', 1, (255, 255, 0))
lose = font2.render("YOU LOSE ", 1, (255, 0, 0))

# we need these pictures:
img_back = "krusty krab.png" # game background
img_hero = "sigma.jpeg" # character
img_alien = "Kominfo.png" # character
img_alien2 = "mermaidman.png"
img_bullet = "bullet.png" # bullet

# tambahkan os
#img_back = os.path.join(script_dir, img_back)
#img_hero = os.path.join(script_dir, img_hero)
#img_alien = os.path.join(script_dir, img_alien)
#img_alien2 = os.path.join(script_dir, img_alien2)
#img_bullet = os.path.join(script_dir, img_bullet)

# variabel untuk skor dan lost
score = 0
missed = 0
goal = 50
max_lost = 3

# parent class for other sprites
class GameSprite(sprite.Sprite):
  # class constructor
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # We call the class constructor (Sprite):
        sprite.Sprite.__init__(self)

        # each sprite must store an image property
        #player_image = os.path.join(script_dir, player_image)

        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        # each sprite must store the rect property it is inscribed in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
  # method that draws the character in the window
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# main player class
class Player(GameSprite):
    # method for controlling the sprite with keyboard arrows
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
  # the "fire" method (use the player's place to create a bullet there)
    def fire(self):
        bullet = Bullet(img_bullet, ship.rect.x + 36, ship.rect.y, 10, 20, 15)
        bullets.add(bullet)

class Monster(GameSprite):
    # method for controlling the sprite with keyboard arrows
    
    def update(self):
        global missed
        # jika posisi y masih dibawah 500 maka arahnya "down"
        if self.rect.y <= 500:
            self.side = "down"
        # jika tidak, maka arahnya menjadi "restart" 
        else:
            self.side = "restart"

        # jika arahnya down, maka koordinat akan ditambah terus menerus
        if self.side == "down":
            self.rect.y += self.speed
        else:
            self.rect.x = random.randint(100,600)
            self.rect.y = 0
            missed += 1

class Bullet(GameSprite):
    # method for bullets
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
# Create the window
win_width = 700
win_height = 500



display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

# create sprites
ship = Player(img_hero, 100, win_height - 100, 80, 100, 30)

# create alien
aliens = sprite.Group()
for i in range(1,5):
    speed_random = random.randint(1,8)
    print("alien ke ",i, "kecepatan = ",speed_random )
    alien = Monster(img_alien, random.randint(100,600), 0, 100, 60, speed_random)
    aliens.add(alien)

# alien v.2
aliens2 = sprite.Group()
for i in range(1,5):
    speed_random = random.randint(1,8)
    print("alien ke ",i, "kecepatan = ",speed_random )
    alien = Monster(img_alien2, random.randint(100,600), 0, 150, 110, speed_random)
    aliens2.add(alien)


# create bullets
bullets = sprite.Group()




# the "game over" variable: as soon as it is True, the sprites stop working in the main loop
finish = False
# Main game loop:
run = True # the flag is cleared with the close window button
while run:
    # the press the Close button event
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()
            
    if not finish:
        # refresh background
        window.blit(background,(0,0))

        # producing sprite movements
        ship.update()
        aliens.update()
        aliens2.update()

        bullets.update()
        
        collides = sprite.groupcollide(aliens, bullets, True, True)
        collides2 = sprite.groupcollide(aliens2, bullets, True, True)

        for c in collides:
            score += 1
            alien = Monster(img_alien, random.randint(100,600), 0, 100, 60, speed_random)
            aliens.add(alien)
        for c2 in collides2:
            score += 1
            alien2 = Monster(img_alien2, random.randint(100,600), 0, 150, 110, speed_random)
            aliens2.add(alien2)
            

            
            
        
                

       

        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        
        text = font2.render("Missed: " + str(missed), 1, (255, 255, 255))
        window.blit(text, (10, 50))

        # updating them at a new location on each iteration of the loop
        ship.reset()
        # aliens.reset()
        aliens.draw(window)
        aliens2.draw(window)
        bullets.draw(window)



        if score >= goal:
            finish = True
            window.blit(win, (280, 250))
        if missed >= max_lost or sprite.spritecollide(ship, aliens, True):
            finish = True
            window.blit(lose, (280, 250))
        display.update()
    # the loop runs every 0.05 seconds
    time.delay(50)
